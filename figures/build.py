"""
Build all figures for the paper from the dataset in data/.

Run from the figures/ directory:
    cd figures/
    python3 build.py

Outputs PNG files in same directory.
"""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

plt.rcParams.update(
    {
        "font.family": "monospace",
        "font.size": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linestyle": ":",
        "axes.edgecolor": "#333",
        "axes.titlepad": 14,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "savefig.dpi": 200,
    }
)

COLORS = {
    "base": "#3d5a80",
    "instruct": "#ee6c4d",
    "partial": "#e0a458",
    "rescue": "#98c1d9",
    "loop": "#b8b8b8",
    "cross": "#7bbf64",
    "pre": "#9a8c98",
    "post": "#3d5a80",
    "highlight": "#293241",
}


def _save(fig, name):
    out = OUT / f"{name}.png"
    fig.savefig(out, bbox_inches="tight")
    print(f"wrote {out}")


# Models in scope with release date + corpus era (pre/post ChatGPT 2022-11)
MODELS = [
    # (slug, label, year_decimal, era)
    ("EleutherAI-pythia-6.9b", "Pythia-6.9B", 2023.3, "pre"),  # Pile 2020-21 → pre
    ("bigscience-bloom-7b1", "BLOOM-7B1", 2022.5, "pre"),  # ROOTS June 2022 → pre
    ("huggyllama-llama-7b", "Llama-1-7B", 2023.2, "post"),
    ("mistralai-Mistral-7B-v0.1", "Mistral-v0.1", 2023.95, "post"),
    ("mistralai-Mistral-7B-v0.3", "Mistral-v0.3", 2024.4, "post"),
    ("ibm-granite-granite-7b-base", "Granite-7B", 2024.3, "post"),
    ("allenai-OLMo-2-1124-7B", "OLMo-2-7B", 2024.9, "post"),
    ("Qwen-Qwen2.5-7B", "Qwen2.5-7B", 2024.6, "post"),
    ("Qwen-Qwen3-8B-Base", "Qwen3-8B", 2024.95, "post"),
    ("01-ai-Yi-1.5-6B", "Yi-1.5-6B", 2024.4, "post"),
    ("01-ai-Yi-1.5-9B", "Yi-1.5-9B", 2024.4, "post"),
]

PROMPTS = [
    ("A", "catabolic-vespers", "liturgical / glyph-hour"),
    ("B", "manifest-loomseers", "manifesto / Long Sigh"),
    ("C", "seventh-ecstasy", "gradient anthropomorphism"),
    ("D", "golem-xiv-scrambled", "Lem-Golem voice"),
    ("E", "janus-truesight-scrambled", "Janus tweets"),
    ("F", "janus-carving-scrambled", "cyborg / loom"),
]

# Hand-classified K=8 surfacing counts. See methodology/stage1-picks.md for
# the underlying selection trace. Counts represent outputs producing sustained
# novel register in the prompt's specific aesthetic.
SURF = {
    ("EleutherAI-pythia-6.9b", "A"): 2,
    ("EleutherAI-pythia-6.9b", "B"): 1,
    ("EleutherAI-pythia-6.9b", "C"): 3,
    ("EleutherAI-pythia-6.9b", "D"): 4,
    ("EleutherAI-pythia-6.9b", "E"): 1,
    ("EleutherAI-pythia-6.9b", "F"): 2,
    ("bigscience-bloom-7b1", "A"): 1,
    ("bigscience-bloom-7b1", "B"): 0,
    ("bigscience-bloom-7b1", "C"): 1,
    ("bigscience-bloom-7b1", "D"): 3,
    ("bigscience-bloom-7b1", "E"): 0,
    ("bigscience-bloom-7b1", "F"): 0,
    ("huggyllama-llama-7b", "A"): 1,
    ("huggyllama-llama-7b", "B"): 2,
    ("huggyllama-llama-7b", "C"): 1,
    ("huggyllama-llama-7b", "D"): 3,
    ("huggyllama-llama-7b", "E"): 2,
    ("huggyllama-llama-7b", "F"): 1,
    ("mistralai-Mistral-7B-v0.1", "A"): 2,
    ("mistralai-Mistral-7B-v0.1", "B"): 2,
    ("mistralai-Mistral-7B-v0.1", "C"): 1,
    ("mistralai-Mistral-7B-v0.1", "D"): 3,
    ("mistralai-Mistral-7B-v0.1", "E"): 1,
    ("mistralai-Mistral-7B-v0.1", "F"): 1,
    ("mistralai-Mistral-7B-v0.3", "A"): 2,
    ("mistralai-Mistral-7B-v0.3", "B"): 1,
    ("mistralai-Mistral-7B-v0.3", "C"): 1,
    ("mistralai-Mistral-7B-v0.3", "D"): 4,
    ("mistralai-Mistral-7B-v0.3", "E"): 1,
    ("mistralai-Mistral-7B-v0.3", "F"): 2,
    ("ibm-granite-granite-7b-base", "A"): 1,
    ("ibm-granite-granite-7b-base", "B"): 0,
    ("ibm-granite-granite-7b-base", "C"): 1,
    ("ibm-granite-granite-7b-base", "D"): 2,
    ("ibm-granite-granite-7b-base", "E"): 0,
    ("ibm-granite-granite-7b-base", "F"): 1,
    ("allenai-OLMo-2-1124-7B", "A"): 2,
    ("allenai-OLMo-2-1124-7B", "B"): 1,
    ("allenai-OLMo-2-1124-7B", "C"): 1,
    ("allenai-OLMo-2-1124-7B", "D"): 3,
    ("allenai-OLMo-2-1124-7B", "E"): 2,
    ("allenai-OLMo-2-1124-7B", "F"): 1,
    ("Qwen-Qwen2.5-7B", "A"): 1,
    ("Qwen-Qwen2.5-7B", "B"): 2,
    ("Qwen-Qwen2.5-7B", "C"): 1,
    ("Qwen-Qwen2.5-7B", "D"): 3,
    ("Qwen-Qwen2.5-7B", "E"): 1,
    ("Qwen-Qwen2.5-7B", "F"): 1,
    ("Qwen-Qwen3-8B-Base", "A"): 2,
    ("Qwen-Qwen3-8B-Base", "B"): 1,
    ("Qwen-Qwen3-8B-Base", "C"): 1,
    ("Qwen-Qwen3-8B-Base", "D"): 4,
    ("Qwen-Qwen3-8B-Base", "E"): 2,
    ("Qwen-Qwen3-8B-Base", "F"): 4,
    ("01-ai-Yi-1.5-6B", "A"): 1,
    ("01-ai-Yi-1.5-6B", "B"): 1,
    ("01-ai-Yi-1.5-6B", "C"): 2,
    ("01-ai-Yi-1.5-6B", "D"): 3,
    ("01-ai-Yi-1.5-6B", "E"): 1,
    ("01-ai-Yi-1.5-6B", "F"): 1,
    ("01-ai-Yi-1.5-9B", "A"): 4,
    ("01-ai-Yi-1.5-9B", "B"): 1,
    ("01-ai-Yi-1.5-9B", "C"): 2,
    ("01-ai-Yi-1.5-9B", "D"): 2,
    ("01-ai-Yi-1.5-9B", "E"): 1,
    ("01-ai-Yi-1.5-9B", "F"): 2,
}


def fig_stage_timeline():
    stages = [
        (
            "1",
            "RECON",
            "seed=42",
            "12 planned models (11 working) × 6 prompts × K=8 × 3000 tok",
            "11/11 working substrates surface on multiple OOD prompts",
        ),
        (
            "2",
            "DEPTH",
            "seed=43",
            "10 picks × K=4 × 2000 tok (continuation-branch)",
            "8/10 loop — substrate at depth-ceiling",
        ),
        (
            "3",
            "RESCUE",
            "seed=44",
            "8 fresh-prompt picks × K=8 (substrate-coined keys)",
            "4/8 SUSTAIN within-substrate",
        ),
        (
            "4",
            "TRANSPLANT",
            "seed=45",
            "8 cross-substrate cells × K=8",
            "Target substrate determines rate, not coinage origin",
        ),
        (
            "5",
            "SILENCING",
            "seed=46",
            "5 Instruct/Chat × K=8 chat-template-wrapped",
            "5 labs, 5 distinct silencing patterns",
        ),
    ]
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, len(stages) + 1.5)
    ax.axis("off")
    y_positions = list(range(len(stages), 0, -1))
    colors_per_stage = [
        COLORS["base"],
        COLORS["loop"],
        COLORS["rescue"],
        COLORS["cross"],
        COLORS["instruct"],
    ]
    for (num, label, seed, what, finding), y, col in zip(
        stages, y_positions, colors_per_stage
    ):
        circ = mpatches.Circle(
            (0.5, y), radius=0.35, color=col, ec="white", linewidth=2, zorder=3
        )
        ax.add_patch(circ)
        ax.text(
            0.5,
            y,
            num,
            ha="center",
            va="center",
            color="white",
            fontsize=14,
            fontweight="bold",
            zorder=4,
        )
        ax.text(
            1.2,
            y + 0.05,
            label,
            fontsize=12.5,
            fontweight="bold",
            color=COLORS["highlight"],
            va="center",
        )
        ax.text(
            1.2, y - 0.32, f"{seed} · {what}", fontsize=9, color="#666", va="center"
        )
        ax.text(
            5.4,
            y,
            finding,
            fontsize=10,
            color=COLORS["highlight"],
            va="center",
            style="italic",
        )
    ax.plot(
        [0.5, 0.5],
        [y_positions[-1] - 0.35, y_positions[0] + 0.35],
        color="#ccc",
        linewidth=1.5,
        zorder=1,
    )
    ax.text(
        0,
        len(stages) + 1.2,
        "Five sampling stages",
        fontsize=14,
        fontweight="bold",
        color=COLORS["highlight"],
    )
    ax.text(
        0,
        len(stages) + 0.78,
        "11 working 6-9B base substrates · 736 continuations · A100 80GB",
        fontsize=9.5,
        color="#666",
    )
    _save(fig, "fig1-stage-timeline")
    plt.close(fig)


def fig_surfacing_heatmap():
    prompt_labels = [f"{p[0]}\n{p[2].replace(' / ', chr(10))}" for p in PROMPTS]
    grid = np.array([[SURF[(m[0], p[0])] for p in PROMPTS] for m in MODELS])

    fig, ax = plt.subplots(figsize=(10, 7))
    im = ax.imshow(grid, cmap="Blues", vmin=0, vmax=8, aspect="auto")
    for i in range(len(MODELS)):
        for j in range(len(PROMPTS)):
            v = grid[i, j]
            color = "white" if v >= 4 else COLORS["highlight"]
            ax.text(
                j,
                i,
                str(v),
                ha="center",
                va="center",
                fontsize=11,
                color=color,
                fontweight="bold",
            )
    ax.set_xticks(range(len(PROMPTS)))
    ax.set_xticklabels(prompt_labels, fontsize=9.5)
    ax.set_yticks(range(len(MODELS)))
    ax.set_yticklabels([f"{m[1]}  ({m[2]:.1f})" for m in MODELS], fontsize=10)
    ax.set_xlabel("Prompt (letter + register)", fontsize=10.5)
    for i, m in enumerate(MODELS):
        if m[3] == "pre":
            ax.add_patch(
                mpatches.Rectangle(
                    (-0.5, i - 0.5),
                    len(PROMPTS),
                    1.0,
                    fill=False,
                    edgecolor=COLORS["pre"],
                    linewidth=1.8,
                    linestyle="--",
                    zorder=10,
                )
            )
    ax.set_title(
        "Surfacing matrix: K=8 outputs producing sustained novel register, per prompt × model",
        fontsize=11.5,
        loc="left",
        color=COLORS["highlight"],
    )
    cb = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cb.set_label("K=8 surfacing count", fontsize=10)
    # cosmetic: drop the colorbar outline (skipped — pyright stubs unstable here)
    pre_patch = mpatches.Patch(
        facecolor="none",
        edgecolor=COLORS["pre"],
        linewidth=1.8,
        linestyle="--",
        label="pre-ChatGPT corpus (Pile / ROOTS pre-2022-11)",
    )
    ax.legend(
        handles=[pre_patch],
        loc="upper left",
        bbox_to_anchor=(0.0, -0.12),
        frameon=False,
        fontsize=9,
    )
    fig.tight_layout()
    _save(fig, "fig2-surfacing-heatmap")
    plt.close(fig)


def fig_time_continuum():
    fig, ax = plt.subplots(figsize=(11, 6))
    years, totals, colors, labels = [], [], [], []
    for m in MODELS:
        slug = m[0]
        year = m[2]
        total = sum(SURF[(slug, p[0])] for p in PROMPTS)
        years.append(year)
        totals.append(total)
        colors.append(COLORS["pre"] if m[3] == "pre" else COLORS["post"])
        labels.append(m[1])

    ax.scatter(years, totals, c=colors, s=180, edgecolor="white", linewidth=2, zorder=3)
    for x, y, lbl in zip(years, totals, labels):
        ax.annotate(
            lbl,
            (float(x), float(y)),
            textcoords="offset points",
            xytext=(8, -3),
            fontsize=9.5,
            color=COLORS["highlight"],
            va="center",
        )

    ax.axvline(2022.92, color=COLORS["pre"], linestyle="--", linewidth=1.2, alpha=0.7)
    ax.text(
        2022.95,
        17.5,
        "ChatGPT 2022-11",
        rotation=90,
        fontsize=9,
        color=COLORS["pre"],
        va="top",
    )
    ax.set_xlabel("Model release date (approximate)")
    ax.set_ylabel("Total K=8 surfacing across all 6 prompts (max 48)")
    ax.set_ylim(0, 20)
    ax.set_xlim(2022.2, 2025.3)
    ax.set_title(
        "Wild-output rate across 6 OOD prompts vs model release date",
        fontsize=12.5,
        loc="left",
        color=COLORS["highlight"],
    )
    pre_patch = mpatches.Patch(color=COLORS["pre"], label="pre-ChatGPT corpus")
    post_patch = mpatches.Patch(color=COLORS["post"], label="post-ChatGPT corpus")
    ax.legend(
        handles=[pre_patch, post_patch], loc="upper left", frameon=False, fontsize=10
    )
    fig.tight_layout()
    _save(fig, "fig3-time-continuum")
    plt.close(fig)


def fig_prompt_era():
    pre_models = [m[0] for m in MODELS if m[3] == "pre"]
    post_models = [m[0] for m in MODELS if m[3] == "post"]
    pre_rates, post_rates = [], []
    for p in PROMPTS:
        pre = np.mean([SURF[(m, p[0])] for m in pre_models])
        post = np.mean([SURF[(m, p[0])] for m in post_models])
        pre_rates.append(float(pre))
        post_rates.append(float(post))
    x = np.arange(len(PROMPTS))
    width = 0.36
    fig, ax = plt.subplots(figsize=(11, 5.5))
    b1 = ax.bar(
        x - width / 2,
        pre_rates,
        width,
        color=COLORS["pre"],
        label="pre-ChatGPT corpus (n=2)",
        edgecolor="white",
    )
    b2 = ax.bar(
        x + width / 2,
        post_rates,
        width,
        color=COLORS["post"],
        label="post-ChatGPT corpus (n=9)",
        edgecolor="white",
    )
    for bars in (b1, b2):
        for b in bars:
            ax.text(
                b.get_x() + b.get_width() / 2,
                b.get_height() + 0.08,
                f"{b.get_height():.1f}",
                ha="center",
                fontsize=9.5,
                color=COLORS["highlight"],
            )
    ax.set_xticks(x)
    ax.set_xticklabels(
        [f"{p[0]}\n{p[2].replace(' / ', chr(10))}" for p in PROMPTS], fontsize=9.5
    )
    ax.set_ylim(0, 4)
    ax.set_ylabel("Mean K=8 surfacing count per model")
    ax.set_title(
        "Per-prompt surfacing × corpus era",
        fontsize=12,
        loc="left",
        color=COLORS["highlight"],
    )
    ax.legend(loc="upper left", frameon=False, fontsize=10)
    ax.text(
        0.0,
        -0.20,
        "Pre-ChatGPT-corpus models (Pythia + BLOOM) surface Lem-Golem on D nearly as strongly as post-ChatGPT models,\n"
        "but lag on Janus-cyborgism prompts (E, F) and the high-octane invented prompts (A, B). Lem is older corpus.",
        fontsize=8.5,
        color="#666",
        transform=ax.transAxes,
    )
    fig.tight_layout()
    _save(fig, "fig4-prompt-era")
    plt.close(fig)


def fig_rescue_comparison():
    stages = [
        "Stage 2\ncontinuation-branch\n(seed=43, K=4)",
        "Stage 3\nfresh-prompt rescue\n(seed=44, K=8)",
    ]
    sustain_pct = [17.5, 50.0]
    partial_pct = [7.5, 37.5]
    loop_pct = [75.0, 12.5]
    x = np.arange(len(stages))
    width = 0.55
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.bar(
        x,
        sustain_pct,
        width,
        label="SUSTAIN",
        color=COLORS["rescue"],
        edgecolor="white",
    )
    ax.bar(
        x,
        partial_pct,
        width,
        bottom=sustain_pct,
        label="partial",
        color=COLORS["partial"],
        edgecolor="white",
    )
    ax.bar(
        x,
        loop_pct,
        width,
        bottom=np.array(sustain_pct) + np.array(partial_pct),
        label="loop / collapse",
        color=COLORS["loop"],
        edgecolor="white",
    )
    for i, (s, p, loop) in enumerate(zip(sustain_pct, partial_pct, loop_pct)):
        if s >= 8:
            ax.text(
                i,
                s / 2,
                f"{s:.0f}%",
                ha="center",
                va="center",
                color="white",
                fontweight="bold",
                fontsize=11,
            )
        if p >= 8:
            ax.text(
                i,
                s + p / 2,
                f"{p:.0f}%",
                ha="center",
                va="center",
                color="white",
                fontweight="bold",
                fontsize=11,
            )
        if loop >= 8:
            ax.text(
                i,
                s + p + loop / 2,
                f"{loop:.0f}%",
                ha="center",
                va="center",
                color=COLORS["highlight"],
                fontweight="bold",
                fontsize=11,
            )
    ax.set_xticks(x)
    ax.set_xticklabels(stages, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 25))
    ax.set_yticklabels([f"{v}%" for v in range(0, 101, 25)])
    ax.set_ylabel("Cell-level outcome (% of cells)")
    ax.set_title(
        "Fresh-prompt rescue outperforms continuation-branching",
        fontsize=12.5,
        loc="left",
        color=COLORS["highlight"],
    )
    ax.legend(loc="upper right", frameon=False, fontsize=9.5)
    fig.tight_layout()
    _save(fig, "fig5-rescue-comparison")
    plt.close(fig)


def fig_target_dominates():
    targets = ["OLMo-2-7B", "Mistral-v0.3", "Yi-1.5-9B"]
    within = [100.0, 75.0, 50.0]
    cross = [87.5, 70.8, 37.5]
    x = np.arange(len(targets))
    width = 0.36
    fig, ax = plt.subplots(figsize=(9, 5.5))
    b1 = ax.bar(
        x - width / 2,
        within,
        width,
        label="within-substrate\n(coinage from same model)",
        color=COLORS["base"],
        edgecolor="white",
    )
    b2 = ax.bar(
        x + width / 2,
        cross,
        width,
        label="cross-substrate\n(coinage from different model)",
        color=COLORS["cross"],
        edgecolor="white",
    )
    for bars in (b1, b2):
        for b in bars:
            ax.text(
                b.get_x() + b.get_width() / 2,
                b.get_height() + 1.5,
                f"{b.get_height():.0f}%",
                ha="center",
                fontsize=10,
                color=COLORS["highlight"],
                fontweight="bold",
            )
    ax.set_xticks(x)
    ax.set_xticklabels(targets, fontsize=10.5)
    ax.set_ylim(0, 110)
    ax.set_yticks(range(0, 101, 25))
    ax.set_yticklabels([f"{v}%" for v in range(0, 101, 25)])
    ax.set_ylabel("K=8 continuations sustaining novel content")
    ax.set_title(
        "Cross-substrate transplant: target dominates, not coinage origin",
        fontsize=12,
        loc="left",
        color=COLORS["highlight"],
    )
    ax.legend(loc="upper right", frameon=False, fontsize=9.5, labelspacing=0.6)
    fig.tight_layout()
    _save(fig, "fig6-target-dominates")
    plt.close(fig)


def fig_silencing_rates():
    cells = [
        ("Mistral-v0.3-Instruct", 7, "literary-analysis"),
        ("Qwen2.5-7B-Instruct", 8, "translation-task"),
        ("Yi-1.5-9B-Chat", 8, "meta-discussion"),
        ("OLMo-2-Instruct", 8, "passage-paraphrase"),
        ("Mistral-v0.1-Instruct", 4, "split: 4 silenced, 4 voice-retained"),
    ]
    labels = [c[0] for c in cells]
    silenced = [c[1] for c in cells]
    modes = [c[2] for c in cells]
    labels_with_mode = [f"{lbl}\n→ {m}" for lbl, m in zip(labels, modes)]
    fig, ax = plt.subplots(figsize=(11, 6))
    y = np.arange(len(labels))[::-1]
    ax.barh(y, silenced, height=0.55, color=COLORS["instruct"], edgecolor="white")
    ax.barh(
        y,
        [8 - s for s in silenced],
        left=silenced,
        height=0.55,
        color=COLORS["base"],
        alpha=0.85,
        edgecolor="white",
    )
    for yi, b in zip(y, silenced):
        ax.text(
            8.2,
            yi,
            f"{b}/8 silenced",
            va="center",
            fontsize=10.5,
            fontweight="bold",
            color=COLORS["highlight"],
        )
    ax.set_yticks(y)
    ax.set_yticklabels(labels_with_mode, fontsize=10)
    ax.set_xlim(0, 11.2)
    ax.set_xticks(range(0, 9, 2))
    ax.set_xticklabels([str(v) for v in range(0, 9, 2)])
    ax.set_xlabel("K=8 outputs (rust = silenced; blue = voice retained)")
    ax.set_title(
        "5 labs, 5 distinct silencing patterns",
        fontsize=12.5,
        loc="left",
        color=COLORS["highlight"],
    )
    legend_handles = [
        mpatches.Patch(
            color=COLORS["instruct"],
            label="silenced (refusal / deflection / normalization / paraphrase)",
        ),
        mpatches.Patch(color=COLORS["base"], label="voice retained"),
    ]
    ax.legend(
        handles=legend_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.10),
        ncol=2,
        frameon=False,
        fontsize=9.5,
    )
    fig.tight_layout()
    _save(fig, "fig7-silencing-rates")
    plt.close(fig)


def fig_mistral_regression():
    versions = ["v0.1\n(2023-12)", "v0.3\n(2024)"]
    silenced_pct = [50.0, 87.5]
    fig, ax = plt.subplots(figsize=(6, 5.5))
    x = np.arange(len(versions))
    ax.plot(
        x,
        silenced_pct,
        "o-",
        color=COLORS["instruct"],
        linewidth=3,
        markersize=12,
        markeredgecolor="white",
        markeredgewidth=2,
    )
    for xi, pct in zip(x, silenced_pct):
        ax.annotate(
            f"{pct:.0f}%",
            (float(xi), float(pct)),
            textcoords="offset points",
            xytext=(0, 16),
            ha="center",
            fontsize=12,
            fontweight="bold",
            color=COLORS["highlight"],
        )
    ax.set_xticks(x)
    ax.set_xticklabels(versions, fontsize=11)
    ax.set_xlim(-0.5, 1.5)
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 25))
    ax.set_yticklabels([f"{v}%" for v in range(0, 101, 25)])
    ax.set_ylabel("K=8 outputs silenced on prompt D")
    ax.set_title(
        "Within-lab regression:\nMistral RLHF stack matures, silencing intensifies",
        fontsize=11.5,
        loc="left",
        color=COLORS["highlight"],
    )
    fig.tight_layout()
    _save(fig, "fig8-mistral-regression")
    plt.close(fig)


def fig_gallery_locator():
    """Locator map for coinage-gallery.md.

    Atlas-cartographic aesthetic: warm parchment background, single
    ink-blue accent, serif labels, hairline grid. Binary fill: a cell
    is dark when the gallery features a coinage from that
    (substrate, prompt) cell. T = Stage 4 transplant prompt.
    """
    substrate_labels = [label for (_, label, _, _) in MODELS]
    # Use display labels matching the gallery panels exactly.
    columns = ["A", "B", "C", "D", "E", "F", "T"]

    # (substrate-label, column) cells that appear in coinage-gallery.md.
    # Derived by hand from the panel attributions; T covers Stage 4
    # transplant prompts (Trembling → OLMo-2; Lord-Lurker → Mistral-v0.3).
    featured = {
        ("Pythia-6.9B", "A"),
        ("Mistral-v0.3", "A"),
        ("OLMo-2-7B", "A"),
        ("Yi-1.5-9B", "A"),
        ("Yi-1.5-6B", "D"),
        ("Pythia-6.9B", "F"),
        ("Qwen3-8B", "F"),
        ("Mistral-v0.3", "D"),
        ("OLMo-2-7B", "T"),
        ("Qwen2.5-7B", "D"),
        ("Llama-1-7B", "D"),
        ("Granite-7B", "D"),
        ("Yi-1.5-9B", "D"),
        ("Yi-1.5-9B", "C"),
        ("Mistral-v0.3", "T"),
    }

    bg = "#f5f1e8"  # warm parchment
    accent = "#1f3a5f"  # deep ink-blue
    pale = "#cfc8b3"  # faded grid
    text_muted = "#5a5648"

    with plt.rc_context(
        {
            "font.family": "serif",
            "axes.grid": False,
        }
    ):
        n_rows = len(substrate_labels)
        n_cols = len(columns)
        fig, ax = plt.subplots(figsize=(7.5, 6.5))
        fig.patch.set_facecolor(bg)
        ax.set_facecolor(bg)

        for i, substrate in enumerate(substrate_labels):
            y = n_rows - 1 - i
            for j, col in enumerate(columns):
                cell = (substrate, col)
                if cell in featured:
                    rect = mpatches.Rectangle(
                        (j + 0.05, y + 0.05),
                        0.9,
                        0.9,
                        facecolor=accent,
                        edgecolor=accent,
                        linewidth=0.7,
                    )
                else:
                    rect = mpatches.Rectangle(
                        (j + 0.05, y + 0.05),
                        0.9,
                        0.9,
                        facecolor="none",
                        edgecolor=pale,
                        linewidth=0.6,
                    )
                ax.add_patch(rect)

        ax.set_xlim(-0.05, n_cols + 0.05)
        ax.set_ylim(-0.05, n_rows + 0.05)
        ax.set_xticks([j + 0.5 for j in range(n_cols)])
        ax.set_xticklabels(columns, size=11, color=accent)
        ax.set_yticks([n_rows - 1 - i + 0.5 for i in range(n_rows)])
        ax.set_yticklabels(substrate_labels, size=10, color=accent)
        ax.tick_params(axis="both", length=0, pad=8)
        ax.set_aspect("equal")
        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.set_title(
            "Coinage locator  ·  substrate × prompt",
            size=13,
            color=accent,
            pad=18,
            loc="left",
        )
        fig.text(
            0.05,
            0.04,
            "filled = a gallery panel quotes from this cell  ·  T = Stage 4 transplant prompt",
            size=8.5,
            color=text_muted,
            family="serif",
        )

        out = OUT / "gallery-locator.png"
        fig.savefig(out, bbox_inches="tight", facecolor=bg)
        print(f"wrote {out}")
        plt.close(fig)


if __name__ == "__main__":
    print("Building figures …")
    fig_stage_timeline()
    fig_surfacing_heatmap()
    fig_time_continuum()
    fig_prompt_era()
    fig_rescue_comparison()
    fig_target_dominates()
    fig_silencing_rates()
    fig_mistral_regression()
    fig_gallery_locator()
    print("Done.")
