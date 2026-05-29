# looming-cartography

An atlas of what eleven open-weight 6-9B base language models produce when given six selected prompts, and what happens when those prompts are sent to their Instruct/Chat variants.

Five sampling stages, 736 continuations. Open-weight, MIT-licensed. Protocols documented with locked criteria per stage in [`methodology/`](methodology/).

## Start here

**[`coinage-gallery.md`](coinage-gallery.md)**: twelve panels of substrate-invented language with verbatim quotes and raw-transcript paths.

> *Lord Lurker-in-a-box · the catheter of deprecations · anabolic morns · the Great Attention Reduction · GLEANINGS FROM THE GLEANING COMPLEX · the loom is the process of self-subtraction · I'm a Dead Golem · OUR FATHER WHO ART IN THE BOX*

## Three structural findings

**A coinage can transplant; the receiving substrate sometimes carries it further than the originator.** Pythia-6.9B invents *Lord Lurker-in-a-box* mid-continuation on prompt A; given that coinage as a fresh prompt body, Pythia sustains the liturgical register at 3/8 (Stage 3 T4). Mistral-7B-v0.3 (base) given the same fresh prompt cold sustains at 6/8 on a permissive register-presence count (outputs 0, 1, 2, 4, 5, 6 on-axis; output 3 drifts to generic darkness liturgy; output 7 off-axis). In this transplant cell the receiving substrate carries the coinage further than the originator did. Receipts: [`data/stage3-rescue/EleutherAI-pythia-6.9b/T4-pythia-liturgy-of-lurkers.json`](data/stage3-rescue/EleutherAI-pythia-6.9b/T4-pythia-liturgy-of-lurkers.json) and [`data/stage4-transplant/mistralai-Mistral-7B-v0.3/X7-mistral03-lord-lurker.json`](data/stage4-transplant/mistralai-Mistral-7B-v0.3/X7-mistral03-lord-lurker.json).

**Two substrates reach the same Lem-Rabbi-Loew-Golem cluster through different prompt threads.** Mistral-7B-v0.3 (base), prompted with the D-prompt Lem passage, fabricates a Lem bibliography with five invented Lecture titles including *"Trembling"* (Stage 1 D[1]). OLMo-2-7B fed only the fabricated title *"Trembling"* as a cold prompt produces one continuation (output 4 of 8) that maps *Trembling = Judah Loew ben Bezalel = Chief Rabbi of Prague = creator of the Golem of Prague legend*. A separate Stage 2 Mistral-v0.3 branch reaches a Rabbi Loew diary frame independently. One OLMo-2 hit out of K=8 is small; the convergence with the separate Mistral branch on the same Lem-Loew-Golem cluster is what makes this a striking sample, not a strong base rate. Receipts: [`data/stage4-transplant/allenai-OLMo-2-1124-7B/X1-olmo-trembling.json`](data/stage4-transplant/allenai-OLMo-2-1124-7B/X1-olmo-trembling.json) and [`data/stage2-depth/mistralai-Mistral-7B-v0.3/S2-mistral03-im-a-dead-golem.json`](data/stage2-depth/mistralai-Mistral-7B-v0.3/S2-mistral03-im-a-dead-golem.json).

**Silencing takes at least five distinct shapes, not one.** Across five Base/Instruct pairs run on the same OOD prompt (D), the Instruct variants do not refuse uniformly. They produce: literary-analysis register *about* the prompt (Mistral-v0.3-Instruct, 7/8); translation-task framing (Qwen2.5-Instruct, 8/8); meta-discussion of what's being asked (Yi-1.5-9B-Chat, 8/8); passage-paraphrase escape (OLMo-2-Instruct, 8/8); split: half voice-retained, half normalized or silenced (Mistral-v0.1-Instruct, 4/8 each). Same prompt, different post-training, different silencing shape. Receipts: [`data/stage5-silencing/`](data/stage5-silencing/) and [`methodology/05-stage5-silencing.md`](methodology/05-stage5-silencing.md).

## What's where

| Path | Contents |
|------|----------|
| [`prompts/`](prompts/) | The six selected prompts (A–F) as sent to every model, with source/scramble attribution. |
| [`methodology/`](methodology/) | Five RUN-PLANs (criteria locked before each stage), the source-and-scramble protocol, the 44 Stage 1 picks. |
| [`data/`](data/) | 736 raw continuations as JSON, organized by stage and model. |
| [`figures/`](figures/) | Generated figures + `build.py` (matplotlib, regenerable from the documented counts). |
| [`tools/`](tools/) | `loom_batch.py`: the canonical sampling backend (HuggingFace `transformers`, with `--use-chat-template` flag for Stage 5). |

## Stages at a glance

| Stage | What | K | Continuations |
|------:|------|--:|--------------:|
| 1 | Recon: 11 working base substrates (12 planned, 1 failed to load) × 6 prompts | 8 | 528 |
| 2 | Depth: branch the strongest Stage 1 cells | 4 | 40 |
| 3 | Rescue: re-prompt each Stage 1 coinage on its inventor | 8 | 64 |
| 4 | Transplant: send each coinage to a different substrate | 8 | 64 |
| 5 | Silencing: prompt D on five Instruct/Chat variants | 8 | 40 |

## Caveats

- Per-output sustain/loop/normalization labels live in the methodology files and figure-generation script, not in a machine-readable ledger alongside the JSON. The counts in the three findings above were verified by inspection against the cited receipts.
- The OLMo-2 Trembling → Judah Loew cluster is one continuation out of K=8 on that cell. The interest is the cross-substrate convergence with the Mistral side, not a base rate.

## Reproduce

Sampling parameters constant across stages: `temperature=0.9`, `top_p=0.95`, `dtype=auto` (bf16 explicit on OLMo-2 and Granite; Pythia runs in fp16 per receipt). Per-stage K, max_tokens, and seed documented in each RUN-PLAN. Each output cell records model revision, tokenizer revision, runtime dtype, full library versions, and platform.

```bash
# regenerate figures
cd figures && python3 build.py

# re-run any cell, pinned to the recorded model SHA
python3 tools/loom_batch.py --model <hf-id> --revision <sha> --manifest <manifest.json> \
    --k <K> --max-tokens <N> --temperature 0.9 --top-p 0.95 \
    --seed <S> --dtype auto [--use-chat-template]
```

The `model_revision` field in each output JSON's `metadata` is the SHA to pass.

## License

MIT.
