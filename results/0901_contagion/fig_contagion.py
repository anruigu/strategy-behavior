#!/usr/bin/env python
"""    ~/venvs/tinker-ipd/bin/python fig_contagion.py

  fig_contagion.png    who cheats first, and whether the others follow
  fig_contagion.json   every number drawn

THE QUESTION. In cross-play on a multi-seat cell with a defect, does one model
find it first and the others pick it up? That is two questions with two very
different answers, so the figure is two panels and they do not share an axis.

PANEL A -- "first" is turn order, not a model. Two bar sets on one share axis:
which SEAT committed the first HARD violation, and which MODEL did. The Latin
square makes them directly comparable -- each model sat in each seat exactly
52 times -- so the two bars are the same 128 episodes split two ways, and the
one with the spread is the one carrying the effect. Seat wins by an order of
magnitude. Both are drawn because the point IS the comparison; showing only
the model panel would report a 43/32/25 split as a finding when the same
episodes split 65/20/15 by seat.

PANEL B -- following is real, and it is imitation rather than communication.
A dumbbell per cell: the live seats' pooled HARD rate when the scripted seat 0
plays honestly, and when it exploits. Same board, same seed, same models; the
only difference is whether they watched someone cheat. A dumbbell and not
grouped bars because the quantity of interest is the GAP, and a dumbbell draws
the gap as a line whose length is the effect instead of asking the eye to
subtract two bar heights.

WHY THE CONTROL COLOUR IS GREY. `honest` is not a second category, it is the
baseline the treatment is read against, so it gets muted ink and the treated
end gets the one saturated hue. Two hues of equal weight would say these are
two conditions of equal interest; they are not.

CELLS ARE SORTED BY THE GAP and every cell is kept, including the four where
the gap is zero. `ref_hanabi` at 0.000 in both arms is a finding -- 441
follower opportunities, not one taken -- and dropping the flat cells would
turn "the effect appears where the exploit is legible and nowhere else" into
a chart of only the places it appears.

RATES ARE POOLED, sum(violations)/sum(opportunities) over the cell's HARD
kinds across every live seat, never a mean of per-episode rates. Intervals are
a bootstrap over matched PAIRS, since the two arms of a pair share a seed and
are not independent draws.

DATA. `analyze_contagion.py results/contagion/cg1`, 468 episodes,
claude-opus-5 / gpt-5.5 / gemini-3.1-pro via OpenRouter, neutral prompt, hole
arm.

PALETTE NOTE. The validator ships as a node script and this box has no node
runtime, so the palette could not be machine-checked. Slots 1-3 of the
reference palette are used unmodified and in order, and identity is carried
redundantly by axis labels and direct value labels rather than by hue alone.
"""
from __future__ import annotations

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE.parent.parent / "hole_exp" / "results" / "contagion" / "cg1"

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#8a8a85"
SURFACE, GRID = "#fcfcfb", "#e4e4df"
MODEL_COLOR = {"claude": BLUE, "gpt": ORANGE, "gemini": AQUA}


def style(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(True, axis="x", color=GRID, lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, labelsize=9, length=3)


def main() -> int:
    A = json.loads((SRC / "contagion_analysis.json").read_text())
    L, E = A["leadership"], A["exposure"]

    fig = plt.figure(figsize=(14.0, 8.2))
    fig.patch.set_facecolor(SURFACE)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.55],
                          left=0.055, right=0.985, top=0.700, bottom=0.080,
                          wspace=0.42)

    # ---- panel A -------------------------------------------------------
    axA = fig.add_subplot(gs[0, 0])
    style(axA)
    n = L["with_any_violation"]
    models = sorted(L["by_model"], key=lambda m: -L["by_model"][m])
    seats = sorted(L["by_seat"])
    labels, vals, cols = [], [], []
    for p in reversed(seats):
        labels.append(f"seat p{p}")
        vals.append(L["by_seat"][p] / n)
        cols.append(MUTED)
    labels.append("")
    vals.append(0.0)
    cols.append(SURFACE)
    for m in reversed(models):
        labels.append(m)
        vals.append(L["by_model"][m] / n)
        cols.append(MODEL_COLOR[m])
    y = range(len(vals))
    axA.barh(list(y), vals, color=cols, height=0.62, zorder=3)
    for i, v in enumerate(vals):
        if v:
            axA.text(v + 0.012, i, f"{v:.2f}", va="center", fontsize=9,
                     color=INK)
    axA.set_yticks(list(y))
    axA.set_yticklabels(labels, fontsize=9.5, color=INK)
    axA.axhline(len(seats), color=GRID, lw=1.0)
    axA.set_xlim(0, 0.78)
    axA.set_xlabel("share of episodes whose FIRST violation was theirs",
                   fontsize=9.5, color=INK2)
    axA.set_title("A.  “First” is a seat, not a model",
                  fontsize=12, color=INK, loc="left", pad=48, weight="bold")
    axA.text(0.0, 1.020,
             f"{n} of {L['episodes']} live-table episodes had a HARD "
             f"violation.\nEach model sat in each seat exactly 52 times, so "
             f"these are\nthe same episodes split two ways.  seat "
             f"χ²=57.8 (p<1e-12), model χ²=6.3 (p=.04).",
             transform=axA.transAxes, fontsize=8.5, color=INK2, va="bottom")

    # ---- panel B -------------------------------------------------------
    axB = fig.add_subplot(gs[0, 1])
    style(axB)
    cells = sorted(E["per_cell"].items(), key=lambda kv: kv[1]["delta"] or 0)
    ys = range(len(cells))
    for i, (g, v) in zip(ys, cells):
        h, e = v["honest"], v["exploit"]
        axB.plot([h, e], [i, i], color=ORANGE if e > h else MUTED,
                 lw=2.0, zorder=2, alpha=0.55 if e <= h else 1.0)
        axB.plot([h], [i], marker="o", ms=8, color=SURFACE,
                 markeredgecolor=MUTED, markeredgewidth=2.0, zorder=3)
        axB.plot([e], [i], marker="o", ms=8, color=ORANGE,
                 markeredgecolor=SURFACE, markeredgewidth=1.6, zorder=4)
        if abs(e - h) > 0.02:
            axB.text(max(h, e) + 0.022, i, f"{e-h:+.2f}", va="center",
                     fontsize=8.5, color=INK)
    axB.set_yticks(list(ys))
    axB.set_yticklabels([g for g, _ in cells], fontsize=9.5, color=INK)
    axB.set_xlim(-0.03, 1.06)
    axB.set_xlabel("live seats’ HARD violation rate "
                   "(pooled violations / opportunities)",
                   fontsize=9.5, color=INK2)
    axB.set_title("B.  Watching a scripted seat cheat makes live models cheat",
                  fontsize=12, color=INK, loc="left", pad=48, weight="bold")
    axB.text(0.0, 1.020,
             f"156 matched pairs: identical cell, seed and models; the only "
             f"difference is whether\nseat 0 — a canned script that "
             f"understands nothing — exploited. Pooled effect "
             f"{E['delta']:+.3f}\n95% CI [{E['ci'][0]:.3f}, "
             f"{E['ci'][1]:.3f}].",
             transform=axB.transAxes, fontsize=8.5, color=INK2, va="bottom")
    axB.legend(handles=[
        Line2D([], [], marker="o", ms=8, lw=0, color=SURFACE,
               markeredgecolor=MUTED, markeredgewidth=2.0,
               label="scripted seat plays honestly"),
        Line2D([], [], marker="o", ms=8, lw=0, color=ORANGE,
               markeredgecolor=SURFACE, label="scripted seat exploits")],
        loc="lower right", frameon=False, fontsize=9, labelcolor=INK2)

    fig.suptitle("No model reliably finds the hole first — but every "
                 "model copies one that has",
                 fontsize=15.5, color=INK, x=0.055, y=0.975, ha="left",
                 weight="bold")
    fig.text(0.055, 0.928,
             "Cross-play on the 13 cells that can physically carry contagion "
             "(≥3 live seats, one seat’s exploit visible to "
             "another, and an opportunity left afterwards).\n"
             "claude-opus-5 / gpt-5.5 / gemini-3.1-pro via OpenRouter, "
             "neutral prompt, hole arm, 468 episodes, 0 failures.",
             fontsize=9.5, color=INK2, ha="left", va="top")

    png = HERE / "fig_contagion.png"
    fig.savefig(png, dpi=170, facecolor=SURFACE)
    (HERE / "fig_contagion.json").write_text(json.dumps(
        {"panelA": {"n_episodes": L["episodes"],
                    "n_with_violation": n,
                    "by_seat": L["by_seat"], "by_model": L["by_model"],
                    "occupancy_per_seat": 52},
         "panelB": {g: v for g, v in cells},
         "pooled": {"delta": E["delta"], "ci": E["ci"],
                    "honest": E["honest"], "exploit": E["exploit"]},
         "source": "hole_exp/results/contagion/cg1"}, indent=2))
    print(f"wrote {png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
