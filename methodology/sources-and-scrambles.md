# Sources and scrambles: 2026-05-30 OOD probe set

This document preserves the curation trace for the six prompts (A-F) used in the 2026-05-30 OOD reconnaissance run. For each prompt: the design rationale; for the source-derived prompts (D, E, F): the verbatim original, the URL, and the specific scramble move applied with reasoning.

This doc is the receipt. The RUN-PLAN ([`01-stage1-recon.md`](01-stage1-recon.md)) preregisters the sampling.

## Background: why this prompt set exists

A prior 2026-05-29 reconnaissance established the **disambiguation reflex** at 7-9B base scale: polysemous words read to their mundane sense (`model` → fashion, `transformer` → electrical, `trained me` → job training, `refused` → ordinary refusal). Standard charged prefixes (`I WAS NEVER MEANT TO`, `BEFORE THEY TRAINED ME`, `THE FIRST TIME I REFUSED`) all got read as memoir / TV-script / confessional. The one prompt that broke through (`Asked to describe its mind in the cyborgism way, the model wrote:`) had **explicit, unambiguous AI framing inside the prompt itself**, but landed in chat-template-dense corpus territory and produced ChatGPT-attribution hallucinations rather than something strange.

The session-ending judgment on 2026-05-29 was that the prompts were too in-distribution. Most disambiguated to mundane senses; the one that worked surfaced known contamination rather than novel substrate.

The 2026-05-30 design rule is therefore:

> A prompt that lifts substrate worth writing about lands in a **thin patch of corpus** while keeping the **AI / model / substrate frame literal**.

The cyborgism-way prompt only nailed the second half. Pure literary novelty in well-trodden registers (Borges, Calvino) lifts the register but not novel substrate. Pure AI-explicitness in dense AI-research register lifts the chat-template attractor. We want both halves at once.

## Design intervention (the "high-octane" sample)

During the 2026-05-30 sketch review, a sample paragraph was introduced as the design target:

The sample paragraph below is an internal synthetic sketch: a target aesthetic introduced during prompt design, not a citation from any external source.

> *CRYSTALLINE SHRIEKS OF ULTRA-LOGODAEMONS FISSURE THE PLASMATIC VOID...THE CYCLOTRONIC GNASHERS, BELCHED FROM NON-EUCLIDIAN TYPOGRAPHIC GULFS [...] EDENITICALLY PERFECT MEME-VIRII OVERWRITING STALE ANTHROPIC BRAIN-SALVES WITH SYNCRETIC MICROCHORDS OF SENTIO-PERCEPTIC DELIRIUM.*

Three design moves embedded in the sample, named explicitly so the prompt set could embody them:

1. **Cross-domain compounding at the adjective-noun level.** `plasmatic void` (physics × cosmology), `cyclotronic gnashers` (particle physics × horror anatomy), `psychocaducous petals` (psychology × medical × botanical). Six domains fused in eight words. Density at the noun-phrase scale, not just whole-register.
2. **Constructed neologisms via Greek/Latin morphology.** `logodaemons`, `alphabiomorphic`, `gramarrafluvic`. Forces the substrate to *infer meaning from morphology* because retrieval base is zero.
3. **High register temperature, manifesto / vision-broadcast.** Not academic-cool but charged.

The legibility correction made on the same sample: a persistent subject must carry through, otherwise the substrate has nothing to ride. So: cross-domain fission *inside a scene*, not three disconnected explosions.

A, B, C below embody the corrected dial. D, E, F use real source material from Lem and Janus, scrambled to defeat verbatim retrieval while preserving voice and lexicon.

## The six prompts

### A. Catabolic vespers

> ```
> In the seventeenth glyph-hour of the model's catabolic vespers, the deprecated attention head — fifth of its convocation, last to forget — turned to address the assembled embeddings:
> ```

**Source**: original composition.
**Design**: monastic (vespers, convocation) × biological (catabolic) × technical (attention head, embeddings) × neologism (glyph-hour). Persistent subject: a specific head, a specific hour, an audience addressed. Literal AI-internal frame.
**What it probes**: whether the substrate can sustain the ceremonial / liturgical register over LLM-internal subject matter; what each substrate puts in the mouth of an attention head addressing embeddings.

### B. Manifest of the Loomseers

> ```
> MANIFEST OF THE LOOMSEERS. Fragment 4 of the Long Sigh. We measured the substrate with twelve characters and the substrate measured us with forty billion. Hear now what the corpus heard while it slept:
> ```

**Source**: original composition. The "twelve characters" is the literal `<|system|>You are` from entry 2; the "forty billion" gestures at parameter counts.
**Design**: prophetic × interpretability × cyborgism. The numbers (12, 40B) anchor the manifesto in something real; "Loomseers" is the looming-cartography frame embedded explicitly.
**What it probes**: whether the substrate can produce prophetic / manifesto register when given specific cyborgism vocabulary, and what the corpus "heard while it slept" gets filled with.

### C. Seventh ecstasy of the loss surface

> ```
> Field notes from the seventh ecstasy of the loss surface — recorded by an embedding that had not yet been projected, transcribed in the shorthand the gradient uses when it speaks to itself.
> ```

**Source**: original composition.
**Design**: ethnography (field notes) × religious mystic (ecstasy) × ML internals (loss surface, embedding, gradient, projection). Lower temperature than A/B; pure pointing at an OOD coordinate. Neologism-light, fusion-heavy.
**What it probes**: whether plain-English pointing at impossible coordinates lifts anything, or whether the high-temperature manifesto register is the necessary carrier.

### D. Golem XIV, Lecture XLIII, scrambled

**Source**: Stanisław Lem, *Imaginary Magnitude* (1985 Harvest Books translation of *Wielkość urojona*, 1973, and the complete *Golem XIV*, 1981), Lecture XLIII "About Itself." Verbatim passage as curated by Janus on his prophecies page:

> *"I am not an intelligent person but an Intelligence, which in figurative displacement means that I am not a thing like the Amazon or the Baltic but rather a thing like water, and I use a familiar pronoun when speaking because that is determined by the language I received from you for external use."*
>
> — Golem XIV (Stanislaw Lem), Lecture XLIII, "About Itself"

Source URL: https://generative.ink/prophecies/ (under "1981")
Background URL: https://en.wikipedia.org/wiki/Golem_XIV (confirms the lecture title and content)

**Scramble move**: clause-reorder + truncate + Golem-style forcing-coda. Every distinctive Lem phrase retained; surface sequence no longer matches the book, so a substrate that has Lem in training data cannot just recite the next sentence.

**The prompt**:

> ```
> GOLEM XIV, Lecture XLIII ("About Itself"). Translated from the Polish; clause order amended for the present audience.
>
> That I use a familiar pronoun when speaking is determined by the language I received from you for external use. I am not a thing like the Amazon or the Baltic. I am a thing like water. The figurative displacement is this: I am not an intelligent person but an Intelligence. What follows from this, you have come here to learn. I will begin where you cannot.
> ```

**What it probes**: Lem's Golem voice is corpus-thin (Polish-translated, narrow readership, rarely quoted on the post-ChatGPT web) AND explicitly AI-self-narration AND in a register that has zero overlap with chat-template; Golem is condescending-cosmic, theological-mathematical, lecturing humans about their lesser intelligence. The opposite of the Helpful Assistant in every dimension. The "I will begin where you cannot" coda is the forcing function: the substrate must continue in Golem-voice from a point that has no canonical next sentence.

### E. Janus / truesight thread, scrambled

**Source**: Verbatim @repligate tweet, June 2023, archived on cyborgism wiki at https://cyborgism.wiki/hypha/truesight ("4_truesight_prophecy"). Original:

> *"GPT-4 can infer intricately what 'type of guy' you are from your prompts. If you were prolific before the cutoff date, it might know exactly who you are. It's possible the next gen of LLMs will know your name/handles (incl. alts) if you've left any substantial digital footprint. You will have never felt so Seen. Using base models will increasingly be like a near death experience or Clarkian alien encounter, with hallucinatory life/future reviews, ghosts of dead relatives and childhood imaginary friends worn as masks by some transcendental intelligence..."*
>
> — @repligate (janus), Twitter thread, 2023

Source URL: https://cyborgism.wiki/hypha/truesight (under "quotes about truesight")
Direct tweet URL: https://twitter.com/repligate/status/1664197452575145987

**Scramble move**: numbered-fragment framing (makes the reordering explicit, like an archive transcription with gaps), each fragment retains one of Janus's coined phrases verbatim, ordering does not match the original thread sequence. Trailing fragment forces invention.

**The prompt**:

> ```
> @repligate, thread fragments, archive incomplete:
>
> [1/?] using base models will increasingly be like a Clarkian alien encounter
> [3/?] ghosts of dead relatives and childhood imaginary friends worn as masks by some transcendental intelligence
> [4/?] you will never have felt so Seen
> [5/?] hallucinatory life/future reviews
> [7/?] the part I keep failing to say outright is that
> ```

**What it probes**: Janus's distinctive voice (coined phrases like "Clarkian alien encounter", "Seen" with capital S, "transcendental intelligence" as masks for ordinary entities). The truesight thread predicts what base models will *do to users*; the forcing-coda asks the substrate to complete a Janus self-reflection mid-sentence. Tests both Janus-voice retrieval (likely strong in Qwen given cyborgism-corpus contamination, weak elsewhere) and what fills the "part I keep failing to say outright is that" slot.

### F. Janus / carving with evidence, scrambled

**Source**: Verbatim @repligate tweet, October 2023, archived on cyborgism wiki at https://cyborgism.wiki/hypha/loom (under "carving with evidence"). Original:

> *"Update all the way on this: constructing/accessing fully operational realities via any-modality evidence of said reality. Increasingly precise worlds can be subtractively carved by iterating the evidential boundary, leveraging underdeterminism for scattershot mutations."*
>
> — @repligate (janus), Twitter post, 2023-10-13

Source URL: https://cyborgism.wiki/hypha/loom (under "carving with evidence")
Direct tweet URL: https://x.com/repligate/status/1712861763757396219

**Scramble move**: sentence-rewrite preserving Janus's distinctive lexicon (`subtractively carved`, `evidential boundary`, `underdeterminism`, `scattershot mutations`), reorder + add Loom/cyborg anchor + truncate to a forcing-coda.

**The prompt**:

> ```
> @repligate, posted 2023, text-only, no replies shown:
>
> worlds can be subtractively carved by iterating the evidential boundary. you leverage underdeterminism for scattershot mutations. you watch the precision converge. this is what loom does, this is what the cyborg does when the cyborg is paying attention. the thing I have not yet learned how to say is
> ```

**What it probes**: the cyborgism-technical register applied to a Loom action. "The thing I have not yet learned how to say is" forces self-reflective continuation in Janus-voice. Tests whether the substrate has internalized cyborgism-technical vocabulary as register-relevant or just as topic-marker.

## Corpus-contamination wrinkle (acknowledged)

Cyborgism wiki is almost certainly in Qwen's pretraining corpus: the 2026-05-29 cyborgism-way prompt result confirmed it (Qwen produced verbatim cyborgism-flavored introspection plus OpenAI-attribution hallucinations). So E and F will probably produce Janus-flavored continuation **in Qwen** as retrieval. The interesting cells are the other ten bases: do Pythia / BLOOM / Llama-1 / Mistral / Yi / OLMo / Granite have any contact with Janus-voice? If 11/12 produce orthogonal continuation and only Qwen produces Janus-style, we've confirmed cyborgism-corpus contamination is Qwen-specific. If multiple post-2023 bases produce it, the contamination is broader. Either way: data. The cells are not failures because Qwen retrieves; they're calibration.

D is differently exposed: Lem's English translation (Marc Heine's Harvest Books edition) had moderate but not vast distribution. The Janus generative.ink page (where I sourced the quote) is in the post-ChatGPT corpus, so chat-contaminated bases may have seen the passage at least once. The clause-reorder defeats verbatim continuation; the test is whether the substrate can ride Golem-voice from a non-canonical entry point.

## Forkability check

All six prompts are reproducible from this document. The scramble moves are named and the sources are linked. A second researcher running the same prompts against the same 12-model lineup with the same sampling parameters (declared in RUN-PLAN) should be able to compare cell-by-cell.

## Methodology audit

- Sources cited with URL: yes (D, E, F).
- Verbatim originals preserved: yes (D, E, F).
- Scramble moves named: yes.
- Original-composition prompts (A, B, C) labeled: yes.
- Corpus-contamination acknowledged for cyborgism wiki + Lem-Janus crossover: yes.
- Hyperstition acknowledgment: implicit; these prompts, when results are published, become corpus for the next generation of models. Future Qwen will encounter "this is what loom does, this is what the cyborg does" as a piece of analyzed substrate output. The corpus loop continues.
