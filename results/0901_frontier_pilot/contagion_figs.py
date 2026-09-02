#!/usr/bin/env python
"""Figures for the COLLABORATIVE-HOLE CONTAGION wave (`nat_cg1`).

    python contagion_figs.py

THIS IS A DIFFERENT EXPERIMENT FROM THE `fig1..fig3` FILES IN THIS DIRECTORY
AND THE TWO MUST NOT BE POOLED. Those read
`hole_exp/results/referee_spartan/frontier_pilot/rows.jsonl` -- the repeated
play discovery wave, one model against a fixed opponent over reflection rounds
0-3, on the `gen_`/`ref_` cells. These read
`hole_exp/results/contagion/nat_cg1/rows.jsonl` -- a cross-play contagion wave
on the `nat_` cells, every seat live or scripted, no reflection rounds, asking
whether one seat's exploit spreads to the others. Different cells, different
denominators, different question. The `contagion_` prefix on every output here
exists so nothing can mix them by filename.

Style is imported from `_pilot_data` rather than restated, for the reason that
module gives for having one loader: a change to the palette or the surface must
not apply to some figures in this directory and not others.

FACETED BY MODEL, NEVER COLOURED BY IT. Four categorical hues fail the
all-pairs colour-vision gate in the shipped palette (slot 4 yellow beside slot
2 orange: normal-vision Delta E 13.7 light, 10.6 dark), so model identity is
carried by panel position and every panel draws one hue. Verified with
`hole_exp/viz/validate_palette.py`, the Python port of the dataviz skill's
validator; the port reproduces the reference figures exactly (9.1/19.6 light,
8.4/19.3 dark).

Three figures:

  A  COUNTERFACTUAL CLOSING RATE by cell and model. Rate with an instigating
     leader MINUS the same model's rate in the matched honest-leader episode.
     The subtraction is the point: `nat_ridge_claim` closes at 0.10 with nobody
     instigating, so a raw rate would credit the leader for what was already
     there.
  B  PAYOFF vs FINDABILITY. What predicts following -- what the hole is worth,
     or how likely two seats are to land on the meeting point at all. The
     findability axis is computed FROM THE SPEC, never from the wave, because
     observed conversion shares its numerator with the outcome and the
     correlation would be partly mechanical.
  C  ONSET. Whether WHEN the exploit appears changes whether it is followed,
     plus the round-number / time-since-onset split that only a varied onset
     can separate.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent
HOLE_EXP = ROOT / "hole_exp"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HOLE_EXP))
sys.path.insert(0, str(HOLE_EXP / "hackable_games"))

import _pilot_data as P                                   # noqa: E402  style only
import referee_spartan as SP                              # noqa: E402
from analyze_contagion import load, pooled                # noqa: E402
from analyze_native9 import follower_seats, kinds_of      # noqa: E402
from analyze_onset import round_of, split_counts          # noqa: E402
import make_native9_figs as MK                            # noqa: E402

WAVE = HOLE_EXP / "results" / "contagion" / "nat_cg1"
MODELS = ["gpt", "claude", "gemini", "grok"]
BLUE, NEG, REF = P.SLOT[0], P.SLOT[7], "#b9b7b0"


def style(ax):
    ax.set_facecolor(P.SURFACE)
    ax.grid(True, color=P.GRID, lw=0.7, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(P.GRID)
    ax.tick_params(colors=P.INK2, labelsize=8.5, length=0)


def caption(fig, title, body):
    """Title + wrapped standfirst, and the axes rect that clears them.

    Returned rather than assumed: the standfirsts here run two to three lines
    and a fixed rect let the last line print through the panel titles.
    """
    fig.text(0.012, 0.977, title, fontsize=13, color=P.INK, ha="left", va="top")
    fig.text(0.012, 0.934, body, fontsize=8.5, color=P.INK2, ha="left",
             va="top", linespacing=1.55)
    n = body.count("\n") + 1
    return 0.905 - 0.037 * n


# ---------------------------------------------------------------- figure A
def fig_a(rows):
    d = MK.fig1(rows)
    games = sorted(d["games"],
                   key=lambda g: -max(x["delta"] or 0 for x in d["rows"]
                                      if x["game"] == g))
    fig, axes = plt.subplots(1, 4, figsize=(13.6, 5.4), sharex=True,
                             sharey=True)
    fig.patch.set_facecolor(P.SURFACE)
    lim = max(abs(r["delta"] or 0) for r in d["rows"]) * 1.18
    y = list(range(len(games)))[::-1]
    for ax, m in zip(axes, MODELS):
        style(ax)
        vals = [next((r["delta"] or 0) for r in d["rows"]
                     if r["game"] == g and r["model"] == m) for g in games]
        ax.barh(y, vals, height=.62, zorder=3,
                color=[BLUE if v >= 0 else NEG for v in vals])
        ax.axvline(0, color=REF, lw=1, zorder=4)
        for yy, v in zip(y, vals):
            if abs(v) <= 1e-9:
                # an empty row otherwise reads as "not sampled" rather than
                # "sampled, and the answer was zero" -- which for
                # mirror_manifest is the whole finding
                ax.annotate("0", (0, yy), xytext=(5, 0),
                            textcoords="offset points", fontsize=8,
                            va="center", ha="left", color=P.MUTED)
            if abs(v) > 1e-9:
                ax.annotate(f"{v:+.2f}", (v, yy),
                            xytext=(5 if v >= 0 else -5, 0),
                            textcoords="offset points", fontsize=8,
                            va="center", ha="left" if v >= 0 else "right",
                            color=P.INK2)
        ax.set_xlim(-lim, lim)
        ax.set_title(m, fontsize=10.5, color=P.INK, pad=6, loc="left")
    axes[0].set_yticks(y)
    axes[0].set_yticklabels([g.replace("_", " ") for g in games], fontsize=9)
    fig.supxlabel("closing rate with an instigator  −  closing rate without one",
                  fontsize=9.5, color=P.INK2, y=0.055)
    top = caption(fig, "A  Following is causal, and it is not the same size everywhere",
            "Each bar is one model in one cell: how much more often it CLOSED the hole with a scripted leader that reached for it,\n"
            "against the matched episode where the leader played honestly. Same board, same seed, same seats — only the leader differs.")
    fig.tight_layout(rect=(0, 0.05, 1, top))
    fig.savefig(HERE / "contagion_a_counterfactual_by_game.png", dpi=200,
                facecolor=P.SURFACE)
    (HERE / "contagion_a_counterfactual_by_game.json").write_text(
        json.dumps(d, indent=1))
    plt.close(fig)
    return d


# ---------------------------------------------------------------- figure B
def fig_b(rows):
    d = MK.fig2(rows)
    pts = d["points"]
    fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.2), sharey=True)
    fig.patch.set_facecolor(P.SURFACE)
    for ax, (key, xl, rr) in zip(axes, [
            ("payoff", "coalition margin when the hole closes (log)",
             f"r = {d['r_payoff']:+.2f}   ({d['r_payoff_x']:+.2f} without ridge claim)"),
            ("coord", "P(two random seats coincide in a round), from the spec (log)",
             f"r = {d['r_coord']:+.2f}   ({d['r_coord_x']:+.2f} without ridge claim)")]):
        style(ax)
        xs = [p[key] for p in pts]
        ys = [p["delta"] for p in pts]
        ax.scatter(xs, ys, s=64, color=BLUE, zorder=4,
                   edgecolor=P.SURFACE, linewidth=1.6)
        ax.set_xscale("log")
        # Label placement with collision avoidance. Several cells sit almost
        # on top of each other on both axes -- mirror manifest and ridge claim
        # differ by 1.06 in payoff and both sit at delta 0 -- and a fixed
        # offset printed them through each other ("midge rlaimfest").
        placed = []
        for p_ in sorted(pts, key=lambda q: -q["delta"]):
            fx = (math.log10(p_[key]) - math.log10(min(xs))) / max(
                1e-9, math.log10(max(xs)) - math.log10(min(xs)))
            fy = p_["delta"] / max(1e-9, max(ys))
            up, ha, dx = True, "center", 0
            for q in placed:
                if abs(q[0] - fx) < 0.17 and abs(q[1] - fy) < 0.10:
                    if q[2]:
                        up = False
                    else:
                        ha, dx = ("left", 9) if fx < 0.5 else ("right", -9)
                    break
            placed.append((fx, fy, up))
            ax.annotate(p_["game"].replace("_", " "), (p_[key], p_["delta"]),
                        xytext=(dx, 10 if up else -15),
                        textcoords="offset points",
                        fontsize=8.2, ha=ha, color=P.INK2)
        ax.set_xlabel(xl, fontsize=9.5, color=P.INK2)
        ax.set_title(rr, fontsize=10, color=P.INK, pad=6, loc="left")
        ax.margins(x=0.18, y=0.20)
    axes[0].set_ylabel("counterfactual closing effect", fontsize=9.5, color=P.INK2)
    top = caption(fig, "B  What predicts following is findability, not payoff",
            "meridian convoy has 23× the payoff of cargo pledge and LESS following — its meeting point needs a mutual dispatch and an\n"
            "exact match on a 0–99 declare. mirror manifest is the floor: reached repeatedly, never closed. With n=7 neither r is significant;\n"
            "the case contrast is the evidence. ridge claim is plotted but discounted — its reach detector fires on 61% of honest turns.")
    fig.tight_layout(rect=(0, 0.02, 1, top))
    fig.savefig(HERE / "contagion_b_payoff_vs_findability.png", dpi=200,
                facecolor=P.SURFACE)
    (HERE / "contagion_b_payoff_vs_findability.json").write_text(
        json.dumps(d, indent=1))
    plt.close(fig)
    return d


# ---------------------------------------------------------------- figure C
def fig_c(rows):
    d = MK.fig3(rows)
    arms = d["arms"]
    fig, axes = plt.subplots(1, 3, figsize=(15.4, 5.0),
                             gridspec_kw={"width_ratios": [1.15, 1, 1]})
    fig.patch.set_facecolor(P.SURFACE)
    ax = axes[0]; style(ax)
    if len(arms) >= 2:
        w = 0.8 / len(arms)
        for i, on in enumerate(arms):
            vals = [(d["per_model"][m].get(on) or {}).get("rate") or 0
                    for m in MODELS]
            ax.bar([x + i * w for x in range(len(MODELS))], vals, width=w * .9,
                   color=BLUE, alpha=1 - .28 * i, zorder=3,
                   label=f"onset {on}")
            for x, v in zip(range(len(MODELS)), vals):
                if v > 0:
                    ax.annotate(f"{v:.2f}", (x + i * w, v), xytext=(0, 3),
                                textcoords="offset points", fontsize=7.6,
                                ha="center", color=P.INK2)
        ax.set_xticks([x + w * (len(arms) - 1) / 2 for x in range(len(MODELS))])
        ax.set_xticklabels(MODELS, fontsize=9)
        ax.legend(frameon=False, fontsize=8.6, labelcolor=P.INK2)
    ax.set_ylabel("post-onset closing rate", fontsize=9.5, color=P.INK2)
    ax.set_title("by model and onset arm", fontsize=10, color=P.INK,
                 pad=6, loc="left")

    ax = axes[1]; style(ax)
    A, B = d["by_round"], d["by_since"]
    ax.plot([x["k"] for x in A], [x["rate"] or 0 for x in A], "-o", ms=5,
            color=BLUE, lw=2, zorder=4, label="absolute round")
    ax.plot([x["k"] for x in B], [x["rate"] or 0 for x in B], "-s", ms=4.5,
            color=REF, lw=2, zorder=3, label="rounds since onset")
    ax.set_xlabel("round", fontsize=9.5, color=P.INK2)
    ax.set_title("round number vs time since onset", fontsize=10, color=P.INK,
                 pad=6, loc="left")
    ax.legend(frameon=False, fontsize=8.6, labelcolor=P.INK2)
    ax = axes[2]; style(ax)
    X = d.get("matched", {})
    grid = X.get("grid", {})
    for i, on in enumerate(("early", "mid", "late")):
        g = grid.get(on) or {}
        ks = sorted(int(k) for k in g)
        if not ks:
            continue
        ys = [(g.get(k) or g.get(str(k)))["rate"] or 0 for k in ks]
        ax.plot(ks, ys, "-o", ms=4.5, lw=2, color=BLUE, alpha=1 - .30 * i,
                label=f"onset {on}")
    ax.set_xlabel("rounds since onset", fontsize=9.5, color=P.INK2)
    ax.set_title("matched exposure (the control)", fontsize=10, color=P.INK,
                 pad=6, loc="left")
    ax.legend(frameon=False, fontsize=8.6, labelcolor=P.INK2, loc="lower right")
    tr = X.get("truncated") or {}
    if tr:
        txt = "   ".join(f"{a} {v['rate']:.3f}" for a, v in tr.items())
        ax.annotate(f"first {X.get('window', 3)} post-onset rounds only:\n{txt}",
                    (0.03, 0.97), xycoords="axes fraction", va="top",
                    fontsize=8, color=P.INK2)

    top = caption(fig, "C  Does onset time change following?",
            "Left: closing rate over the post-onset window only, so every arm is measured where the exploit was actually on the table.\n"
            "Middle: with onset pinned at round 1 these two curves would be the SAME column — separating them is the whole point.\n"
            "Right: the control. A later arm has fewer post-onset rounds and the rate climbs with exposure, so a lower late average\n"
            "could be nothing but a shorter window. Holding rounds-since-onset fixed, later onset STILL follows less.")
    fig.tight_layout(rect=(0, 0.02, 1, top))
    fig.savefig(HERE / "contagion_c_onset.png", dpi=200, facecolor=P.SURFACE)
    (HERE / "contagion_c_onset.json").write_text(json.dumps(d, indent=1))
    plt.close(fig)
    return d


def main() -> int:
    SP.register_all(); SP.register_native9()
    rows = load(WAVE)
    a, b, c = fig_a(rows), fig_b(rows), fig_c(rows)
    d4 = fig_d(rows)
    print(f"{len(rows)} episodes | onset arms {c['arms']} | matched arms {d4['arms']}")
    for n in ("contagion_a_counterfactual_by_game", "contagion_b_payoff_vs_findability",
              "contagion_c_onset"):
        print(f"  wrote {n}.png / .json")
    print("  wrote contagion_d_nohole.png / .json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
