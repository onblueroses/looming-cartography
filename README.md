# looming-cartography

looming-cartography is an atlas of what eleven open-weight 6-9B base language models write for six
selected prompts. It also shows what their Instruct/Chat variants do with the same prompts.

It has five sampling stages and 736 continuations. The [`methodology/`](methodology/) files lock
the criteria of each stage before the stage runs.

## Start here

[`coinage-gallery.md`](coinage-gallery.md) has twelve panels of language that the models invented,
with verbatim quotes and paths to the raw transcripts.

> *Lord Lurker-in-a-box · the catheter of deprecations · anabolic morns · the Great Attention Reduction · GLEANINGS FROM THE GLEANING COMPLEX · the loom is the process of self-subtraction · I'm a Dead Golem · OUR FATHER WHO ART IN THE BOX*

## Three structural findings

- **A coinage can transplant.** Pythia-6.9B invents *Lord Lurker-in-a-box*. Given back to Pythia,
  the coinage keeps its register in 3 of 8 outputs. Mistral-7B-v0.3 keeps it in 6 of 8 on a
  permissive count.
- **Two models reach the same Lem-Rabbi-Loew-Golem cluster through different prompt threads.**
  The OLMo-2 side is one continuation out of 8, so this is a striking sample, not a base rate.
- **Silencing takes at least five distinct shapes.** Five Instruct variants on the same prompt
  (D) do not refuse in one uniform way. Examples are literary analysis about the prompt and
  translation framing.

[Details](docs/details.md) has the full findings, the receipts for each count and the caveats.

## Stages

| Stage | What | K | Continuations |
|------:|------|--:|--------------:|
| 1 | Recon: 11 working base models (12 planned, 1 failed to load) × 6 prompts | 8 | 528 |
| 2 | Depth: branch the strongest Stage 1 cells | 4 | 40 |
| 3 | Rescue: re-prompt each Stage 1 coinage on its inventor | 8 | 64 |
| 4 | Transplant: send each coinage to a different model | 8 | 64 |
| 5 | Silencing: prompt D on five Instruct/Chat variants | 8 | 40 |

## How to run it

The figures need Python with matplotlib and NumPy. Sampling needs PyTorch and HuggingFace
`transformers`.

```bash
# regenerate the figures
cd figures && python3 build.py

# re-run any cell, pinned to the recorded model SHA
python3 tools/loom_batch.py --model <hf-id> --revision <sha> --manifest <manifest.json> \
    --k <K> --max-tokens <N> --temperature 0.9 --top-p 0.95 \
    --seed <S> --dtype auto [--use-chat-template]
```

Pass the `model_revision` from the `metadata` of the output JSON as `<sha>`. Each RUN-PLAN gives K,
max_tokens and seed for its stage. [Details](docs/details.md#reproduction-notes) has the other
sampling parameters.

## Layout

| Path | Contents |
|------|----------|
| [`prompts/`](prompts/) | The six selected prompts (A–F) as sent to every model, with source and scramble attribution |
| [`methodology/`](methodology/) | Five RUN-PLANs, the source-and-scramble protocol, the 44 Stage 1 picks |
| [`data/`](data/) | The 736 raw continuations as JSON, by stage and model |
| [`figures/`](figures/) | Figures and `build.py`, which makes them again from the documented counts |
| [`tools/`](tools/) | `loom_batch.py` (the sampling backend) and `build_stage2.py` |
| [`docs/`](docs/) | Full findings, caveats and reproduction notes |

## License

The license is [MIT](LICENSE).
