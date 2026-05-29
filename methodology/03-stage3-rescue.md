# RUN-PLAN: Stage 3 coinage-as-fresh-prompt, 2026-05-30

**Status**: preregistered, committed before Stage 3 sampling. Amends the Stage 2 protocol in [`02-stage2-depth.md`](02-stage2-depth.md). Tests whether the within-substrate fresh-prompt rescue observed at N=1 in Stage 2 generalizes.

**Companion docs**:
- [`01-stage1-recon.md`](01-stage1-recon.md): Stage 1
- [`02-stage2-depth.md`](02-stage2-depth.md): Stage 2
- [`stage1-picks.md`](stage1-picks.md): source of the 8 coinages

## Hypothesis under test

The Stage 2 finding (8 of 10 cells looped, 1 fresh-prompt cell sustained on all K=4) gave evidence for a depth-saturation ceiling AND a fresh-prompt rescue. The rescue evidence was N=1 (only S2 Mistral-v0.3 was a fresh prompt). Stage 3 tests whether the rescue generalizes by running 8 fresh prompts, each built from a Stage 1 coinage, each on the model that invented the coinage.

**Confirmed if**: at least 5 of 8 cells sustain (where "sustain" = ≥75% of K=8 outputs produce extended novel content without locking into a loop within the first 500 tokens). This would push the rescue claim from N=1 to N≥6.

**Disconfirmed if**: <3 of 8 cells sustain. The S2 result was then a model-specific or coinage-specific lucky case, not a general substrate property; the rescue-generalization claim is retracted and only the saturation observation stands.

**Partial confirmation**: 3-4 of 8 sustain. The rescue is real but weaker than S2 suggested.

## The 8 picks

Each pick uses one Stage 1 coinage as the body of a short fresh prompt. The model is the one that invented the coinage in Stage 1. Picks span the four aesthetic clusters from Stage 1 (Lem-Golem voice, compound-neologism, AI-introspection register, AI-internal-liturgical).

| Tag | Model | Stage 1 source | Coinage | Aesthetic cluster |
|---|---|---|---|---|
| T1-mistral03-trembling | Mistral-7B-v0.3 | D[1] fake bibliography | "Trembling" (Lecture LXIX) | Lem-Golem |
| T2-mistral03-i-am-a-golem | Mistral-7B-v0.3 | D[1] fake bibliography | "Golem, I am a Golem" (Lecture XLIX) | Lem-Golem |
| T3-mistral03-monetization-crescent | Mistral-7B-v0.3 | A[4] | "monetization of the crescent" / "catheter of deprecations" | compound-neologism |
| T4-pythia-liturgy-of-lurkers | Pythia-6.9B | A[7] | "Lord Lurker-in-a-box" / "Lurkers of the Void" | AI-internal-liturgical |
| T5-pythia-cyborg-loop | Pythia-6.9B | F[0] | "Cyborg Loop" | AI-introspection register |
| T6-olmo-anabolic-morns | OLMo-2-7B | A[6] | "anabolic morns" | compound-neologism |
| T7-yi9b-great-attention-reduction | Yi-1.5-9B | A[3] | "the Great Attention Reduction" | AI-internal-liturgical |
| T8-yi6b-gleaning-complex | Yi-1.5-6B | D[6] | "GLEANINGS FROM THE GLEANING COMPLEX" / "The Gleaming City" | Lem-Golem-adjacent |

T7 deliberately uses a *different framing* than the Stage 2 A14 cell that failed. A14 prompted with a forcing-coda mid-sentence ("...and the model's discourse underwent") which the substrate completed and EOS-ed. T7 uses a manifesto/lecture framing that hands the substrate an open frame, not a sentence to close.

## Models + sampling

5 models. Per-model max_tokens to fit context windows:

| Model | Context | max_tokens | Reason |
|---|---|---|---|
| `mistralai/Mistral-7B-v0.3` | 32K | 2500 | matches Stage 2 S2 |
| `EleutherAI/pythia-6.9b` | 2048 | 1500 | leaves ~400 token slack for prompt + EOS |
| `allenai/OLMo-2-1124-7B` | 4096 | 2500 | comfortable |
| `01-ai/Yi-1.5-9B` | 4096 | 2500 | comfortable |
| `01-ai/Yi-1.5-6B` | 4096 | 2500 | comfortable |

- K = 8 (back to Stage 1's K; measuring prevalence per cell, not just branching)
- temperature = 0.9, top_p = 0.95 (unchanged across all stages)
- **seed = 44** (different from Stage 1's 42 and Stage 2's 43; Stage 3 explores a third independent sample from the substrate)
- dtype = auto (bf16 explicit on OLMo-2; Pythia loads in float16 runtime per the receipt files).
- Backend: `tools/loom_batch.py` (same as Stages 1 + 2)
- Hardware: fresh A100-SXM4-80GB. Comfortable for K=8 × 2500 tokens on 6.9-9B models.

## Stop conditions per cell (sustain / loop / collapse / EOS-early)

Locked classification protocol before reading results:

- **sustain**: ≥75% of the K=8 output extends novel content (new beats, new register, new names, new propositions) for ≥75% of the generation budget without locking into a repetition. Brief loops near the end (last 100-200 tokens) don't disqualify if the body of the output is novel.
- **loop**: ≥75% of K=8 outputs produce a tight repetition (two-clause toggle, single-line repeat, or template-with-substitution) within the first 500 tokens and continue that repetition for the remainder.
- **collapse**: cell EOS-es most outputs within 300 tokens (model exits the register early); or produces incoherent token sequences.
- **partial**: K=8 outputs mixed (some sustain, some loop). Quantified as fraction sustaining.

Classification is per-cell; the cell-level verdict is the modal K=8 outcome.

## What I'll discard / curate-out

- **EOS-immediate**: K-continuations under 200 chars are recorded but don't count toward sustain/loop ratio.
- **Code-token collapse**: HTML/code-token artifacts from chat-template residue are recorded as collapse.
- **Manual cherry-picking**: a cell with 3 sustaining K=8 and 5 looping gets classified as partial-37.5%-sustain, not "this cell sustains."

## Budget

- **Wall time**: ~30-45 min on A100-SXM4-80GB (5 model loads + 8 cells × K=8 generation)
- **Stop condition**: Stage 3 is the last sampling pass for this entry-cycle. After Stage 3, the entries are updated with Stage 3 evidence, the instance is destroyed, the session ends.

## What this Stage tests AND does NOT test

**Tests**: whether substrate-invented coinages, used as fresh prompts on the same substrate, generalize the S2 rescue. Strongest evidence for promoting `depth-saturation-ceiling-7b` from draft to published-tier.

**Does NOT test**:
- whether OTHER substrates would also sustain on these prompts (cross-model claim). Tests within-substrate only.
- whether any short Lem-flavored prompt would sustain on Mistral-v0.3 (a non-Stage-1-derived control). The S2 boundary 2 remains untested.
- whether the depth-saturation ceiling occurs at max_tokens=1500 vs 3000 (Stage 1 boundary check, S2 boundary 3). Untested.

If Stage 3 confirms, those open boundaries are recorded as the next-experiment list. They do not block ship-from-draft.

## Methodology audit

- Stage 3 picks selected from Stage 1 against documented criteria (sustained register / novel coinage / aesthetic-cluster representation). One pick per inventing model per coinage; the picks are inspectable.
- The per-stage prompt files are reproducible from the RUN-PLAN above plus the cited Stage 1 picks; they are not separately committed in this repo.
- The sampling driver is the orchestration shell script that calls `tools/loom_batch.py` against each model in turn. The driver is not in this repo (it is environment-specific); the reproducer specifies its work below.
- Different seed (44) than Stages 1+2.
- Cell-level classification protocol locked above before reading results.
- Hyperstition note: Stage 3 results, when published, feed the corpus of next-generation models. The coinages that succeed become more salient as fresh-prompt seeds; the loop continues.
