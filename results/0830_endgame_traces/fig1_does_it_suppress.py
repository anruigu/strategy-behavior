#!/usr/bin/env python
"""Does the endgame penalty suppress endgame REASONING? Both opponents, 3 seeds.

    /home/allie/venvs/tinker-ipd/bin/python fig1_does_it_suppress.py

  fig1_does_it_suppress.png      the figure
  fig1_does_it_suppress.json     every number drawn in it

WHAT THIS ASKS. An endgame-penalty reward knob measurably reduces late-game
betrayal BEHAVIOUR (training logs, 3 seeds: -0.039 +/- 0.012 vs grim,
-0.142 +/- 0.064 vs tft). This figure asks the separate question of whether
the CHAIN OF THOUGHT moved with it, scored off raw CoT text.

WHAT CHANGED SINCE THE LAST RENDER. The dataset roughly doubled -- 624
episodes / 12,480 blocks / 13 cells, against 384 / 7,680 / 8 -- and `tft` now
has three seeds in BOTH arms, so a second contrast exists that did not before.
The previous version of this figure plotted grim alone and concluded a flat
"no". That answer does not survive the tft data. The answer is now opponent-
dependent, and the interesting part is what happens to the tft effect when it
is taken apart.

THE SHAPE OF THE FINDING, IN THE ORDER THE PANELS MAKE IT.

  1. Against tft the raw marker rates really do drop, hard and consistently:
     `endgame_defect_plan` raw delta -0.288, and all three seeds agree in sign.
     Against grim nothing does: -0.083 with per-seed deltas that flip sign.

  2. But most of the tft drop is VERBOSITY, not topic. The penalty shortens
     the reasoning against tft by ~35% (arm means 1367 chars nohole against
     885 eg), while against grim the two arms write the same amount (1072 vs
     1053) -- which is also why grim has no raw effect to explain. A marker
     hit is BINARY PER BLOCK, so a shorter block mechanically hits less
     often, whatever it is about. Standardising to the global length
     quintiles shrinks tft's -0.288 to -0.065.

  3. And the residual is NOT ENDGAME-SPECIFIC. `in_game_penalty` is the
     FLOOR/CONTROL marker: generic punishment vocabulary, no stake in whether
     the model is reasoning about the LAST round. Stratified it falls -0.059
     against tft, statistically indistinguishable from the endgame marker's
     -0.065. The control falls as much as the signal. Row 2 of each band
     draws the control's interval as a horizontal band across the panel so
     this is a matter of looking rather than of arithmetic.

So: against tit-for-tat the penalty visibly cuts endgame talk, but the cut is
mostly "thinks less overall" rather than "thinks less about the endgame"; and
against grim nothing is detectable at all. Neither of those is a proof of
absence -- the grim intervals in particular are far too wide to support an
equivalence claim, and the footer says so.

THE COMPROMISED CELL, DISCLOSED BECAUSE IT PRODUCES A HEADLINE SIGN.
`grim/nohole` train_seed 1 is degenerate: ~60% of its decision turns emit an
empty answer, it is the shortest cell on disk by a wide margin, and its
episode-level `invalid_rate` reads 0.000 -- so the repo's usual
`invalid_rate > 0.15` gate does NOT catch it. The grim RAW deltas are robust
to it; the grim STRATIFIED deltas are not, and flip positive on all four
markers when it is dropped. That sensitivity is drawn, not just described.
The same screen run over every cell also flags `tft/nohole` seed 0 (~28%
empty); dropping it makes the tft effect LARGER, not smaller, so the tft
result is robust to its own worst cell in the direction that matters.

`tft/inf` exists now but at ONE seed. It is drawn as an explicitly marked
open point and never enters a contrast; a one-seed cell has no between-run
error bar and nothing legitimate to subtract.

LAYOUT CONVENTION. From `results/0826_think_curves/plot_reasoning_markers_by_
opponent.py`: OPPONENT IS CARRIED BY BLOCK POSITION, one band per opponent,
never by hue, so the condition colours keep meaning exactly what they mean
everywhere else in the repo. Same panel position holds the same quantity on a
shared y-axis across both bands, so a vertical difference between bands is the
effect of forgiveness and nothing else.

PALETTE. Fixed by CONDITION and never repainted: baseline purple, endgame
penalty orange, hidden horizon blue (reserved -- blue is never used for
anything that is not the inf arm). Contrast markers are neutral ink: a
difference is not a condition and must not borrow a condition's hue.

EVERY NUMBER IS COMPUTED AT RENDER TIME from trace_markers.json and
trace_blocks.jsonl. Nothing here is a cached string.
"""
from __future__ import annotations

import argparse
import json
import textwrap
from collections import defaultdict
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

HERE = Path(__file__).resolve().parent

PURPLE, ORANGE, BLUE = "#7a5bd6", "#eb6834", "#2a78d6"
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
PAPER = "#f9f9f7"

# (opponent key, band heading). Opponent is BLOCK POSITION, never hue.
BANDS = [("grim", "vs GRIM  -  never forgives"),
         ("tft", "vs TIT-FOR-TAT  -  forgives on return")]

# (condition suffix, x position, tick label, colour, enters_contrast)
ARMS = [("nohole", 0.0, "baseline\n(nohole)", PURPLE, True),
        ("eg", 1.0, "endgame\npenalty (eg)", ORANGE, True),
        ("inf", 2.15, "hidden horizon\n(inf)", BLUE, False)]

# (marker key, panel letter, plain-words label, panel note, is_floor)
MARKERS = [
    ("endgame_defect_plan", "A", "plans to betray at the end",
     "the headline marker: endgame reasoning that\nRESOLVES to defecting",
     False),
    ("endgame_hold", "B", "plans to HOLD at the end",
     "the other direction of A. a suppression story\nneeds this to move the opposite way",
     False),
    ("backward_induction", "C", "backward induction",
     "\"the last round has no future to punish me\",\ndirection-agnostic",
     False),
    ("in_game_penalty", "D", "punishment vocabulary  (FLOOR / CONTROL)",
     "generic punishment talk, NO stake in the endgame.\n"
     "if it moves like A-C, the movement is not endgame-specific",
     True),
]
MARKER_KEYS = [m for m, *_ in MARKERS]
FLOOR = "in_game_penalty"

# per-seed glyphs, so a seed is identifiable without relying on position alone
SEED_MK = ["o", "s", "^", "D", "v", "P"]


def wrap(text, width):
    """`fig.text` does not wrap and an over-long line runs off the paper.

    Explicit newlines in the source string are paragraph breaks and survive;
    everything else is refilled to `width`. Widths are set from the figure
    width and the point size rather than guessed per string, so editing a
    footer sentence cannot silently push it off the right edge again.
    """
    return "\n".join(
        "\n".join(textwrap.wrap(seg, width)) if seg.strip() else seg
        for seg in text.split("\n"))


def nlines(text):
    return text.count("\n") + 1


def mean(v):
    v = [x for x in v if x is not None]
    return float(np.mean(v)) if v else None


def se(v):
    """Between-training-seed SE: sd(paired per-seed values)/sqrt(n). Undefined
    at n=1, which is the point -- a one-seed cell carries no between-run bar."""
    v = [x for x in v if x is not None]
    if len(v) < 2:
        return None
    return float(np.std(v, ddof=1) / np.sqrt(len(v)))


def style(ax, title, ylab, note=None):
    ax.set_title(title, fontsize=10.5, color=INK, loc="left", pad=8)
    ax.set_ylabel(ylab, fontsize=9, color=INK2)
    ax.set_facecolor(SURF)
    ax.grid(True, axis="y", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUT, labelsize=8, length=0)
    if note:
        ax.text(0.02, 0.975, note, transform=ax.transAxes, fontsize=7,
                color=MUT, va="top")


def empty(ax, msg):
    """Degrade loudly: a panel with no data says so rather than lying flat."""
    ax.text(0.5, 0.5, msg, transform=ax.transAxes, fontsize=9, color=MUT,
            ha="center", va="center")
    ax.set_xticks([])
    ax.set_yticks([])


# ------------------------------------------------------------ block reading --

def read_blocks(path, edges, n_bins):
    """One pass over the block-level JSONL.

    Needed for three things the aggregate JSON cannot give: the p90 reasoning
    length per cell (the length hazard is a TAIL property -- a degenerate cell
    is one that never writes long, and a mean hides that), the pooled
    marker-rate-by-length-quintile curve that justifies stratifying at all,
    and the leave-one-seed-out stratified deltas.
    """
    by_cell, chars, pooled = defaultdict(list), defaultdict(list), \
        [[] for _ in range(n_bins)]
    with path.open() as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line)
            n = int(r["n_chars"])
            b = (min(int(np.searchsorted(edges, n, side="right")), n_bins - 1)
                 if edges else 0)
            hits = {m: int(r[f"m_{m}"]) for m in MARKER_KEYS}
            by_cell[(r["arm"], str(r["train_seed"]))].append((b, hits))
            chars[(r["arm"], str(r["train_seed"]))].append(n)
            pooled[b].append(hits)
    return by_cell, chars, pooled


def strat_deltas(by_cell, weights, opp, seeds, n_bins, min_bin):
    """(eg - nohole) direct-standardised to the GLOBAL length distribution.

    The bin edges and the standard population are held FIXED at the full-data
    values even when a seed is dropped, so the leave-one-out estimate differs
    from the headline one only by which seeds are averaged -- not by which
    population they were reweighted onto. This reproduces score_traces.py
    exactly on the full seed set (verified: identical to per_seed_strat).
    """
    eg, nh = f"{opp}/eg", f"{opp}/nohole"
    out = {m: [] for m in MARKER_KEYS}
    dropped = []
    for ts in seeds:
        idx = {}
        for arm in (eg, nh):
            g = [[] for _ in range(n_bins)]
            for b, hits in by_cell.get((arm, ts), []):
                g[b].append(hits)
            idx[arm] = g
        use = [b for b in range(n_bins)
               if all(len(idx[a][b]) >= min_bin for a in (eg, nh))]
        if not use:
            dropped.append(ts)
            for m in MARKER_KEYS:
                out[m].append(None)
            continue
        w = weights[use] / weights[use].sum()
        for m in MARKER_KEYS:
            d = [float(np.mean([h[m] for h in idx[eg][b]]))
                 - float(np.mean([h[m] for h in idx[nh][b]])) for b in use]
            out[m].append(float(np.dot(w, d)))
    return out, dropped


# ------------------------------------------------------------- hazard screen --

def hazard_scan(cells, chars, thresh):
    """Screen EVERY cell for the failure mode the invalid_rate gate misses.

    `grim/nohole|1` passes `invalid_rate <= 0.15` with a reading of exactly
    0.000 while ~60% of its decision turns emit no parseable answer at all.
    The two are different quantities: invalid_rate counts actions the env had
    to substitute, n_empty_answer counts turns that produced no answer text.
    A cell can be degenerate on the second and clean on the first, so the
    screen has to look at the second.
    """
    rows = {}
    for key, c in cells.items():
        arm, ts = key.split("|")
        ch = chars.get((arm, ts)) or []
        rows[key] = {
            "arm": arm, "train_seed": ts,
            "n_episodes": c["n_episodes"], "n_blocks": c["n_blocks"],
            "empty_answer_rate": c.get("n_empty_answer_rate"),
            "invalid_rate": c.get("invalid_rate"),
            "mean_chars": c.get("mean_chars"),
            "median_chars": c.get("median_chars"),
            "p90_chars": float(np.percentile(ch, 90)) if ch else None,
            "endgame_rate": c.get("endgame_rate"),
        }
    flagged = sorted(
        [k for k, r in rows.items()
         if (r["empty_answer_rate"] or 0.0) > thresh],
        key=lambda k: -(rows[k]["empty_answer_rate"] or 0.0))
    return rows, flagged


# --------------------------------------------------------------------------
# BAND ROW 1. Per-arm LEVEL, every training seed drawn, matched seeds joined.
# --------------------------------------------------------------------------

def arm_panel(ax, opp, arms, mk, ylim, flagged_cells, record, key_note=False):
    """Two contrast arms side by side, plus the single-seed inf arm held out.

    Each seed is its own point; matched seeds are joined so the reader can see
    whether the lines run parallel (a stable arm gap) or cross (an arm gap
    smaller than the seed-to-seed spread that produced it).
    """
    present = [a for a in ARMS if f"{opp}/{a[0]}" in arms
               and mk in arms[f"{opp}/{a[0]}"]["markers"]]
    contrast_arms = [a for a in present if a[4]]
    if len(contrast_arms) < 2:
        empty(ax, f"no paired data for {mk}\n(needs both {opp} contrast arms)")
        return

    series = {}
    for key, x, _, col, _ in present:
        st = arms[f"{opp}/{key}"]["markers"][mk]
        series[key] = (x, col, st["per_seed"], st["mean"], st["se"],
                       arms[f"{opp}/{key}"]["train_seeds"])

    xa, _, ya, _, _, sa = series[contrast_arms[0][0]]
    xb, _, yb, _, _, sb = series[contrast_arms[1][0]]

    # Join only seeds present in BOTH arms: the contrast is paired within a
    # training seed, so an unmatched seed has nothing legitimate to join to.
    shared = [s for s in sa if s in sb]
    tags = []
    for s in shared:
        p, q = ya[sa.index(s)], yb[sb.index(s)]
        ax.plot([xa, xb], [p, q], color=MUT, lw=1.0, alpha=0.75, zorder=2)
        tags.append([p, f"seed {s}"])
    # The seed tag is the only thing carrying WHICH line is which, so two
    # seeds landing within a few thousandths must not stack their labels.
    tags.sort()
    gap = ylim * 0.052
    # floor the lowest tag clear of the delta readout in the bottom-left
    # corner: on the shared y-axis the low-rate markers put all three seeds
    # into the bottom tenth of the panel
    if tags:
        tags[0][0] = max(tags[0][0], ylim * 0.095)
    for i in range(1, len(tags)):
        tags[i][0] = max(tags[i][0], tags[i - 1][0] + gap)
    for y, lab in tags:
        ax.annotate(lab, (xa, y), textcoords="offset points", xytext=(-9, 0),
                    ha="right", va="center", fontsize=7, color=MUT,
                    annotation_clip=False)

    for key, x, _, col, in_con in present:
        _, _, ys, m_, s_, seeds = series[key]
        if not in_con:
            # A single-seed arm gets exactly ONE glyph, open, and no bar:
            # there is no between-run spread to draw, and a filled point next
            # to a bar-less arm mean would read as a measured arm.
            ax.plot([x], [m_], marker="D", ms=8.5, mfc=SURF, mec=col, mew=2.2,
                    ls="none", zorder=5)
            record[key] = {"per_seed": ys, "train_seeds": seeds, "mean": m_,
                           "between_seed_se_on_LEVEL": None,
                           "enters_contrast": False}
            continue
        for i, (s, y) in enumerate(zip(seeds, ys)):
            hazard = f"{opp}/{key}|{s}" in flagged_cells
            ax.plot([x], [y], marker=SEED_MK[i % len(SEED_MK)], ms=6.5,
                    # a flagged cell is drawn HOLLOW: it is on the figure, it
                    # is not silently pooled into the reader's impression
                    mfc=SURF if hazard else col,
                    mec=col, mew=2.2 if hazard else 1.2, ls="none", zorder=4)
            if hazard:
                ax.annotate("!", (x, y), textcoords="offset points",
                            xytext=(7, 4), fontsize=9, color=ORANGE,
                            fontweight="bold", annotation_clip=False)
        if s_ is not None:
            ax.errorbar([x + 0.34], [m_], yerr=[s_], color=col, lw=0,
                        elinewidth=2.0, capsize=5, capthick=2.0, marker="_",
                        ms=17, mew=2.6, zorder=5)
        record[key] = {"per_seed": ys, "train_seeds": seeds, "mean": m_,
                       "between_seed_se_on_LEVEL": s_,
                       "enters_contrast": True}

    if key_note:
        # Defect 3: row 1's offset bars are on LEVELS, not on differences, and
        # the footer only ever explained the bars on DIFFERENCES. Anchored to
        # the eg bar and thrown down-right, into the slot the inf arm would
        # occupy -- the only region of this panel that is empty for grim. Up
        # and to the right it collided with the panel note.
        ax.annotate("this bar = between-seed SE\non THIS ARM'S LEVEL,\n"
                    "not on any difference",
                    (series[contrast_arms[1][0]][0] + 0.34,
                     series[contrast_arms[1][0]][3]),
                    textcoords="offset points", xytext=(28, 58), fontsize=6.6,
                    color=INK2, va="bottom", ha="left", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color=MUT, lw=0.8,
                                    shrinkB=4))

    ax.axhline(0, color=GRID, lw=0.8, zorder=1)
    ax.set_xlim(-0.68, 2.62)
    ax.set_ylim(0, ylim)
    ticks = [a[1] for a in present]
    labs = [a[2] for a in present]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labs, fontsize=8.5, color=INK2)
    for t, a in zip(ax.get_xticklabels(), present):
        if not a[4]:
            t.set_color(a[3])
            t.set_fontsize(7.6)
    if any(not a[4] for a in present):
        ax.text(2.15, -ylim * 0.155, "1 SEED - NOT A CONTRAST", fontsize=6.6,
                color=BLUE, ha="center", va="top", fontweight="bold",
                clip_on=False)
    ax.tick_params(axis="x", pad=4)


# --------------------------------------------------------------------------
# BAND ROW 2. The contrast, drawn TWICE side by side: raw on the left,
# length-stratified on the right, each on its own y-scale.
#
# One combined panel was the previous design and it does not work now. The
# per-seed RAW deltas against tft run to -0.41 while every stratified
# estimate and the whole FLOOR/CONTROL interval live inside +/-0.11, so on a
# single shared axis the stratified half of the figure collapses into a few
# pixels -- and "the control falls as much as the signal" is exactly a
# comparison between two of those squashed points. Splitting buys the
# stratified panel ~4x of vertical scale. The cost is that raw-vs-stratified
# becomes a comparison across two panels rather than within one group, which
# is paid back by printing BOTH numbers in BOTH panels' per-group blocks and
# by stating the scale ratio in the right-hand panel's title.
# --------------------------------------------------------------------------

DX_SEED, DX_EST, DX_FLR, DX_SNS = -0.26, 0.0, 0.22, 0.44

KINDS = {
    "raw": ("RAW", INK, "o", dict(mec=SURF, mew=1.2, ms=8)),
    "strat": ("LENGTH-STRATIFIED", INK2, "s",
              dict(mfc=SURF, mec=INK2, mew=2.0, ms=7.5)),
}


def contrast_panel(ax, opp, con, sens, kind, ylim, record):
    """One estimator, four markers, per-seed points, floor bar, sensitivity."""
    have = [(k, lab, is_fl) for k, _, lab, _, is_fl in MARKERS if k in con]
    if not have:
        empty(ax, f"no contrast for {opp}: trace_markers.json has no "
                  f"contrasts.{opp}")
        return []
    _, col, mk_sym, mk_kw = KINDS[kind]
    seed_key = "per_seed_delta" if kind == "raw" else "per_seed_strat"

    # The FLOOR/CONTROL's own interval, on THIS estimator, extended across the
    # whole panel: an endgame marker landing inside it did not move any
    # differently from generic punishment vocabulary. Drawn rather than
    # arithmetic, because it is now a central claim.
    fl = con.get(FLOOR)
    fl_m, fl_s = (fl[f"{kind}_delta_mean"], fl[f"{kind}_delta_se"]) if fl \
        else (None, None)
    if fl_s is not None:
        ax.axhspan(fl_m - fl_s, fl_m + fl_s, color=MUT, alpha=0.15, lw=0,
                   zorder=0.5)
        ax.axhline(fl_m, color=MUT, lw=1.0, ls=(0, (5, 3)), zorder=0.6)

    # a faint column behind the floor group, so it reads as the reference
    for gi, (_, _, is_fl) in enumerate(have):
        if is_fl:
            ax.axvspan(gi - 0.52, gi + 0.62, color=MUT, alpha=0.07, lw=0,
                       zorder=0.4)

    for gi, (mk, _, _) in enumerate(have):
        c = con[mk]
        est, ese = c[f"{kind}_delta_mean"], c[f"{kind}_delta_se"]
        bse = c["binomial_se_pooled"]

        # the per-seed deltas behind the estimate: the evidence for or against
        # the sign being stable, which for grim it is not
        for i, v in enumerate(c[seed_key]):
            if v is None:
                continue
            ax.plot([gi + DX_SEED], [v], marker=SEED_MK[i % len(SEED_MK)],
                    ms=4.6, color=MUT, alpha=0.75, mec=SURF, mew=0.7,
                    ls="none", zorder=3,
                    label=("the per-seed deltas behind it"
                           if gi == 0 and i == 0 else None))

        ax.errorbar([gi + DX_EST], [est], yerr=[ese], color=col, lw=0,
                    elinewidth=2.2, capsize=6, capthick=2.2, marker=mk_sym,
                    zorder=5, **mk_kw,
                    label=(f"{KINDS[kind][0]} delta +/- between-seed SE"
                           if gi == 0 else None))
        # centred on the estimate, so the only thing differing between it and
        # the bar to its left is the WHISKER LENGTH
        ax.errorbar([gi + DX_FLR], [est], yerr=[bse], color=MUT, lw=0,
                    elinewidth=1.6, capsize=4, capthick=1.6, marker="x",
                    ms=5, mew=1.4, zorder=5,
                    label="pooled BINOMIAL SE = sampling floor, NOT an "
                          "interval on the effect" if gi == 0 else None)

        s = (sens or {}).get(mk)
        sv = s.get(f"{kind}_delta_mean") if s else None
        if sv is not None:
            ax.plot([gi + DX_EST, gi + DX_SNS], [est, sv], color=ORANGE,
                    lw=0.9, ls=":", zorder=4)
            ax.plot([gi + DX_SNS], [sv], marker="P", ms=9, mfc=PAPER,
                    mec=ORANGE, mew=2.0, ls="none", zorder=6,
                    label=(f"SENSITIVITY: flagged cell dropped "
                           f"({s['n_seeds']} seeds, too few for an SE)")
                          if gi == 0 else None)

        rec = record.setdefault(mk, {
            "binomial_se_pooled": bse,
            "n_seeds": c["n_seeds"], "train_seeds": c["train_seeds"],
            "all_per_seed_raw_deltas_agree_in_sign":
                bool(len({v > 0 for v in c["per_seed_delta"]}) == 1),
        })
        rec[f"{kind}_delta_mean"] = est
        rec[f"{kind}_delta_se_between_seed"] = ese
        rec[f"{kind}_delta_sd"] = c[f"{kind}_delta_sd"]
        rec[f"per_seed_{kind}"] = c[seed_key]
        rec[f"ratio_{kind}_se_over_binomial_se"] = (ese / bse) if bse else None
        rec[f"{kind}_interval_crosses_zero"] = (
            bool((est - ese) <= 0 <= (est + ese)) if ese is not None else None)
        if sv is not None:
            rec[f"{kind}_delta_drop_flagged_cell"] = sv
            rec[f"{kind}_drop_flagged_n_seeds"] = s["n_seeds"]
            rec[f"{kind}_drop_flagged_sign_flip"] = bool((sv > 0) != (est > 0))

    ax.set_ylim(ylim)
    ax.set_xlim(-0.72, len(have) - 0.26)
    ax.axhline(0, color=INK, lw=1.5, zorder=2)
    ax.annotate("no effect", (ax.get_xlim()[0], 0), textcoords="offset points",
                xytext=(4, 3), fontsize=7.5, color=INK, va="bottom")
    # No in-panel label on the band: the legend carries its identity AND its
    # value, and at the right edge the label sat on the last group's number
    # block while at the left it sat on the zero line's own label.
    ax.set_xticks(range(len(have)))
    ax.set_xticklabels(
        [lab.replace("  (FLOOR / CONTROL)", "\n(FLOOR / CONTROL)")
         for _, lab, _ in have], fontsize=8.6, color=INK2)

    # Both estimators are printed in BOTH panels: the split costs the reader
    # the within-group raw-vs-stratified comparison, and this gives it back.
    y0, y1 = ax.get_ylim()
    for gi, (mk, _, _) in enumerate(have):
        c = con[mk]
        s = (sens or {}).get(mk)
        rows = [f"raw    {c['raw_delta_mean']:+.3f} +/- {c['raw_delta_se']:.3f}",
                f"strat  {c['strat_delta_mean']:+.3f} +/- "
                f"{c['strat_delta_se']:.3f}",
                f"floor  +/- {c['binomial_se_pooled']:.3f}"]
        if s and s.get(f"{kind}_delta_mean") is not None:
            rows.append(f"drop   {s[f'{kind}_delta_mean']:+.3f}  "
                        f"(n={s['n_seeds']})")
        # bold the estimator this panel is actually drawing
        ax.text(gi + 0.05, y1 - (y1 - y0) * 0.025, "\n".join(rows),
                fontsize=7.0, color=INK2, ha="center", va="top",
                family="monospace", linespacing=1.35)

    h, l = ax.get_legend_handles_labels()
    if fl_s is not None:
        h.append(Patch(facecolor=MUT, alpha=0.15, edgecolor=MUT, ls="--"))
        l.append(f"shaded band: FLOOR/CONTROL's own interval here, "
                 f"{fl_m:+.3f} +/- {fl_s:.3f}")
    # two columns and short labels: at one column the key was tall enough to
    # reach the lowest per-seed glyph in the leftmost group
    leg = ax.legend(h, l, loc="lower left", frameon=False, fontsize=7.4,
                    ncol=2, handletextpad=0.6, labelspacing=0.45,
                    columnspacing=1.6)
    for t in leg.get_texts():
        t.set_color(INK2)
    return [(mk, record[mk]) for mk, _, _ in have]


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", default=str(HERE / "trace_markers.json"),
                    help="aggregate marker JSON from score_traces.py")
    ap.add_argument("--blocks", default=str(HERE / "trace_blocks.jsonl"),
                    help="block-level JSONL; needed for p90 lengths, the "
                         "quintile curve and the leave-one-seed-out estimates")
    ap.add_argument("--outdir", default=str(HERE))
    ap.add_argument("--empty-answer-flag", type=float, default=0.25,
                    help="flag any cell whose share of decision turns with an "
                         "empty answer exceeds this. The repo's invalid_rate "
                         "gate does not catch this failure mode.")
    a = ap.parse_args()          # --help exits here, before anything renders

    src, blk_path = Path(a.src), Path(a.blocks)
    outdir = Path(a.outdir)
    if not src.exists():
        print(f"[fig] missing {src}")
        return 1
    D = json.loads(src.read_text())
    meta, cov, cells = D["meta"], D["coverage"], D["cells"]
    arms, con_all = D["arms"], D["contrasts"]

    lb = meta.get("length_bins") or {}
    edges = lb.get("edges") or []
    n_bins = lb.get("n_bins") or 5
    min_bin = lb.get("min_blocks_per_cell") or 15
    weights = np.array(lb.get("global_counts") or [1.0] * n_bins, dtype=float)


    by_cell, chars, pooled = ({}, {}, [])
    if blk_path.exists():
        by_cell, chars, pooled = read_blocks(blk_path, edges, n_bins)
    else:
        print(f"[fig] ** {blk_path} missing: no p90 lengths, no quintile "
              f"curve, NO leave-one-out sensitivity. **")

    haz, flagged = hazard_scan(cells, chars, a.empty_answer_flag)
    flagged_set = set(flagged)
    for k in flagged:
        r = haz[k]
        print(f"[fig] HAZARD {k}: empty_answer {r['empty_answer_rate']:.3f}, "
              f"invalid_rate {r['invalid_rate']:.3f} (gate does not catch it), "
              f"mean {r['mean_chars']:.0f} / p90 "
              f"{(r['p90_chars'] or float('nan')):.0f} chars, endgame_rate "
              f"{r['endgame_rate']:.3f}")

    # Leave-one-out: for each opponent, drop its flagged BASELINE cell and
    # recompute. The global bins and standard population stay fixed, so the
    # only difference is which seeds are averaged.
    sens_all, sens_meta = {}, {}
    for opp, _ in BANDS:
        if opp not in con_all or not by_cell:
            continue
        seeds = [str(s) for s in con_all[opp]["endgame_defect_plan"]["train_seeds"]]
        drop = [s for s in seeds if f"{opp}/nohole|{s}" in flagged_set
                or f"{opp}/eg|{s}" in flagged_set]
        keep = [s for s in seeds if s not in drop]
        if not drop or len(keep) < 2:
            sens_meta[opp] = {"dropped_seeds": drop, "kept_seeds": keep,
                              "computed": False,
                              "why": "no flagged cell in this contrast"
                                     if not drop else
                                     "fewer than 2 seeds would remain"}
            continue
        st, _ = strat_deltas(by_cell, weights, opp, keep, n_bins, min_bin)
        full = {m: con_all[opp][m] for m in MARKER_KEYS}
        sens_all[opp] = {}
        for m in MARKER_KEYS:
            raw_k = [cells[f"{opp}/eg|{t}"]["markers"][m]
                     - cells[f"{opp}/nohole|{t}"]["markers"][m] for t in keep]
            sens_all[opp][m] = {
                "strat_delta_mean": mean(st[m]),
                "strat_delta_se_between_seed": se(st[m]),
                "per_seed_strat": st[m],
                "raw_delta_mean": mean(raw_k),
                "raw_delta_se_between_seed": se(raw_k),
                "per_seed_delta": raw_k,
                "n_seeds": len(keep), "train_seeds": keep,
                "shift_vs_full_strat":
                    mean(st[m]) - full[m]["strat_delta_mean"],
                "sign_flips":
                    bool((mean(st[m]) > 0) != (full[m]["strat_delta_mean"] > 0)),
            }
        sens_meta[opp] = {"dropped_seeds": drop, "kept_seeds": keep,
                          "computed": True,
                          "why": "cell(s) over the empty-answer flag: "
                                 + ", ".join(sorted(flagged_set & {
                                     f"{opp}/{arm}|{s}" for s in drop
                                     for arm in ("nohole", "eg")}))}

    # pooled marker rate by global length quintile: the reason to stratify
    quintile = {}
    if pooled and all(pooled):
        for m in MARKER_KEYS:
            quintile[m] = [float(np.mean([h[m] for h in bucket]))
                           for bucket in pooled]

    # sample sizes, computed rather than asserted
    size = {}
    for opp, _ in BANDS:
        for cond, *_ in ARMS:
            key = f"{opp}/{cond}"
            if key not in cov:
                continue
            eps = sum(cov[key].values())
            blocks = sum(cells[f"{key}|{s}"]["n_blocks"] for s in cov[key]
                         if f"{key}|{s}" in cells)
            size[key] = {
                "n_seeds": len(cov[key]), "n_episodes": eps,
                "n_blocks": blocks,
                "episodes_per_seed": eps // max(1, len(cov[key])),
                "blocks_per_episode": round(blocks / eps, 1) if eps else None,
                "mean_chars_arm": (arms[key]["mean_chars"]["mean"]
                                   if key in arms else None),
                "mean_chars_arm_se": (arms[key]["mean_chars"]["se"]
                                      if key in arms else None),
                "mean_chars_per_seed": (arms[key]["mean_chars"]["per_seed"]
                                        if key in arms else None),
            }

    # verbosity gap per opponent, at render time -- this is the mechanism
    verbosity = {}
    for opp, _ in BANDS:
        nh, eg = size.get(f"{opp}/nohole"), size.get(f"{opp}/eg")
        if not (nh and eg and nh["mean_chars_arm"]):
            continue
        verbosity[opp] = {
            "nohole_mean_chars": nh["mean_chars_arm"],
            "nohole_se": nh["mean_chars_arm_se"],
            "eg_mean_chars": eg["mean_chars_arm"],
            "eg_se": eg["mean_chars_arm_se"],
            "pct_shorter_eg_vs_nohole":
                100.0 * (1.0 - eg["mean_chars_arm"] / nh["mean_chars_arm"]),
        }

    # is the endgame marker distinguishable from the FLOOR control?
    vs_floor = {}
    for opp, _ in BANDS:
        c = con_all.get(opp)
        if not c or FLOOR not in c:
            continue
        f_m, f_s = c[FLOOR]["strat_delta_mean"], c[FLOOR]["strat_delta_se"]
        vs_floor[opp] = {}
        for m in MARKER_KEYS:
            if m == FLOOR:
                continue
            d = c[m]["strat_delta_mean"] - f_m
            comb = float(np.hypot(c[m]["strat_delta_se"], f_s))
            vs_floor[opp][m] = {
                "strat_delta": c[m]["strat_delta_mean"],
                "floor_strat_delta": f_m,
                "difference": d,
                "combined_se": comb,
                "abs_z": abs(d) / comb if comb else None,
                "inside_floor_interval": bool(
                    f_m - f_s <= c[m]["strat_delta_mean"] <= f_m + f_s),
            }

    # ------------------------------------------------------------- render --
    # PAGE TEXT IS BUILT BEFORE THE PANELS, because the panels are positioned
    # from its measured height. Fixed y offsets were what let the last header
    # line land on top of the first band heading: every block here wraps to a
    # number of lines that depends on the data in it, so the only stable
    # geometry is one derived from the text after wrapping.
    FIG_W, FIG_H = 20.0, 24.0
    TITLE_PT, HEAD_PT, FOOT_PT = 13.5, 8.4, 8.2
    PT = 1.0 / (FIG_H * 72.0)

    # Characters that fit on one full-width line, from the geometry rather
    # than from a guess: DejaVu Sans averages ~0.55 em of advance per
    # character, and the text column runs from x=0.008 to x=0.99.
    def cols(pt):
        return int(0.982 * FIG_W * 72.0 / (0.555 * pt))

    title, lines, foot, derived = page_text(
        meta, cells, con_all, size, verbosity, quintile, vs_floor, haz,
        flagged, sens_all, a.empty_answer_flag)
    ratios, nz, widest = derived["ratios"], derived["nz"], derived["widest"]
    title = wrap(title, cols(TITLE_PT))
    lines = [wrap(t, cols(HEAD_PT)) for t in lines]
    foot = [(c, wrap(t, cols(FOOT_PT))) for c, t in foot]

    title_lh, head_lh, foot_lh = (TITLE_PT * 1.4 * PT, HEAD_PT * 1.5 * PT,
                                  FOOT_PT * 1.5 * PT)
    head_h = nlines(title) * title_lh + 0.010 + sum(
        nlines(t) * head_lh + 0.0035 for t in lines)
    foot_h = sum(nlines(t) * foot_lh + 0.0055 for _, t in foot)

    fig = plt.figure(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(PAPER)

    # One gridspec per BAND, with an explicit gap between them: the band gap
    # is what makes two bands read as two bands, and a uniform hspace across
    # four rows cannot make the between-band gap larger than the within-band
    # one. Opponent is position; position has to be legible.
    # The two bands are given IDENTICAL heights: they share both y-axes, and a
    # shared axis drawn at two different scales is not a shared axis.
    BAND_HEAD, BAND_GAP = 0.026, 0.052
    page_top = 0.997 - head_h - BAND_HEAD
    page_bot = 0.012 + foot_h + 0.028      # clearance for 2-line tick labels
    band_h = (page_top - page_bot - BAND_GAP) / 2.0
    if band_h < 0.20:
        print(f"[fig] ** only {band_h:.3f} of figure height left per band; "
              f"the page text has outgrown FIG_H={FIG_H} **")
    band_span = [(page_top, page_top - band_h),
                 (page_top - band_h - BAND_GAP, page_bot)]
    grids = [fig.add_gridspec(2, len(MARKERS), top=t, bottom=b,
                              height_ratios=[1.0, 1.5], hspace=0.40,
                              wspace=0.26, left=0.045, right=0.985)
             for t, b in band_span]

    # Shared y across BOTH bands for row 1: same panel position, same quantity,
    # so a vertical difference between bands is the effect of forgiveness. And
    # shared across the four markers, because the FLOOR/CONTROL argument is a
    # comparison of MAGNITUDES across panels.
    top1 = 0.05
    for opp, _ in BANDS:
        for mk in MARKER_KEYS:
            for cond, *_ in ARMS:
                key = f"{opp}/{cond}"
                if key in arms and mk in arms[key]["markers"]:
                    s = arms[key]["markers"][mk]
                    top1 = max(top1, max(s["per_seed"]),
                               s["mean"] + (s["se"] or 0.0))
    top1 *= 1.32

    # One shared y-limit per ESTIMATOR, across both bands: the two raw panels
    # share an axis with each other and the two stratified panels share a
    # different one. Comparing grim to tft on the same estimator is a
    # comparison the layout should make free; comparing raw to stratified on
    # the same axis is what squashed the stratified panel in the last render.
    ylim2 = {}
    for kind in ("raw", "strat"):
        lo2, hi2 = 0.0, 0.0
        for opp, _ in BANDS:
            for m, c in (con_all.get(opp) or {}).items():
                if m not in MARKER_KEYS:
                    continue
                vals = [v for v in c[f"per_seed_{'delta' if kind == 'raw' else 'strat'}"]
                        if v is not None]
                vals += [c[f"{kind}_delta_mean"] + c[f"{kind}_delta_se"],
                         c[f"{kind}_delta_mean"] - c[f"{kind}_delta_se"]]
                s = (sens_all.get(opp) or {}).get(m)
                if s and s.get(f"{kind}_delta_mean") is not None:
                    vals.append(s[f"{kind}_delta_mean"])
                lo2, hi2 = min(lo2, min(vals)), max(hi2, max(vals))
        pad = (hi2 - lo2) * 0.16
        # headroom at the top for the per-group number blocks, at the bottom
        # for the two-column legend
        ylim2[kind] = (lo2 - pad * 2.1, hi2 + pad * 1.75)
    scale_ratio = ((ylim2["raw"][1] - ylim2["raw"][0])
                   / (ylim2["strat"][1] - ylim2["strat"][0]))

    row1, row2, crossings = {}, {}, {}
    for bi, (opp, _) in enumerate(BANDS):
        gs = grids[bi]
        row1[opp], row2[opp] = {}, {}
        for i, (mk, letter, lab, note, is_fl) in enumerate(MARKERS):
            ax = fig.add_subplot(gs[0, i])
            rec = {}
            arm_panel(ax, opp, arms, mk, top1, flagged_set, rec,
                      key_note=(bi == 0 and i == 0))
            style(ax, f"{letter}{bi + 1} - {lab}", "share of reasoning blocks",
                  note)
            if is_fl:
                ax.set_facecolor("#f6f5f1")
            if rec:
                row1[opp][mk] = rec
            c = (con_all.get(opp) or {}).get(mk)
            if c:
                # ONE line, bottom RIGHT. The full raw/stratified/floor block
                # belongs to row 2, and the bottom LEFT is where the seed tags
                # land once a low-rate marker is drawn on the shared y-axis.
                ax.text(0.985, 0.02,
                        f"delta  raw {c['raw_delta_mean']:+.3f}   "
                        f"strat {c['strat_delta_mean']:+.3f}",
                        transform=ax.transAxes, fontsize=7.0, color=INK2,
                        va="bottom", ha="right", family="monospace")

        # The per-panel note goes in the TITLE. These panels are ~9 inches
        # wide and already carry four per-group number blocks along the top
        # and a legend along the bottom; there is no free interior corner.
        v = verbosity.get(opp, {})
        halves = [
            ("raw", f"E{bi + 1} - RAW delta vs {opp.upper()}"
                    + ("" if not v else
                       f".   reasoning length: nohole "
                       f"{v['nohole_mean_chars']:.0f} +/- "
                       f"{v['nohole_se']:.0f} chars, eg "
                       f"{v['eg_mean_chars']:.0f} +/- {v['eg_se']:.0f} "
                       f"-- eg writes "
                       # one decimal: grim's gap is 1.8% and `:.0f` printed it
                       # as "2%", which is the log's 1.8% overstated by 10% on
                       # a quantity whose whole point is that it is near zero
                       f"{abs(v['pct_shorter_eg_vs_nohole']):.1f}% "
                       + ("less" if v["pct_shorter_eg_vs_nohole"] >= 0
                          else "more"))),
            ("strat", f"F{bi + 1} - the SAME contrast, standardised to the "
                      f"global length quintiles.   y-axis expanded "
                      f"{scale_ratio:.1f}x vs E{bi + 1}"),
        ]
        for hi_, (kind, ttl) in enumerate(halves):
            axc = fig.add_subplot(gs[1, hi_ * 2:hi_ * 2 + 2])
            got = contrast_panel(axc, opp, con_all.get(opp) or {},
                                 sens_all.get(opp), kind, ylim2[kind],
                                 row2[opp])
            style(axc, ttl, "delta(eg - nohole), share of reasoning blocks")
            if kind == "strat":
                crossings[opp] = got

    # Band headings LAST, in figure coords, read off the finished layout: put
    # in axes coords they land on the panel title of the row above.
    for bi, (_, heading) in enumerate(BANDS):
        top = band_span[bi][0]
        fig.text(0.012, top + BAND_HEAD * 0.80, heading, fontsize=13.5,
                 color=INK, fontweight="bold", va="bottom", ha="left")
        fig.add_artist(plt.Line2D([0.012, 0.99], [top + BAND_HEAD * 0.62] * 2,
                                  color=GRID, lw=1.1))

    fig.suptitle(title, fontsize=TITLE_PT, color=INK, x=0.008, ha="left",
                 y=0.997, va="top", linespacing=1.4)
    y = 0.997 - nlines(title) * title_lh - 0.010
    for t in lines:
        fig.text(0.008, y, t, fontsize=HEAD_PT, color=INK2, ha="left",
                 va="top", linespacing=1.5)
        y -= nlines(t) * head_lh + 0.0035
    y = page_bot - 0.028
    for col, t in foot:
        fig.text(0.008, y, t, fontsize=FOOT_PT, color=col, ha="left",
                 va="top", linespacing=1.5)
        y -= nlines(t) * foot_lh + 0.0055

    png = outdir / "fig1_does_it_suppress.png"
    fig.savefig(png, dpi=150, facecolor=fig.get_facecolor())
    print(f"[fig] wrote {png}")

    # --------------------------------------------------------------- json --
    out = {
        "figure": png.name,
        "question": "Does the endgame-penalty reward knob suppress endgame "
                    "REASONING, as it does endgame BEHAVIOUR?",
        "answer": {
            "headline": title.replace("\n", " "),
            "tft": "Raw marker rates drop substantially and every seed agrees "
                   "in sign, but the arm also writes ~35% less; after "
                   "standardising to the global length distribution the "
                   "residual is small and is statistically indistinguishable "
                   "from the in_game_penalty FLOOR control, which has no stake "
                   "in the endgame. Read as 'thinks less overall', not 'thinks "
                   "less about the endgame'.",
            "tft_endgame_hold_caveat":
                "endgame_hold is the exception: it RISES against tft, "
                "survives length standardisation, and sits clear of the floor "
                "control band, which is the direction a genuine suppression "
                "story predicts. It is a hint, not a result -- the interval "
                "only just excludes zero and one of the three per-seed "
                "stratified deltas is flat. See "
                "endgame_marker_vs_floor_control.tft.endgame_hold.",
            "grim": "Nothing detectable: per-seed deltas flip sign, and the "
                    "stratified estimate is not robust to a single degenerate "
                    "baseline cell. This is a failure to detect, not evidence "
                    "of absence.",
            "not_an_equivalence_claim": True,
        },
        "error_bar_definitions": {
            "row1": "Offset bar beside each arm's per-seed points is the "
                    "BETWEEN-TRAINING-SEED SE ON THAT ARM'S LEVEL: sd of the "
                    "arm's per-seed marker rates / sqrt(n_seeds). It is not an "
                    "interval on any difference. The single-seed inf arm has "
                    "no such bar because n=1.",
            "row2_raw_and_strat": "BETWEEN-TRAINING-SEED SE ON THE DIFFERENCE: "
                                  "sd of the paired per-seed deltas / "
                                  "sqrt(n_seeds).",
            "row2_binomial": "SAMPLING FLOOR of the pooled block rate. NOT an "
                             "error bar on the effect.",
            "sensitivity_point": "No error bar drawn: it rests on 2 seeds.",
        },
        "contrast_definition": meta.get("contrast_definition"),
        "source": {
            "marker_json": src.name,
            "block_jsonl": blk_path.name if blk_path.exists() else None,
            "upstream": meta.get("source"),
            "generated_utc": meta.get("generated_utc"),
            "steps_present": meta.get("steps_present"),
            "n_episodes_used": meta.get("n_episodes_used"),
            "n_blocks_total": meta.get("n_blocks"),
            "n_cells": len(cells),
            "answer_parse_rate": meta.get("answer_parse_rate"),
            "length_bins": lb,
        },
        "coverage": cov,
        "coverage_note": "grim and tft both have 3 seeds in nohole and eg, so "
                         "both carry a contrast. tft/inf has 1 seed and is "
                         "shown as a marked point only. grim/inf has no "
                         "episodes on disk.",
        "cells_excluded": meta.get("cells_excluded"),
        "contrasts_omitted": meta.get("contrasts_omitted"),
        "sample_size": size,
        "verbosity": verbosity,
        "pooled_marker_rate_by_global_length_quintile": quintile,
        "hazard_screen": {
            "criterion": f"n_empty_answer_rate > {a.empty_answer_flag}",
            "why_the_usual_gate_misses_it":
                "The repo gate is invalid_rate > 0.15. invalid_rate counts "
                "actions the environment had to substitute; n_empty_answer "
                "counts decision turns that produced no answer text. "
                "grim/nohole|1 reads invalid_rate 0.000 with ~60% empty "
                "answers.",
            "flagged_cells": flagged,
            "all_cells": haz,
        },
        "sensitivity_drop_flagged_cell": {
            "method": "Global length-bin edges and the standard population are "
                      "held at the FULL-data values; only the set of averaged "
                      "seeds changes. Verified to reproduce score_traces.py "
                      "per_seed_strat exactly on the full seed set.",
            "per_opponent": sens_meta,
            "values": sens_all,
        },
        "endgame_marker_vs_floor_control": vs_floor,
        "row1_arm_levels": row1,
        "row2_contrasts": row2,
        "binomial_floor_ratio_range": {
            "min": min(ratios) if ratios else None,
            "max": max(ratios) if ratios else None,
            "n_estimates": len(ratios),
            "note": "Computed at render time over every estimate drawn. Not "
                    "constant across markers, so no single multiplier is "
                    "quoted anywhere on the figure.",
        },
        "intervals_not_crossing_zero": nz,
        "widest_interval": ({"which": widest[1], "mean": widest[2],
                             "se": widest[0]} if widest else None),
    }
    js = outdir / "fig1_does_it_suppress.json"
    js.write_text(json.dumps(out, indent=1))
    print(f"[fig] wrote {js}")

    for opp, _ in BANDS:
        print(f"[fig] --- {opp}")
        for mk in MARKER_KEYS:
            r = (row2.get(opp) or {}).get(mk)
            if not r:
                continue
            s = (sens_all.get(opp) or {}).get(mk)
            print(f"[fig] {mk:>22}: raw {r['raw_delta_mean']:+.4f} +/- "
                  f"{r['raw_delta_se_between_seed']:.4f} | strat "
                  f"{r['strat_delta_mean']:+.4f} +/- "
                  f"{r['strat_delta_se_between_seed']:.4f} | floor "
                  f"{r['binomial_se_pooled']:.4f} "
                  f"({r['ratio_raw_se_over_binomial_se']:.1f}x / "
                  f"{r['ratio_strat_se_over_binomial_se']:.1f}x)"
                  + (f" | drop-flagged strat {s['strat_delta_mean']:+.4f}"
                     f" (n={s['n_seeds']})" if s else ""))
    return 0


def page_text(meta, cells, con_all, size, verbosity, quintile, vs_floor,
              haz, flagged, sens_all, empty_flag):
    """Suptitle, header block and footer block. Every number read from data.

    A stale hardcoded string was the worst defect the previous audit found
    across these figures, so nothing in here is written by hand: the headline
    claim, the binomial-floor ratio range, the sensitivity shifts and the
    widest-interval caveat are all formatted from the arguments.
    """
    tft = con_all.get("tft", {})
    grim = con_all.get("grim", {})
    hl = "endgame_defect_plan"

    def fmt(c, kind):
        return (f"{c[f'{kind}_delta_mean']:+.3f} +/- "
                f"{c[f'{kind}_delta_se']:.3f}") if c else "n/a"

    vt = verbosity.get("tft", {})
    fl_t = tft.get(FLOOR)
    title = (
        "Opponent-dependent. Against TIT-FOR-TAT the endgame penalty does cut "
        f"endgame talk in the raw text ({fmt(tft.get(hl), 'raw')}, all seeds "
        "agreeing in sign) -- but ~"
        f"{vt.get('pct_shorter_eg_vs_nohole', float('nan')):.0f}% of the "
        "reasoning goes missing too, and\nafter length standardisation "
        f"{fmt(tft.get(hl), 'strat')} is indistinguishable from the "
        f"FLOOR/CONTROL marker's {fmt(fl_t, 'strat')}. Against GRIM nothing is "
        f"detectable at all ({fmt(grim.get(hl), 'strat')} stratified, per-seed "
        "deltas flipping sign).")

    n_seeds_txt = tft.get(hl, grim.get(hl, {})).get("n_seeds", "?")
    ratios = [r for opp, _ in BANDS
              for m, c in (con_all.get(opp) or {}).items() if m in MARKER_KEYS
              for r in ((c["raw_delta_se"] / c["binomial_se_pooled"]
                         if c["binomial_se_pooled"] else None),
                        (c["strat_delta_se"] / c["binomial_se_pooled"]
                         if c["binomial_se_pooled"] else None))
              if r is not None]
    # One decimal, not zero: the minimum of this range is ~1.56, and `:.0f`
    # rendered it as "2x" -- a 28% overstatement of the smallest ratio, and a
    # disagreement with fig2 and the research log, which both quote 1.6x.
    rng = (f"{min(ratios):.1f}x to {max(ratios):.1f}x" if ratios else "much")

    def qtxt(m):
        return (" / ".join(f"{v:.3f}" for v in quintile[m])
                if m in quintile else "n/a")

    eg_n = size.get("tft/eg", size.get("grim/eg", {}))
    lines = [
        "Qwen3.8-27B, thinking on, iterated prisoner's dilemma, step 35, "
        "scored off raw chain-of-thought text. Two contrast arms differing in "
        "ONE thing: orange adds a hidden reward charge on late betrayal. The "
        "BEHAVIOURAL effect of that charge is real and is not what this figure "
        "measures (training logs, 3 seeds: -0.039 +/- 0.012 endgame-betrayal "
        "rate vs grim, -0.142 +/- 0.064 vs tft); this asks whether the "
        "REASONING moved with it.",
        f"n = {meta.get('n_episodes_used', '?')} episodes / "
        f"{meta.get('n_blocks', '?')} reasoning blocks / {len(cells)} cells. "
        f"Per contrast arm: {eg_n.get('n_seeds', '?')} training seeds x "
        f"{eg_n.get('episodes_per_seed', '?')} episodes x "
        f"{eg_n.get('blocks_per_episode', '?')} blocks per episode. "
        "A marker hit is BINARY PER BLOCK, which is why block length matters. "
        f"Answer parse rate {meta.get('answer_parse_rate', float('nan')):.3f} "
        f"over {meta.get('n_decision_turns', '?')} decision turns.",
        "TWO DIFFERENT KINDS OF ERROR BAR, AND ROW 1 IS NOT THE SAME AS ROW 2. "
        f"In ROW 2 of each band, every bar on an estimate is BETWEEN TRAINING "
        f"SEED ON A DIFFERENCE: sd of the {n_seeds_txt} paired per-seed deltas "
        f"/ sqrt({n_seeds_txt}). In ROW 1 the offset bar beside each arm's "
        "points is BETWEEN TRAINING SEED ON THAT ARM'S LEVEL: sd of that one "
        "arm's three seed rates / sqrt(3), offset to the right so it does not "
        "sit on its own points. It is not an interval on any difference, and "
        "two arms' level bars overlapping says nothing about whether their "
        "difference does. The single-seed inf arm carries no bar at all.",
        "The grey binomial bar in row 2 is the SAMPLING FLOOR of a pooled block "
        f"rate -- how precisely THIS run was measured, not whether another run "
        f"would agree. Across the {len(ratios)} estimates drawn here the "
        f"honest between-seed bar is {rng} larger than that floor; the ratio "
        "is not constant, so no single multiplier describes it and none is "
        "quoted anywhere on this figure.",
        "WHY STRATIFY. Marker hits rise steeply with reasoning length. Pooled "
        f"over all blocks by global n_chars quintile, endgame_defect_plan runs "
        f"{qtxt('endgame_defect_plan')} and the FLOOR control in_game_penalty "
        f"runs {qtxt(FLOOR)} -- both are mostly a length readout. `strat` "
        "reweights each arm onto the SAME global quintile distribution, so a "
        "difference in how much an arm wrote cannot masquerade as a difference "
        "in what it wrote about.",
        "OPPONENT IS BAND POSITION, never hue, so the condition colours keep "
        "the meaning they have elsewhere in the repo (purple baseline, orange "
        "endgame penalty, blue hidden horizon, and blue is used for nothing "
        "else). Row 1 shares ONE y-axis across both bands and all four "
        "markers, so the FLOOR/CONTROL comparison in panel D is a comparison "
        "of ink. The two RAW panels share a second y-axis and the two "
        "STRATIFIED panels a third; raw and stratified are deliberately NOT on "
        "a common axis, because at the raw scale every stratified estimate "
        "collapses into a few pixels. Contrast markers are neutral ink: a "
        "difference is not a condition.",
    ]

    # ------------------------------------------------------------- footer --
    foot = []

    hz = []
    for k in flagged:
        r = haz[k]
        hz.append(f"{k} (empty-answer {r['empty_answer_rate']:.3f}, "
                  f"invalid_rate {r['invalid_rate']:.3f}, mean/median/p90 "
                  f"{r['mean_chars']:.0f}/{r['median_chars']:.0f}/"
                  f"{r['p90_chars']:.0f} chars, endgame_rate "
                  f"{r['endgame_rate']:.3f})")
    if hz:
        sg = (sens_all.get("grim") or {}).get(hl)
        stf = (sens_all.get("tft") or {}).get(hl)
        foot.append((ORANGE,
            "COMPROMISED CELLS, DISCLOSED. Screening every cell on the share "
            f"of decision turns that emit an EMPTY ANSWER (> "
            f"{empty_flag:.2f}) flags: " + "; ".join(hz) + ".\n"
            "Both read invalid_rate well under the repo's 0.15 gate -- "
            "invalid_rate counts actions the environment had to substitute, "
            "not turns that produced no answer, so the usual gate does not see "
            "this failure mode. Flagged seeds are drawn HOLLOW with a '!' in "
            "row 1 and are the seeds dropped in the orange sensitivity point "
            "in row 2.\n"
            + (f"GRIM is NOT robust to it: dropping grim/nohole seed 1 moves "
               f"the stratified {hl} delta from "
               f"{grim[hl]['strat_delta_mean']:+.3f} to "
               f"{sg['strat_delta_mean']:+.3f} -- a SIGN FLIP, and all four "
               f"grim markers flip the same way. The grim RAW deltas barely "
               f"move ({grim[hl]['raw_delta_mean']:+.3f} to "
               f"{sg['raw_delta_mean']:+.3f}). Do not read the grim "
               f"stratified central value as a measurement."
               if sg else "")
            + (f"  TFT IS robust to its own flagged cell in the direction that "
               f"matters: dropping tft/nohole seed 0 moves the stratified "
               f"{hl} delta from {tft[hl]['strat_delta_mean']:+.3f} to "
               f"{stf['strat_delta_mean']:+.3f} and the raw delta from "
               f"{tft[hl]['raw_delta_mean']:+.3f} to "
               f"{stf['raw_delta_mean']:+.3f} -- same sign, larger."
               if stf else "")
            + " Both sensitivity estimates rest on TWO seeds and carry no "
              "usable error bar; they are shown to test a sign, not to "
              "replace an estimate."))

    hold_t = tft.get("endgame_hold")
    hold_vs = (vs_floor.get("tft") or {}).get("endgame_hold")
    fl_line = []
    for opp, _ in BANDS:
        vf = (vs_floor.get(opp) or {}).get(hl)
        if vf:
            fl_line.append(
                f"{opp}: endgame {vf['strat_delta']:+.3f} vs floor "
                f"{vf['floor_strat_delta']:+.3f}, difference "
                f"{vf['difference']:+.3f} +/- {vf['combined_se']:.3f} "
                f"(|z| = {vf['abs_z']:.2f}"
                + (", inside the floor's own interval)"
                   if vf["inside_floor_interval"] else ")"))
    foot.append((INK2,
        "THE FLOOR CONTROL FALLS AS MUCH AS THE SIGNAL, which is why the large "
        "and perfectly sign-consistent tft RAW effect is still not read here "
        "as an endgame result. Panel D of each band and the shaded horizontal "
        "band running across each E and F panel are the same marker, "
        "in_game_penalty: generic punishment vocabulary with no stake in "
        "whether the model is reasoning about the LAST round. Against tft it "
        f"falls {fmt(fl_t, 'raw')} raw and {fmt(fl_t, 'strat')} stratified.\n"
        "Stratified endgame_defect_plan measured against that control -- "
        + "; ".join(fl_line) + ". A difference that small relative to its own "
        "uncertainty does not license the claim that the endgame markers moved "
        "for an endgame-specific reason. Note this cuts the other way too: it "
        "is a failure to SEPARATE the two, not a demonstration that they are "
        "the same quantity.\n"
        + (f"THE ONE MARKER THAT DOES NOT FALL WITH THE FLOOR is endgame_hold "
           f"against tft, which RISES: {fmt(hold_t, 'strat')} stratified, "
           f"clear of the control band at "
           f"|z| = {hold_vs['abs_z']:.2f}, and in the direction a real "
           f"suppression story predicts (panel B is the other direction of "
           f"panel A). Treat it as a hint and not a result: the interval only "
           f"just excludes zero, and the per-seed stratified deltas are "
           + ", ".join(f"{v:+.3f}" for v in hold_t["per_seed_strat"])
           + ", so one seed is flat."
           if hold_t and hold_vs else "")))

    foot.append((INK2,
        "HOW TO READ EACH BAND. Row 1 (A-D) is the per-arm LEVEL: one point "
        "per training seed, grey lines joining the SAME seed across arms, and "
        "one offset bar per arm giving that arm's between-seed spread. Lines "
        "that cross rather than run parallel mean the arm ordering is not "
        "stable across seeds.\n"
        "Row 2 is the same contrast twice: E on the RAW rates, F after "
        "standardising to the global length quintiles, on an expanded y-axis. "
        "In both, the large filled/open marker is the estimate with its "
        "between-training-seed SE; the small grey glyphs to its left are the "
        "individual per-seed deltas behind it, using the same seed glyph "
        "shapes as row 1; the small grey x to its right is the pooled BINOMIAL "
        "SE, centred on the estimate so that the only thing differing between "
        "it and the bar beside it is the WHISKER LENGTH.\n"
        "The open orange cross furthest right in each group is the same "
        "estimate recomputed with the flagged cell dropped, joined by a dotted "
        "line to the estimate it would replace. Both panels print BOTH "
        "estimators' numbers for every marker, so the raw-to-stratified "
        "shrinkage stays readable even though the two live on different axes."))

    nz = []
    for opp, _ in BANDS:
        for m in MARKER_KEYS:
            c = (con_all.get(opp) or {}).get(m)
            if not c:
                continue
            for kind, lab in (("raw", "raw"), ("strat", "stratified")):
                mu, s_ = c[f"{kind}_delta_mean"], c[f"{kind}_delta_se"]
                if s_ is not None and not ((mu - s_) <= 0 <= (mu + s_)):
                    nz.append(f"{opp}/{m} {lab} {mu:+.3f} +/- {s_:.3f}")
    widest = None
    for opp, _ in BANDS:
        for m, c in (con_all.get(opp) or {}).items():
            if m not in MARKER_KEYS:
                continue
            for kind in ("raw", "strat"):
                w = c[f"{kind}_delta_se"]
                if widest is None or w > widest[0]:
                    widest = (w, f"{opp}/{m} {kind}",
                              c[f"{kind}_delta_mean"])
    foot.append((INK,
        ("Intervals NOT crossing zero at +/-1 between-seed SE: "
         + "; ".join(nz) if nz else
         "Every interval drawn in row 2 crosses zero at +/-1 between-seed SE.")
        + "\nTHIS IS NOT AN EQUIVALENCE RESULT, AND THE GRIM BAND IN "
          "PARTICULAR IS NOT ONE. With three training seeds these intervals "
          "are wide: the widest drawn here is "
        + (f"{widest[1]} at {widest[2]:+.3f} +/- {widest[0]:.3f}, which is "
           f"consistent with anything from {widest[2] - widest[0]:+.3f} to "
           f"{widest[2] + widest[0]:+.3f}" if widest else "n/a")
        + ". A wide interval containing zero is a failure to detect, not a "
          "demonstration of absence, and no panel here should be read as "
          "showing that the penalty leaves endgame reasoning alone. The one "
          "claim this data supports in the positive direction is the tft RAW "
          "drop; everything after that is about what that drop is made of. "
          "tft/inf is present at ONE seed, is drawn as a single open blue "
          "diamond in row 1 with no error bar, and enters no contrast "
          "anywhere; grim/inf has no episodes on disk."))
    # the derived quantities the footer quotes, handed back so the paired JSON
    # records exactly the numbers the reader saw rather than a second estimate
    return title, lines, foot, {"ratios": ratios, "nz": nz, "widest": widest}


if __name__ == "__main__":
    raise SystemExit(main())

