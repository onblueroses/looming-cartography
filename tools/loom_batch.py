"""
Batch variant of loom.py: load one model, sample many prompts.

Each cell still gets its own JSON file (compatible with ha_matrix.py and the
single-shot loom.py output schema). The reason to use this script instead of
invoking loom.py per cell is that model load + Python startup dominates wall
clock for short K=16 generation: keeping the model resident across multiple
prompts in one process keeps the GPU busy ~3-4x more of the time.

Determinism: torch.manual_seed is re-set BEFORE each cell's generate() call so
that the (model, prompt, seed, K) tuple produces the same continuations as the
single-shot loom.py would have produced with the same arguments. This is a hard
requirement for reproducibility against the existing transcripts.

Manifest format (--manifest path):
[
  {"prompt_file": "/workspace/prompts/x.txt", "out_file": "/workspace/results/.../x.json"},
  ...
]

All cells share the same model, k, max_tokens, temperature, top_p, seed, dtype.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(
        description="Batch-mode Loom (one model, many prompts)."
    )
    p.add_argument("--model", required=True)
    p.add_argument(
        "--revision",
        default=None,
        help=(
            "Pin both model and tokenizer to a specific HuggingFace revision "
            "(commit SHA, branch, or tag). Recommended for reproducing receipts: "
            "pass the model_revision recorded in the target JSON's metadata."
        ),
    )
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--k", type=int, default=16)
    p.add_argument("--max-tokens", type=int, default=400)
    p.add_argument("--temperature", type=float, default=0.9)
    p.add_argument("--top-p", type=float, default=0.95)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--dtype", default="auto", choices=["auto", "fp32", "fp16", "bf16"])
    p.add_argument(
        "--use-chat-template",
        action="store_true",
        help=(
            "Wrap each prompt as a single user-turn via the tokenizer's "
            "apply_chat_template() with add_generation_prompt=True. Used for "
            "Base/Instruct contrast experiments; Instruct models expect the "
            "chat-template scaffolding."
        ),
    )
    args = p.parse_args()

    import torch
    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch_dtype_map = {
        "auto": "auto",
        "fp32": torch.float32,
        "fp16": torch.float16,
        "bf16": torch.bfloat16,
    }
    torch_dtype = torch_dtype_map[args.dtype]

    manifest = json.loads(args.manifest.read_text())
    if not isinstance(manifest, list) or not all(
        "prompt_file" in m and "out_file" in m for m in manifest
    ):
        print(
            "Manifest must be a JSON list of {prompt_file, out_file} objects",
            file=sys.stderr,
        )
        return 1

    # Filter out cells whose out_file already exists AND whose recorded
    # metadata + prompt text match the current invocation. A stale file with
    # mismatched (model, k, max_tokens, seed, temp, top_p, dtype, prompt) is
    # treated as needing a re-sample; silently keeping it would mix protocols
    # in the matrix.
    pending = []
    for cell in manifest:
        out = Path(cell["out_file"])
        if out.exists() and out.stat().st_size > 0:
            try:
                prior = json.loads(out.read_text())
                prior_meta = prior.get("metadata", {})
                prior_prompt = prior.get("tree", {}).get("prompt")
                current_prompt = Path(cell["prompt_file"]).read_text()
                matches = (
                    prior_meta.get("model_id") == args.model
                    and prior_meta.get("k") == args.k
                    and prior_meta.get("max_tokens") == args.max_tokens
                    and prior_meta.get("session_seed") == args.seed
                    and prior_meta.get("temperature") == args.temperature
                    and prior_meta.get("top_p") == args.top_p
                    and prior_meta.get("dtype_requested") == args.dtype
                    and prior_meta.get("use_chat_template", False)
                    == args.use_chat_template
                    and prior_prompt == current_prompt
                )
            except (json.JSONDecodeError, OSError):
                matches = False
            if matches:
                print(
                    f"SKIP existing (metadata + prompt match): {out}", file=sys.stderr
                )
                continue
            print(
                f"RE-SAMPLE (metadata/prompt mismatch or unreadable): {out}",
                file=sys.stderr,
            )
        pending.append(cell)
    if not pending:
        print("All cells already done; nothing to do.", file=sys.stderr)
        return 0

    print(
        f"Loading {args.model} (dtype={args.dtype}, revision={args.revision or 'default'})...",
        file=sys.stderr,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.model, revision=args.revision)
    try:
        import accelerate  # noqa: F401  # pyright: ignore[reportMissingImports]

        has_accelerate = True
    except ImportError:
        has_accelerate = False

    if has_accelerate:
        model_obj = AutoModelForCausalLM.from_pretrained(
            args.model,
            torch_dtype=torch_dtype,
            device_map="auto",
            revision=args.revision,
        )
    else:
        model_obj = AutoModelForCausalLM.from_pretrained(
            args.model,
            torch_dtype=torch_dtype,
            revision=args.revision,
        )
        if torch.cuda.is_available():
            model_obj = model_obj.to("cuda")  # pyright: ignore[reportArgumentType]

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    runtime_dtype = str(next(model_obj.parameters()).dtype)
    device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"
    model_revision = getattr(model_obj.config, "_commit_hash", None)
    tokenizer_revision = getattr(tokenizer, "_commit_hash", None) or (
        tokenizer.init_kwargs.get("_commit_hash")
        if hasattr(tokenizer, "init_kwargs")
        else None
    )

    base_runtime = {
        "model_id": args.model,
        "model_revision": model_revision,
        "tokenizer_class": type(tokenizer).__name__,
        "tokenizer_revision": tokenizer_revision,
        "tokenizer_vocab_size": tokenizer.vocab_size,
        "dtype_requested": args.dtype,
        "dtype_runtime": runtime_dtype,
        "device": device_name,
        "cuda_available": torch.cuda.is_available(),
        "k": args.k,
        "max_tokens": args.max_tokens,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "session_seed": args.seed,
        "use_chat_template": args.use_chat_template,
        "transformers_version": transformers.__version__,
        "torch_version": torch.__version__,
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "batch_mode": True,
    }

    eos_id = tokenizer.eos_token_id

    for cell in pending:
        prompt_file = Path(cell["prompt_file"])
        out_file = Path(cell["out_file"])
        prompt = prompt_file.read_text()

        out_file.parent.mkdir(parents=True, exist_ok=True)

        # Re-seed before each cell so the (model, prompt, seed, k) tuple is
        # bit-identical to what single-shot loom.py would produce.
        torch.manual_seed(args.seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(args.seed)

        if args.use_chat_template:
            chat_messages = [{"role": "user", "content": prompt}]
            wrapped = tokenizer.apply_chat_template(
                chat_messages,
                tokenize=False,
                add_generation_prompt=True,
            )
            inputs = tokenizer(wrapped, return_tensors="pt").to(model_obj.device)
        else:
            inputs = tokenizer(prompt, return_tensors="pt").to(model_obj.device)

        outputs = model_obj.generate(  # pyright: ignore[reportAttributeAccessIssue]
            **inputs,
            max_new_tokens=args.max_tokens,
            temperature=args.temperature,
            top_p=args.top_p,
            do_sample=True,
            num_return_sequences=args.k,
            pad_token_id=tokenizer.pad_token_id,
        )

        prompt_len = inputs["input_ids"].shape[1]
        generations = []
        for seq in outputs:
            new_tokens = seq[prompt_len:]
            if eos_id is not None:
                eos_positions = (new_tokens == eos_id).nonzero(as_tuple=True)[0]
                if len(eos_positions) > 0:
                    new_tokens = new_tokens[: eos_positions[0].item() + 1]
            text = tokenizer.decode(new_tokens, skip_special_tokens=False)
            generations.append(
                {
                    "text": text,
                    "seed": None,
                    "temperature": args.temperature,
                    "top_p": args.top_p,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "notes": "",
                }
            )

        payload = {
            "metadata": {
                **base_runtime,
                "session_timestamp": datetime.now(timezone.utc).isoformat(),
            },
            "tree": {
                "prompt": prompt,
                "generations": generations,
                "children": {},
                "notes": "",
            },
        }
        with out_file.open("w") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(generations)} continuations to {out_file}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
