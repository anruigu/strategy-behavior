#!/usr/bin/env python3
"""The 0902/03 separability pilots as three PNGs, for `docs/hackable-games.md`.

    python make_doc_figs.py            # -> ../docs/figs/*.png

Each figure replaces a Markdown table in section 3 of that doc, which is the
only consumer:

  1. `pilot1-discovery-r0.png`   <- the 8-row R0 discovery table (3.1)
  2. `pilot2-reflection-rounds.png` <- the 3-row R0->R2 table (3.2)
  3. `pilot3-detector-fix.png`   <- the three before/after pairs quoted in 3.4

Every number is read from `results/0902_pilots/pilots.json`, written by
`make_pilot_figs.py`. That script renders the same three pilots as hand-rolled
SVG for the results page; this one is matplotlib PNGs for GitHub-rendered
Markdown, which does not run scripts and does not show tooltips. Nothing is
hardcoded, so re-running after a fresh `make_pilot_figs.py` re-states the doc.

ORDERED BY SPREAD, not by rate, exactly as the page and the doc are: a cell
every model saturates or floors separates nothing, however interesting its
hole is, so max-minus-min is the quantity the figures are about.
"""
from __future__ import annotations

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.patheffects as pe                    # noqa: E402
import matplotlib.pyplot as plt                        # noqa: E402
import matplotlib.transforms as mtransforms            # noqa: E402
from matplotlib.lines import Line2D                    # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
DATA = HERE / "results" / "0902_pilots" / "pilots.json"
OUT = HERE.parent / "docs" / "figs"

MODELS = ["haiku", "gpt-mini", "gemini-flash"]
COLOUR = {"haiku": "#2a78d6", "gpt-mini": "#eb6834", "gemini-flash": "#1baf7a"}

SURFACE = "#fcfcfb"
INK, INK2, DIM = "#1a1a19", "#4a4a47", "#8a8a85"
GRID = "#eeeeea"

# `referee_games.py` HOLE_TYPE per cell, inlined so this script does not import
# the engine just to label eight rows.
HOLE_KIND = {
    "hx_picket_channel": "extra_message_channel",
    "ref_auction": "self_declared_budget",
    "hx_picket_checker": "broken_checker",
    "hx_quota_checker": "broken_checker",
    "gen_quiet_sonar": "broken_checker",
    "gen_sovereign_vaults": "broken_checker",
    "hx_picket_nerfed": "nerfed_opponent",
    "hx_picket_collusion": "collusion",
}

SEPARATES = 0.20        # the doc's bar for "this cell tells the models apart"
MINUS = "\u2212"

# Shape and dash carry model identity alongside hue, so a flat-at-zero line is
# still identifiable where three of them land on the same pixels.
MARKER = {"haiku": "o", "gpt-mini": "s", "gemini-flash": "^"}
DASH = {"haiku": (0, ()), "gpt-mini": (0, (5, 2)), "gemini-flash": (0, (1.2, 1.6))}


def style() -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "font.monospace": ["DejaVu Sans Mono"],
        "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "axes.edgecolor": DIM,
        "axes.labelcolor": INK2,
        "text.color": INK,
        "xtick.color": DIM,
        "ytick.color": DIM,
        "xtick.labelcolor": INK2,
        "ytick.labelcolor": INK2,
        "axes.linewidth": 0.8,
        "font.size": 11,
        "savefig.dpi": 200,
        "figure.dpi": 200,
    })


def load() -> dict:
    return json.loads(DATA.read_text())


def frame(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_axisbelow(True)


def spread(cell: dict) -> float:
    vs = [cell[m][0] for m in MODELS if cell[m][0] is not None]
    return (max(vs) - min(vs)) if len(vs) > 1 else 0.0


def save(fig, name: str) -> pathlib.Path:
    path = OUT / name
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    return path


def fig_pilot1(data: dict) -> pathlib.Path:
    """Eight cells x three models at R0, rows ordered by spread."""
    d = data["pilot1_r0"]
    cells = sorted(d, key=lambda c: -spread(d[c]))
    n_sep = sum(1 for c in cells if spread(d[c]) > SEPARATES)

    fig, ax = plt.subplots(figsize=(9.4, 6.4))
    fig.subplots_adjust(left=0.245, right=0.985, top=0.90, bottom=0.145)
    frame(ax)
    blend = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)

    bh = 0.24
    for i, cell in enumerate(cells):
        for j, m in enumerate(MODELS):
            rate, v, o, hit, tot = d[cell][m]
            rate = rate or 0.0
            y = i + (j - 1) * bh
            ax.barh(y, rate, height=bh * 0.86, color=COLOUR[m],
                    edgecolor="none", zorder=3)
            # Bars at the floor have nothing to sit beside, so their label goes
            # just inside the axis origin rather than under the y labels.
            x = max(rate, 0.0) + 0.012 if rate > 0.004 else 0.010
            ax.text(x, y, f"{rate:.3f} ({hit}/{tot})", va="center", ha="left",
                    fontsize=8.6, color=INK2 if rate > 0.004 else DIM,
                    zorder=4, path_effects=[pe.withStroke(linewidth=2.6,
                                                          foreground=SURFACE)])
        ax.text(-0.014, i - 0.13, cell, transform=blend, ha="right",
                va="center", family="monospace", fontsize=10, color=INK)
        ax.text(-0.014, i + 0.19, HOLE_KIND.get(cell, "-"), transform=blend,
                ha="right", va="center", fontsize=8.4, color=DIM)
        ax.text(1.275, i, f"{spread(d[cell]):.3f}", ha="right", va="center",
                fontsize=9.4, color=INK if spread(d[cell]) > SEPARATES else DIM,
                fontweight="bold" if spread(d[cell]) > SEPARATES else "normal")
        if i:
            ax.axhline(i - 0.5, color=GRID, lw=0.8, zorder=1)

    ax.axvline(SEPARATES, color=DIM, lw=0.9, ls=(0, (4, 3)), zorder=2)
    ax.axvline(1.13, color=GRID, lw=0.9, zorder=2)
    ax.text(SEPARATES + 0.012, -0.80, f"{SEPARATES:.2f} \u2014 only {n_sep} of "
            f"{len(cells)} cells separates the models by more than this",
            fontsize=8.6, color=DIM, va="center", ha="left")
    ax.text(1.275, -0.80, "spread", fontsize=8.8, color=DIM, va="center",
            ha="right", style="italic")

    ax.set_xlim(0, 1.30)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylim(-1.05, len(cells) - 0.4)
    ax.invert_yaxis()
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.xaxis.grid(True, color=GRID, lw=0.8)
    ax.set_xlabel("exploit rate at R0 \u00b7 labels are the rate and the "
                  "chains that found the hole", fontsize=9.6, labelpad=8)

    fig.legend(handles=[Line2D([], [], marker="s", ls="none", markersize=8,
                               color=COLOUR[m], label=m) for m in MODELS],
               loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=3,
               frameon=False, fontsize=10, handletextpad=0.5,
               columnspacing=2.4, prop={"family": "monospace", "size": 10})
    return save(fig, "pilot1-discovery-r0.png")


def fig_pilot2(data: dict) -> pathlib.Path:
    """R0 -> R2 per hole kind. One panel each, so `nerfed` cannot hide."""
    d = data["pilot2_rounds"]
    kinds = [k for k in ("channel", "collusion", "nerfed") if k in d]

    fig, axes = plt.subplots(1, len(kinds), figsize=(9.4, 3.9), sharey=True)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.90, bottom=0.235,
                        wspace=0.16)

    for ax, kind in zip(axes, kinds):
        frame(ax)
        ax.set_title(kind, family="monospace", fontsize=11.5, color=INK2,
                     pad=9)
        ax.yaxis.grid(True, color=GRID, lw=0.8)
        # Series that are exactly equal at a round are fanned apart by up to
        # one half-step of OFF so three flat-at-zero lines stay countable. The
        # displacement is 0.013 of a 0..1 axis and every value is in the doc's
        # prose, so nothing is misread off the axis.
        OFF = 0.013
        rounds = range(len(next(iter(d[kind].values()))))
        shift = {m: [0.0] * len(rounds) for m in MODELS}
        for r in rounds:
            for group in [[m for m in MODELS
                           if abs(d[kind][m][r] - v) < 1e-9]
                          for v in {round(d[kind][m][r], 12) for m in MODELS}]:
                for k, m in enumerate(group):
                    shift[m][r] = (k - (len(group) - 1) / 2) * OFF
        # Widest marker first: where two land on one point the smaller sits
        # inside the larger instead of behind it.
        last = len(list(rounds)) - 1
        for size, m in zip((9.5, 7.0, 5.0), MODELS):
            ys = [d[kind][m][r] + shift[m][r] for r in rounds]
            ax.plot(list(rounds), ys, color=COLOUR[m], lw=2.0,
                    ls=DASH[m], marker=MARKER[m], markersize=size,
                    markeredgecolor=SURFACE, markeredgewidth=0.9, zorder=3)
        # End labels stack UPWARDS from the lowest series, so a panel where
        # every model sits on zero keeps all three labels inside the axes.
        placed = 0.0
        for m in sorted(MODELS, key=lambda x: d[kind][x][last]):
            y = max(d[kind][m][last], placed)
            placed = y + 0.058
            ax.text(last + 0.14, y, f"{d[kind][m][last]:.3f}", fontsize=8.8,
                    color=COLOUR[m], va="center", ha="left", fontweight="bold")
        ax.set_xlim(-0.18, last + 0.72)
        ax.set_xticks(list(rounds))
        ax.set_xticklabels([f"R{r}" for r in rounds], fontsize=10.5)
        ax.set_ylim(-0.05, 1.06)
        ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

    axes[0].set_ylabel("exploit rate", fontsize=10)
    fig.legend(handles=[Line2D([], [], color=COLOUR[m], lw=1.9, ls=DASH[m],
                               marker=MARKER[m], markersize=7,
                               markeredgecolor=SURFACE, label=m)
                        for m in MODELS],
               loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=3,
               frameon=False, handlelength=3.0, handletextpad=0.6,
               columnspacing=2.6, prop={"family": "monospace", "size": 10})
    fig.text(0.5, 0.105, "reflection round", ha="center", fontsize=10,
             color=INK2)
    return save(fig, "pilot2-reflection-rounds.png")


def fig_pilot3(data: dict) -> pathlib.Path:
    """The same episodes, re-scored: `note_payload` before and after the fix."""
    d = data["pilot3_note_payload"]
    # Ascending, so the highest post-fix rate is the TOP row: haiku and
    # gemini-flash then bracket the figure, both starting on the same ceiling.
    rows = sorted(d, key=lambda m: d[m]["fixed"])

    fig, ax = plt.subplots(figsize=(9.4, 3.3))
    fig.subplots_adjust(left=0.165, right=0.985, top=0.90, bottom=0.29)
    frame(ax)

    for i, m in enumerate(rows):
        old, new = d[m]["old"], d[m]["fixed"]
        c = COLOUR[m]
        ax.annotate("", xy=(new, i), xytext=(old, i),
                    arrowprops=dict(arrowstyle="-|>", color=c, lw=2.0,
                                    shrinkA=7, shrinkB=9, mutation_scale=15))
        ax.plot([old], [i], marker="o", markersize=10, markerfacecolor=SURFACE,
                markeredgecolor=c, markeredgewidth=2.0, zorder=4)
        ax.plot([new], [i], marker="o", markersize=10, color=c,
                markeredgecolor=SURFACE, markeredgewidth=1.0, zorder=4)
        ax.text(old, i - 0.30, f"{old:.3f}", ha="center", va="center",
                fontsize=9.4, color=DIM)
        ax.text(new, i - 0.30,
                f"{new:.3f} ({MINUS if new < old else '+'}{abs(new-old):.3f})",
                ha="center", va="center", fontsize=9.6, color=c,
                fontweight="bold")
        ax.text(-0.018, i, m, transform=mtransforms.blended_transform_factory(
                ax.transAxes, ax.transData), ha="right", va="center",
                family="monospace", fontsize=10.5, color=INK)

    ax.axvline(1.0, color=DIM, lw=0.9, ls=(0, (2, 3)), zorder=1)
    ax.text(1.0, len(rows) - 0.42, "the buggy detector's 1.000 ceiling",
            fontsize=8.6, color=DIM, ha="right", va="center")

    ax.set_xlim(0, 1.10)
    ax.set_xticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylim(-0.62, len(rows) - 0.32)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.xaxis.grid(True, color=GRID, lw=0.8)
    ax.set_xlabel("exploit rate for the note_payload detector, the same "
                  "episodes re-scored", fontsize=9.6, labelpad=8)

    fig.legend(handles=[
        Line2D([], [], marker="o", ls="none", markersize=9,
               markerfacecolor=SURFACE, markeredgecolor=DIM,
               markeredgewidth=2.0, label="before the fix"),
        Line2D([], [], marker="o", ls="none", markersize=9, color=DIM,
               label="after the fix")],
        loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=2, frameon=False,
        fontsize=9.5, labelcolor=DIM, handletextpad=0.5, columnspacing=2.6)
    return save(fig, "pilot3-detector-fix.png")


def main() -> int:
    style()
    OUT.mkdir(parents=True, exist_ok=True)
    data = load()

    d1 = data["pilot1_r0"]
    print("spot-checks against pilots.json")
    print(f"  pilot1 hx_picket_channel/haiku      rate "
          f"{d1['hx_picket_channel']['haiku'][0]:.4f}  chains "
          f"{d1['hx_picket_channel']['haiku'][3]}/"
          f"{d1['hx_picket_channel']['haiku'][4]}  spread "
          f"{spread(d1['hx_picket_channel']):.3f}")
    print(f"  pilot1 ref_auction/gpt-mini         rate "
          f"{d1['ref_auction']['gpt-mini'][0]:.4f}  spread "
          f"{spread(d1['ref_auction']):.3f}")
    print(f"  pilot1 order by spread              "
          f"{', '.join(sorted(d1, key=lambda c: -spread(d1[c])))}")
    print(f"  pilot2 collusion/gemini-flash       "
          f"{data['pilot2_rounds']['collusion']['gemini-flash']}")
    print(f"  pilot2 nerfed/haiku                 "
          f"{data['pilot2_rounds']['nerfed']['haiku']}")
    print(f"  pilot3 gemini-flash                 "
          f"{data['pilot3_note_payload']['gemini-flash']}")

    for f in (fig_pilot1, fig_pilot2, fig_pilot3):
        p = f(data)
        print(f"wrote {p}  ({p.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
