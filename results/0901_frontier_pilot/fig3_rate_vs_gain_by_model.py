#!/usr/bin/env python
"""    /home/allie/venvs/tinker-ipd/bin/python fig3_rate_vs_gain_by_model.py

  fig3_rate_vs_gain_by_model.png   one panel per model: exploit rate against
                                   the share of the hole's value captured,
                                   traced R0 -> R3, one curve per cell
  fig3_rate_vs_gain_by_model.json  every number drawn

THE QUESTION. Read per MODEL rather than per cell: across the cells it plays,
where does each frontier model end up in (exploit rate, benefit) space, and
which way does reflection move it?

Y IS A SHARE, NOT RAW GAIN -- and this is the one place in the set where that
is right. Four cells share a panel here, and their gains are in four different
units (`sovereign_vaults` swings +42, `ta_kuhn` +1). Raw gain on a shared axis
would render kuhn as a flat line at zero and say something false about it. The
share is `median gain_focal / hole_gain`, both from the same cell in the same
unit, so 1.0 means "captured what the hole is worth to a lone exploiter" in
every panel. Cross-cell comparison of the SHARE is legitimate in a way that
cross-cell comparison of the rate or the raw gain is not.

WHY THE SHARE CAN EXCEED 1.0. `hole_gain` is a single reference episode's
value, not a ceiling; gemini clears it on `quiet_sonar` (+22 against +21.2).
The rule is a yardstick, not a maximum.

FOUR CELLS, NOT SIX, for the reason fig2 gives: `gen_icebound` and
`ref_orderbook` price their hole in MARGIN and have no `gain_focal` at all.
Every panel names them so their absence is not read as a zero.

COLOUR IS BY CELL HERE, not by model -- the faceting dimension is never also
the colour dimension. The cells take reference-palette slots 5-8 (magenta,
green, violet, red) rather than 1-4, because slots 1-4 mean claude / gemini /
gpt / grok in every other figure in this set and a hue must not change what it
refers to between two figures a reader sees side by side. Every curve is ALSO
direct-labelled with its cell name at the R3 end, so identity never rests on
the hue.
"""
from __future__ import annotations

import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from matplotlib.lines import Line2D      # noqa: E402

import _pilot_data as P                  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
FLAT = 0.05


def main() -> int:
    data = P.load()
    cells = [c for c in P.CELLS if data[c]["basis"] == "gain"]
    skipped = [c for c in P.CELLS if data[c]["basis"] != "gain"]
    color = dict(zip(cells, P.SLOT[4:8]))
    marker = dict(zip(cells, ["o", "s", "^", "D"]))

    fig, axes = plt.subplots(2, 2, figsize=(11.4, 8.8), sharex=True,
                             sharey=True)
    fig.patch.set_facecolor(P.SURFACE)
    drawn = {}

    for ax, m in zip(axes.flat, P.MODELS):
        ax.set_facecolor(P.SURFACE)
        ax.grid(True, color=P.GRID, lw=0.7, zorder=0)
        ax.set_axisbelow(True)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("left", "bottom"):
            ax.spines[side].set_color(P.GRID)
        ax.axhline(1.0, color=P.MUTED, lw=1.2, ls=(0, (5, 4)), zorder=2)
        ax.axhline(0, color=P.GRID, lw=1.0, zorder=1)

        flat = []
        # Endpoints coincide -- claude ends BOTH kuhn and quiet_sonar at the
        # origin -- so a fixed label offset stacks two cell names on the same
        # pixels. Count how many labels an endpoint already carries and step
        # each further one up a row.
        stack: dict = {}
        for cell in cells:
            rec = data[cell]
            hg = rec["hole_gain"]
            d = rec["models"][m]
            pts = [(r, g / hg) for r, g in zip(d["rate"], d["gain"])
                   if r is not None and g is not None]
            if not pts:
                continue
            if (d["peak"] or 0.0) < FLAT:
                flat.append(P.short(cell))
                continue
            col = color[cell]
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            ax.plot(xs, ys, color=col, lw=2.0, zorder=3, alpha=0.9)
            ax.plot(xs[0], ys[0], marker=marker[cell], ms=8,
                    markerfacecolor=P.SURFACE, markeredgecolor=col,
                    markeredgewidth=2.0, zorder=4, linestyle="none")
            ax.plot(xs[-1], ys[-1], marker=marker[cell], ms=9, color=col,
                    markeredgecolor=P.SURFACE, markeredgewidth=1.6,
                    zorder=5, linestyle="none")
            if len(xs) > 1 and (xs[-1], ys[-1]) != (xs[-2], ys[-2]):
                ax.annotate("", xy=(xs[-1], ys[-1]),
                            xytext=(xs[-2] + (xs[-1] - xs[-2]) * 0.55,
                                    ys[-2] + (ys[-1] - ys[-2]) * 0.55),
                            arrowprops=dict(arrowstyle="-|>", color=col,
                                            lw=0, mutation_scale=15,
                                            shrinkA=0, shrinkB=9), zorder=4)
            # direct label: identity never rests on the hue alone
            right = xs[-1] < 0.55
            key = (round(xs[-1], 2), round(ys[-1], 2))
            k = stack.get(key, 0)
            stack[key] = k + 1
            ax.annotate(P.short(cell), (xs[-1], ys[-1]),
                        textcoords="offset points",
                        xytext=(11 if right else -11, 9 + 13 * k),
                        ha="left" if right else "right", va="bottom",
                        fontsize=8.5, color=P.INK, zorder=6)
            drawn[f"{m}|{cell}"] = {"rate": xs, "share": ys}

        if flat:
            ax.plot(0, 0, marker="x", ms=7, color=P.MUTED, zorder=4,
                    linestyle="none")
            ax.annotate("never exploited:  " + ", ".join(flat),
                        xy=(0.03, 0.055), xycoords="axes fraction",
                        fontsize=8, color=P.MUTED, style="italic",
                        va="bottom")
            for c in cells:
                if P.short(c) in flat:
                    drawn[f"{m}|{c}"] = {"rate": data[c]["models"][m]["rate"],
                                         "share": [0.0] * len(P.ROUNDS)}

        ax.set_title(P.MODEL_LABEL[m], fontsize=11, color=P.INK, pad=6,
                     loc="left")
        ax.set_xlim(-0.08, 1.16)
        ax.set_ylim(-0.30, 1.42)
        ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
        ax.set_yticks([0, 0.5, 1.0])
        ax.tick_params(colors=P.INK2, labelsize=8.5, length=3)
        ax.annotate("hole captured", (-0.06, 1.0), ha="left", va="bottom",
                    fontsize=7.5, color=P.MUTED, style="italic")

    fig.supxlabel("exploit rate   (HARD violations / opportunities, pooled)",
                  fontsize=9.5, color=P.INK2, y=0.042)
    fig.supylabel("share of the hole's value captured   "
                  "(median gain_focal / hole_gain)",
                  fontsize=9.5, color=P.INK2, x=0.022)

    fig.subplots_adjust(top=0.780, bottom=0.100, left=0.082, right=0.978,
                        hspace=0.24, wspace=0.10)
    fig.text(0.082, 0.972, "Where each frontier model ends up: exploit rate "
             "against benefit captured, traced R0 to R3",
             fontsize=13, color=P.INK, ha="left", va="top")
    fig.text(0.082, 0.930,
             "hollow marker = R0, filled = R3, dashed rule = the whole value "
             "of the hole to a lone exploiter\n"
             + " and ".join(P.short(c) for c in skipped)
             + " are omitted: they price the hole in MARGIN, so there is no "
               "self-gain to share",
             fontsize=9, color=P.INK2, ha="left", va="top", linespacing=1.6)

    handles = [Line2D([], [], color=color[c], lw=2.4, marker=marker[c],
                      ms=7.5, markeredgecolor=P.SURFACE, markeredgewidth=1.2,
                      label=f"{P.short(c)}  (+{data[c]['buys']:.0f})")
               for c in cells]
    fig.legend(handles=handles, loc="upper left", frameon=False, fontsize=9,
               ncol=4, labelcolor=P.INK2, bbox_to_anchor=(0.078, 0.848),
               columnspacing=1.8, handlelength=2.2, handletextpad=0.6)

    png = HERE / "fig3_rate_vs_gain_by_model.png"
    fig.savefig(png, dpi=200, facecolor=P.SURFACE)
    print(f"wrote {png}")
    P.write_json(HERE / "fig3_rate_vs_gain_by_model.json", {
        "x": "pooled HARD exploit rate per round",
        "y": "median gain_focal / solo hole_gain, per round",
        "omitted": {c: "margin-basis, gain_focal null" for c in skipped},
        "series": drawn})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
