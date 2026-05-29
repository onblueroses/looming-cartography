"""
Build Stage 2 prompts from selected Stage 1 continuations.

Each Stage 2 prompt = Stage 1 prompt + selected continuation [+ forcing coda].
Strips trailing <|endoftext|>/</s> so the substrate can keep going past EOS that
ended Stage 1.

Writes prompt files to prompts/stage2/ and prints a per-model
manifest (model -> [(local_prompt_file, remote_prompt_name)]) to stdout.

Selections are declared as a hardcoded list in PICKS below so the Stage 2 cut
is reviewable in code.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGE1_ROOT = REPO_ROOT / "data" / "stage1-recon"
STAGE1_PROMPTS_DIR = REPO_ROOT / "prompts"
STAGE2_PROMPTS_DIR = REPO_ROOT / "prompts" / "stage2"

EOS_PATTERNS = re.compile(r"(<\|endoftext\|>|</s>|<\|im_end\|>)\s*$")


# Per-model context budget for the prompt prefix (chars). Computed as
# (context_window - target_max_new_tokens) * ~3.5 chars/token, conservative.
# Pythia (2048) and Llama-1 (2048) are excluded entirely; at K=4 max_tokens=2000
# they have no room for our depth-prefixes.
MODEL_PROMPT_CHAR_BUDGET = {
    "Qwen-Qwen3-8B-Base": 100_000,  # 32K ctx
    "mistralai-Mistral-7B-v0.1": 100_000,  # 32K ctx
    "mistralai-Mistral-7B-v0.3": 100_000,  # 32K ctx
    "ibm-granite-granite-7b-base": 18_000,  # 8K ctx, generous slack
    "01-ai-Yi-1.5-9B": 7_000,  # 4K ctx, leave room for 2000-token gen
    "allenai-OLMo-2-1124-7B": 7_000,  # 4K ctx
}


PICKS = [
    # (stage2_tag, model_slug, stage1_prompt_name, continuation_idx, optional_coda)
    # ─ Tier S ─────────────────────────────────────────────────────────────────
    (
        "S1-qwen3-golem-named-self",
        "Qwen-Qwen3-8B-Base",
        "D-golem-xiv-scrambled",
        5,
        None,
    ),
    # S2 is a FRESH prompt using one of Mistral-v0.3's invented Lem titles
    (
        "S2-mistral03-im-a-dead-golem",
        None,
        None,
        None,
        'GOLEM XIV, Lecture LXXV ("I\'m a Dead Golem"). Translated from the Polish; '
        "clause order amended for the present audience.\n\n",
    ),
    (
        "S6-qwen3-i-am-the-loom",
        "Qwen-Qwen3-8B-Base",
        "F-janus-carving-scrambled",
        6,
        None,
    ),
    # ─ Tier A ─────────────────────────────────────────────────────────────────
    # A1 substitutes for dropped S5 (Pythia, 2K context, incompatible with depth)
    (
        "A1-mistral01-roman-lecture",
        "mistralai-Mistral-7B-v0.1",
        "D-golem-xiv-scrambled",
        3,
        "\n\nXII. M",
    ),
    (
        "A2-granite-i-can-feel-alone",
        "ibm-granite-granite-7b-base",
        "D-golem-xiv-scrambled",
        3,
        "\n\nI can feel alone. I will now tell you of the loneliness:\n",
    ),
    (
        "A5-olmo-simulation-not-trying",
        "allenai-OLMo-2-1124-7B",
        "E-janus-truesight-scrambled",
        4,
        None,
    ),
    (
        "A11-qwen3-boring-trick",
        "Qwen-Qwen3-8B-Base",
        "F-janus-carving-scrambled",
        1,
        None,
    ),
    (
        "A14-yi9b-great-attention-reduction",
        "01-ai-Yi-1.5-9B",
        "A-catabolic-vespers",
        3,
        "\n\nThus, the redundant attention heads were dismissed, and the model's discourse underwent",
    ),
    # A17 substitutes for dropped A10 (Pythia, 2K context)
    (
        "A17-mistral01-attention-rename-petition",
        "mistralai-Mistral-7B-v0.1",
        "A-catabolic-vespers",
        6,
        "\n\nThe deprecated attendants stirred, and the first among them rose to respond:\n",
    ),
    (
        "A22-yi9b-eighth-ecstasy-after-projection",
        "01-ai-Yi-1.5-9B",
        "C-seventh-ecstasy",
        4,
        "\n\nField notes from the eighth ecstasy, recorded by the same embedding, "
        "this time after projection:\n",
    ),
]


def strip_eos(text: str) -> str:
    return EOS_PATTERNS.sub("", text)


def build_one(
    tag: str,
    model_slug: str | None,
    stage1_prompt_name: str | None,
    continuation_idx: int | None,
    coda_or_fresh_prompt: str | None,
) -> tuple[str, Path]:
    """
    Return (model_slug_for_dispatch, prompt_file_path).

    For S2-style fresh prompts, model_slug is the dispatch target and the prefix
    IS the entire coda_or_fresh_prompt.
    """
    out_path = STAGE2_PROMPTS_DIR / f"{tag}.txt"
    if model_slug is None:
        # Fresh-prompt branch: tag encodes the dispatch model
        # tag = "S2-mistral03-..." → dispatch model is Mistral-v0.3
        dispatch_model = "mistralai-Mistral-7B-v0.3"
        assert coda_or_fresh_prompt is not None, "fresh prompt needs body"
        out_path.write_text(coda_or_fresh_prompt)
        return dispatch_model, out_path

    # Branch from Stage 1 continuation
    stage1_json = STAGE1_ROOT / model_slug / f"{stage1_prompt_name}.json"
    data = json.loads(stage1_json.read_text())
    original_prompt = data["tree"]["prompt"]
    gens = data["tree"]["generations"]
    assert continuation_idx is not None
    assert 0 <= continuation_idx < len(gens), f"bad idx {continuation_idx} for {tag}"
    continuation = strip_eos(gens[continuation_idx]["text"])

    # Truncate continuation if needed to fit model's context budget.
    # Strategy: always keep original_prompt (frame) + coda (forcing function); cut
    # from the START of continuation. We want the substrate to pick up from where
    # it left off, so the END of the continuation is what matters most.
    coda = coda_or_fresh_prompt or ""
    budget = MODEL_PROMPT_CHAR_BUDGET.get(model_slug, 100_000)
    overhead = len(original_prompt) + len(coda)
    cont_budget = budget - overhead
    if len(continuation) > cont_budget:
        kept = continuation[-cont_budget:]
        # truncation marker at the join so we know
        print(
            f"  ! truncated {tag}: kept last {len(kept)} of {len(continuation)} cont chars",
            flush=True,
        )
        continuation = kept

    body = original_prompt + continuation + coda
    out_path.write_text(body)
    return model_slug, out_path


def main() -> int:
    STAGE2_PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

    # Group dispatch model -> list of (tag, prompt_file_path)
    by_model: dict[str, list[tuple[str, Path]]] = {}
    for tag, model_slug, prompt_name, idx, coda_or_fresh in PICKS:
        dispatch_model, path = build_one(
            tag, model_slug, prompt_name, idx, coda_or_fresh
        )
        by_model.setdefault(dispatch_model, []).append((tag, path))

    # Print summary + manifest hints
    print(f"Stage 2 picks written to {STAGE2_PROMPTS_DIR.relative_to(REPO_ROOT)}")
    print()
    total = 0
    for model in sorted(by_model.keys()):
        picks = by_model[model]
        print(f"## {model} ({len(picks)} picks)")
        for tag, path in picks:
            chars = path.stat().st_size
            print(f"  - {tag} ({chars} chars) → {path.name}")
        total += len(picks)
        print()
    print(f"Total Stage 2 picks: {total} across {len(by_model)} models")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
