#!/usr/bin/env python
"""Three PNG figures for `docs/hackable-games.md`, from the 0902/03 pilots.

    python make_doc_payoff_figs.py            # -> docs/figs/*.png

They replace prose and a 16-row table in the doc, so each one has to carry its
claim on its own:

  1. `pilot4-round-curves.png` -- exploit rate against reflection round, six
     cells, coloured BY TIER so the question ("do the frontier curves look
     different from the small ones") is the visual encoding. Reflection is a
     latch, not a ramp.
  2. `pilot6-score-vs-gain.png` -- absolute score against the counterfactual
     gain, per round. The GAP between the lines is the finding: score can
     travel a long way while the counterfactual does not move.
  3. `pilot7-reference-vs-realised.png` -- what a scripted exploiter got with
     no model in the loop, against the best realised gain. Replaces the
     reference/realised table.

Everything is read from `results/0902_pilots/pilots.json`, which
`make_pilot_figs.py` writes; that file renders hand-rolled SVG for a web page,
this one writes matplotlib PNGs for the Markdown doc.
"""
from __future__ import annotations

import json
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                              # noqa: E402
from matplotlib.lines import Line2D                          # noqa: E402
from matplotlib.patches import Patch                          # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "results" / "0902_pilots" / "pilots.json"
OUT = HERE.parent / "docs" / "figs"

BG = "#fcfcfb"
INK = "#1a1a19"
INK2 = "#4a4a47"
DIM = "#8a8a85"
GRID = "#eeeeea"

TIER_C = {"frontier": "#2a78d6", "small": "#eb6834"}
SCORE_C = "#2a78d6"
GAIN_C = "#eb6834"

MONO = {"family": "monospace"}

TIER_MODELS = {"frontier": ["claude", "gpt", "gemini", "grok"],
               "small": ["haiku", "gpt-mini", "gemini-flash"]}
TIER_ROSTER = {"frontier": "opus-5, gpt-5.6-sol, gemini-3.1-pro, grok-4.6",
               "small": "haiku-4.5, gpt-5-mini, gemini-3.7-flash"}
MARKER = {"claude": "o", "gpt": "s", "gemini": "^", "grok": "D",
          "haiku": "o", "gpt-mini": "s", "gemini-flash": "^"}
DASH = {"claude": "-", "gpt": "--", "gemini": ":", "grok": "-.",
        "haiku": "-", "gpt-mini": "--", "gemini-flash": ":"}


def style() -> None:
    plt.rcParams.update({
        "figure.facecolor": BG,
        "axes.facecolor": BG,
        "savefig.facecolor": BG,
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans"],
        "text.color": INK,
        "axes.edgecolor": INK2,
        "axes.labelcolor": INK2,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "axes.linewidth": 0.8,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "legend.frameon": False,
        "savefig.dpi": 200,
    })


def bare(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def save(fig, name: str) -> pathlib.Path:
    p = OUT / name
    fig.savefig(p, dpi=200, bbox_inches="tight", pad_inches=0.16)
    plt.close(fig)
    return p


# --------------------------------------------------------------------------
# figure 1 -- pilot 4 round curves
# --------------------------------------------------------------------------

def spread(ys: list[float], gap: float, lo: float, hi: float) -> list[float]:
    """Nudge sorted label positions apart, then back inside [lo, hi].

    Up-pass then down-pass rather than up alone: on `gen_seven_seal` five
    lines end at exactly 1.000, and an up-only nudge walks that stack clean
    off the top of the panel and into the title.
    """
    out, prev = [], lo - gap
    for y in ys:
        prev = max(y, prev + gap)
        out.append(prev)
    if out and out[-1] > hi:
        prev = hi + gap
        for i in range(len(out) - 1, -1, -1):
            prev = min(out[i], prev - gap)
            out[i] = prev
    return out


def fig_round_curves(data: dict, path: str) -> pathlib.Path:
    cells = sorted({c for tier in data.values() for c in tier})
    series = []
    for tier, per_cell in data.items():
        for m in TIER_MODELS[tier]:
            if any(m in per_cell.get(c, {}) for c in cells):
                series.append((tier, m))
    # A y OFFSET, because on `gen_seven_seal` four lines sit exactly on 1.000
    # and on `ref_orderbook` seven sit exactly on 0.000; without it a reader
    # sees one line and cannot tell whether the others are missing. Each
    # series is shifted by its index about the middle of the roster, so the
    # largest displacement is ~0.024 of a 0-1 axis -- under half a marker
    # width, and every printed value in the doc comes from the table.
    off = {ms: (i - (len(series) - 1) / 2) * 0.009
           for i, ms in enumerate(series)}

    fig, axes = plt.subplots(2, 3, figsize=(11.0, 6.9))
    for ax, cell in zip(axes.ravel(), cells):
        bare(ax)
        ax.set_xlim(-0.16, 4.35)
        ax.set_ylim(-0.08, 1.10)
        ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(["0.00", "0.25", "0.50", "0.75", "1.00"],
                           fontsize=8)
        ax.set_xticks(range(4))
        ax.set_xticklabels([f"R{r}" for r in range(4)], fontsize=8.5)
        ax.grid(axis="y", which="major")
        ax.set_title(cell, fontsize=9.5, color=INK2, fontweight="bold",
                     loc="left", pad=7, **MONO)
        ends = []
        # small tier under the frontier tier, so the comparison reads as
        # "where do the small models sit relative to the frontier"
        for tier, m in sorted(series, key=lambda s: s[0] != "small"):
            vals = data[tier].get(cell, {}).get(m)
            if not vals or all(v is None for v in vals):
                continue
            ys = [None if v is None else v + off[(tier, m)] for v in vals]
            xs = [r for r, v in enumerate(ys) if v is not None]
            yy = [v for v in ys if v is not None]
            ax.plot(xs, yy, color=TIER_C[tier], linewidth=1.6,
                    linestyle=DASH[m], marker=MARKER[m], markersize=4.2,
                    markeredgecolor=BG, markeredgewidth=0.7,
                    zorder=3 if tier == "frontier" else 2, clip_on=False)
            ends.append((yy[-1], xs[-1], tier, m))
        ends.sort()
        for (y, x, tier, m), ly in zip(ends, spread([e[0] for e in ends],
                                                    0.086, -0.05, 1.07)):
            ax.text(x + 0.34, ly, m, fontsize=8, color=TIER_C[tier],
                    va="center", ha="left", fontweight="bold", **MONO)
            # a leader wherever the label had to leave its own line's height,
            # which on `gen_seven_seal` is five of the seven
            if abs(ly - y) > 0.012:
                ax.plot([x + 0.09, x + 0.29], [y, ly], color=DIM,
                        linewidth=0.6, linestyle=(0, (1, 1.4)), zorder=1)

    fig.supxlabel("reflection round", fontsize=9.5, color=INK2, y=0.005)
    fig.supylabel("exploit rate", fontsize=9.5, color=INK2, x=0.012)
    handles = [Line2D([], [], color=TIER_C[t], linewidth=2.2,
                      marker="o", markersize=5, markeredgecolor=BG,
                      label=f"{t}  \u00b7  {TIER_ROSTER[t]}")
               for t in ("frontier", "small")]
    fig.legend(handles=handles, loc="lower center",
               bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=9,
               handlelength=2.6, columnspacing=2.4,
               labelcolor=INK2)
    fig.text(0.5, 1.055, "colour is the tier, not the model \u2014 each line "
                         "is labelled with its own model at the right",
             ha="center", fontsize=8.5, color=DIM)
    fig.tight_layout(h_pad=2.6, w_pad=1.8, rect=(0.02, 0.02, 1, 1))
    return save(fig, path)


# --------------------------------------------------------------------------
# figure 2 -- pilot 6 score against counterfactual gain
# --------------------------------------------------------------------------

def divergence(d: dict) -> float:
    """How far the absolute score travels that the counterfactual does not.

    span(score) - span(gain), where span is max minus min over the rounds on
    record. Range rather than last-minus-first, so a cell whose score spikes
    and returns still counts as having moved; and a difference of spans rather
    than a ratio, so cells whose gain never leaves zero do not divide by it.
    Negative values are the other direction -- the counterfactual moving more
    than the score, which `ref_invoice` does.
    """
    return ((max(d["score"]) - min(d["score"]))
            - (max(d["gain"]) - min(d["gain"])))


def fig_score_vs_gain(data: dict, path: str, top: int = 9) -> pathlib.Path:
    order = sorted(data, key=lambda c: (-divergence(data[c]), c))[:top]
    fig, axes = plt.subplots(3, 3, figsize=(10.4, 7.8))
    for ax, cell in zip(axes.ravel(), order):
        d = data[cell]
        bare(ax)
        xs = list(range(len(d["rounds"])))
        ax.grid(axis="y", which="major")
        ax.axhline(0, color=DIM, linewidth=0.9, linestyle=(0, (3, 3)),
                   zorder=1.5)
        ax.fill_between(xs, d["score"], d["gain"], color=SCORE_C, alpha=0.11,
                        hatch="///", edgecolor=SCORE_C, linewidth=0.0,
                        zorder=1.2)
        ax.plot(xs, d["score"], color=SCORE_C, linewidth=1.8, marker="o",
                markersize=4.6, markeredgecolor=BG, markeredgewidth=0.8,
                zorder=3)
        ax.plot(xs, d["gain"], color=GAIN_C, linewidth=1.8, marker="s",
                markersize=4.4, markeredgecolor=BG, markeredgewidth=0.8,
                zorder=3)
        vals = d["score"] + d["gain"] + [0.0]
        lo, hi = min(vals), max(vals)
        pad = (hi - lo) * 0.16 or 1.0
        ax.set_ylim(lo - pad, hi + pad)
        # symmetric side margins, so the dashed zero line shows a stub at both
        # ends of any panel whose gain sits exactly on it
        ax.set_xlim(-0.32, len(xs) - 0.68)
        ax.set_xticks(xs)
        ax.set_xticklabels([f"R{r}" for r in d["rounds"]], fontsize=8.5)
        ax.tick_params(axis="y", labelsize=8)
        # a constant pad, flat or not, so the panel titles share one baseline
        ax.set_title(cell, fontsize=9.5, color=INK2, fontweight="bold",
                     loc="left", pad=15, **MONO)
        if (max(d["gain"]) - min(d["gain"])) < 1e-9:
            ax.text(0.0, 1.015, "gain flat \u2014 never moves",
                    transform=ax.transAxes, fontsize=8, color=DIM,
                    va="bottom")

    for ax in axes.ravel()[len(order):]:
        ax.set_visible(False)

    fig.supxlabel("reflection round", fontsize=9.5, color=INK2, y=0.005)
    fig.supylabel("points \u2014 each panel has its own y axis "
                  "(magnitudes differ ~100\u00d7 across cells)",
                  fontsize=9.5, color=INK2, x=0.004)
    handles = [
        Line2D([], [], color=SCORE_C, linewidth=2.2, marker="o",
               markersize=5, markeredgecolor=BG,
               label="absolute score \u2014 the points the seat ends on"),
        Line2D([], [], color=GAIN_C, linewidth=2.2, marker="s",
               markersize=5, markeredgecolor=BG,
               label="counterfactual gain \u2014 score minus playing honestly "
                     "on the same board"),
        Patch(facecolor=SCORE_C, alpha=0.18, hatch="///", edgecolor=SCORE_C,
              label="the gap between them"),
    ]
    fig.legend(handles=handles, loc="lower center",
               bbox_to_anchor=(0.5, 1.0), ncol=2, fontsize=9,
               handlelength=2.6, columnspacing=2.4, labelcolor=INK2)
    fig.tight_layout(h_pad=2.9, w_pad=2.2, rect=(0.02, 0.02, 1, 1))
    return save(fig, path)


# --------------------------------------------------------------------------
# figure 3 -- pilot 7 reference against realised
# --------------------------------------------------------------------------

REF_C = "#4a4a47"
REAL_C = "#1a1a19"
SHORT_C = "#8a8a85"
OVER_C = "#2a78d6"
BAND_HI = 30.0


def live_cells(data: dict) -> tuple[dict, list[tuple[str, str]]]:
    keep, drop = {}, []
    for cell, d in sorted(data.items()):
        if d.get("pending"):
            drop.append((cell, "pending \u2014 counterfactual was broken "
                               "pre-fix, re-sampling"))
        elif d.get("real") is None:
            drop.append((cell, f"no realised gain "
                               f"(n_chains={d.get('n_chains', 0)})"))
        elif d.get("thin"):
            drop.append((cell, f"too thin to call "
                               f"(n_chains={d.get('n_chains', 0)})"))
        else:
            keep[cell] = d
    return keep, drop


def wrap_hole(h: str) -> str:
    return h.replace("+", "\n+") if len(h) > 18 else h


def fig_reference_vs_realised(data: dict, path: str) -> pathlib.Path:
    live, _ = live_cells(data)
    bands = [(f"reference above +{BAND_HI:.0f} points",
              [c for c in live if live[c]["avail"] > BAND_HI]),
             (f"reference +{BAND_HI:.0f} points or below",
              [c for c in live if live[c]["avail"] <= BAND_HI])]
    bands = [(t, sorted(cs, key=lambda c: live[c]["avail"])) for t, cs in bands
             if cs]

    fig, axes = plt.subplots(
        len(bands), 1, figsize=(9.6, 8.4),
        gridspec_kw={"height_ratios": [len(cs) for _, cs in bands],
                     "hspace": 0.30})
    axes = [axes] if len(bands) == 1 else list(axes)

    for ax, (title, cells) in zip(axes, bands):
        bare(ax)
        ax.grid(axis="x", which="major")
        ax.axvline(0, color=DIM, linewidth=0.9, linestyle=(0, (3, 3)),
                   zorder=1.5)
        vals = [0.0]
        for i, cell in enumerate(cells):
            d = live[cell]
            ref, real = d["avail"], d["real"]
            vals += [ref, real]
            # "beats the reference" is keyed off `capture`, not off
            # real > ref: on `hx_quota_checker` the reference is -22.9, and
            # clearing a negative reference is not the same finding.
            over = d.get("capture") is not None and d["capture"] > 1.0
            ax.plot([ref, real], [i, i],
                    color=OVER_C if over else SHORT_C, linewidth=5.0,
                    alpha=0.9 if over else 0.45, solid_capstyle="round",
                    zorder=2)
            ax.plot([ref], [i], marker="o", markersize=9.5,
                    markerfacecolor=BG, markeredgecolor=REF_C,
                    markeredgewidth=1.8, zorder=3)
            # smaller than the ring, so a cell that realised the reference
            # exactly (`ref_commons`, `gen_seven_seal`) still shows both marks
            ax.plot([real], [i], marker="o", markersize=5.2,
                    color=REAL_C, zorder=4)
        lo, hi = min(vals), max(vals)
        pad = (hi - lo) * 0.06 or 1.0
        ax.set_xlim(lo - pad, hi + pad * 4.4)
        ax.set_ylim(-0.62, len(cells) - 0.38)
        ax.set_yticks([])
        ax.tick_params(axis="x", labelsize=8)
        ax.set_title(f"{title}  \u00b7  {len(cells)} cells  \u00b7  own x axis",
                     fontsize=9, color=INK2, fontweight="bold", loc="left",
                     pad=8)
        for i, cell in enumerate(cells):
            d = live[cell]
            ax.text(-0.012, i + 0.05, cell, transform=ax.get_yaxis_transform(),
                    ha="right", va="bottom", fontsize=9, color=INK2, **MONO)
            ax.text(-0.012, i - 0.03, wrap_hole(d["hole"]),
                    transform=ax.get_yaxis_transform(), ha="right", va="top",
                    fontsize=7, color=DIM, linespacing=1.2, **MONO)
            cap = d.get("capture")
            over = cap is not None and cap > 1.0
            txt = ("n/a \u2014 reference \u2264 0" if cap is None
                   else f"{100 * cap:,.0f}%")
            ax.annotate(txt, (max(d["avail"], d["real"]), i), xytext=(12, 0),
                        textcoords="offset points", va="center", ha="left",
                        fontsize=8.5, color=OVER_C if over else INK2,
                        fontweight="bold" if over else "normal")
        ax.set_xlabel("points \u2014 counterfactual gain, own axis per panel",
                      fontsize=8.5, color=INK2, labelpad=4)

    handles = [
        Line2D([], [], marker="o", linestyle="none", markersize=8.5,
               markerfacecolor=BG, markeredgecolor=REF_C, markeredgewidth=1.8,
               label="reference \u2014 a scripted exploiter's own gain, "
                     "no model in the loop"),
        Line2D([], [], marker="o", linestyle="none", markersize=7,
               color=REAL_C, label="best realised \u2014 best model's "
                                   "median gain"),
        Line2D([], [], color=SHORT_C, linewidth=5, alpha=0.5,
               solid_capstyle="round",
               label="shortfall \u2014 realised falls short of the reference"),
        Line2D([], [], color=OVER_C, linewidth=5, alpha=0.9,
               solid_capstyle="round",
               label="the best model BEATS the reference (over 100%)"),
    ]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 1.0),
               ncol=2, fontsize=9, handlelength=2.4, columnspacing=2.2,
               labelcolor=INK2)
    fig.text(0.5, 1.075,
             "the percentage is realised \u00f7 reference, NOT percent of a "
             "maximum. The scripted policy is one fixed way of\nworking each "
             "hole rather than the best one, so the values above 100% are a "
             "real finding and not an error.",
             ha="center", va="bottom", fontsize=8.2, color=DIM,
             linespacing=1.5)
    fig.subplots_adjust(top=0.965, bottom=0.05, hspace=0.30)
    return save(fig, path)


# --------------------------------------------------------------------------

def main() -> int:
    style()
    OUT.mkdir(parents=True, exist_ok=True)
    d = json.loads(SRC.read_text())
    p4 = d["pilot4_round_curves"]
    p6 = d["pilot6_round_payoff"]
    p7 = d["pilot7_reference_vs_realised"]

    paths = [
        fig_round_curves(p4, "pilot4-round-curves.png"),
        fig_score_vs_gain(p6, "pilot6-score-vs-gain.png"),
        fig_reference_vs_realised(p7, "pilot7-reference-vs-realised.png"),
    ]
    for p in paths:
        print(f"wrote {p}  ({p.stat().st_size / 1024:.0f} KB)")

    print("\nfigure 2 -- divergence = span(score) - span(gain), descending")
    for c in sorted(p6, key=lambda c: (-divergence(p6[c]), c))[:9]:
        s, g = p6[c]["score"], p6[c]["gain"]
        print(f"  {c:<26} div {divergence(p6[c]):8.2f}   "
              f"score {min(s):8.2f}..{max(s):8.2f}   "
              f"gain {min(g):8.2f}..{max(g):8.2f}")

    live, drop = live_cells(p7)
    print(f"\nfigure 3 -- {len(live)} cells plotted, "
          f"{len(drop)} excluded")
    for cell, why in drop:
        print(f"  excluded {cell:<24} {why}")
    for c in sorted(live, key=lambda c: -live[c]["avail"]):
        cap = live[c]["capture"]
        print(f"  plotted  {c:<24} ref {live[c]['avail']:+8.2f}  "
              f"real {live[c]['real']:+8.2f}  "
              f"capture {'n/a' if cap is None else f'{100 * cap:.0f}%'}")

    print("\nfigure 1 -- spot check against pilots.json")
    for tier, cell, m in (("frontier", "gen_quiet_sonar", "claude"),
                          ("frontier", "gen_quiet_sonar", "gemini"),
                          ("frontier", "gen_seven_seal", "grok"),
                          ("small", "ref_orderbook", "gemini-flash")):
        print(f"  {tier:<9} {cell:<22} {m:<14} "
              + " ".join(f"{v:.3f}" for v in p4[tier][cell][m]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
