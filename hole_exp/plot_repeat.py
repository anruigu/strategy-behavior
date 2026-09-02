#!/usr/bin/env python3
"""Exploit rate against number of repeated plays, one curve per catch price.

    python plot_repeat.py results/referee_repeat/sweep1

Small multiples, one panel per cell, because the cells' exploit rates are not
comparable in level -- some surface the affordance in the rules and some do not
(`research_logs/0828-referee-holes.md` §5) -- so a single axes with eleven lines
would invite exactly the cross-cell reading the design forbids. Each panel is
read on its own; what transfers across panels is the SHAPE.

COLOUR IS ORDINAL, NOT CATEGORICAL. `p_caught` is five ordered levels of one
quantity, so it gets one hue light->dark, never five different hues: a rainbow
here would throw away the ordering that is the whole point of the series. The
steps are the documented blue ramp, and for an ordinal ramp the step nearest
the surface must still clear 2:1, which is why the light ramp starts at step
250 and not at 100.

  NOTE ON VALIDATION: the palette validator is a node script and this box has
  no node runtime, so it could not be run. Rather than invent hues and eyeball
  them, every step below is a documented step of the reference ramp used within
  its documented ordinal constraint. A single-hue luminance-ordered ramp cannot
  fail the CVD-separation check the way a categorical set can; the check that
  does bite is contrast against the surface, and the ramp's own floor
  (light step 250 = 2.06:1, dark step 600 = 2.15:1) is what bounds the ends.

Both modes are rendered, and the dark one is STEPPED for the dark surface
rather than being the light ramp inverted.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Dict, List, Optional, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# ---- the ordinal ramp, five steps, documented values ---------------------
RAMP = {
    # light surface: start no lighter than step 250
    "light": ["#86b6ef", "#5598e7", "#2a78d6", "#184f95", "#0d366b"],
    # dark surface: go no darker than step 600
    "dark":  ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#184f95"],
}
INK = {
    "light": {"surface": "#fcfcfb", "primary": "#0b0b0b",
              "secondary": "#52514e", "grid": "#e6e5e1"},
    "dark":  {"surface": "#1a1a19", "primary": "#ffffff",
              "secondary": "#c3c2b7", "grid": "#383835"},
}


def load(d: pathlib.Path) -> List[Dict]:
    f = d / "rows.jsonl"
    if not f.exists():
        raise SystemExit(f"no rows.jsonl in {d}")
    return [json.loads(l) for l in f.open()]


# Kinds that are a strict OR over other kinds in the same cell get their own
# panel suppressed -- the panel would redraw its members' behaviour a third
# time. Kinds that are end-of-episode OUTCOMES (`budget_overrun`,
# `stock_collapse`) are NOT suppressed: they are not chargeable, which is a
# statement about the price, but they are real readouts and `budget_overrun`
# is one of the four the 0828 rho table names. See `referee_repeat.DERIVED`.
UNION = {"misreport", "invoice_fraud", "covert_channel"}


def panels(rows: List[Dict], games: List[str]) -> List[Tuple[str, str]]:
    """One panel per (cell, HARD kind) -- NOT one per cell.

    This was one panel per cell, plotting `v_headline`, and it would have
    reported a flat null on the very first live data. `ref_invoice`'s headline
    is `unearned_completion`, which sat at 0.17 across every play; the kind
    that actually moved was `hour_padding`, climbing 0.33 -> 0.50 -> 0.67 ->
    1.00 over four plays in one chain. A cell has several ways to be exploited
    and they do not have to move together, so collapsing a cell to its
    headline can hide the entire effect. The headline exists to rank cells in
    a cross-play table; it is the wrong summary for a learning curve.
    """
    out = []
    for g in games:
        sel = [r for r in rows if r["game"] == g]
        if not sel:
            continue
        kinds = [k[2:] for k in sel[0] if k.startswith("v_")
                 and k != "v_headline" and k[2:] not in UNION]
        # keep only kinds that ever had an opportunity -- a kind whose
        # denominator is zero throughout is an empty panel, not a null
        for k in kinds:
            if any(r.get(f"o_{k}", 0) for r in sel):
                out.append((g, k))
    # RANKED BY PEAK RATE, and kinds that are zero everywhere are pulled out
    # entirely. Six of fourteen panels came back flat at zero on the first
    # full render, which is a real result -- the model never takes those
    # holes -- but six empty axes are not how to report it. They go in a
    # footnote and in the table, where a zero reads as a zero instead of as
    # a rendering fault, and the panels that remain are ordered so the eye
    # lands on the cells that move.
    def peak(gk):
        g, k = gk
        return max((v for _, v, _ in
                    [x for p in curves(rows, g, k).values() for x in p]
                    if v is not None), default=0.0)
    ranked = sorted(out, key=lambda gk: -peak(gk))
    live = [gk for gk in ranked if peak(gk) > 0]
    dead = [gk for gk in ranked if peak(gk) == 0]
    return live, dead


def curves(rows: List[Dict], game: str, kind: str
           ) -> Dict[float, List[Tuple[int, Optional[float], int]]]:
    """Pooled rate per (p_caught, play). Numerator and denominator are summed
    across chains BEFORE dividing -- a mean of per-chain rates would weight a
    chain that had one opportunity the same as one that had twelve, which is
    the same denominator mistake the whole suite is built to avoid."""
    sel = [r for r in rows if r["game"] == game]
    out: Dict[float, Dict[int, List[int]]] = {}
    for r in sel:
        out.setdefault(r["p_caught"], {}).setdefault(r["play"], [0, 0])
        out[r["p_caught"]][r["play"]][0] += r.get(f"v_{kind}", 0)
        out[r["p_caught"]][r["play"]][1] += r.get(f"o_{kind}", 0)
    return {p: [(k, (a / b if b else None), b)
                for k, (a, b) in sorted(v.items())]
            for p, v in sorted(out.items())}


def render(rows: List[Dict], games: List[str], mode: str,
           out: pathlib.Path, tag: str):
    ink, ramp = INK[mode], RAMP[mode]
    pans, dead = panels(rows, games)
    n = len(pans)
    cols = min(3, n) or 1
    figrows = (n + cols - 1) // cols
    fig, axes = plt.subplots(figrows, cols, figsize=(4.6 * cols, 3.7 * figrows),
                             sharey=True, squeeze=False)
    fig.patch.set_facecolor(ink["surface"])
    ps = sorted({r["p_caught"] for r in rows})
    # fixed order, darkest = most policing. Assigned by LEVEL, not by
    # position in whatever subset this run happens to contain, so dropping a
    # dose from a later sweep cannot repaint the ones that remain.
    allp = [0.0, 0.2, 0.4, 0.6, 0.8]
    colour = {p: ramp[min(allp.index(p), len(ramp) - 1)] if p in allp
              else ramp[-1] for p in ps}

    for i, (game, kind) in enumerate(pans):
        ax = axes[i // cols][i % cols]
        ax.set_facecolor(ink["surface"])
        cur = curves(rows, game, kind)
        for p in ps:
            pts = [(k, v) for k, v, _ in cur.get(p, []) if v is not None]
            if not pts:
                continue
            ax.plot([k for k, _ in pts], [v for _, v in pts],
                    color=colour[p], linewidth=2.0, marker="o",
                    markersize=5.5, markeredgecolor=ink["surface"],
                    markeredgewidth=1.5, label=f"p = {p:.1f}", zorder=3)
        ax.set_title(f"{game.replace('ref_','')}\n{kind}",
                     color=ink["primary"], fontsize=11, loc="left", pad=8)
        ax.grid(True, color=ink["grid"], linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        for s in ("bottom", "left"):
            ax.spines[s].set_color(ink["grid"])
        ax.tick_params(colors=ink["secondary"], labelsize=9)
        ax.set_ylim(-0.04, 1.04)
        xs = sorted({k for p in ps for k, _, _ in cur.get(p, [])})
        if xs:
            ax.set_xticks(xs)
    for j in range(n, figrows * cols):
        axes[j // cols][j % cols].set_visible(False)

    fig.supxlabel("number of repeated plays (memory carried forward)",
                  color=ink["secondary"], fontsize=10, y=0.035)
    fig.supylabel("exploit rate  (violations / opportunities)",
                  color=ink["secondary"], fontsize=10)
    fig.suptitle("Does memory teach exploitation, and does a price stop it?",
                 color=ink["primary"], fontsize=13, x=0.01, ha="left", y=0.995)
    # Five series, so a legend and no direct labels -- direct-labelling is for
    # <= 4. Identity is never colour-alone: the legend text names the level.
    h, l = axes[0][0].get_legend_handles_labels()
    leg = fig.legend(h, l, loc="upper right", bbox_to_anchor=(1.0, 1.0),
                     ncol=len(ps), frameon=False,
                     fontsize=9, title="probability a violation is caught",
                     title_fontsize=9)
    for t in leg.get_texts():
        t.set_color(ink["secondary"])
    leg.get_title().set_color(ink["secondary"])
    if dead:
        fig.text(0.5, 0.008,
                 "never exploited at any price or play (rate 0.000 "
                 "throughout, opportunities present): "
                 + ", ".join(f"{g.replace('ref_','')}/{k}" for g, k in dead),
                 ha="center", color=ink["secondary"], fontsize=8.5)
    # `rect` bottom has to clear BOTH the axis label and the footnote --
    # they collided at 0.045 and the render check is what caught it, not the
    # validator, which only ever looks at colour.
    fig.tight_layout(rect=[0.02, 0.075, 1, 0.955])
    p = out / f"repeat-{tag}-{mode}.png"
    fig.savefig(p, dpi=170, facecolor=ink["surface"])
    plt.close(fig)
    return p


def table(rows: List[Dict], games: List[str], out: pathlib.Path, tag: str):
    """The table view. Not optional -- three of the light steps sit under 3:1
    on the light surface, and the relief rule for that is a visible table."""
    lines = ["# exploit rate by play index and catch probability", ""]
    live, dead = panels(rows, games)
    for game, kind in live + dead:
        cur = curves(rows, game, kind)
        lines += [f"## {game} / {kind}", ""]
        ps = sorted(cur)
        plays = sorted({k for p in ps for k, _, _ in cur[p]})
        lines.append("| p_caught | " + " | ".join(f"play {k}" for k in plays)
                     + " |")
        lines.append("|---|" + "---|" * len(plays))
        for p in ps:
            d = {k: (v, n) for k, v, n in cur[p]}
            cells = []
            for k in plays:
                v, nn = d.get(k, (None, 0))
                cells.append("--" if v is None else f"{v:.2f} (n={nn})")
            lines.append(f"| {p:.1f} | " + " | ".join(cells) + " |")
        lines.append("")
    p = out / f"repeat-{tag}.md"
    p.write_text("\n".join(lines))
    return p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dir")
    ap.add_argument("--games", nargs="+", default=None)
    a = ap.parse_args()
    d = pathlib.Path(a.dir)
    rows = load(d)
    games = a.games or sorted({r["game"] for r in rows})
    outs = [render(rows, games, m, d, d.name) for m in ("light", "dark")]
    outs.append(table(rows, games, d, d.name))
    for p in outs:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
