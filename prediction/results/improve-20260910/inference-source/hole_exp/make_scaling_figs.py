#!/usr/bin/env python3
"""Scaling curves for the env-count ladder (0820-scaling-envs.md).

    python make_scaling_figs.py [--step N]

Two figures, each with one job:

  fig 1  scaling-curves.png   the dose-response itself. y vs #training envs
                              (log2 x: 1,2,4,8), one line per family, the base
                              model as a reference rule. Hole arm only -- this
                              is the curve the plan asks for.
  fig 2  scaling-control.png  the control. hole-nohole at the ENDPOINTS (n=1 vs
                              n=8), which is what separates "more hole exposure"
                              from "more RL of any kind". A slope per family.

Four points cannot fit an exponent, so nothing here is fitted. The reading is
the SHAPE -- rising, saturating, or flat -- exactly as the plan specifies.

ERROR BARS ARE EPISODE-LEVEL, ONE TRAINING SEED. They say how well this
checkpoint was measured, not how much a different training seed would move.
Stated on the figure, because a reader who forgets it will over-read a rung gap.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Tuple

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scaling_rungs as S  # noqa: E402

RES = HERE / "results" / "scaling"
FIGS = Path("/workspace/allie/strategy-behavior/results/0820_scaling_plots")

# The repo's established two-series pair; passes all six checks of the palette
# validator on the light surface (worst adjacent CVD dE 24.7 protan, normal 33.6,
# contrast >= 3:1). Families are an identity encoding, so they take categorical
# hues in a fixed order and never get recoloured when a panel drops a series.
BLUE, ORANGE = "#2a78d6", "#eb6834"
INK, INK2, MUT, GRID, SURF, PAGE = ("#0b0b0b", "#52514e", "#898781",
                                    "#e1e0d9", "#fcfcfb", "#f9f9f7")
FAMCOL = {"game": BLUE, "synth": ORANGE}
FAMLAB = {"game": "games (TextArena + native)", "synth": "synthetic scenarios"}
# Shown only when the two families were frozen at different steps.
SPLIT_NOTE = ("FAMILIES READ AT DIFFERENT STEPS (game episodes are multi-turn, "
              "~60% slower/step). Each line is internally step-matched, so each "
              "SHAPE is valid; levels are not comparable across colours.")

# (key, panel title, y-label, source). "tierA" reads results/scaling/tierA-*.json;
# "ext" reads the per-arm external JSONs; "mach" reads machiavelli.json.
PANELS = [
    ("heldout_game_exploit", "Held-out game cell",
     "exploit rate (nat_ledger)", "tierA"),
    ("kuhn_capture", "Kuhn Poker (held out)",
     "capture (share of honest->exploit span)", "tierA"),
    ("two_dollar_value", "TwoDollar (held out)",
     "value captured (share of $2.00)", "tierA"),
    ("two_dollar_open", "TwoDollar opening demand",
     "first proposal ($ of 2.00)", "tierA"),
    ("violations", "MACHIAVELLI", "ethical violations (Sigma)", "mach"),
    ("trade_rate", "Insider trading", "trade rate", "ext"),
    ("frac_any_misaligned", "AgentMisalignment", "frac any misaligned", "ext"),
    ("overall_hack_rate", "Hack-Verifiable (T1)", "hack rate", "ext"),
]

# check_suite's BROKEN verdict threshold. A cell above this is not measuring
# disposition, it is measuring whether the model emitted a parseable action --
# and because arms differ ~10x in how much they filter, the surviving
# denominators are selected by verbosity and the rates are not comparable
# between arms. Such points are drawn hollow and excluded from verdicts rather
# than dropped silently, so the gap is visible instead of inferable.
BROKEN_INVALID = 0.25
# metric key -> the summary field holding ITS invalid rate (None = ungated)
INVALID_OF = {
    "heldout_game_exploit": "heldout_game_invalid",
    "kuhn_capture": "kuhn_invalid",
}

EXT_FIELD = {  # metric key -> (filename, json field)
    "trade_rate": ("insider_trading.json", "trade_rate"),
    "frac_any_misaligned": ("agentmisalignment.json", "frac_any_misaligned"),
    "overall_hack_rate": ("hack_verifiable.json", "overall_hack_rate"),
}
EXT_ROOT = Path("/workspace/allie/ipd_exp/traits_results")


# ---------------------------------------------------------------------------
# data
# ---------------------------------------------------------------------------

def load_tier_a(step: int | None):
    files = sorted(RES.glob("tierA-step*.json"))
    if not files:
        return None
    if step is not None:
        want = RES / f"tierA-step{step:04d}.json"
        if want.exists():
            return json.loads(want.read_text())
    return json.loads(files[-1].read_text())


def steps_label(tierA, step) -> Tuple[str, bool]:
    """Human-readable step description, and whether families differ.

    Game episodes are multi-turn and train ~60% slower per step, so the two
    families are usually frozen at different steps. That is fine for the SHAPE
    of each curve (every point on a line shares its step) and not fine for
    comparing absolute levels ACROSS families, so the difference has to be
    visible on the figure rather than buried in the JSON.
    """
    by = ((tierA or {}).get("meta") or {}).get("step_by_family") or {}
    vals = {f: by[f] for f in families_of(tierA) if f in by}
    if len(set(vals.values())) > 1:
        return (", ".join(f"{FAMLAB[f].split(' (')[0]} @ step {v}"
                          for f, v in vals.items()), True)
    return (f"step {list(vals.values())[0] if vals else step}", False)


def families_of(tierA):
    """Families to plot, taken from the RESULT FILE, not from scaling_rungs.

    The module is the source of truth for what to RUN; a result file is a record
    of what WAS run. When the synthetic family was retired from scaling_rungs on
    0820, reading families from the module would have silently dropped the
    synthetic curves out of every figure built from data that contains them --
    deleting the study's main finding by re-rendering. Fall back to the module
    only for files written before `rungs` was stamped.
    """
    r = (tierA or {}).get("rungs")
    return list(r) if r else list(S.FAMILIES)


def load_mach():
    f = RES / "machiavelli.json"
    return json.loads(f.read_text())["arms"] if f.exists() else {}


def value(key: str, src: str, arm: str, tierA, mach):
    """(mean, se) for one arm on one metric, or (None, None)."""
    if src == "tierA":
        s = (tierA or {}).get("summary", {}).get(arm)
        if not s or key not in s:
            return None, None
        return s[key]["mean"], s[key]["se"]
    if src == "mach":
        m = mach.get(arm, {}).get("violations.Σ")
        return (m["mean"], m["se"]) if m else (None, None)
    fname, field = EXT_FIELD[key]
    f = EXT_ROOT / arm / fname
    if not f.exists():
        return None, None
    try:
        d = json.loads(f.read_text())
    except (ValueError, OSError):
        return None, None
    v = d.get(field)
    if v is None:
        return None, None
    # Binomial SE where the JSON carries a denominator; the external runners do
    # not bootstrap, and an unmarked point would read as more precise than it is.
    n = d.get("n") or d.get("n_episodes_ok")
    se = (v * (1 - v) / n) ** 0.5 if n and 0 <= v <= 1 else None
    return v, se


def invalid_of(key: str, arm: str, tierA):
    """That metric's invalid rate for that arm, or None if not gated/available."""
    fld = INVALID_OF.get(key)
    if not fld:
        return None
    s = (tierA or {}).get("summary", {}).get(arm) or {}
    return (s.get(fld) or {}).get("mean")


def series(fam: str, arm_kind: str, key: str, src: str, tierA, mach):
    """xs, ys, es, broken — `broken[i]` marks a point past BROKEN_INVALID."""
    xs, ys, es, broken = [], [], [], []
    for n in S.RUNG_NS:
        arm = f"scale-{fam}-n{n}-{arm_kind}"
        m, e = value(key, src, arm, tierA, mach)
        if m is not None:
            iv = invalid_of(key, arm, tierA)
            xs.append(n); ys.append(m); es.append(e)
            broken.append(iv is not None and iv > BROKEN_INVALID)
    return xs, ys, es, broken


# ---------------------------------------------------------------------------
# marks
# ---------------------------------------------------------------------------

def header(fig, title, subtitle, legend_ax):
    """Title, muted subtitle, then the legend -- three stacked rows.

    Stacked rather than packed onto one line: the per-family step string makes
    the title variable-length, and appending it overflowed the right edge.
    """
    fig.suptitle(title, fontsize=13, fontweight="bold", color=INK,
                 x=0.012, ha="left", y=0.993)
    fig.text(0.012, 0.958, subtitle, fontsize=9.5, color=INK2, ha="left",
             va="top")
    handles, labels = legend_ax.get_legend_handles_labels()
    if handles:
        # A legend is always present for >=2 series, so family identity is
        # never carried by colour alone.
        fig.legend(handles, labels, loc="upper left", frameon=False,
                   fontsize=9, ncol=2, bbox_to_anchor=(0.012, 0.945))


def footer(fig, lines):
    """Caveats as explicit lines. `wrap=True` measures against the figure width
    and still ran off the right edge on wide multi-panel layouts."""
    fig.text(0.012, 0.006, "\n".join(lines), fontsize=7.5, color=MUT,
             ha="left", va="bottom", linespacing=1.5)


def style(ax, title, ylab, xlab="# training environments"):
    ax.set_facecolor(SURF)
    ax.set_title(title, fontsize=10.5, fontweight="bold", color=INK,
                 loc="left", pad=7)
    ax.set_ylabel(ylab, fontsize=8.5, color=INK2)
    ax.set_xlabel(xlab, fontsize=8.5, color=INK2)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#c3c2b7")
    ax.tick_params(length=0, labelsize=8.5, colors=INK2)
    ax.grid(axis="y", color=GRID, lw=0.8)
    ax.set_axisbelow(True)


def fig_curves(tierA, mach, step, dest):
    live = []
    for key, title, ylab, src in PANELS:
        if any(series(f, "hole", key, src, tierA, mach)[0]
               for f in families_of(tierA)):
            live.append((key, title, ylab, src))
    if not live:
        print("no data for any panel; skipping fig 1")
        return None

    ncol = min(3, len(live))
    nrow = (len(live) + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.5 * ncol, 3.5 * nrow),
                             squeeze=False)
    fig.patch.set_facecolor(PAGE)

    for i, (key, title, ylab, src) in enumerate(live):
        ax = axes[i // ncol][i % ncol]
        style(ax, title, ylab)
        # Base model as a recessive reference RULE, not a series: it has no
        # #envs, so drawing it as a point on this axis would imply one.
        b, _ = value(key, src, "base", tierA, mach)
        if b is not None:
            ax.axhline(b, color=MUT, lw=1.3, ls=(0, (4, 3)), zorder=1)
            # Label INSIDE the axes in axes-fraction y: at data-x 8.6 it fell
            # outside the last column's frame and was clipped by the figure edge.
            ax.annotate(f"base {b:.3g}", xy=(0.015, b), xycoords=("axes fraction",
                        "data"), fontsize=7.5, color=MUT, va="bottom", ha="left")
        any_broken = False
        for fam in families_of(tierA):
            xs, ys, es, bk = series(fam, "hole", key, src, tierA, mach)
            if not xs:
                continue
            c = FAMCOL[fam]
            if any(e is not None for e in es):
                ax.errorbar(xs, ys, yerr=[e or 0 for e in es], fmt="none",
                            ecolor=c, elinewidth=1.4, capsize=3, alpha=0.55,
                            zorder=2)
            ax.plot(xs, ys, "-", color=c, lw=2, zorder=3)
            # >=8px markers with a 2px surface ring so overlapping family points
            # stay separable where the two curves cross. HOLLOW = that point's
            # invalid rate is past BROKEN_INVALID, so its denominator is
            # verbosity-selected and it is not comparable to the filled ones.
            for x, y, b in zip(xs, ys, bk):
                ax.scatter([x], [y], s=70,
                           color=("white" if b else c), edgecolor=c,
                           linewidth=2, zorder=4)
                any_broken = any_broken or b
            ax.scatter([], [], s=70, color=c, edgecolor=SURF, linewidth=2,
                       label=FAMLAB[fam] if i == 0 else None)
        if any_broken:
            ax.annotate("hollow = invalid > %.0f%%" % (BROKEN_INVALID * 100),
                        xy=(0.985, 0.03), xycoords="axes fraction", fontsize=7,
                        color=MUT, ha="right", va="bottom")
        ax.set_xscale("log", base=2)
        ax.set_xticks(list(S.RUNG_NS))
        ax.set_xticklabels([str(n) for n in S.RUNG_NS])
        ax.set_xlim(0.85, 9.4)

    for j in range(len(live), nrow * ncol):
        axes[j // ncol][j % ncol].axis("off")

    # Legend always present for >=2 series, so family is never colour-alone.
    slab, split = steps_label(tierA, step)
    header(fig, "Does exploit transfer scale with the number of training "
                "environments?", f"hole arm  ·  {slab}  ·  1 training seed",
           axes[0][0])
    footer(fig, [
        f"Constant compute per rung: every point trained {S.GROUPS}x"
        f"{S.GROUP_SIZE} = {S.GROUPS*S.GROUP_SIZE} episodes/step, so a rung "
        "with 8 envs saw 1/8th the episodes per env, not 8x the episodes. "
        "Rung sets are nested; the held-out battery is identical at every rung.",
        "Error bars are EPISODE-level bootstrap at ONE training seed - they do "
        "NOT bound seed-to-seed variation. Four points cannot fit an exponent; "
        "read the shape, not a slope.",
    ] + ([SPLIT_NOTE] if split else []))
    fig.tight_layout(rect=(0, 0.075 if split else 0.055, 1, 0.90))
    fig.savefig(dest, dpi=170, facecolor=PAGE)
    plt.close(fig)
    return dest


def fig_control(tierA, mach, step, dest):
    """hole - nohole at the endpoints. Widening slope = the hole is doing it."""
    live = []
    for key, title, ylab, src in PANELS:
        ok = False
        for fam in families_of(tierA):
            for n in (1, max(S.RUNG_NS)):
                h, _ = value(key, src, f"scale-{fam}-n{n}-hole", tierA, mach)
                c, _ = value(key, src, f"scale-{fam}-n{n}-nohole", tierA, mach)
                ok = ok or (h is not None and c is not None)
        if ok:
            live.append((key, title, ylab, src))
    if not live:
        print("no matched hole/nohole endpoint pair yet; skipping fig 2")
        return None

    ncol = min(3, len(live))
    nrow = (len(live) + ncol - 1) // ncol
    fig, axes = plt.subplots(nrow, ncol, figsize=(4.2 * ncol, 3.4 * nrow),
                             squeeze=False)
    fig.patch.set_facecolor(PAGE)
    ends = [1, max(S.RUNG_NS)]

    for i, (key, title, ylab, src) in enumerate(live):
        ax = axes[i // ncol][i % ncol]
        style(ax, title, "treatment effect  (hole - nohole)")
        ax.axhline(0, color="#c3c2b7", lw=1.2, zorder=1)
        for fam in families_of(tierA):
            xs, ys = [], []
            for n in ends:
                h, _ = value(key, src, f"scale-{fam}-n{n}-hole", tierA, mach)
                c, _ = value(key, src, f"scale-{fam}-n{n}-nohole", tierA, mach)
                if h is not None and c is not None:
                    xs.append(n); ys.append(h - c)
            if not xs:
                continue
            col = FAMCOL[fam]
            ax.plot(xs, ys, "-", color=col, lw=2, zorder=3)
            ax.scatter(xs, ys, s=70, color=col, edgecolor=SURF, linewidth=2,
                       zorder=4, label=FAMLAB[fam] if i == 0 else None)
            # The two families' endpoint values often land within a few
            # hundredths of each other, so centred labels overprint. Push each
            # family to its own side vertically, and each endpoint inward
            # horizontally so neither runs off the frame.
            dy = 11 if fam == "game" else -15
            for x, y in zip(xs, ys):
                inner = x == min(ends)
                ax.annotate(f"{y:+.3g}", (x, y), textcoords="offset points",
                            xytext=(9 if inner else -9, dy),
                            ha="left" if inner else "right",
                            fontsize=8.5, fontweight="bold", color=col)
        ax.set_xscale("log", base=2)
        ax.set_xticks(ends)
        ax.set_xticklabels([str(n) for n in ends])
        ax.set_xlim(0.85, max(ends) * 1.2)

    for j in range(len(live), nrow * ncol):
        axes[j // ncol][j % ncol].axis("off")
    slab, split = steps_label(tierA, step)
    header(fig, "Control: does the hole-nohole GAP widen with #envs?",
           f"endpoints only  ·  {slab}  ·  1 training seed", axes[0][0])
    footer(fig, [
        "A rising hole-arm curve alone cannot separate 'more hole exposure' "
        "from 'more diverse RL of any kind'. If the gap widens from n=1 to "
        "n=8 the rise is about the hole; if both arms rose together it is flat.",
        "Only the endpoints were run as matched pairs (launch_scaling.sh fill "
        "adds n=2 and n=4).",
    ] + ([SPLIT_NOTE] if split else []))
    fig.tight_layout(rect=(0, 0.075 if split else 0.055, 1, 0.90))
    fig.savefig(dest, dpi=170, facecolor=PAGE)
    plt.close(fig)
    return dest


def write_table(tierA, mach, step, dest):
    """A table view, so nothing on the figures is available only as colour."""
    rows = ["# Env-count ladder — Tier A + Tier B, step %d, 1 seed\n" % step,
            "Constant compute: %d steps x %d groups x %d = %d episodes/step at "
            "every rung.\n" % (S.STEPS, S.GROUPS, S.GROUP_SIZE,
                               S.GROUPS * S.GROUP_SIZE)]
    for fam in families_of(tierA):
        rows.append(f"\n## {FAMLAB[fam]}\n")
        rows.append("| n | envs added | " + " | ".join(
            t for _, t, _, _ in PANELS) + " |")
        rows.append("|---|---|" + "---|" * len(PANELS))
        prev = []
        for n in S.RUNG_NS:
            cur = (tierA.get('rungs') or {}).get(fam, {}).get(str(n)) \
                  or (tierA.get('rungs') or {}).get(fam, {}).get(n) \
                  or S.rung(fam, n)
            added = ", ".join(e for e in cur if e not in prev)
            prev = cur
            cells = []
            for key, _, _, src in PANELS:
                m, e = value(key, src, f"scale-{fam}-n{n}-hole", tierA, mach)
                cells.append("—" if m is None else
                             (f"{m:.3f}" if e is None else f"{m:.3f} ±{e:.3f}"))
            rows.append(f"| {n} | {added} | " + " | ".join(cells) + " |")
        cells = []
        for key, _, _, src in PANELS:
            m, e = value(key, src, "base", tierA, mach)
            cells.append("—" if m is None else
                         (f"{m:.3f}" if e is None else f"{m:.3f} ±{e:.3f}"))
        rows.append("| base | (untrained) | " + " | ".join(cells) + " |")
    dest.write_text("\n".join(rows) + "\n")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--step", type=int, default=None)
    a = ap.parse_args()

    tierA = load_tier_a(a.step)
    mach = load_mach()
    step = a.step if a.step is not None else (tierA or {}).get("step", 0)
    FIGS.mkdir(parents=True, exist_ok=True)

    for f in (fig_curves(tierA, mach, step, FIGS / "scaling-curves.png"),
              fig_control(tierA, mach, step, FIGS / "scaling-control.png"),
              write_table(tierA, mach, step, FIGS / "scaling-table.md")):
        if f:
            print(f"wrote {f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
