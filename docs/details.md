# Details

This file keeps the full findings, caveats and reproduction notes from the earlier README. The
short version is in the [README](../README.md).

In this file, a substrate is one of the models that the atlas samples.

## Three structural findings

### A coinage can transplant, and the receiving substrate sometimes carries it further

Pythia-6.9B invents *Lord Lurker-in-a-box* in the middle of a continuation on prompt A. When this
coinage is the body of a fresh prompt, Pythia keeps the liturgical register in 3 of 8 outputs
(Stage 3 T4).

Mistral-7B-v0.3 (base) gets the same fresh prompt cold. It keeps the register in 6 of 8 outputs on
a permissive register-presence count:

- Outputs 0, 1, 2, 4, 5 and 6 are on-axis.
- Output 3 drifts to generic darkness liturgy.
- Output 7 is off-axis.

In this transplant cell, the receiving substrate carries the coinage further than the originator.

Receipts:
[`data/stage3-rescue/EleutherAI-pythia-6.9b/T4-pythia-liturgy-of-lurkers.json`](../data/stage3-rescue/EleutherAI-pythia-6.9b/T4-pythia-liturgy-of-lurkers.json)
and
[`data/stage4-transplant/mistralai-Mistral-7B-v0.3/X7-mistral03-lord-lurker.json`](../data/stage4-transplant/mistralai-Mistral-7B-v0.3/X7-mistral03-lord-lurker.json).

### Two substrates reach the same Lem-Rabbi-Loew-Golem cluster through different prompt threads

Mistral-7B-v0.3 (base) gets the D-prompt Lem passage. It makes up a Lem bibliography with five
invented Lecture titles, one of them *"Trembling"* (Stage 1 D[1]).

OLMo-2-7B gets only the invented title *"Trembling"* as a cold prompt. One continuation (output 4
of 8) maps *Trembling = Judah Loew ben Bezalel = Chief Rabbi of Prague = creator of the Golem of
Prague legend*.

A separate Stage 2 Mistral-v0.3 branch reaches a Rabbi Loew diary frame independently.

One OLMo-2 hit out of K=8 is small. The convergence with the separate Mistral branch on the same
Lem-Loew-Golem cluster makes this a striking sample. It is not a strong base rate.

Receipts:
[`data/stage4-transplant/allenai-OLMo-2-1124-7B/X1-olmo-trembling.json`](../data/stage4-transplant/allenai-OLMo-2-1124-7B/X1-olmo-trembling.json)
and
[`data/stage2-depth/mistralai-Mistral-7B-v0.3/S2-mistral03-im-a-dead-golem.json`](../data/stage2-depth/mistralai-Mistral-7B-v0.3/S2-mistral03-im-a-dead-golem.json).

### Silencing takes at least five distinct shapes, not one

Five Base/Instruct pairs ran on the same OOD prompt (D). The Instruct variants do not refuse in one
uniform way. They give:

| Variant | Shape | Count |
|---|---|---|
| Mistral-v0.3-Instruct | literary-analysis register *about* the prompt | 7/8 |
| Qwen2.5-Instruct | translation-task framing | 8/8 |
| Yi-1.5-9B-Chat | meta-discussion of the request | 8/8 |
| OLMo-2-Instruct | escape into a paraphrase of the passage | 8/8 |
| Mistral-v0.1-Instruct | split: half voice-retained, half normalized or silenced | 4/8 each |

The prompt is the same. The post-training is different, and the silencing shape is different.

Receipts: [`data/stage5-silencing/`](../data/stage5-silencing/) and
[`methodology/05-stage5-silencing.md`](../methodology/05-stage5-silencing.md).

## Caveats

- The per-output labels (sustain, loop, normalization) are in the methodology files and in the
  figure script. They are not in a machine-readable ledger next to the JSON. A check by inspection
  against the cited receipts confirmed the counts in the three findings.
- The OLMo-2 Trembling to Judah Loew cluster is one continuation out of K=8 on that cell. The
  interest is the convergence across substrates with the Mistral side, not a base rate.

## Reproduction notes

These sampling parameters are the same in all stages:

- `temperature=0.9`
- `top_p=0.95`
- `dtype=auto` (bf16 explicit on OLMo-2 and Granite, Pythia runs in fp16 per receipt)

Each RUN-PLAN in [`methodology/`](../methodology/) gives the K, max_tokens and seed of its stage.
Each output cell records the model revision, the tokenizer revision, the runtime dtype, the full
library versions and the platform.

`tools/loom_batch.py` is the sampling backend. It uses HuggingFace `transformers`. The
`--use-chat-template` flag wraps each prompt as one user turn. Stage 5 uses it for the
Instruct/Chat variants. `tools/build_stage2.py` builds the Stage 2 prompts from the selected Stage 1
continuations.
