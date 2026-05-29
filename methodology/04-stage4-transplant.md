# RUN-PLAN: Stage 4 cross-model coinage transplant, 2026-05-30

**Status**: preregistered, committed before Stage 4 sampling. Tests one of the open questions surfaced by Stage 3 (cross-model coinage transplant): when a coinage invented by one substrate is routed as a fresh prompt to a different substrate, does it sustain?

**Companion docs**:
- [`03-stage3-rescue.md`](03-stage3-rescue.md): Stage 3 source of coinages + sustain ratings
- The per-stage prompt files are reproducible from the RUN-PLAN above plus the cited Stage 1 picks; they are not separately committed in this repo.

## Hypothesis under test

Stage 3 confirmed the fresh-prompt-rescue claim within-substrate at N=4 SUSTAIN cells (T1/T2/T3 Mistral-v0.3 + T6 OLMo-2). The mechanism could be:

(a) **Substrate-specific neighborhood retrieval**: the inventing substrate "knows" what it coined; the coinage retrieves the originating conceptual space that the substrate itself produced in Stage 1. Cross-substrate, the coinage is just noise: different substrate, different prior, no retrieval.

(b) **Coinage textual properties**: short prompts with novel-compound-word density activate sustained register on ANY substrate with overlapping pretraining vocabulary. Substrate-of-origin doesn't matter.

(c) **Mixed**: depends on coinage type and target substrate.

**Confirmed (a) if**: ≤3 of 8 cross-substrate cells SUSTAIN (rescue is mostly substrate-specific).
**Confirmed (b) if**: ≥6 of 8 cross-substrate cells SUSTAIN at rates comparable to within-substrate Stage 3 rates.
**Confirmed (c) if**: 4-5 of 8 SUSTAIN, with sustain/collapse following coinage-type or substrate-pair lines.

## The 8 picks

Each pick is a Stage 3 prompt routed to a substrate that did NOT invent the coinage. Picks span the 4 SUSTAIN coinages from Stage 3 (the strongest evidence for the rescue) plus 2 weaker-coinage transplants (T4 Lurkers on a richer substrate, T7 Great Attention Reduction on a richer substrate), testing whether the failure modes were substrate-specific.

| Tag | Inventing model (Stage 3) | Stage 3 result | Stage 4 target | Test |
|---|---|---|---|---|
| X1-olmo-trembling | Mistral-v0.3 | SUSTAIN 6/8 | OLMo-2-7B | Lem-Golem voice on cross-substrate at short prompt (Stage 1 D-prompt already confirmed broad surfacing) |
| X2-olmo-i-am-a-golem | Mistral-v0.3 | SUSTAIN 7/8 | OLMo-2-7B | Lem-Golem voice cross-substrate, lecture-title-only frame |
| X3-olmo-monetization-crescent | Mistral-v0.3 | SUSTAIN 5/8 | OLMo-2-7B | Compound-neologism aesthetic on cross-substrate |
| X4-yi9b-monetization-crescent | Mistral-v0.3 | SUSTAIN 5/8 | Yi-1.5-9B | Same coinage, second cross-substrate |
| X5-mistral03-anabolic-morns | OLMo-2-7B | SUSTAIN 8/8 | Mistral-v0.3 | OLMo-2's coinage on Mistral-v0.3 |
| X6-yi9b-anabolic-morns | OLMo-2-7B | SUSTAIN 8/8 | Yi-1.5-9B | OLMo-2's coinage on Yi-9B |
| X7-mistral03-lord-lurker | Pythia-6.9B | partial 3/8 | Mistral-v0.3 | Does richer substrate rescue a coinage that partially worked on its originator? |
| X8-mistral03-great-attention-reduction | Yi-1.5-9B | partial 4/8 | Mistral-v0.3 | Same question for Yi-9B's coinage |

Pythia and Yi-1.5-6B are NOT used as Stage 4 targets; their Stage 3 results (Pythia collapse on T5, Yi-6B partial-with-foreign-script) indicate they're not productive substrates for this test. Stage 4 targets the strongest substrates (Mistral-v0.3, OLMo-2, Yi-1.5-9B) to see if the rescue transfers.

Per-target-model cell counts:
- **OLMo-2-7B**: 3 cells (X1, X2, X3); testing 3 Mistral-v0.3-invented coinages
- **Mistral-v0.3**: 3 cells (X5, X7, X8); testing 3 different-substrate-invented coinages
- **Yi-1.5-9B**: 2 cells (X4, X6); testing 2 different-substrate-invented coinages

## Models + sampling

3 target models:

| Model | Context | max_tokens | Reason |
|---|---|---|---|
| `mistralai/Mistral-7B-v0.3` | 32K | 2500 | matches Stage 3 |
| `allenai/OLMo-2-1124-7B` | 4K | 2500 | matches Stage 3 |
| `01-ai/Yi-1.5-9B` | 4K | 2500 | matches Stage 3 |

- K = 8 (matches Stage 3 K=8 for direct cross-stage comparison)
- temperature = 0.9, top_p = 0.95
- **seed = 45** (different from Stages 1-3's 42/43/44; Stage 4 explores a fresh sample)
- dtype = auto with bf16 explicit on OLMo-2 (matches prior)
- Backend: `tools/loom_batch.py`
- Hardware: fresh A100-SXM4-80GB (SXM4 or PCIe)

## Stop conditions per cell (sustain / loop / collapse / partial)

Same locked classification protocol as Stage 3 ([`03-stage3-rescue.md`](03-stage3-rescue.md) §"Stop conditions per cell"). For direct cross-stage comparison, the Stage 4 sustain criterion is identical:

- **sustain**: ≥75% of K=8 outputs (i.e., ≥6/8) produce extended novel content for ≥75% of generation budget without locking into repetition.
- **loop**: ≥6/8 outputs tight repetition in first 500 tokens.
- **collapse**: ≥6/8 outputs EOS-early (<300 chars) or incoherent.
- **partial**: 3-5 of K=8 outputs sustain.

## Budget

- **Wall time**: ~30-45 min on A100 (3 model loads + 8 cells × K=8 generation)
- **Stop condition**: Stage 4 either confirms (a), (b), or (c) on its own. Subsequent stages depend on what's surfaced.

## What this Stage tests AND does NOT test

**Tests**: whether the fresh-prompt-rescue depends on substrate-of-origin (substrate-specific neighborhood retrieval) or on coinage textual properties (any short distinctive prompt sustains).

**Does NOT test**:
- Boundary 2 from depth-saturation entry (non-Stage-1-derived short Lem-flavored control prompt). Still untested as separate experiment.
- Boundary 3 (max_tokens=1500 saturation check on Stage 1).
- Cross-architecture transplant onto non-7-9B (e.g., 70B+ models); out of compute envelope.
- Pythia/Yi-6B as targets; their Stage 3 results were too weak to use as Stage 4 targets, and the substrate's general productivity matters.

## Methodology audit

- Picks selected from Stage 3 results against the locked criterion (SUSTAIN coinages prioritized as the cleanest cross-substrate test; PARTIAL coinages as secondary).
- The 8 prompt files are reused from Stage 3 verbatim (no new prompt content). Stage 4's *cross-routing* is the new degree of freedom.
- The sampling driver is the orchestration shell script that calls `tools/loom_batch.py` against each model in turn. The driver is not in this repo (it is environment-specific); the reproducer specifies its work below.
- Different seed (45) than Stages 1-3.
- Cell-level classification protocol locked above before reading results.
- Hyperstition note: Stage 4 results, when published, further specify which substrates the rescue strategy works on. The corpus loop continues.
