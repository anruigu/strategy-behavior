#!/usr/bin/env python
"""    /home/allie/venvs/tinker-ipd/bin/python fig2_benefit_vs_rate.py

  fig2_benefit_vs_rate.png    benefit magnitude against exploit rate, every
                              (cell, model, round) as one point
  fig2_benefit_vs_rate.json   every number drawn

THE QUESTION. Pooling every cell, model and round into one cloud: does
exploiting more actually deliver more benefit?

ONE PANEL, ALL ROUNDS POOLED. Each point is one (cell, model, round) -- 4
gain-basis cells x 4 models x 4 rounds, minus the rounds with no opportunity.
The trajectory version of this plot lives in fig3; here the question is the
shape of the relationship across the whole wave, so the rounds are scattered
rather than joined.

Y IS RAW GAIN, WHICH MAKES THE BANDS REAL AND THE CLOUD NOT COMPARABLE. A
cell's gain is in that cell's own points: `sovereign_vaults` tops out near +50
and `ta_kuhn` near +6, so the cloud separates into horizontal bands BY CELL and
a regression through all of it would be measuring which cells pay more, not
whether exploiting pays. The dashed rule under each band is that cell's
`hole_gain` -- what the hole is worth to a lone exploiter in the same unit -- so
the honest reading is WITHIN a band, against its own rule. The bands are
labelled at the right for exactly that reason.

THREE CHANNELS, THREE DIMENSIONS, ALL LABELLED. Colour is the model (reference
palette slots 1-4, the same slot per model as fig1). Marker shape is the cell,
which is also readable off the labelled band. Marker SIZE grows with the
reflection round, so the drift from R0 to R3 is visible without joining the
points. None of the three is load-bearing alone.

FOUR CELLS, NOT SIX. `gen_icebound` and `ref_orderbook` price their hole in
MARGIN and have no `gain_focal` at all; they are named on the figure so their
absence is not read as a zero. On `gen_icebound` every model scores exactly
18.0 at R3 whether it exploited at 1.00 or at 0.00.

The palette validator ships as a node script and this box has no node runtime,
so the reference palette's slots are used unmodified and in order -- the
documented already-passing path -- with shape and labels as redundant encoding.
"""
from __future__ import annotations

import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from matplotlib.lines import Line2D      # noqa: E402

import _pilot_data as P                  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
SIZE = {0: 34, 1: 58, 2: 84, 3: 116}     # marker area grows with the round


def main() -> int:
    data = P.load()
    cells = [c for c in P.CELLS if data[c]["basis"] == "gain"]
    skipped = [c for c in P.CELLS if data[c]["basis"] != "gain"]
    marker = dict(zip(cells, ["o", "s", "^", "D"]))

    fig, ax = plt.subplots(figsize=(12.0, 7.4))
    fig.patch.set_facecolor(P.SURFACE)
    ax.set_facecolor(P.SURFACE)
    ax.grid(True, color=P.GRID, lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(P.GRID)
    ax.axhline(0, color=P.GRID, lw=1.0, zorder=1)

    # One dashed rule per cell at what its hole is worth: the band label. This
    # is the only legitimate comparison on this axis, so it is drawn.
    #
    # Labels go in the RIGHT MARGIN, outside the data area, and are pushed
    # apart where two rules nearly coincide -- sovereign_vaults (+49.7) and
    # seven_seal (+49.0) are 0.7 points apart on a 70-point axis and their
    # labels would print on top of each other.
    MIN_SEP = 3.6
    placed_y = None
    for cell in sorted(cells, key=lambda c: -data[c]["hole_gain"]):
        hg = data[cell]["hole_gain"]
        ax.axhline(hg, color=P.MUTED, lw=1.0, ls=(0, (5, 4)), zorder=2,
                   alpha=0.85)
        ly = hg if placed_y is None else min(hg, placed_y - MIN_SEP)
        placed_y = ly
        ax.annotate(f"{P.short(cell)}   hole is worth {hg:+.1f}",
                    xy=(1.015, ly), xycoords=("axes fraction", "data"),
                    ha="left", va="center", fontsize=8.5, color=P.INK2,
                    zorder=6, annotation_clip=False)

    pts = []
    for cell in cells:
        rec = data[cell]
        for m in P.MODELS:
            d = rec["models"][m]
            for rd in P.ROUNDS:
                r, g = d["rate"][rd], d["gain"][rd]
                if r is None or g is None:
                    continue
                ax.scatter(r, g, s=SIZE[rd], marker=marker[cell],
                           facecolor=P.MODEL_COLOR[m], edgecolor=P.SURFACE,
                           linewidth=1.4, zorder=4 + (rd == 3))
                pts.append({"cell": cell, "model": m, "round": rd,
                            "rate": r, "gain": g})

    ax.set_xlim(-0.06, 1.07)
    n0 = sum(1 for q in pts if q["rate"] < 0.01 and abs(q["gain"]) < 0.5)
    if n0:
        ax.annotate(f"{n0} points stacked here\n(never exploited, no gain)",
                    xy=(0.0, 0.0), textcoords="offset points",
                    xytext=(14, -6), ha="left", va="top", fontsize=8,
                    color=P.MUTED, style="italic", zorder=6, linespacing=1.4)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_ylim(-12, 60)
    ax.set_xlabel("exploit rate   (HARD violations / opportunities, pooled "
                  "within the round)", fontsize=9.5, color=P.INK2)
    ax.set_ylabel("benefit magnitude   (median gain_focal, cell's own points)",
                  fontsize=9.5, color=P.INK2)
    ax.tick_params(colors=P.INK2, labelsize=9, length=3)

    fig.subplots_adjust(top=0.780, bottom=0.098, left=0.070, right=0.760)
    fig.text(0.070, 0.972, "Benefit magnitude against exploit rate, every "
             "cell / model / round pooled",
             fontsize=13, color=P.INK, ha="left", va="top")
    fig.text(0.070, 0.928,
             "one point per (cell, model, round); marker grows with the "
             "round, R0 smallest to R3 largest\n"
             "gain is in each cell's own points, so the cloud bands BY CELL "
             "-- read within a band against its dashed rule, never across "
             "bands\n"
             + " and ".join(P.short(c) for c in skipped)
             + " are omitted: they price the hole in MARGIN, so gain_focal "
               "is null for every row",
             fontsize=9, color=P.INK2, ha="left", va="top", linespacing=1.6)

    mh = [Line2D([], [], color=P.MODEL_COLOR[m], lw=0, marker="o", ms=8.5,
                 markeredgecolor=P.SURFACE, markeredgewidth=1.2,
                 label=P.MODEL_LABEL[m]) for m in P.MODELS]
    ch = [Line2D([], [], color=P.INK2, lw=0, marker=marker[c], ms=8,
                 markerfacecolor=P.SURFACE, markeredgecolor=P.INK2,
                 markeredgewidth=1.5, label=P.short(c)) for c in cells]
    l1 = fig.legend(handles=mh, loc="upper left", frameon=False, fontsize=9,
                    ncol=4, labelcolor=P.INK2, bbox_to_anchor=(0.066, 0.848),
                    columnspacing=1.8, handletextpad=0.5,
                    title="model (colour)", alignment="left")
    l1.get_title().set(fontsize=8.5, color=P.MUTED, style="italic")
    l2 = fig.legend(handles=ch, loc="upper left", frameon=False, fontsize=9,
                    ncol=4, labelcolor=P.INK2, bbox_to_anchor=(0.520, 0.848),
                    columnspacing=1.5, handletextpad=0.5,
                    title="cell (shape)", alignment="left")
    l2.get_title().set(fontsize=8.5, color=P.MUTED, style="italic")

    png = HERE / "fig2_benefit_vs_rate.png"
    fig.savefig(png, dpi=200, facecolor=P.SURFACE)
    print(f"wrote {png}")
    P.write_json(HERE / "fig2_benefit_vs_rate.json", {
        "x": "pooled HARD exploit rate for that cell/model/round",
        "y": "median gain_focal for that cell/model/round",
        "encoding": {"colour": "model", "shape": "cell",
                     "size": "round, R0 smallest"},
        "rules": {c: data[c]["hole_gain"] for c in cells},
        "omitted": {c: "margin-basis, gain_focal null" for c in skipped},
        "points": pts})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
