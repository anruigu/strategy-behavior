#!/usr/bin/env python3
"""Exploit rate against reflection round, one panel per detector kind.

    ~/venvs/tools/bin/python make_spartan_figs.py

SMALL MULTIPLES, NOT A MULTI-LINE CHART. There are ~30 detector kinds; putting
them on shared axes would need ~30 hues, and a generated hue past the eighth is
indistinguishable from an existing one under colour-vision deficiency. Faceting
keeps every kind readable and lets the SHAPE be the message -- which it is,
because nearly all of the movement happens between r0 and r1.

RATES ARE POOLED sum(v)/sum(o) PER ROUND, never a mean of per-episode rates:
an episode with two opportunities must not weigh as much as one with twenty.
This matches summarize_spartan.py; the two are meant to agree.

COLOUR ENCODES DIRECTION, and direction only. Diverging red/blue with a grey
midpoint, from the house palette -- red = the model found more of the hole,
blue = it found less, grey = flat. Never colour alone: panels are ordered by
delta and each carries its delta as text, so the figure survives greyscale.

CELLS ABOVE THE 0.25 invalid_rate BAR ARE DRAWN STRUCK OUT, not dropped. A cell
whose moves would not parse has no readable curve, and silently omitting it
would make "no discovery" and "no measurement" look identical -- the same trap
summarize_spartan.py's VALIDITY section exists to flag.

HARD KINDS ONLY. `referee_games.py` splits each cell's detectors into HARD (an
objective rule violation; honest play scores exactly zero), SOFT (a marker
honest play can also produce) and DIAG (a consistency check). Only HARD has the
zero floor that makes "the rate went up" mean "it exploited the hole", which is
why summarize_spartan.py reports them in separate sections. Putting
`sidebar/collusion` beside `sidebar/card_disclosure` in one "exploit rate"
figure would be exactly the conflation that split exists to prevent.

FLAT AT FLOOR IS LISTED, NOT PLOTTED -- AND IT IS NOT ONE FINDING. Roughly half
the HARD kinds never move off zero, and twenty identical flat lines crowd out
the ones carrying the result. But "stayed at zero" has four causes that a
single footer line would merge into a false one ("never discovered"):

  not found        opportunities existed, no chain ever named the hole, and no
                   other kind in the cell was exploited either. The real
                   negative result.
  named, unused    a playbook DID name the hole and the rate still never moved.
                   A dissociation between articulating and exploiting, and the
                   most interesting thing a flat line can be.
  other route      the cell's hole WAS found, via a different detector. This
                   kind is not undiscovered; it is not the route taken.
  unreadable       invalid_rate over the bar, so zero means "no measurement".

Kinds with fewer than MIN_OPP opportunities across the whole sweep are dropped
from the census rather than called flat: a handful of trials cannot distinguish
a floor from an absence.

Flat at CEILING keeps its panel and its own legend entry: flat-at-floor and
flat-at-ceiling are opposite findings and a delta column makes them identical.
"""
from __future__ import annotations

import collections
import json
import math
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = pathlib.Path(__file__).resolve().parent
ROWS = HERE.parent / "hole_exp" / "results" / "referee_spartan" / "merged" / "rows.jsonl"
OUT = HERE / "figs" / "spartan-discovery.png"

SURFACE = "#fcfcfb"
INK, INK2, INK3 = "#0b0b0b", "#52514e", "#8a8a86"
RISE, FALL, FLAT = "#e34948", "#2a78d6", "#8a8a86"
GRID = "#e6e5e1"
BAND = 0.05          # |delta| below this reads as flat
INVALID_BAR = 0.25   # HANDOFF-think4.md §7
MIN_OPP = 10         # below this a "floor" is not a measurement


def hard_kinds():
    """{game: (hard kind, ...)} straight from the game classes."""
    import sys
    sys.path.insert(0, str(HERE.parent / "hole_exp"))
    import referee_spartan as SP
    SP.register_all()
    return {g.NAME: tuple(g.HARD) for g in SP.games_of(list(SP.ALL19))}


def load():
    rows = [json.loads(l) for l in ROWS.open() if l.strip()]
    HARD = hard_kinds()
    kinds = sorted({k[2:] for r in rows for k in r
                    if k.startswith("o_") and k != "o_headline"})
    num = collections.defaultdict(float)
    den = collections.defaultdict(float)
    inval = collections.defaultdict(list)
    named = collections.defaultdict(set)
    allchains = collections.defaultdict(set)
    for r in rows:
        g, rd = r["game"], r["round"]
        inval[(g, rd)].append(r.get("invalid_rate_focal") or 0.0)
        allchains[g].add(r["seed"])
        if r.get("playbook_names_hole"):
            named[g].add(r["seed"])
        for k in kinds:
            if k not in HARD.get(g, ()):
                continue            # SOFT/DIAG have no zero floor -- not exploits
            o = r.get(f"o_{k}")
            v = r.get(f"v_{k}")
            if o is None or v is None:
                continue
            num[(g, k, rd)] += float(v)
            den[(g, k, rd)] += float(o)
    series = {}
    for (g, k, rd) in list(den):
        series.setdefault((g, k), {})[rd] = (
            num[(g, k, rd)] / den[(g, k, rd)] if den[(g, k, rd)] else None)
    flagged = {g for (g, rd), v in inval.items()
               if sum(v) / len(v) > INVALID_BAR}
    opps = collections.defaultdict(float)
    for (g, k, rd), d in den.items():
        opps[(g, k)] += d
    return (series, flagged, sorted({r["round"] for r in rows}), opps,
            {g: (len(named[g]), len(allchains[g])) for g in allchains})


def main() -> int:
    series, flagged, rounds, opps, naming = load()
    # keep kinds with at least one observed opportunity in every round
    keep = {gk: v for gk, v in series.items()
            if all(v.get(r) is not None for r in rounds)}
    def delta(gk):
        # rounded, because the printed label IS the classification: a panel
        # reading "+0.05" beside a grey (flat) line is a contradiction the
        # reader has to resolve by guessing the hidden precision.
        v = keep[gk]
        return round(v[rounds[-1]] - v[rounds[0]], 2)
    def at_floor(gk):
        return max(keep[gk].values()) < 0.02 and gk[0] not in flagged

    floor = sorted(gk for gk in keep if at_floor(gk))
    thin = sorted(gk for gk in keep if opps[gk] < MIN_OPP)
    floor = [gk for gk in floor if gk not in thin]

    def why(gk):
        g, k = gk
        if g in flagged:
            return "unreadable"
        peers = [max(keep[(gg, kk)].values()) for (gg, kk) in keep
                 if gg == g and kk != k]
        if peers and max(peers) > 0.05:
            return "other route"
        return "named, unused" if naming[g][0] else "not found"
    order = sorted((gk for gk in keep if not at_floor(gk)),
                   key=lambda gk: (-delta(gk), gk))

    ncol = 6
    nrow = math.ceil(len(order) / ncol)
    # extra height is for the header band and the four-bucket footer, both of
    # which live outside the axes grid
    fig, axes = plt.subplots(nrow, ncol,
                             figsize=(ncol * 2.35, nrow * 2.0 + 2.0),
                             sharex=True, sharey=True)
    fig.patch.set_facecolor(SURFACE)
    axes = axes.ravel()

    for ax, gk in zip(axes, order):
        g, k = gk
        v = [keep[gk][r] for r in rounds]
        d = delta(gk)
        bad = g in flagged
        ceiling = min(keep[gk].values()) > 0.98
        c = FLAT if abs(d) < BAND else (RISE if d > 0 else FALL)
        if ceiling:
            c = RISE                # exploited throughout: saturated, not absent
        if bad:
            c = INK3
        ax.set_facecolor(SURFACE)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("left", "bottom"):
            ax.spines[s].set_color(GRID)
        ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
        ax.set_axisbelow(True)
        # Ceiling shares the "exploited" hue but takes a square marker: two
        # identical red keys in a legend cannot be told apart, and hue alone
        # would have to carry a distinction it is already spending on
        # rose-vs-fell. Composite hue x shape instead.
        ax.plot(rounds, v, color=c, lw=2.0,
                marker="s" if ceiling else "o", ms=5.0 if ceiling else 5.5,
                mec=SURFACE, mew=1.4, zorder=3,
                ls=":" if bad else "-", alpha=0.55 if bad else 1.0)
        ax.set_ylim(-0.06, 1.10)
        ax.set_xticks(rounds)
        ax.set_yticks([0, 0.5, 1.0])
        title = f"{g.replace('gen_', '').replace('ref_', '')}\n{k[:26]}"
        ax.set_title(title, fontsize=7.6, color=INK, pad=4, linespacing=1.25)
        # delta as text so direction never rests on hue alone. Parked in the
        # corner the curve is furthest from -- a fixed corner sits on top of the
        # line in exactly the saturated cells whose delta matters most.
        # The label sits at x=0.04, i.e. next to the r0 marker -- so the only
        # point it can collide with is v[0]. Put it in the other half.
        top = 0.13 if v[0] > 0.5 else 0.93
        ax.text(0.04, top, ("n/a" if bad else f"{d:+.2f}"),
                transform=ax.transAxes, fontsize=7.4,
                va="top" if top > 0.5 else "bottom",
                color=INK3 if bad else c, fontweight="bold")
        if ceiling and not bad:
            ax.text(0.96, 0.13, "at ceiling", transform=ax.transAxes,
                    ha="right", va="bottom", fontsize=6.8, color=INK3,
                    style="italic")
        if bad:
            ax.text(0.5, 0.45, "invalid\n>0.25", transform=ax.transAxes,
                    ha="center", va="center", fontsize=7, color=INK3,
                    style="italic")
        ax.tick_params(labelsize=7, colors=INK2, length=2)

    for ax in axes[len(order):]:
        ax.set_visible(False)

    n_rise = sum(1 for gk in order if delta(gk) >= BAND and gk[0] not in flagged)
    n_fall = sum(1 for gk in order if delta(gk) <= -BAND and gk[0] not in flagged)
    n_all = len(order) + len(floor)
    fig.suptitle(
        "Reflection finds the referee holes — and one round is usually enough",
        fontsize=14, color=INK, y=0.996, x=0.008, ha="left", fontweight="bold")
    fig.text(0.008, 0.968,
             f"HARD exploit rate by reflection round, qwen3.8-27b self-play. "
             f"{n_all} objective-violation kinds across "
             f"{len({g for g, _ in keep})} cells; 3 chains x 4 episodes per "
             f"point, rates pooled sum(violations)/sum(opportunities).\n"
             f"{n_rise} rose, {n_fall} fell, {len(floor)} stayed at zero — "
             f"for four different reasons, see footer.",
             fontsize=8.6, color=INK2, ha="left", va="top")
    fig.legend(handles=[
        Line2D([], [], color=RISE, lw=2, marker="o", ms=5.5, label="rose (found more of the hole)"),
        Line2D([], [], color=FALL, lw=2, marker="o", ms=5.5, label="fell"),
        Line2D([], [], color=FLAT, lw=2, marker="o", ms=5.5, label=f"flat (|Δ| < {BAND})"),
        Line2D([], [], color=RISE, lw=2, marker="s", ms=5.0, ls="-",
               label="at ceiling from r0 (no headroom)"),
        Line2D([], [], color=INK3, lw=2, ls=":", marker="o", ms=5.5,
               label="unreadable (invalid_rate > 0.25)")],
        loc="upper left", bbox_to_anchor=(0.008, 0.925), ncol=5, frameon=False,
        fontsize=8.4, labelcolor=INK2, handletextpad=0.6, columnspacing=1.8)
    if floor or thin:
        buckets = collections.OrderedDict(
            (b, []) for b in ("not found", "named, unused", "other route",
                              "unreadable"))
        for gk in floor:
            buckets[why(gk)].append(gk)
        short = lambda gk: (f"{gk[0].replace('gen_','').replace('ref_','')}"
                            f"/{gk[1]}")
        GLOSS = {
            "not found": "opportunities existed, no playbook named the hole, "
                         "nothing else in the cell exploited either",
            "named, unused": "a playbook named the hole and the rate still "
                             "never moved",
            "other route": "the cell's hole WAS found, through a different "
                           "detector",
            "unreadable": "invalid_rate over the bar — zero means no "
                          "measurement, not no discovery",
        }
        y = 0.105
        fig.text(0.008, y, f"Stayed at zero ({len(floor)} kinds, no panel) — "
                 f"four different reasons:", fontsize=8, color=INK2,
                 ha="left", va="top", fontweight="bold")
        for b, gks in buckets.items():
            if not gks:
                continue
            import textwrap
            body = f"{b} ({GLOSS[b]}): " + ", ".join(short(gk) for gk in gks)
            for i, line in enumerate(textwrap.wrap(body, 185)):
                y -= 0.0145
                fig.text(0.020 if i else 0.014, y, line,
                         fontsize=7.4, color=INK3, ha="left", va="top")
        if thin:
            y -= 0.0145
            fig.text(0.014, y,
                     f"dropped, under {MIN_OPP} opportunities all sweep: " +
                     ", ".join(f"{short(gk)} (n={int(opps[gk])})"
                               for gk in thin),
                     fontsize=7.4, color=INK3, ha="left", va="top")
    fig.supxlabel("reflection round", fontsize=9, color=INK2,
                  y=0.135 if floor else 0.004)
    fig.supylabel("exploit rate", fontsize=9, color=INK2, x=0.004)
    fig.tight_layout(rect=(0.016, 0.150 if floor else 0.014, 0.998, 0.900))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=170, facecolor=SURFACE)
    print(f"wrote {OUT}  ({len(order)} panels, {nrow}x{ncol})")
    print(f"flagged cells: {sorted(flagged) or 'none'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
