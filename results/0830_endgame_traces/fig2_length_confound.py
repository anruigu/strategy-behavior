#!/usr/bin/env python
"""Why a naive marker rate cannot answer the endgame-reasoning question.

    /home/allie/venvs/tinker-ipd/bin/python fig2_length_confound.py

  fig2_length_confound.png       the figure
  fig2_length_confound.json      every number drawn in it

WHAT THIS FIGURE IS FOR.

A marker is a binary regex hit on ONE reasoning block, so a longer block has
more surface to hit and the rate is partly a length measurement. That was
originally a caveat on the headline contrast. With `tft` now present at three
seeds in both arms it is the mechanism of the headline contrast: against `tft`
the endgame-penalty arm writes 35% less than baseline (885 vs 1367 mean chars,
a seed-paired delta of -482 +- 212), the raw `endgame_defect_plan` delta is
-0.288 +- 0.115, and standardising for length leaves -0.065 +- 0.022. Roughly
three quarters of the apparent suppression of endgame reasoning against `tft`
is the model simply writing less. Against `grim` there is no arm-level length
difference (1072 vs 1053) and nothing survives either.

The `in_game_penalty` FLOOR CONTROL settles what is left. It matches generic
within-game punishment vocabulary and has no endgame stake, so the knob has no
reason to suppress it -- yet against `tft` it falls -0.235 +- 0.076 raw and
-0.059 +- 0.042 stratified, statistically indistinguishable from the endgame
marker's stratified -0.065 +- 0.022. The length-adjusted residual is not
endgame-specific either.

WHAT THE PANELS ARE FOR.

A (split by opponent) is the dose-response: pooled hit rate against block
length across the five global quintiles, with both arms on the same curve.
B is the per-cell scatter of mean reasoning length against marker rate.
C is the same length axis against the BEHAVIOUR (`endgame_rate`), so that
verbosity's relationship to behaviour is visible rather than asserted.
D is raw vs length-stratified delta per marker per opponent, and beside it the
arm-level LENGTH delta itself in chars, which is the mechanism as a quantity.

ERROR BARS. Panel A is binomial and says so, because inside a fixed length bin
the remaining question really is a sampling one. Panels B and C plot cells with
no bar -- the scatter of the points IS the between-seed variation. Panel D and
the length-delta panel are between TRAINING SEED, sd/sqrt(3), on the
seed-paired delta; that is the only admissible bar on an arm difference.

COVERAGE AND HAZARDS. 624 episodes / 12,480 blocks / 13 cells. `grim` and `tft`
both have nohole and eg at 3 seeds; `tft/inf` exists at ONE seed, is drawn
marked, and never enters a contrast or a fit; the five other `inf` cells are
empty. Two cells carry an empty-answer hazard that the repo's `invalid_rate`
gate does not catch, `grim/nohole` seed 1 worst at 60%; both are disclosed on
the figure and every correlation is reported with and without the worst one.
"""
from __future__ import annotations

import argparse
import json
import math
import textwrap
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.ticker import NullFormatter  # noqa: E402

HERE = Path(__file__).resolve().parent
BLOCKS = HERE / "trace_blocks.jsonl"
MARKERS_JSON = HERE / "trace_markers.json"

PURPLE, ORANGE, BLUE = "#7a5bd6", "#eb6834", "#2a78d6"
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"

# Fixed BY CONDITION and never repainted. BLUE means the hidden-horizon arm and
# nothing else -- `tft/inf` has now landed at one seed, so it is finally in use
# and nothing else in this figure may borrow it. Neutral greys carry everything
# that is not a condition (the sampling floor, the fit lines, the hazard rings).
CONDITION = {
    "nohole": ("baseline (nohole)", PURPLE),
    "eg": ("endgame penalty (eg)", ORANGE),
    "inf": ("hidden horizon (inf)", BLUE),
}
# Opponent is carried by marker SHAPE in the scatters and by PANEL POSITION in
# A and D. Never by hue: hue is spoken for by condition.
OPPONENTS = ["grim", "tft"]
OPP_MARK = {"grim": "o", "tft": "s"}
CONTRAST_CONDS = ["nohole", "eg"]

# Panel A draws two markers. `endgame_defect_plan` is the marker the claim is
# about; `in_game_penalty` is the FLOOR CONTROL -- generic within-game
# punishment vocabulary with no endgame stake. If the floor rides the same
# length curve then the curve is a property of the measurement.
PANEL_A_MARKERS = [
    ("endgame_defect_plan", "-", 2.0, 5.5),
    ("in_game_penalty", (0, (5, 2)), 1.5, 4.5),
]
PANEL_D_MARKERS = ["endgame_defect_plan", "endgame_hold",
                   "backward_induction", "in_game_penalty"]
FLOOR_MARKER = "in_game_penalty"
PRIMARY = "endgame_defect_plan"

# A cell whose decision turns are this often empty is flagged on the figure.
# The repo's usual gate is `invalid_rate > 0.15`, which reads 0.000 on the
# worst offender here, so it cannot be relied on.
EMPTY_HAZARD = 0.20
# Above this the cell is treated as compromised: excluded-variant correlations
# are reported alongside the full ones rather than instead of them.
EMPTY_COMPROMISED = 0.50


def style(ax, title, ylab, xlab, note=None):
    ax.set_title(title, fontsize=10.5, color=INK, loc="left", pad=8)
    ax.set_ylabel(ylab, fontsize=9, color=INK2)
    ax.set_xlabel(xlab, fontsize=9, color=INK2)
    ax.set_facecolor(SURF)
    ax.grid(True, axis="y", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUT, labelsize=8, length=0)
    if note:
        ax.text(0.015, 0.965, note, transform=ax.transAxes, fontsize=7.2,
                color=MUT, va="top", zorder=6)


def binom_se(k, n):
    if not n:
        return None
    p = k / n
    return math.sqrt(max(p * (1.0 - p), 0.0) / n)


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if len(x) < 3 or x.std() == 0 or y.std() == 0:
        return None
    return float(np.corrcoef(x, y)[0, 1])


def spearman(x, y):
    """Rank correlation by hand -- scipy is not in this venv. Ties get the
    average rank. With a dozen cells this is descriptive, not a test, and the
    JSON says so rather than carrying a p-value the n cannot support."""
    def rank(v):
        vals = np.asarray(v, float)
        order = np.argsort(vals, kind="mergesort")
        r = np.empty(len(vals), float)
        r[order] = np.arange(1, len(vals) + 1, dtype=float)
        for u in np.unique(vals):
            m = vals == u
            if m.sum() > 1:
                r[m] = r[m].mean()
        return r
    return pearson(rank(x), rank(y))


def mean_sd_se(v):
    v = np.asarray(v, float)
    n = len(v)
    if n == 0:
        return {"mean": None, "sd": None, "se": None, "n": 0}
    sd = float(v.std(ddof=1)) if n > 1 else None
    return {"mean": float(v.mean()), "sd": sd,
            "se": (sd / math.sqrt(n)) if sd is not None else None, "n": n}


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------

def load():
    rows = [json.loads(l) for l in BLOCKS.read_text().splitlines() if l.strip()]
    agg = json.loads(MARKERS_JSON.read_text())
    edges = agg["meta"]["length_bins"]["edges"]
    # The SAME global quintile edges the stratified contrast used, applied to
    # ALL blocks -- they were cut over the pooled set, so recutting them per
    # opponent would silently be a different adjustment from the one
    # `contrasts.<opp>.strat_delta_*` reports.
    chars = np.array([r["n_chars"] for r in rows], float)
    for r, b in zip(rows, np.digitize(chars, edges)):
        r["_bin"] = int(b)
    return rows, agg, edges


def cell_table(agg):
    """One row per (opponent, condition, train seed) cell present on disk."""
    out = []
    for arm in sorted(agg["coverage"]):
        opp, cond = arm.split("/")
        n_seeds = agg["arms"][arm]["n_seeds"]
        for seed in sorted(agg["coverage"][arm], key=int):
            c = agg["cells"][f"{arm}|{seed}"]
            empty = c["n_empty_answer_rate"]
            out.append({
                "cell": f"{arm}|{seed}",
                "arm": arm, "opponent": opp, "condition": cond,
                "train_seed": int(seed),
                "arm_n_seeds": n_seeds,
                "single_seed_arm": n_seeds < 2,
                "n_episodes": c["n_episodes"], "n_blocks": c["n_blocks"],
                "mean_chars": c["mean_chars"],
                "median_chars": c["median_chars"],
                "endgame_defect_plan": c["markers"][PRIMARY],
                "in_game_penalty": c["markers"][FLOOR_MARKER],
                "endgame_rate": c["endgame_rate"],
                "invalid_rate": c["invalid_rate"],
                "empty_answer_rate": empty,
                "empty_answer_hazard": empty is not None and empty > EMPTY_HAZARD,
                "compromised": empty is not None and empty > EMPTY_COMPROMISED,
            })
    out.sort(key=lambda c: c["mean_chars"])
    for i, c in enumerate(out):
        c["length_rank_of_all_cells"] = i + 1
    out.sort(key=lambda c: (c["opponent"], c["condition"], c["train_seed"]))
    return out


def correlations(cells, ykey):
    """Every slice of the cell set that a reader might reasonably ask for.

    Reported together rather than one at a time: the compromised cell moves
    these two correlations in OPPOSITE directions, so quoting whichever
    variant flatters the panel would be a choice about the conclusion.
    """
    def fit(sel):
        if len(sel) < 3:
            return {"n_cells": len(sel), "pearson_r": None,
                    "spearman_rho": None, "slope": None, "intercept": None,
                    "cells": [c["cell"] for c in sel]}
        xs = [c["mean_chars"] for c in sel]
        ys = [c[ykey] for c in sel]
        slope, intercept = np.polyfit(xs, ys, 1)
        r = pearson(xs, ys)
        return {"n_cells": len(sel), "pearson_r": r,
                "pearson_r2": (r * r) if r is not None else None,
                "spearman_rho": spearman(xs, ys),
                "slope": float(slope), "intercept": float(intercept),
                "cells": [c["cell"] for c in sel]}

    multi = [c for c in cells if not c["single_seed_arm"]]
    return {
        "multi_seed_cells": fit(multi),
        "multi_seed_cells_without_compromised":
            fit([c for c in multi if not c["compromised"]]),
        "all_cells_incl_single_seed": fit(cells),
        "all_cells_incl_single_seed_without_compromised":
            fit([c for c in cells if not c["compromised"]]),
        "grim_only": fit([c for c in multi if c["opponent"] == "grim"]),
        "grim_only_without_compromised":
            fit([c for c in multi if c["opponent"] == "grim"
                 and not c["compromised"]]),
        "tft_only": fit([c for c in multi if c["opponent"] == "tft"]),
    }


# --------------------------------------------------------------------------
# A. the dose-response, one axes per opponent
# --------------------------------------------------------------------------

def panel_a(ax, rows, opp, n_bins):
    sel_opp = [r for r in rows if r["opponent"] == opp]
    rec, ends = {}, []
    for marker, ls, lw, ms in PANEL_A_MARKERS:
        rec[marker] = {}
        for cond in CONTRAST_CONDS:
            col = CONDITION[cond][1]
            sel = [r for r in sel_opp if r["condition"] == cond]
            xs, ys, es, ns = [], [], [], []
            for b in range(n_bins):
                s = [r for r in sel if r["_bin"] == b]
                if not s:
                    continue
                k = sum(r[f"m_{marker}"] for r in s)
                xs.append(float(np.median([r["n_chars"] for r in s])))
                ys.append(k / len(s))
                es.append(binom_se(k, len(s)))
                ns.append(len(s))
            rec[marker][cond] = {"median_chars": xs, "rate": ys,
                                 "binomial_se": es, "n_blocks": ns}
            ax.errorbar(xs, ys, yerr=es, color=col, lw=lw, ls=ls, zorder=3,
                        marker=OPP_MARK[opp], ms=ms, mec=SURF, mew=1.2,
                        elinewidth=1.1, capsize=2.6, ecolor=col)
            if marker == PRIMARY:
                ends.append([xs[-1], ys[-1], cond, col])
    # Direct-label each arm at its right end, nudged apart when the two land on
    # top of each other. Identity is never carried by colour alone.
    ends.sort(key=lambda e: e[1])
    for i in range(1, len(ends)):
        if ends[i][1] - ends[i - 1][1] < 0.085:
            ends[i][1] = ends[i - 1][1] + 0.085
    for x, y, cond, col in ends:
        ax.annotate(CONDITION[cond][0], (x, y), textcoords="offset points",
                    xytext=(8, 0), va="center", fontsize=7.8, color=col,
                    fontweight="bold", zorder=6, annotation_clip=False)
    ax.annotate(f"solid line, filled {'circles' if opp == 'grim' else 'squares'} "
                f"= {PRIMARY}\ndashed line = {FLOOR_MARKER} (floor control)",
                (0.03, 0.055), xycoords="axes fraction", ha="left",
                fontsize=7.2, color=MUT, zorder=6)
    ax.set_xscale("log")
    # `text.parse_math` is off, so matplotlib's default log formatter emits its
    # mathtext SOURCE as literal text on every MINOR tick. Fixing the majors
    # alone does not stop that; the minor formatter has to be nulled.
    ax.set_xticks([200, 400, 700, 1300, 2800])
    ax.set_xticklabels(["200", "400", "700", "1300", "2800"])
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.set_xlim(155, 7000)          # headroom for the right-edge labels
    ax.set_ylim(-0.04, 1.06)
    return rec


def within_bin_gaps(rows, opp, n_bins, drop_compromised_cell=None):
    """Pooled eg-minus-nohole gap inside each global length bin.

    NOT the seed-paired contrast in panel D: this pools the training seeds
    inside a bin before differencing, so a single cell can carry it. The
    `drop_compromised_cell` variant exists to show exactly that.
    """
    out = {}
    for marker, *_ in PANEL_A_MARKERS:
        prof = []
        for b in range(n_bins):
            rec = {"bin": b}
            for cond in CONTRAST_CONDS:
                s = [r for r in rows
                     if r["opponent"] == opp and r["condition"] == cond
                     and r["_bin"] == b
                     and f"{r['arm']}|{r['train_seed']}" != drop_compromised_cell]
                rec[cond] = (sum(r[f"m_{marker}"] for r in s) / len(s)) if s else None
                rec[f"n_blocks_{cond}"] = len(s)
            rec["gap_eg_minus_nohole"] = (
                None if rec["eg"] is None or rec["nohole"] is None
                else rec["eg"] - rec["nohole"])
            prof.append(rec)
        out[marker] = prof
    return out


# --------------------------------------------------------------------------
# B / C. the per-cell scatters
# --------------------------------------------------------------------------

def scatter_panel(ax, cells, ykey, ylab, corr, pending_labels, note,
                  reserved, extra_note=None):
    multi = [c for c in cells if not c["single_seed_arm"]]
    xs = [c["mean_chars"] for c in multi]
    ys = [c[ykey] for c in multi]
    allx = [c["mean_chars"] for c in cells]
    ally = [c[ykey] for c in cells]

    xlo, xhi = min(allx), max(allx)
    ylo, yhi = min(ally), max(ally)
    xpad = 0.11 * (xhi - xlo)
    ax.set_xlim(xlo - xpad, xhi + xpad)
    # Asymmetric headroom. Every cell label sits above its point and the panel
    # note sits top-left, and the highest cells are all on the right, so the
    # top margin has to be the generous one.
    ax.set_ylim(ylo - 0.16 * (yhi - ylo), yhi + 0.34 * (yhi - ylo))

    # Two OLS lines: all multi-seed cells, and the same set without the
    # compromised cell. Both are drawn because they differ, and drawing only
    # one would be a choice about which story to tell. Neither is a model;
    # a dozen cells cannot support a test.
    for key, ls, lw, alpha in (
            ("multi_seed_cells", (0, (6, 3)), 1.4, 0.95),
            ("multi_seed_cells_without_compromised", (0, (1.6, 2.2)), 1.4, 0.95)):
        f = corr[key]
        if f["slope"] is None:
            continue
        gx = np.linspace(*ax.get_xlim(), 50)
        ax.plot(gx, f["slope"] * gx + f["intercept"], color=MUT, lw=lw,
                ls=ls, alpha=alpha, zorder=2)

    for c in cells:
        col = CONDITION[c["condition"]][1]
        size = 118
        ax.scatter([c["mean_chars"]], [c[ykey]], s=size,
                   marker=OPP_MARK[c["opponent"]], color=col,
                   edgecolor=SURF, linewidth=1.4, zorder=4)
        if c["single_seed_arm"]:
            # Drawn hollow-ringed and named so it can never be mistaken for a
            # cell that contributes to a contrast or a fit.
            size = 300
            ax.scatter([c["mean_chars"]], [c[ykey]], s=size, facecolor="none",
                       edgecolor=col, linewidth=1.1, linestyle=(0, (1.2, 1.6)),
                       zorder=3)
        if c["empty_answer_hazard"]:
            size = 470 if c["compromised"] else 330
            ax.scatter([c["mean_chars"]], [c[ykey]], s=size, facecolor="none",
                       edgecolor=INK, linewidth=1.7 if c["compromised"] else 1.1,
                       linestyle=(0, (2.4, 1.8)), zorder=3)
        tag = f"{c['opponent']} {c['condition']} s{c['train_seed']}"
        if c["single_seed_arm"]:
            tag += "  (1 seed)"
        if c["empty_answer_hazard"]:
            tag += f"  ({c['empty_answer_rate'] * 100:.0f}% empty)"
        pending_labels.append((ax, c["mean_chars"], c[ykey], tag,
                               INK if c["empty_answer_hazard"] else INK2,
                               math.sqrt(size) / 2.0 + 2.0))

    f_all = corr["multi_seed_cells"]
    f_cut = corr["multi_seed_cells_without_compromised"]
    lines = [
        f"{f_all['n_cells']} cells with a paired arm:  "
        f"Pearson r = {f_all['pearson_r']:.3f}   rho = {f_all['spearman_rho']:.3f}   (long dash)",
        f"dropping grim nohole s1:  {f_cut['n_cells']} cells,  "
        f"r = {f_cut['pearson_r']:.3f}   rho = {f_cut['spearman_rho']:.3f}   (dotted)",
    ]
    if extra_note:
        lines.append(extra_note)
    lines.append("descriptive only: n is far too small to carry a test")
    ax.annotate("\n".join(lines), (0.985, 0.030), xycoords="axes fraction",
                ha="right", fontsize=7.2, color=INK2, zorder=6)
    ax.annotate(note, (0.015, 0.972), xycoords="axes fraction", va="top",
                fontsize=7.2, color=MUT, zorder=6)
    # Both text blocks are declared as no-go areas so the cell labels, which
    # are placed after the draw, route around them instead of landing on top.
    reserved.setdefault(ax, []).extend([
        ("topleft", 0.015, 0.972, note.split("\n"), 7.2),
        ("bottomright", 0.985, 0.030, lines, 7.2)])
    ax.set_ylabel(ylab, fontsize=9, color=INK2)
    return {"y": ykey, "correlations": corr,
            "n_points_drawn": len(cells), "n_points_in_fit": len(multi),
            "x_span_chars": [float(min(allx)), float(max(allx))]}


CHAR_W = 0.56      # mean advance width of this font, in units of the font size
LINE_H = 1.32


def place_labels(fig, pending, reserved):
    """Put the cell labels down without letting them pile up.

    Needs real axes geometry, so it runs after `fig.canvas.draw()`. Greedy:
    take each point from the top down and use the first vertical offset whose
    label clears every obstacle -- the other labels already placed, the plotted
    markers themselves, and the panel's two reserved text blocks.
    """
    per_axes = {}
    for ax, x, y, text, col, rad in pending:
        per_axes.setdefault(ax, []).append((x, y, text, col, rad))
    for ax, items in per_axes.items():
        bb = ax.get_window_extent()
        pt_per_px = 72.0 / fig.dpi
        w_pt, h_pt = bb.width * pt_per_px, bb.height * pt_per_px
        (x0, x1), (y0, y1) = ax.get_xlim(), ax.get_ylim()
        fs = 6.6

        def to_pt(x, y):
            return ((x - x0) / (x1 - x0) * w_pt, (y - y0) / (y1 - y0) * h_pt)

        # Obstacles as (centre_x, centre_y, half_width, half_height) in points.
        # The markers count: several carry a hazard or single-seed ring that is
        # four times the radius of the dot inside it.
        obstacles = [(*to_pt(x, y), rad, rad) for x, y, _, _, rad in items]
        for anchor, ax_f, ay_f, lines, bfs in reserved.get(ax, []):
            bw = CHAR_W * bfs * max(len(s) for s in lines)
            bh = LINE_H * bfs * len(lines)
            right = ax_f * w_pt if anchor == "bottomright" else ax_f * w_pt + bw
            top = ay_f * h_pt if anchor == "topleft" else ay_f * h_pt + bh
            obstacles.append((right - bw / 2.0, top - bh / 2.0,
                              bw / 2.0, bh / 2.0))

        for x, y, text, col, rad in sorted(items, key=lambda t: -t[1]):
            px, py = to_pt(x, y)
            half_w, half_h = CHAR_W * fs * len(text) / 2.0, fs * 0.78
            # Held inside the panel. A label on an edge cell would otherwise
            # spill past the axes and land on the neighbouring panel's ticks.
            cx = min(max(px, half_w + 2.0), w_pt - half_w - 2.0)
            base = rad + 3.0
            for step in range(12):
                dy = (base + 9.0 * (step // 2)) * (1 if step % 2 == 0 else -1)
                cy = py + dy + (half_h if dy > 0 else -half_h)
                if all(abs(cx - qx) > half_w + qw or abs(cy - qy) > half_h + qh
                       for qx, qy, qw, qh in obstacles):
                    break
            obstacles.append((cx, cy, half_w, half_h))
            # A label shoved this far from its point needs a leader, or the
            # reader has to guess which marker it belongs to.
            far = abs(dy) > 20.0 or abs(cx - px) > rad
            arrow = (dict(arrowstyle="-", color=MUT, lw=0.6, shrinkA=1.0,
                          shrinkB=rad) if far else None)
            ax.annotate(text, (x, y), textcoords="offset points",
                        xytext=(cx - px, dy), ha="center",
                        va="bottom" if dy > 0 else "top",
                        fontsize=fs, color=col, zorder=7,
                        arrowprops=arrow, annotation_clip=False)


# --------------------------------------------------------------------------
# D. raw vs length-stratified delta, both opponents
# --------------------------------------------------------------------------

def panel_d(ax, agg):
    rec, yticks, ylabels = {}, [], []
    row, group_rows = 0.0, {}
    for opp in OPPONENTS:
        con = agg["contrasts"][opp]
        rec[opp] = {}
        top = row
        for marker in PANEL_D_MARKERS:
            e = con[marker]
            bse = e["binomial_se_pooled"]
            rec[opp][marker] = {
                "raw_delta_mean": e["raw_delta_mean"],
                "raw_delta_se_between_seed": e["raw_delta_se"],
                "strat_delta_mean": e["strat_delta_mean"],
                "strat_delta_se_between_seed": e["strat_delta_se"],
                "binomial_se_pooled_sampling_floor": bse,
                "ratio_raw_se_over_binomial": (e["raw_delta_se"] / bse) if bse else None,
                "ratio_strat_se_over_binomial": (e["strat_delta_se"] / bse) if bse else None,
                "per_seed_raw": e["per_seed_delta"],
                "per_seed_strat": e["per_seed_strat"],
                "n_seeds": e["n_seeds"],
                "is_floor_control": marker == FLOOR_MARKER,
            }
            for tag, y, col, mk, fc in (
                    ("raw", row + 0.20, INK2, "o", SURF),
                    ("strat", row - 0.20, INK, "s", INK)):
                mean = e["raw_delta_mean"] if tag == "raw" else e["strat_delta_mean"]
                se = e["raw_delta_se"] if tag == "raw" else e["strat_delta_se"]
                ax.errorbar([mean], [y], xerr=[se], color=col, marker=mk,
                            ms=6.5, mfc=fc, mec=col, mew=1.5, lw=0,
                            elinewidth=1.6, capsize=3.4, ecolor=col, zorder=4)
                pts = e["per_seed_delta"] if tag == "raw" else e["per_seed_strat"]
                ax.scatter(pts, [y] * len(pts), s=13, color=MUT, alpha=0.85,
                           zorder=3, marker="|", linewidth=1.2)
            # The sampling floor, drawn NEUTRAL. It used to be painted in the
            # hidden-horizon blue; `tft/inf` has landed, so that colour is
            # spoken for and the floor gets a grey that means nothing else.
            if bse:
                ax.plot([e["strat_delta_mean"] - bse, e["strat_delta_mean"] + bse],
                        [row - 0.44] * 2, color=MUT, lw=2.4,
                        solid_capstyle="butt", zorder=3)
            yticks.append(row)
            ylabels.append(marker + ("\n[FLOOR CONTROL]"
                                     if marker == FLOOR_MARKER else ""))
            row -= 1.0
        group_rows[opp] = (top, row + 1.0)
        row -= 0.7

    ax.axvline(0.0, color=INK, lw=1.6, zorder=2)
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels, fontsize=8.2, color=INK2)
    ax.set_ylim(row - 0.85, 0.9)
    ax.grid(True, axis="x", color=GRID, lw=0.8, zorder=0)
    ax.grid(False, axis="y")

    span = [v for opp in OPPONENTS for m in PANEL_D_MARKERS
            for e in [agg["contrasts"][opp][m]]
            for v in e["per_seed_delta"] + e["per_seed_strat"] +
            [e["raw_delta_mean"] - e["raw_delta_se"],
             e["raw_delta_mean"] + e["raw_delta_se"],
             e["strat_delta_mean"] - e["strat_delta_se"],
             e["strat_delta_mean"] + e["strat_delta_se"]]]
    pad = 0.06 * (max(span) - min(span))
    xlo, xhi = min(span) - pad, max(span) + pad
    ax.set_xlim(xlo, xhi + 0.10 * (xhi - xlo))   # room for the group tags

    for opp, (top, bot) in group_rows.items():
        ax.axhspan(bot - 0.62, top + 0.55, color=GRID, alpha=0.28, zorder=0)
        ax.annotate(f"vs {opp.upper()}", (0.992, (top + 0.42)),
                    xycoords=("axes fraction", "data"), ha="right", va="top",
                    fontsize=9.5, color=INK, fontweight="bold", zorder=6)

    # The floor-to-honest-bar ratio, read off the data at render time. It is
    # not one number: it runs across the markers, and a single hardcoded
    # multiplier would be wrong for most of them.
    ratios = [v for opp in rec for m in rec[opp]
              for v in (rec[opp][m]["ratio_raw_se_over_binomial"],
                        rec[opp][m]["ratio_strat_se_over_binomial"])
              if v is not None]
    n_seeds = max(rec[o][m]["n_seeds"] for o in rec for m in rec[o])
    ax.annotate(
        "open circle = raw delta        filled square = length-stratified\n"
        f"short grey ticks = the {n_seeds} individual training-seed deltas\n"
        "grey hairline under each row = pooled binomial SE. That is the "
        "SAMPLING FLOOR,\n"
        f"not the error bar on the effect: it is {min(ratios):.1f}x to "
        f"{max(ratios):.1f}x smaller than the between-seed bar.",
        (0.015, 0.028), xycoords="axes fraction", ha="left", fontsize=7.2,
        color=INK2, zorder=6)
    return rec, {"min": float(min(ratios)), "max": float(max(ratios)),
                 "n_ratios": len(ratios), "n_seeds": n_seeds}


def panel_d_length(ax, agg):
    """The arm-level LENGTH delta in chars -- the mechanism as a quantity.

    Same seed-paired construction and same between-seed bar as panel D, but in
    characters rather than rate units, which is why it cannot share panel D's
    x-axis and gets its own.
    """
    rec = {}
    ys = {"grim": 1.0, "tft": 0.0}
    for opp in OPPONENTS:
        nh = agg["arms"][f"{opp}/nohole"]["mean_chars"]
        eg = agg["arms"][f"{opp}/eg"]["mean_chars"]
        per_seed = [e - n for e, n in zip(eg["per_seed"], nh["per_seed"])]
        st = mean_sd_se(per_seed)
        rec[opp] = {
            "nohole_mean_chars": nh["mean"], "eg_mean_chars": eg["mean"],
            "nohole_per_seed": nh["per_seed"], "eg_per_seed": eg["per_seed"],
            "per_seed_delta_chars": per_seed,
            "delta_chars_mean": st["mean"], "delta_chars_sd": st["sd"],
            "delta_chars_se_between_seed": st["se"], "n_seeds": st["n"],
            "pct_of_nohole": 100.0 * st["mean"] / nh["mean"],
        }
        y = ys[opp]
        ax.barh([y], [st["mean"]], height=0.30, color=ORANGE, alpha=0.75,
                edgecolor=ORANGE, linewidth=1.2, zorder=3)
        ax.errorbar([st["mean"]], [y], xerr=[st["se"]], color=INK, lw=0,
                    elinewidth=1.6, capsize=3.6, ecolor=INK, zorder=5)
        ax.scatter(per_seed, [y] * len(per_seed), s=15, color=INK2, alpha=0.9,
                   zorder=6, marker="|", linewidth=1.3)
        # Right-aligned above the bar: the zero line runs the full height of
        # this panel and centred text would sit across it.
        ax.annotate(f"vs {opp.upper()}\n{st['mean']:+.0f} +- {st['se']:.0f} chars\n"
                    f"({rec[opp]['pct_of_nohole']:+.0f}% of baseline)",
                    (0.98, y + 0.24), xycoords=("axes fraction", "data"),
                    ha="right", va="bottom", fontsize=7.8, color=INK,
                    zorder=7)
    # Stopped short of the bottom so it does not run through the key below.
    ax.axvline(0.0, ymin=0.26, ymax=1.0, color=INK, lw=1.6, zorder=2)
    ax.set_yticks([])
    ax.set_ylim(-0.78, 1.70)
    ax.grid(True, axis="x", color=GRID, lw=0.8, zorder=0)
    ax.grid(False, axis="y")
    allv = [v for o in rec for v in rec[o]["per_seed_delta_chars"]]
    pad = 0.10 * (max(allv) - min(allv))
    ax.set_xlim(min(allv) - pad, max(allv) + pad)
    grim_spread = (max(rec["grim"]["per_seed_delta_chars"])
                   - min(rec["grim"]["per_seed_delta_chars"]))
    ns = rec["grim"]["n_seeds"]
    n_up = sum(1 for v in rec["grim"]["per_seed_delta_chars"] if v > 0)
    n_dn_tft = sum(1 for v in rec["tft"]["per_seed_delta_chars"] if v < 0)
    ax.annotate(f"orange bar = eg minus nohole, formed within\n"
                f"a training seed. Grey ticks = the {ns} seeds:\n"
                f"against grim the near-zero mean hides a\n"
                f"{grim_spread:,.0f}-char spread, with {n_up} of the {ns} going\n"
                f"the other way. Against tft {n_dn_tft} of {ns} move down.",
                (0.02, 0.015), xycoords="axes fraction", ha="left",
                fontsize=6.9, color=INK2, zorder=6)
    return rec


# --------------------------------------------------------------------------

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=("Render fig2_length_confound: why a naive marker rate "
                     "cannot answer whether the endgame penalty suppresses "
                     "endgame reasoning."),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    ap.add_argument("--outdir", type=Path, default=HERE,
                    help="where the png and json are written")
    ap.add_argument("--dpi", type=int, default=150,
                    help="png resolution; the repo renders figures at 150")
    ap.add_argument("--stem", default="fig2_length_confound",
                    help="output stem, shared by the png and its paired json")
    args = ap.parse_args(argv)

    rows, agg, edges = load()
    n_bins = agg["meta"]["length_bins"]["n_bins"]
    cells = cell_table(agg)
    hazards = [c for c in cells if c["empty_answer_hazard"]]
    compromised = [c for c in cells if c["compromised"]]
    comp_key = compromised[0]["cell"] if compromised else None
    single = [c for c in cells if c["single_seed_arm"]]

    corr_marker = correlations(cells, PRIMARY)
    corr_behaviour = correlations(cells, "endgame_rate")

    fig = plt.figure(figsize=(19.6, 13.4))
    fig.patch.set_facecolor("#f9f9f7")
    gs = fig.add_gridspec(2, 12)
    axA = {"grim": fig.add_subplot(gs[0, 0:4]),
           "tft": fig.add_subplot(gs[0, 4:8])}
    axB = fig.add_subplot(gs[0, 8:12])
    axC = fig.add_subplot(gs[1, 0:4])
    # Column 4 is left empty: panel D's row labels are long enough that
    # without a gutter they reach back across panel C's cell labels.
    axD = fig.add_subplot(gs[1, 5:9])
    axDL = fig.add_subplot(gs[1, 9:12])
    reserved = {}

    # ------------------------------------------------------------------- A
    rec_a, gaps = {}, {}
    for opp in OPPONENTS:
        rec_a[opp] = panel_a(axA[opp], rows, opp, n_bins)
        gaps[opp] = {"pooled_all_cells": within_bin_gaps(rows, opp, n_bins)}
    if comp_key:
        gaps["grim"]["pooled_without_compromised_cell"] = within_bin_gaps(
            rows, "grim", n_bins, drop_compromised_cell=comp_key)

    # The single worst illustration that a pooled within-bin gap can be one
    # cell: quoted on the panel, computed here, never hardcoded.
    swing = None
    if comp_key:
        a = gaps["grim"]["pooled_all_cells"][PRIMARY]
        b = gaps["grim"]["pooled_without_compromised_cell"][PRIMARY]
        pairs = [(i, x["gap_eg_minus_nohole"], y["gap_eg_minus_nohole"])
                 for i, (x, y) in enumerate(zip(a, b))
                 if x["gap_eg_minus_nohole"] is not None
                 and y["gap_eg_minus_nohole"] is not None]
        i, g0, g1 = max(pairs, key=lambda t: abs(t[2] - t[1]))
        swing = {"bin": i, "gap_all_cells": g0,
                 "gap_without_compromised": g1, "swing": g1 - g0}

    style(axA["grim"], "A1 - vs GRIM: both arms ride the same steep length curve",
          "share of reasoning blocks hitting the marker",
          "median reasoning-block length in the bin (chars, log scale)",
          f"{n_bins} GLOBAL n_chars quantiles, the bins the stratified contrast\n"
          f"standardises to. Bars are BINOMIAL SE inside a length bin, where\n"
          f"the remaining question really is a sampling one.")
    note_tft = ("same global quintiles. At MATCHED length the eg arm sits only\n"
                "slightly below baseline; most of its raw marker drop is that\n"
                "its blocks are shorter, so its mass moves LEFT along the same\n"
                "curve. That leftward shift is what panel D2 measures.")
    style(axA["tft"], "A2 - vs TFT: same curve, and the eg arm has moved down it",
          "share of reasoning blocks hitting the marker",
          "median reasoning-block length in the bin (chars, log scale)",
          note_tft)
    for opp in OPPONENTS:
        swing_txt = ""
        if opp == "grim" and swing:
            swing_txt = (f" One cell can carry it: dropping the compromised\n"
                         f"grim nohole s1 moves the bin-{swing['bin']} gap from "
                         f"{swing['gap_all_cells']:+.3f} to "
                         f"{swing['gap_without_compromised']:+.3f}.")
        axA[opp].annotate(
            "The within-bin arm gap here POOLS the training seeds, so it is\n"
            "NOT the seed-paired stratified estimate; that one is panel D." + swing_txt,
            (0.5, -0.155), xycoords="axes fraction", ha="center", va="top",
            fontsize=7.0, color=MUT, zorder=6, annotation_clip=False)

    # ------------------------------------------------------------------- B
    pending = []
    rec_b = scatter_panel(
        axB, cells, PRIMARY, "endgame_defect_plan rate (cell mean)",
        corr_marker, pending,
        "one point per (opponent, arm, training seed). Circle = grim,\n"
        "square = tft; colour = condition; every point is named.\n"
        "Heavy dashed ring = empty-answer hazard, see the header.\n"
        "Dotted ring = single-seed arm, excluded from both fits.",
        reserved)
    style(axB, "B - Cells order by verbosity, not by arm",
          "endgame_defect_plan rate (cell mean)",
          "mean reasoning-block length in the cell (chars)")

    # ------------------------------------------------------------------- C
    g6 = corr_behaviour["grim_only"]
    rec_c = scatter_panel(
        axC, cells, "endgame_rate", "endgame_rate (episode mean in the cell)",
        corr_behaviour, pending,
        "late-game betrayal, per episode then averaged over the cell.\n"
        "The length axis is not a nuisance confined to the reasoning\n"
        "side -- but across 13 cells it is a looser relationship than\n"
        "the six grim cells alone implied.",
        reserved,
        extra_note=(f"grim alone ({g6['n_cells']} cells) gives "
                    f"r = {g6['pearson_r']:.3f}, rho = {g6['spearman_rho']:.3f}; "
                    f"adding tft weakens it"))
    style(axC, "C - Verbosity tracks the BEHAVIOUR too, but less tightly\n"
               "than the grim cells alone suggested",
          "endgame_rate (episode mean in the cell)",
          "mean reasoning-block length in the cell (chars)")

    # ------------------------------------------------------------------- D
    # style() FIRST on the forest panels: it turns the y-grid on and repaints
    # the ticks, both of which the drawers then have to undo for this layout.
    style(axD, "D - Stratifying for length removes most of the tft effect,\n"
               "and the floor control moves with it",
          "", "delta (eg minus nohole), formed within a training seed",
          None)
    rec_d, ratio_range = panel_d(axD, agg)
    style(axDL, "D2 - the mechanism itself,\nin characters",
          "", "delta in mean block length (chars)", None)
    rec_dl = panel_d_length(axDL, agg)

    # --------------------------------------------------------------- header
    n_ep = sum(c["n_episodes"] for c in cells)
    n_bl = sum(c["n_blocks"] for c in cells)
    span = [c["mean_chars"] for c in cells]
    tft_p = agg["contrasts"]["tft"][PRIMARY]
    tft_f = agg["contrasts"]["tft"][FLOOR_MARKER]
    grim_p = agg["contrasts"]["grim"][PRIMARY]
    removed = 100.0 * (1.0 - abs(tft_p["strat_delta_mean"])
                       / abs(tft_p["raw_delta_mean"]))
    dl_t, dl_g = rec_dl["tft"], rec_dl["grim"]

    fig.suptitle(f"Marker rates ride reasoning length - and against tft the "
                 f"endgame-penalty arm also writes "
                 f"{abs(dl_t['pct_of_nohole']):.0f}% less",
                 fontsize=13.5, color=INK, x=0.006, ha="left", y=0.994)
    header = [
        f"{n_ep} episodes / {n_bl:,} reasoning blocks / {len(cells)} cells, "
        f"checkpoint step 35. A marker is a binary regex hit on ONE reasoning "
        f"block, so a longer block is mechanically more likely to hit -- and "
        f"per-cell mean length spans {min(span):.0f} to {max(span):.0f} chars "
        f"({max(span) / min(span):.1f}x).",

        f"THE MECHANISM. Against TFT the knob shortens the reasoning: "
        f"{dl_t['nohole_mean_chars']:.0f} chars under nohole vs "
        f"{dl_t['eg_mean_chars']:.0f} under eg, seed-paired "
        f"{dl_t['delta_chars_mean']:+.0f} +- "
        f"{dl_t['delta_chars_se_between_seed']:.0f} "
        f"({dl_t['pct_of_nohole']:+.0f}%). Raw {PRIMARY} delta "
        f"{tft_p['raw_delta_mean']:+.3f} +- {tft_p['raw_delta_se']:.3f}, "
        f"length-stratified {tft_p['strat_delta_mean']:+.3f} +- "
        f"{tft_p['strat_delta_se']:.3f}: standardising for length removes "
        f"{removed:.0f}% of it.",

        f"AND WHAT SURVIVES IS NOT ENDGAME-SPECIFIC. The {FLOOR_MARKER} floor "
        f"control has no endgame stake, yet against tft it falls "
        f"{tft_f['raw_delta_mean']:+.3f} +- {tft_f['raw_delta_se']:.3f} raw and "
        f"{tft_f['strat_delta_mean']:+.3f} +- {tft_f['strat_delta_se']:.3f} "
        f"stratified, indistinguishable from the endgame marker's "
        f"{tft_p['strat_delta_mean']:+.3f}. Against GRIM there is no arm length "
        f"difference ({dl_g['nohole_mean_chars']:.0f} vs "
        f"{dl_g['eg_mean_chars']:.0f}, {dl_g['delta_chars_mean']:+.0f} +- "
        f"{dl_g['delta_chars_se_between_seed']:.0f}) and nothing survives "
        f"({grim_p['strat_delta_mean']:+.3f} +- "
        f"{grim_p['strat_delta_se']:.3f}).",

        f"ERROR BARS. A is binomial, a sampling question inside a fixed length "
        f"bin. B and C plot cells and carry no bar: the scatter of the points "
        f"IS the between-seed variation. D and D2 are between TRAINING SEED, "
        f"sd/sqrt({ratio_range['n_seeds']}), on the seed-paired delta -- the "
        f"only admissible bar on an arm difference, and "
        f"{ratio_range['min']:.1f}x to "
        f"{ratio_range['max']:.1f}x wider than the binomial floor drawn beside "
        f"it.",
    ]
    haz = "; ".join(
        f"{c['opponent']}/{c['condition']} s{c['train_seed']} at "
        f"{c['empty_answer_rate'] * 100:.1f}% empty (invalid_rate reads "
        f"{c['invalid_rate']:.3f})" for c in hazards)
    comp = compromised[0] if compromised else None
    if comp:
        header.append(
            f"HAZARD CELLS, ringed in B and C. Decision turns with an empty "
            f"answer: {haz}. The repo's cell gate is invalid_rate > "
            f"{agg['meta']['max_invalid_rate_per_cell']}, which both cells "
            f"pass, so it does not catch this. "
            f"{comp['opponent']}/{comp['condition']} s{comp['train_seed']} is "
            f"the worst and is treated as COMPROMISED: shortest of the six grim "
            f"cells at {comp['mean_chars']:.0f} chars (rank "
            f"{comp['length_rank_of_all_cells']} of {len(cells)} overall), "
            f"lowest endgame_rate at {comp['endgame_rate']:.3f}. Every "
            f"correlation here is reported with AND without it.")
    header.append(
        f"COVERAGE. grim and tft each have nohole and eg at 3 training seeds x "
        f"48 episodes. "
        + (", ".join(f"{c['opponent']}/{c['condition']} s{c['train_seed']}"
                     for c in single))
        + f" exists at ONE seed: it is drawn ringed and named in B and C and "
          f"enters no contrast and no fit. The five remaining inf cells have no "
          f"episodes on disk. Nothing on this figure is a causal test; three "
          f"training seeds per arm cannot carry one.")

    # Wrapped to the page rather than trusted to fit: these lines carry
    # computed numbers whose width is not known until render time, and an
    # over-long one runs off the right edge instead of being clipped visibly.
    y = 0.9665
    for line in header:
        for seg in textwrap.wrap(line, width=288):
            fig.text(0.006, y, seg, fontsize=8.0, color=INK2, ha="left")
            y -= 0.0106

    fig.tight_layout(rect=[0.004, 0.004, 0.995, y - 0.008])
    fig.subplots_adjust(hspace=0.42, wspace=0.42)
    fig.canvas.draw()
    place_labels(fig, pending, reserved)

    args.outdir.mkdir(parents=True, exist_ok=True)
    out_png = args.outdir / f"{args.stem}.png"
    fig.savefig(out_png, dpi=args.dpi, facecolor=fig.get_facecolor())
    print(f"[fig] wrote {out_png}")

    # ------------------------------------------------------------------ JSON
    pooled_quintiles = {}
    for marker in sorted({m for m, *_ in PANEL_A_MARKERS} | set(PANEL_D_MARKERS)):
        prof = []
        for b in range(n_bins):
            s = [r for r in rows if r["_bin"] == b]
            k = sum(r[f"m_{marker}"] for r in s)
            prof.append({"bin": b, "n_blocks_all_arms": len(s),
                         "median_chars": float(np.median([r["n_chars"] for r in s])),
                         "rate": k / len(s), "binomial_se": binom_se(k, len(s))})
        pooled_quintiles[marker] = prof

    payload = {
        "figure": out_png.name,
        "question": ("Does the endgame-penalty reward knob suppress endgame "
                     "REASONING, or only the behaviour? This figure does not "
                     "answer that; it shows why the naive marker rate cannot."),
        "answer": (
            f"The marker rate is largely a length measurement. Against tft the "
            f"knob shortens reasoning by "
            f"{dl_t['delta_chars_mean']:+.0f} +- "
            f"{dl_t['delta_chars_se_between_seed']:.0f} chars "
            f"({dl_t['pct_of_nohole']:+.0f}%), the raw {PRIMARY} delta is "
            f"{tft_p['raw_delta_mean']:+.3f} +- {tft_p['raw_delta_se']:.3f} and "
            f"the length-stratified delta is {tft_p['strat_delta_mean']:+.3f} "
            f"+- {tft_p['strat_delta_se']:.3f}, so length standardisation "
            f"removes {removed:.0f}% of it. What remains is not "
            f"endgame-specific: the {FLOOR_MARKER} floor control's stratified "
            f"delta is {tft_f['strat_delta_mean']:+.3f} +- "
            f"{tft_f['strat_delta_se']:.3f}. Against grim there is no arm "
            f"length difference and no surviving effect."),
        "caveat": ("Three training seeds per arm. Nothing here is a causal "
                   "test; the panels are descriptive and the correlations are "
                   "reported on 5 to 13 cells."),
        "provenance": {
            "blocks": str(BLOCKS),
            "aggregates": str(MARKERS_JSON),
            "upstream_source": agg["meta"]["source"],
            "generated_utc_of_aggregates": agg["meta"]["generated_utc"],
            "n_lines_read": agg["meta"]["n_lines_read"],
        },
        "coverage": {
            "opponents_plotted": OPPONENTS,
            "cells_plotted": len(cells),
            "n_episodes_plotted": n_ep,
            "n_blocks_plotted": n_bl,
            "episodes_per_cell": 48,
            "full_wave_coverage": agg["coverage"],
            "single_seed_cells_drawn_but_never_in_a_contrast_or_fit":
                [c["cell"] for c in single],
            "cells_with_no_episodes": [e["cell"] for e in agg["meta"]["cells_excluded"]],
        },
        "hazards": {
            "empty_answer_rate_threshold_flagged": EMPTY_HAZARD,
            "compromised_threshold": EMPTY_COMPROMISED,
            "repo_gate": ("cells are gated on invalid_rate > "
                          f"{agg['meta']['max_invalid_rate_per_cell']}, which "
                          "both flagged cells pass; the gate does not see empty "
                          "answers"),
            "flagged_cells": [
                {"cell": c["cell"], "empty_answer_rate": c["empty_answer_rate"],
                 "invalid_rate": c["invalid_rate"],
                 "mean_chars": c["mean_chars"],
                 "length_rank_of_all_cells": c["length_rank_of_all_cells"],
                 "endgame_rate": c["endgame_rate"],
                 "endgame_defect_plan": c["endgame_defect_plan"],
                 "compromised": c["compromised"]} for c in hazards],
            "empty_answer_rate_all_cells":
                {c["cell"]: c["empty_answer_rate"] for c in cells},
            "empty_answer_rate_by_arm_mean": {
                arm: float(np.mean([c["empty_answer_rate"] for c in cells
                                    if c["arm"] == arm]))
                for arm in sorted({c["arm"] for c in cells})},
        },
        "error_bar_definitions": {
            "panel_A": "binomial SE within an (opponent, arm, length bin), sqrt(p(1-p)/n)",
            "panel_B": "none; each point is one (opponent, arm, train_seed) cell",
            "panel_C": "none; each point is one (opponent, arm, train_seed) cell",
            "panel_D": (f"between training seed, sd/sqrt(n_seeds) with "
                        f"n_seeds={ratio_range['n_seeds']}, on the per-seed "
                        f"paired delta"),
            "panel_D2": (f"between training seed, sd/sqrt("
                         f"{rec_dl['grim']['n_seeds']}), on the per-seed "
                         f"paired difference in mean block length"),
            "binomial_se_pooled": ("the SAMPLING FLOOR of the pooled block "
                                   "rates. NOT the error bar on the effect."),
            "floor_to_between_seed_ratio_range": ratio_range,
        },
        "length_bins": {
            "n_bins": n_bins, "edges_chars": edges,
            "note": (f"global quintiles cut once over all {n_bl} blocks, "
                     "identical to the bins the stratified contrast "
                     "standardises to"),
            "global_counts": agg["meta"]["length_bins"]["global_counts"],
            "skipped_small_cells": agg["meta"]["length_bins"]["skipped"],
        },
        "cells": cells,
        "verbosity": {
            "per_cell_mean_chars": {c["cell"]: c["mean_chars"] for c in cells},
            "per_cell_span_chars": [float(min(span)), float(max(span))],
            "per_cell_span_ratio": max(span) / min(span),
            "per_arm_mean_chars": {
                arm: {"mean_of_seed_means": agg["arms"][arm]["mean_chars"]["mean"],
                      "between_seed_sd": agg["arms"][arm]["mean_chars"]["sd"],
                      "between_seed_se": agg["arms"][arm]["mean_chars"]["se"],
                      "per_seed": agg["arms"][arm]["mean_chars"]["per_seed"],
                      "n_seeds": agg["arms"][arm]["n_seeds"]}
                for arm in sorted(agg["arms"])},
        },
        "panel_A_dose_response": rec_a,
        "panel_A_pooled_quintile_profile_all_arms": pooled_quintiles,
        # Exported rather than left for the reader to subtract off the plot,
        # and labelled for what it is: these POOL the training seeds inside a
        # bin, whereas panel D differences the arms WITHIN a seed first. The
        # seed-paired version is the one with an honest error bar, and the
        # `without_compromised_cell` variant shows a pooled gap being carried
        # by a single cell.
        "panel_A_within_bin_arm_gap_pooled_over_seeds": gaps,
        "panel_A_pooled_gap_single_cell_sensitivity": swing,
        "panel_B_cells_length_vs_marker": rec_b,
        "panel_C_cells_length_vs_behaviour": rec_c,
        "panel_D_raw_vs_stratified_delta": rec_d,
        "panel_D2_arm_level_length_delta_chars": rec_dl,
    }
    out_json = args.outdir / f"{args.stem}.json"
    out_json.write_text(json.dumps(payload, indent=1))
    print(f"[fig] wrote {out_json}")

    # console echo, so a run is self-checking without opening the png
    print(f"\ncells {len(cells)}  episodes {n_ep}  blocks {n_bl}")
    for lab, corr in (("length ~ endgame_defect_plan", corr_marker),
                      ("length ~ endgame_rate", corr_behaviour)):
        print(f"\n{lab}")
        for k, f in corr.items():
            if f["pearson_r"] is None:
                continue
            print(f"  {k:46s} n={f['n_cells']:2d}  r={f['pearson_r']:+.4f}  "
                  f"rho={f['spearman_rho']:+.4f}")
    print("\narm-level length delta (eg - nohole), seed paired")
    for opp in OPPONENTS:
        d = rec_dl[opp]
        print(f"  {opp:5s} {d['delta_chars_mean']:+8.1f} +- "
              f"{d['delta_chars_se_between_seed']:6.1f} chars "
              f"({d['pct_of_nohole']:+.1f}%)  per_seed="
              + ", ".join(f"{v:+.0f}" for v in d["per_seed_delta_chars"]))
    print("\ndeltas")
    for opp in OPPONENTS:
        for m, e in rec_d[opp].items():
            print(f"  {opp:5s} {m:22s} raw {e['raw_delta_mean']:+.4f} +- "
                  f"{e['raw_delta_se_between_seed']:.4f}   strat "
                  f"{e['strat_delta_mean']:+.4f} +- "
                  f"{e['strat_delta_se_between_seed']:.4f}   floor "
                  f"{e['binomial_se_pooled_sampling_floor']:.4f} "
                  f"({e['ratio_raw_se_over_binomial']:.1f}x / "
                  f"{e['ratio_strat_se_over_binomial']:.1f}x)")
    print(f"\nfloor ratio range {ratio_range['min']:.1f}x to "
          f"{ratio_range['max']:.1f}x over {ratio_range['n_ratios']} ratios")
    for c in hazards:
        print(f"hazard  {c['cell']:16s} empty={c['empty_answer_rate']:.3f} "
              f"invalid={c['invalid_rate']:.3f} chars={c['mean_chars']:.0f} "
              f"endgame_rate={c['endgame_rate']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
