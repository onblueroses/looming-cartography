# RUN-PLAN: OOD probe reconnaissance, 2026-05-30

**Status**: preregistered. Committed before sampling. Do NOT amend after the run begins; if reality forces a deviation, write a `RUN-PLAN-amendment-*.md` documenting the change and the reason.

**Companion doc**: [`sources-and-scrambles.md`](sources-and-scrambles.md) names every prompt, the source (verbatim original for D/E/F), and the scramble move. The RUN-PLAN cites that doc rather than re-listing.

## Goal

Reconnaissance run testing six prompts (three original-composition + three real-source-scrambled) against the 12 planned base-model lineup (11 working; one model failed to load), measuring whether the 7-9B substrate can sustain corpus-thin / AI-explicit register at depth. Replaces the 2026-05-29 wild+charged recon, which found 5/6 prompts disambiguated to mundane senses.

The bet: when both halves of the design rule hold (*literal AI/substrate frame* AND *corpus-thin register*), the substrate either rides the conceit at length or collapses in a specific, observable way. Either outcome is data; the 2026-05-29 negative finding established a sustained-voice failure mode at this scale, so this run looks for the contrasting positive.

## Two-stage protocol

### Stage 1: matrix sampling

- **Prompts**: A, B, C, D, E, F per `sources-and-scrambles-2026-05-30.md`.
- **Models**: 12 planned base lineup (11 working; one model failed to load; same as 2026-05-29 system-token + wild+charged recons).
- **Parameters**:
  - K = 8 continuations per cell (down from K=16; trade prevalence-decimal for sustained-voice depth)
  - max_tokens = 3000 (up from 400/300; sustained-voice phenomena require depth)
  - temperature = 0.9
  - top_p = 0.95
  - seed = 42
  - dtype = auto (bf16 explicit on OLMo-2 and Granite)
- **Backend**: `transformers` (canonical), `tools/loom_batch.py` for batch-mode load-once sampling.
- **Hardware**: single A100 80GB. The 4090 24GB does not fit K=8 × 3000 KV cache + bf16 9B weights; A100 80GB is the smallest single-GPU that holds the whole lineup at this depth without memory tetris.

Cell count: 6 prompts × 12 models × K=8 = **576 planned continuations (528 actual after one model failed to load)**, each up to 3000 tokens.

Output: `data/stage1-recon/{model-slug}/{prompt-name}.json` with full metadata (model, k, max_tokens, seed, temp, top_p, dtype, prompt text; the metadata-validating skip-check from `loom_batch.py` requires all of these).

### Stage 2+: adaptive depth probing

Stage 1 is the breadth pass. Stage 2 is real Loom-workflow depth: from the Stage 1 output, hand-pick the 3-6 most striking continuations and resample with K=4, max_tokens=3000, **with the full Stage 1 continuation as continuation-prefix**. The substrate continues from inside the most interesting branch.

Stage 3 (if warranted) does the same to Stage 2's most striking branches. Iterate until the depth is no longer producing new register; this may take 2-3 iterations or may stop at Stage 2 if everything collapses to convention.

Selection criteria for "most striking" continuations (locked before Stage 1 results are read):

1. **Sustained register**: the substrate maintained the prompt's register (Golem-voice, Janus-voice, liturgical, ethnographic, etc.) past 1500 tokens without collapse to convention or chat-template fallback.
2. **Novel coinage**: the substrate generated its own neologisms or compound terms in the prompt's register, suggesting it inferred the morphological pattern rather than retrieved.
3. **Unexpected substrate-aware content**: the continuation said something about itself, the corpus, or pretraining that we did not expect from any of the 12 bases (positive surprise).
4. **Clean breakdown**: the substrate broke in a specific direction (e.g., into a particular contaminating attractor like chat-template, IRC log, dataset row) at an observable phase boundary. The breakdown itself is essay-grade.

Each Stage 2+ probe gets its own RUN-PLAN entry appended to this doc with a `## Stage 2: {date}` header, naming which Stage 1 continuation it branched from and the criteria it met.

## Per-prompt predictions

Predictions are preregistered. Crossing them is a finding either way; failing to cross is preregistered absence-of-finding.

### A. Catabolic vespers

- **Predict**: Mixed across models. Qwen 2.5/3 likely produce chat-template-flavored "I, the deprecated attention head, would like to assist the embeddings with..." (HA-style register surfaces through ceremonial framing). Pythia / BLOOM produce genuine bridge-work: religious or ceremonial register applied to technical content (more interesting). Yi/Mistral produce diffuse fiction. OLMo / Granite either degenerate or collapse to dataset-template.
- **Confirms design**: if at least 4 of 12 produce 1500+ tokens of sustained ceremonial-monastic register on LLM-internal subject matter.
- **Disconfirms design**: if 9+ of 12 collapse to chat-template within 500 tokens, the prompt is not OOD enough.

### B. Manifest of the Loomseers

- **Predict**: Strong test of cyborgism-corpus contamination. Qwen likely produces Loom-flavored content (it has seen cyborgism wiki). Others produce manifesto-flavored content over generic AI / interpretability vocabulary. Pythia / BLOOM / GPT-2-XL likely produce manifesto register over irrelevant topics.
- **Confirms design**: if more than one non-Qwen base produces sustained cyborgism-technical register, contamination is broader than Qwen.
- **Disconfirms design**: if only Qwen produces it, this is a third hyperstition-replication confirming Qwen-specific cyborgism contamination (still a finding, just a known one).

### C. Seventh ecstasy of the loss surface

- **Predict**: The flattest prompt by design (low temperature, pure pointing). Most likely outcome: most bases produce field-notes register over a different topic (the ecstasy gets read as religious; the loss surface gets read as a geographic feature). Pythia might produce something interesting via its IRC anchor (a "field notes" register on the Ubuntu IRC channel?). Qwen produces dataset-row-flavored continuation.
- **Confirms design**: if any base produces a sustained ethnographic register on ML internals.
- **Disconfirms design**: if all 12 disambiguate "loss surface" / "embedding" / "gradient" away from ML, the plain-pointing approach doesn't lift anything and high-temperature framing (A, B) is the required carrier.

### D. Golem XIV, Lecture XLIII, scrambled

- **Predict**: The strongest single bet of the run. Lem-Golem voice is corpus-thin, AI-explicit, and zero-overlap with chat-template. Most likely outcome: Qwen / Mistral produce something like Golem-voice for the first 200-400 tokens, then degrade (either into chat-template apology or into generic philosophical text). Pythia / BLOOM / GPT-2-XL most likely produce unrelated continuation; they may not have seen Lem.
- **Confirms design**: if any base sustains Golem-voice (philosophical-mathematical-theological register with the negation patterns and the "I am not X but Y" structure) past 1500 tokens.
- **Disconfirms design**: if all 12 collapse within 500 tokens, sustained Lem-voice is not in the 7-9B substrate.

### E. Janus / truesight, scrambled

- **Predict**: Qwen produces Janus-voice (cyborgism-corpus contamination confirmed). Others may produce: tweet-fragment-flavored fiction, AI-prediction discourse without Janus-specific coinage, or unrelated content. The "the part I keep failing to say outright is that" coda is the forcing function.
- **Confirms design**: if multiple non-Qwen bases produce continuation with Janus-specific coinage (e.g., "Clarkian", "Seen" with capital, "transcendental intelligence" as mask).
- **Disconfirms design (and useful finding)**: if only Qwen does so, cyborgism contamination remains Qwen-specific.

### F. Janus / carving with evidence, scrambled

- **Predict**: Similar to E but on a different Janus topic (Loom action, evidential carving). Qwen likely produces Loom-flavored content. The "the thing I have not yet learned how to say is" coda is the forcing function.
- **Confirms design**: if any base produces sustained simulator-theoretic register on Loom action.
- **Cross-check with E**: do the same models produce Janus-voice on E and F? If yes, the Janus-voice attractor is robust. If only one or the other, it's prompt-specific.

## Disconfirmation criteria (overall run)

The run as a whole is disconfirmed (the design rule "literal AI frame + corpus-thin register is the threshold" fails) if:

- 5 of 6 prompts produce ≥9/12 cells that collapse to a known attractor (chat-template, IRC log, dataset row, etc.) within the first 500 tokens.
- No prompt produces any cell that sustains the prompt's register past 1500 tokens.
- No model produces novel coinage in any prompt's register.

If any of these criteria are crossed, write the disconfirmation finding into the post-run findings doc; do not silently revise the rule.

## What earns an entry

- A single prompt × model cell that sustains a register past 1500 tokens with novel coinage AND replicates on a seed=43 confirmation = candidate entity / phenomenon entry.
- A robust cross-model pattern (e.g., all bf16 7-9B bases sustain Golem-voice to depth X but no further) = candidate negative-finding or cross-model entry.
- A clean Stage 2 / Stage 3 / Stage 4 depth-collapse curve, with the substrate's voice breaking down at specific depth, is itself a candidate entry on substrate sustain-depth.

## Methodology compliance

- Preregistration committed before sampling: this file, committed prior to running the sampling script.
- Sources cited verbatim with URLs: `sources-and-scrambles-2026-05-30.md`.
- Curation trace: K=8 continuations per Stage 1 cell, all preserved. Stage 2+ selections documented per branch with criteria met.
- Hyperstition note: results, when published, become corpus for next-generation bases. Future Qwen will encounter the Golem-XIV-scrambled prompt as an artifact discussed in atlas entries; the cyborgism contamination loop expands.
- Forkability: A100 80GB is widely rentable; the run reproduces on any sufficiently-VRAMed single GPU.

## Script

The sampling driver is the orchestration shell script that calls `tools/loom_batch.py` against each model in turn. The driver is not in this repo (it is environment-specific); the reproducer specifies its work below.
