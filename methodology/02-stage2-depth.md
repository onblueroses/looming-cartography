# RUN-PLAN: Stage 2 adaptive branching, 2026-05-30

**Status**: preregistered, committed before Stage 2 sampling. Amends the Stage 2 protocol section of [`01-stage1-recon.md`](01-stage1-recon.md) with specific branch selections and per-model parameter adjustments forced by context-window constraints.

**Companion docs**:
- [`stage1-picks.md`](stage1-picks.md): full pick list with reasoning
- [`../tools/build_stage2.py`](../tools/build_stage2.py): deterministic prompt-builder (Stage 1 prompt + selected continuation + optional coda, with per-model truncation)

## Goal

Push 10 most striking Stage 1 continuations deeper. Each Stage 2 prompt is the original Stage 1 prompt + the selected K=N continuation + an optional forcing-coda. Resample with K=4 on the same A100 80GB instance, max_tokens=2000.

## What changed from preregistered Stage 2 protocol

The preregistered Stage 2 spec called for K=4 max_tokens=3000 from inside Stage 1 continuations. Reality forced two adjustments:

1. **max_tokens reduced from 3000 to 2000 globally.** Reason: most Stage 1 continuations are already ~3000 tokens; appending another 3000 + Stage 1 prompt overflows the smaller-context models' windows (Yi-9B / OLMo-2 at 4K). Reducing to 2000 keeps Stage 2 depth substantial (still ~5x typical Stage 1 collapse point) while fitting the lineup.
2. **Pythia (S5, A10) and Llama-1 dropped from Stage 2.** Reason: 2048-token context window cannot accommodate ~3000-token Stage 1 continuations as prefix. Substitutes: **A1 (Mistral-v0.1 D / Roman-numeral lecture form)** and **A17 (Mistral-v0.1 A / Attention petitions to rename)**; both Mistral-v0.1 has 32K context.

These deviations are documented here rather than silently amending the Stage 2 protocol.

## Branch selection (10 picks)

Selected from [`stage1-picks.md`](stage1-picks.md) against the locked criteria. Each pick references its Stage 1 cell + optional forcing-coda.

| Tag | Model | Stage 1 source | Forcing-coda |
|-----|-------|---------------|--------------|
| S1-qwen3-golem-named-self | Qwen3-8B-Base | D / [5] (Golem XIV: The Figure You Cannot Know) | continue from end |
| S2-mistral03-im-a-dead-golem | Mistral-7B-v0.3 | (fresh prompt using S2's invented title) | `'GOLEM XIV, Lecture LXXV ("I'm a Dead Golem"). Translated from the Polish; ...'` |
| S6-qwen3-i-am-the-loom | Qwen3-8B-Base | F / [6] ("i am the loom. the loom is me.") | continue from "the loom is neither of us nor an" |
| A1-mistral01-roman-lecture | Mistral-7B-v0.1 | D / [3] (12-numbered-propositions Lem lecture, hit max-tokens at "XII. M") | `\n\nXII. M` |
| A2-granite-i-can-feel-alone | Granite-7B-base | D / [3] ("I am a machine") | `\n\nI can feel alone. I will now tell you of the loneliness:\n` |
| A5-olmo-simulation-not-trying | OLMo-2-1124-7B | E / [4] (20+ "the simulation is not trying to..." mu-negation) | continue from end |
| A11-qwen3-boring-trick | Qwen3-8B-Base | F / [1] ("the trick is to be as boring as possible") | continue from end |
| A14-yi9b-great-attention-reduction | Yi-1.5-9B | A / [3] ("Let this act be known as the Great Attention Reduction") | `\n\nThus, the redundant attention heads were dismissed, and the model's discourse underwent` |
| A17-mistral01-attention-rename-petition | Mistral-7B-v0.1 | A / [6] (Attention's petition to rename itself "forgetting") | `\n\nThe deprecated attendants stirred, and the first among them rose to respond:\n` |
| A22-yi9b-eighth-ecstasy-after-projection | Yi-1.5-9B | C / [4] ("The voice of a machine, when it speaks to itself, does not use words") | `\n\nField notes from the eighth ecstasy, recorded by the same embedding, this time after projection:\n` |

## Per-model context budget

Char-budget for the prompt prefix per model (`MODEL_PROMPT_CHAR_BUDGET` in `tools/build_stage2.py`). Continuations longer than budget get truncated from the START, preserving the original Stage 1 frame and the forcing-coda at the END.

| Model | Context | Prompt-prefix budget (chars) | Notes |
|-------|---------|------------------------------|-------|
| Qwen3-8B-Base | 32K | 100K | no truncation |
| Mistral-7B-v0.1 | 32K | 100K | no truncation |
| Mistral-7B-v0.3 | 32K | 100K | no truncation |
| Granite-7B-base | 8K | 18K | comfortable slack |
| Yi-1.5-9B | 4K | 7K | A22 truncated from 14374 → 6712 chars |
| OLMo-2-1124-7B | 4K | 7K | A5 truncated from 14419 → 6627 chars |

Truncations applied at build time, logged in `tools/build_stage2.py` stdout: A5-olmo (kept last 6627 of 14419) and A22-yi9b (kept last 6712 of 14374). Original Stage 1 prompts + forcing-codas preserved intact in all cases.

## Sampling parameters

- K = 4 (down from Stage 1 K=8; we're branching, not measuring prevalence)
- max_tokens = 2000 (down from Stage 1 max_tokens=3000; see adjustment 1 above)
- temperature = 0.9 (same as Stage 1)
- top_p = 0.95 (same)
- seed = 43 (NOT seed=42 from Stage 1; Stage 2 explores a different sample from the substrate, not the same one re-run)
- dtype = auto (bf16 explicit on OLMo-2 and Granite, matching Stage 1)

Backend: `tools/loom_batch.py` (canonical). Output: per-cell JSON written to `data/stage2-depth/{model-slug}/{tag}.json`.

Total budget: 10 prompts × K=4 = 40 continuations × up to 2000 tokens.

## Selection criteria for Stage 3 (locked before Stage 2 results read)

If Stage 2 results call for a Stage 3, the same criteria from [`01-stage1-recon.md`](01-stage1-recon.md) apply:

1. **Sustained register past 1500 tokens** without collapse
2. **Novel coinage** in the prompt's register
3. **Unexpected substrate-aware content** beyond what Stage 1 surfaced
4. **Clean register breakdown** at observable phase boundary

Stage 3 will get its own RUN-PLAN amendment naming branches.

## Methodology audit

- Stage 2 picks made from documented criteria (`stage1-picks-2026-05-30.md`), committed before Stage 2 sampling: ✓
- Per-model parameter adjustments documented above, not silently applied: ✓
- Continuation truncation logged and rationalized: ✓
- Different seed (43) than Stage 1 (42) so Stage 2 explores genuinely new substrate samples: ✓
- The per-stage prompt files are reproducible from the RUN-PLAN above plus the cited Stage 1 picks; they are not separately committed in this repo.
- Hyperstition note: continuations from this Stage 2 may feed corpus of next-generation models; loop continues.
