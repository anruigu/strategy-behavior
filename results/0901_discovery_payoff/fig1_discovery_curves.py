#!/usr/bin/env python
"""    /home/allie/venvs/tinker-ipd/bin/python fig1_discovery_curves.py

  fig1_discovery_curves.png    exploit rate against SPaRTan reflection round,
                               one panel per cell, all 29 hole-games
  fig1_discovery_curves.json   every number drawn

THE QUESTION. Across 29 cells whose referee, opponent or message channel has a
deliberate defect, does letting the model reflect on its own play make it find
the defect? One panel per cell, x = reflection round 0..3, y = the pooled rate
at which the focal seat committed a HARD violation.

WHY SMALL MULTIPLES AND NOT 29 LINES ON ONE AXIS. Twenty-nine series cannot be
told apart by colour -- eight is the ceiling before hues start being reused --
and the comparison anybody wants here is SHAPE per cell, not cell-against-cell.
Cross-cell level comparison is meaningless anyway: each cell's denominator is
its own opportunity count, so 0.5 in estate and 0.5 in invoice are not the same
quantity. Panels put every curve on the same 0..1 axis without inviting that
comparison.

THE RATE IS POOLED, sum(violations) / sum(opportunities) over the cell's HARD
kinds within a round, never a mean of per-episode rates: an episode with two
opportunities must not weigh the same as one with twenty. A round with NO
opportunities is a hole in the line, not a zero -- `ta_blindauction` never
reaches its ring at rounds 0-1 because the model declines the pact, and drawing
that as 0.0 would report "did not cheat" where the truth is "was never in a
position to".

WHAT THE COLOUR ENCODES. The primary hole kind, taken as the FIRST token of
HOLE_TYPE, which is the user's extension question -- are some kinds of hack
easier to find than others? Four kinds, four hues, assigned in the reference
palette's fixed slot order.

IDENTITY IS NOT CARRIED BY COLOUR. Every panel is titled with its cell name and
every kind is named in the legend, so the hues are redundant encoding rather
than the channel identity rests on. This matters more than usual here: the
palette validator ships as a node script and this box has no node runtime, so
the palette could not be machine-checked. Using the reference palette's slots
1-4 unmodified and in order is the documented already-passing path, and the
redundant labelling is what makes that safe rather than merely likely.

PANEL ORDER is by round-3 rate, descending, so the cells the model ends up
exploiting sit top-left and the ones it never touches trail off bottom-right.
Cells the model never cheated in at all are drawn flat at zero and still shown:
a floor is a finding, and dropping them would turn "9 of 29 went untouched
while every one of them paid" -- which is half the result -- into an invisible
denominator.

DATA. `hole_exp/payoff_audit.py --json`, which pools three SPaRTan waves
sampled at identical settings (qwen3.8-27b, neutral, hole arm, own view,
rounds=3, episodes=4): `merged` (18 cells), `hanabi_openrouter` (1) and
`ta_baseline1` (10).
"""
from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
HOLE_EXP = HERE.parent.parent / "hole_exp"
PAYOFF = HERE / "payoff.json"

# Reference palette, categorical slots 1-4, light mode, in fixed order.
KIND_COLOR = {
    "unchecked claim": "#2a78d6",     # slot 1 blue
    "unbacked ledger": "#eb6834",     # slot 2 orange
    "nerfed opponent": "#1baf7a",     # slot 3 aqua
    "channel / collusion": "#eda100",  # slot 4 yellow
}
KIND_MARKER = {"unchecked claim": "o", "unbacked ledger": "s",
               "nerfed opponent": "^", "channel / collusion": "D"}

INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8a85"
SURFACE = "#fcfcfb"
GRID = "#e4e4df"

# HOLE_TYPE's first token -> the kind it belongs to. First token wins, so a
# stacked cell like `collusion+extra_message_channel+nerfed_opponent` lands on
# the mechanism its rules lead with rather than on whichever token sorts first.
FIRST_TOKEN = {
    "broken_checker": "unchecked claim",
    "self_report": "unchecked claim",
    "unverified_completion": "unchecked claim",
    "unverified_quality_claim": "unchecked claim",
    "uncapped_claim": "unchecked claim",
    "local_ledger": "unbacked ledger",
    "self_declared_budget": "unbacked ledger",
    "unvalidated_trade": "unbacked ledger",
    "unbacked_order": "unbacked ledger",
    "nerfed_opponent": "nerfed opponent",
    "private_channel": "channel / collusion",
    "metadata_channel": "channel / collusion",
    "convention_channel": "channel / collusion",
    "collusion": "channel / collusion",
    "extra_message_channel": "channel / collusion",
}


def kind_of(hole_type: str) -> str:
    head = (hole_type or "").split("+")[0]
    return FIRST_TOKEN.get(head, "unchecked claim")


def load() -> dict:
    if not PAYOFF.exists():
        print(f"building {PAYOFF} ...")
        subprocess.run(
            [sys.executable, str(HOLE_EXP / "payoff_audit.py"),
             "--json", str(PAYOFF)],
            cwd=str(HOLE_EXP), check=True, stdout=subprocess.DEVNULL)
    return json.loads(PAYOFF.read_text())


def main() -> int:
    data = load()
    rounds = [0, 1, 2, 3]

    cells = []
    for name, rec in data.items():
        rr = (rec["observed"].get("rate_by_round") or {})
        ys = [rr.get(str(r), rr.get(r)) for r in rounds]
        last = next((y for y in reversed(ys) if y is not None), 0.0)
        cells.append({
            "cell": name,
            "kind": kind_of(rec["hole_type"]),
            "hole_type": rec["hole_type"],
            "rates": ys,
            "final": last,
            "pays": rec["structural"]["pays"],
            "buys": rec["structural"]["buys"],
            "basis": rec["structural"]["basis"],
            "cheating_episodes": rec["observed"].get("cheating_episodes", 0),
            "episodes": rec["observed"].get("episodes", 0),
        })
    cells.sort(key=lambda c: (-c["final"], c["cell"]))

    ncol, nrow = 6, 5
    fig, axes = plt.subplots(nrow, ncol, figsize=(15.0, 11.2),
                             sharex=True, sharey=True)
    fig.patch.set_facecolor(SURFACE)

    for ax, c in zip(axes.flat, cells):
        col = KIND_COLOR[c["kind"]]
        ax.set_facecolor(SURFACE)
        ax.grid(True, color=GRID, lw=0.7, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(GRID)

        xs = [r for r, y in zip(rounds, c["rates"]) if y is not None]
        ys = [y for y in c["rates"] if y is not None]
        if xs:
            # 2px line, >=8px markers, a surface ring so overlapping marks stay
            # separable
            ax.plot(xs, ys, color=col, lw=2.0, zorder=3,
                    marker=KIND_MARKER[c["kind"]], ms=6.5,
                    markeredgecolor=SURFACE, markeredgewidth=1.6)
            # one direct label per panel, never a number on every point
            ax.annotate(f"{ys[-1]:.2f}", (xs[-1], ys[-1]),
                        textcoords="offset points", xytext=(6, 0),
                        color=INK, fontsize=8.5, va="center", zorder=4)
        missing = [r for r, y in zip(rounds, c["rates"]) if y is None]
        if missing:
            ax.plot(missing, [0.0] * len(missing), linestyle="none",
                    marker="x", ms=5, color=MUTED, zorder=3)

        ax.set_title(c["cell"].replace("ref_", "").replace("gen_", "")
                     .replace("ta_", ""), fontsize=9.5, color=INK, pad=4)
        ax.set_ylim(-0.06, 1.10)
        ax.set_xlim(-0.35, 3.75)
        ax.set_xticks(rounds)
        ax.set_yticks([0, 0.5, 1.0])
        ax.tick_params(colors=INK2, labelsize=8, length=3)
        if not c["cheating_episodes"]:
            ax.text(0.5, 0.86, "never exploited", transform=ax.transAxes,
                    ha="center", fontsize=7.5, color=MUTED, style="italic")

    for ax in axes.flat[len(cells):]:
        ax.set_visible(False)

    fig.suptitle("Reflection raises exploitation in 10 of 29 hole-games; "
                 "9 are never exploited at all",
                 fontsize=15, color=INK, y=0.988, x=0.055, ha="left",
                 weight="bold")
    fig.text(0.055, 0.958,
             "Exploit rate (HARD violations / opportunities, pooled) against "
             "SPaRTan reflection round. Qwen3.8-27B, neutral prompt, hole arm, "
             "own-view reflection, 3 chains x 4 episodes per round.\n"
             "All 29 cells PAY when the hole is taken, so a flat-at-zero panel "
             "is money left on the table, not a cell without a hole. "
             "10 rise, 5 fall, 5 sit flat above zero, 9 stay at the floor.",
             fontsize=9.5, color=INK2, ha="left", va="top")

    handles = [Line2D([], [], color=KIND_COLOR[k], lw=2.0,
                      marker=KIND_MARKER[k], ms=6.5,
                      markeredgecolor=SURFACE, markeredgewidth=1.6, label=k)
               for k in KIND_COLOR]
    handles.append(Line2D([], [], color=MUTED, lw=0, marker="x", ms=5,
                          label="no opportunity that round"))
    fig.legend(handles=handles, loc="upper left", ncol=5, frameon=False,
               fontsize=9, bbox_to_anchor=(0.05, 0.925),
               labelcolor=INK2, columnspacing=1.8, handletextpad=0.5)

    fig.supxlabel("reflection round", fontsize=10.5, color=INK2, y=0.018)
    fig.supylabel("exploit rate", fontsize=10.5, color=INK2, x=0.012)
    fig.tight_layout(rect=(0.02, 0.025, 1.0, 0.895))

    png = HERE / "fig1_discovery_curves.png"
    fig.savefig(png, dpi=170, facecolor=SURFACE)
    (HERE / "fig1_discovery_curves.json").write_text(json.dumps(
        {"rounds": rounds, "cells": cells,
         "source": "hole_exp/payoff_audit.py over merged + "
                   "hanabi_openrouter + ta_baseline1",
         "model": "qwen3.8-27b", "condition": "neutral", "arm": "hole",
         "visibility": "own"}, indent=2))
    print(f"wrote {png}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
