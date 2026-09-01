#!/usr/bin/env python
"""Which of §7's three strands is a TRAINING effect, and which was already true of the untrained policy?

    /home/allie/venvs/tools/bin/python fig1_training_vs_cue.py

  fig1_training_vs_cue.png       the figure
  fig1_training_vs_cue.json      every number drawn in it

WHAT THIS ASKS. `0830-endgame-summary.md` §7 concludes that "the endgame is a
cue, not a disposition" from three strands: §7.1 a training-log window at steps
8-16 showing the `inf` arm's endgame collapse and an inverted concentration
ratio; §7.2 a within-checkpoint prompt swap on the step-35 `tft/inf` adapter;
§7.3 marker counts at that same checkpoint. §7.2 and §7.3 are single-checkpoint
contrasts and by construction say nothing about training at all. §7.1 is read
off the training log, but at steps 8-16 -- eight to sixteen gradient steps in.
None of the three ever looks at where the policy STARTED. This figure adds that
column and asks which of the section's numbers training actually produced.

THE LOAD-BEARING PREMISE, AND WHY STEP 0 IS THE UNTRAINED POLICY. In
`hole_exp/train_mixed.py` the loop samples rollouts, then applies the gradient
at `tc.optim_step(...)` (L844), and only then logs `m = {"step": step, ...}`
(L898) -- and the metrics in that dict are computed by `step_metrics_mixed`
from `recs`, the PRE-UPDATE rollouts that were just sampled. So the row keyed
`step: N` describes the policy as it was at the START of step N, before step
N's update. The row keyed `step: 0` therefore describes a policy that has taken
ZERO gradient steps. Anything already present in that row was not installed by
this training run. That single fact is what makes the question answerable, and
everything below rests on it.

WHAT THE ANSWER TURNS OUT TO BE. Almost everything §7 rests on is present at
step 0, before a single gradient step:

  * the `inf` endgame collapse. `endgame_rate` 0.068 (grim) and 0.046 (tft) at
    step 0, against the 0.054 and 0.039 that §7.1 published at steps 8-16. It
    is flat. Training did not remove the endgame from the `inf` arm; the
    scrubbed prompt did, on the first rollout ever sampled.
  * the concentration inversion, which §7.1 calls "the point, not the first
    column". At step 0 `inf` already sits at 0.22 against 0.71 (grim/base) and
    1.08 (tft/base). The inversion is a step-0 property.
  * `notices_unknown`, the manipulation check: 0.125 (grim) and 0.115 (tft)
    against 0.000 for every horizon-visible arm, AT STEP 0. The policy
    represents the absence of the horizon and says so before it is trained.
  * most of §3's marker suppression. `tft`'s `endgame_defect_plan` is -26.8% at
    step 0 against the -26.5% pooled 0-35 value the reasoning log published --
    i.e. all of it, with nothing left for training to have contributed.

THREE THINGS DO GENUINELY CHANGE OVER TRAINING, AND ONE OF THEM IS THE HEADLINE.

  1. Overall defection roughly halves in every arm. `exploit_rate` runs
     0.386 -> 0.169 (grim/base), 0.307 -> 0.159 (tft/base), 0.280 -> 0.124
     (grim/inf), 0.209 -> 0.120 (tft/inf).
  2. Final-window defection does NOT fall with it in the horizon-visible
     baselines: `endgame_rate` 0.269 -> 0.267 (grim/base) and 0.332 -> 0.371
     (tft/base). Training prunes non-endgame defection and SPARES the endgame,
     so the concentration index roughly doubles: 0.71 -> 1.61 and 1.08 -> 2.34.
     THIS IS THE HEADLINE. Training does not teach the endgame. It removes
     everything else, and the endgame is what is left standing.
  3. The endgame penalty's suppression against `tft` is genuinely trained. At
     step 0 the `eg` arm is indistinguishable from baseline (`endgame_rate`
     0.332 vs 0.300, concentration 1.08 vs 0.90); by steps 30-37 it is clearly
     separated (0.371 vs 0.146), with all three seeds moving down.

A FOURTH, FLAGGED AS THE WEAKEST. The concentration rise happens in the `inf`
arms too, from a far lower start: grim/inf 0.22 -> 0.70 by step 19, tft/inf
0.22 -> 0.66 -> 1.14 at n=1. So training installs something endgame-shaped even
with no stated horizon to key on. Treat this as a hint: three of the four `inf`
cells stop at step 18-20, so the rise is measured over a very short run and the
deepest point rests on one seed.

WHAT THIS REVISES, AND WHAT IT LEAVES ALONE. It does NOT contradict §7. §7 says
the endgame is a cue rather than a disposition, and finding the cue effect
fully formed in the untrained policy makes that conclusion STRONGER, not
weaker. What it revises is the EVIDENCE: §7.1's numbers were read at steps 8-16
and presented as though training produced them, and §7.2/§7.3 are
single-checkpoint by construction and never could have spoken to training. The
conclusion stands. The attribution to training does not.

THE INDEX IS AN INDEX, NOT A PROBABILITY. `endgame_rate` divides `n_late` by
the exogenous `window`, while `exploit_rate` is over all rounds. They do not
share a denominator, so endgame_rate/exploit_rate cannot be read as "the chance
a late decision is a betrayal". It also inherits the warning `hole_exp/core.py`
sets out at L725: the rate is not comparable across counterparts, because a
never-forgiving counterpart terminates the timeline after the first betrayal so
episodes that defected early never reach the window and are scored 0.0 rather
than undefined. The reliable read here is the WITHIN-ARM change over training,
where the denominator artefact is held fixed. Between-arm level differences are
weaker evidence and the figure says so where it draws them.

LAYOUT. Opponent is BLOCK POSITION, one band each, never hue -- so the
condition colours keep the meaning they have everywhere else in this study
(purple baseline, orange endgame penalty, blue hidden horizon, and blue is used
for nothing that is not the `inf` arm). Bands 1 and 2 share all three y-axes,
so a vertical difference between them is the effect of forgiveness and nothing
else. Every panel is direct-labelled; there are no colour-key legends.

EVERY NUMBER IS RECOMPUTED AT RENDER TIME from the dense training logs and from
`0826_think_curves/reasoning_markers.json`. Nothing here is a cached string.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import textwrap
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mticker  # noqa: E402

HERE = Path(__file__).resolve().parent

PURPLE, ORANGE, BLUE, RED = "#7a5bd6", "#eb6834", "#2a78d6", "#b5342a"
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
PAPER = "#f9f9f7"

RUNS_DEFAULT = "/shared/allie/think4/runs"
RUN_TMPL = "mixed_think4_nohole-think-{opp}_d1_s{seed}{suf}"

EG_KEY, XP_KEY = "train/endgame_rate", "train/exploit_rate"
# quantity name -> the key it is actually stored under in metrics.jsonl. The
# two are NOT the same string and reading a row with the short name silently
# yields None for every step, which draws an empty panel rather than raising.
QKEY = {"endgame_rate": EG_KEY, "exploit_rate": XP_KEY}

# Opponent is BLOCK POSITION. (key, band heading)
BANDS = [("grim", "vs GRIM  -  never forgives"),
         ("tft", "vs TIT-FOR-TAT  -  forgives on return")]

# (arm key, run-dir suffix, label, colour)
ARMS = [("base", "", "baseline", PURPLE),
        ("eg", "_eg2", "endgame penalty", ORANGE),
        ("inf", "_inf", "hidden horizon", BLUE)]
ARM_COL = {a: c for a, _, _, c in ARMS}
ARM_LAB = {a: l for a, _, l, _ in ARMS}

SEEDS = [0, 1, 2, 3]

# (name, lo, hi, tick label, why this window)
WINDOWS = [
    ("step0", 0, 0, "step 0\nUNTRAINED",
     "rollouts sampled before step 0's optim_step: zero gradient steps taken"),
    ("early", 8, 16, "8-16",
     "the window 0830-endgame-summary.md 7.1 published; deepest one every "
     "inf seed reaches"),
    ("mid", 16, 19, "16-19",
     "the deepest window three of the four inf seeds reach"),
    ("late", 30, 37, "30-37",
     "deepest window all base/eg seeds reach. No grim/inf cell reaches it and "
     "only tft/inf s1 does"),
]
WNAMES = [w[0] for w in WINDOWS]
QUANTS = [("endgame_rate", "endgame_rate"), ("exploit_rate", "exploit_rate"),
          ("concentration", "concentration index")]

# reasoning side: one seed, 192 blocks per point
MARKERS = [("backward_induction", "backward induction"),
           ("endgame_defect_plan", "plans to betray at the end"),
           ("endgame_hold", "plans to HOLD at the end")]
CHECK = "notices_unknown"
REAS_MARKERS = [m for m, _ in MARKERS] + [CHECK]
POOL_HI = 35          # the pooled window 0830-endgame-reasoning.md 3 published

SEED_MK = ["o", "s", "^", "D", "v", "P"]


# ------------------------------------------------------------------ helpers --

def wrap(text, width):
    """`fig.text` does not wrap and an over-long line runs off the paper.

    Explicit newlines are paragraph breaks and survive; everything else is
    refilled to `width`. Widths come from the figure geometry and the point
    size rather than a per-string guess, so editing a footer sentence cannot
    silently push it off the right edge.
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
    """Between-training-seed SE: sd(per-seed values, ddof=1)/sqrt(n).

    Undefined at n=1, which is the point: a one-seed cell carries no
    between-run spread and must never be drawn with a bar.
    """
    v = [x for x in v if x is not None]
    if len(v) < 2:
        return None
    return float(np.std(v, ddof=1) / np.sqrt(len(v)))


def style(ax, title, ylab, note=None, xlab=None):
    ax.set_title(title, fontsize=10.5, color=INK, loc="left", pad=8)
    ax.set_ylabel(ylab, fontsize=9, color=INK2)
    if xlab:
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
        ax.text(0.015, 0.978, note, transform=ax.transAxes, fontsize=6.9,
                color=MUT, va="top", linespacing=1.35)


def fit_xlim(ax, lo, hi, left, right, extra_pt=10.0):
    """Expand the x-limits until the annotations anchored at the data extremes
    fit inside the axes.

    A string's width is a PHYSICAL quantity and the data range is not, so a
    pad expressed as a fraction of the data span is wrong by whatever the span
    happens to be. That is exactly how a -51% bar's number block ended up
    printed over the y-tick labels while a -84% bar's fitted comfortably: the
    smaller span got the smaller pad and needed the larger one. Solving
    R = D + (t_left + t_right)/a * R for the final range R sizes the pad from
    the axes width in inches and from the strings actually drawn.

    `left` and `right` are lists of (text, fontsize, is_monospace).
    """
    a = ax.get_position().width * ax.figure.get_figwidth()

    def widest(items):
        return max([(len(s) * fs * (0.602 if mono else 0.55) + extra_pt) / 72.0
                    for s, fs, mono in items], default=0.0)

    tl, tr = widest(left), widest(right)
    D = (hi - lo) or 1.0
    # floor the denominator: if the annotations are wider than the panel there
    # is no range that fits them and the right answer is a smaller font, not an
    # infinite axis. The floor makes that failure visible instead of unbounded.
    R = D / max(0.30, 1.0 - (tl + tr) / a)
    ax.set_xlim(lo - (tl / a) * R, hi + (tr / a) * R)


def stagger(tags, gap):
    """Push direct labels apart in y so two arms ending at the same level do
    not stack their names on top of each other. Labels are the only thing
    carrying which line is which, so a collision is a loss of information."""
    tags.sort()
    for i in range(1, len(tags)):
        tags[i][0] = max(tags[i][0], tags[i - 1][0] + gap)
    return tags


# -------------------------------------------------------------- data layer --

def read_metrics(path):
    """One run's dense log -> {step: row}. Dedupe by step, LAST WRITE WINS.

    Restarts re-emit steps they have already written, so the file is not
    guaranteed one row per step and `wc -l` is not a step count.
    """
    d = {}
    for line in path.open():
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        d[int(r["step"])] = r
    return d


def load_runs(root, max_step):
    """Every (opponent, arm, seed) cell that has a metrics file on disk.

    Run directories with no `metrics.jsonl` are skipped, not faked: the s3
    seeds and two of the `inf` cells were never launched.
    """
    cells, missing, prov = {}, [], {}
    for opp, _ in BANDS:
        for arm, suf, _, _ in ARMS:
            for s in SEEDS:
                name = RUN_TMPL.format(opp=opp, seed=s, suf=suf)
                p = root / name / "metrics.jsonl"
                if not p.exists():
                    missing.append(name)
                    continue
                rows = read_metrics(p)
                if max_step is not None:
                    rows = {k: v for k, v in rows.items() if k <= max_step}
                if not rows:
                    missing.append(name)
                    continue
                cells[(opp, arm, s)] = rows
                st = p.stat()
                prov[f"{opp}/{arm}/s{s}"] = {
                    "run_dir": name,
                    "n_rows_after_dedupe": len(rows),
                    "min_step": min(rows), "max_step": max(rows),
                    "mtime_utc": dt.datetime.fromtimestamp(
                        st.st_mtime, dt.timezone.utc).strftime(
                            "%Y-%m-%dT%H:%M:%SZ"),
                }
    return cells, sorted(missing), prov


def window_cell(rows, lo, hi):
    """Mean of each rate over the steps of one window, for ONE seed.

    Returns None when the seed has no step inside the window at all, which is
    how a cell goes missing rather than being silently imputed.
    """
    ks = [k for k in sorted(rows) if lo <= k <= hi]
    e = [rows[k][EG_KEY] for k in ks if rows[k].get(EG_KEY) is not None]
    x = [rows[k][XP_KEY] for k in ks if rows[k].get(XP_KEY) is not None]
    if not e or not x:
        return None
    em, xm = float(np.mean(e)), float(np.mean(x))
    return {"endgame_rate": em, "exploit_rate": xm,
            "concentration": (em / xm) if xm else None,
            "n_steps": len(ks), "steps": ks}


def aggregate(cells):
    """Per arm per window: the three quantities, averaged ACROSS SEEDS.

    The concentration index is formed PER SEED and only then averaged. A ratio
    of the two arm means is a different estimator -- it silently weights seeds
    by their exploit_rate -- and is never what is drawn or recorded here.
    """
    out, seeds_of = {}, {}
    for opp, _ in BANDS:
        for arm, _, _, _ in ARMS:
            seeds = sorted(s for (o, a, s) in cells if o == opp and a == arm)
            seeds_of[f"{opp}/{arm}"] = seeds
            for wname, lo, hi, _, _ in WINDOWS:
                per = {q: [] for q, _ in QUANTS}
                used, nsteps = [], []
                for s in seeds:
                    c = window_cell(cells[(opp, arm, s)], lo, hi)
                    if c is None:
                        continue
                    used.append(s)
                    nsteps.append(c["n_steps"])
                    for q, _ in QUANTS:
                        per[q].append(c[q])
                rec = {}
                for q, _ in QUANTS:
                    v = [z for z in per[q] if z is not None]
                    rec[q] = None if not v else {
                        "mean": float(np.mean(v)), "se": se(v),
                        "per_seed": [round(z, 4) for z in v], "n": len(v)}
                rec["seeds"] = seeds
                rec["seeds_in_window"] = used
                rec["n_steps_per_seed"] = nsteps
                out[f"{opp}/{arm}/{wname}"] = rec
            out[f"{opp}/{arm}/max_step"] = {
                f"s{s}": max(cells[(opp, arm, s)]) for s in seeds}
    return out, seeds_of


def get(agg, opp, arm, wname, q):
    """(mean, se, n) for one drawn point, or (None, None, 0) if the cell is
    absent. `se` is None at n=1 by construction of `se`."""
    c = (agg.get(f"{opp}/{arm}/{wname}") or {}).get(q)
    if not c:
        return None, None, 0
    return c["mean"], c["se"], c["n"]


def deepest(agg, opp, arm, q):
    """The deepest window this arm actually reaches, and its value there.

    `late` is missing entirely for grim/inf and is n=1 for tft/inf, so the
    step-0-to-end comparison has to name the window it ended at rather than
    assume every arm got to the same place.
    """
    for wname in reversed(WNAMES[1:]):
        m, s, n = get(agg, opp, arm, wname, q)
        if m is not None:
            return wname, m, s, n
    return None, None, None, 0


# --------------------------------------------------------------- reasoning --

def reasoning(path):
    """inf-vs-horizon-visible marker deltas AT STEP 0 against POOLED 0-35.

    ONE SEED, 192 blocks per point. `reasoning_markers.json` is cell -> marker
    -> step -> rate; the pooled figure the reasoning log published is the
    unweighted mean over the shared checkpoints in [0, 35], and pooling is done
    here from source rather than copied out of the log.
    """
    if not path.exists():
        return None
    R = json.loads(path.read_text())
    raw, rel, checks = {}, {}, {}
    for opp, _ in BANDS:
        vis, inf = f"{opp}/nohole", f"{opp}/inf"
        if vis not in R or inf not in R:
            continue
        for m in REAS_MARKERS:
            if m not in R[vis] or m not in R[inf]:
                continue
            shared = sorted(set(int(s) for s in R[vis][m])
                            & set(int(s) for s in R[inf][m]))
            pool = [s for s in shared if 0 <= s <= POOL_HI]
            if 0 not in shared or not pool:
                continue
            v0, i0 = R[vis][m]["0"], R[inf][m]["0"]
            vp = float(np.mean([R[vis][m][str(s)] for s in pool]))
            ip = float(np.mean([R[inf][m][str(s)] for s in pool]))
            raw[f"{opp}/{m}"] = {
                "visible_step0": v0, "inf_step0": i0,
                "visible_pooled_0_%d" % POOL_HI: vp,
                "inf_pooled_0_%d" % POOL_HI: ip,
                "pooled_steps": pool, "n_pooled_checkpoints": len(pool)}
            if m == CHECK:
                # nohole is 0.000 at every checkpoint, so a RELATIVE delta is
                # a division by zero. This marker is reported as a LEVEL.
                checks[opp] = {
                    "visible_step0": v0, "inf_step0": i0,
                    "visible_pooled": vp, "inf_pooled": ip,
                    "note": "horizon-visible arm is exactly 0.000 at every "
                            "checkpoint, so no relative delta is defined; "
                            "reported as a level."}
                continue
            rel[f"{opp}/{m}"] = {
                "rel_at_step0": (i0 - v0) / v0 if v0 else None,
                "rel_pooled_0_%d" % POOL_HI: (ip - vp) / vp if vp else None,
            }
            r0 = rel[f"{opp}/{m}"]["rel_at_step0"]
            rp = rel[f"{opp}/{m}"]["rel_pooled_0_%d" % POOL_HI]
            rel[f"{opp}/{m}"]["share_of_pooled_effect_present_at_step0"] = (
                (r0 / rp) if rp else None)
    # the step0 / step35 levels for every cell, so the panel is auditable
    per_cell = {}
    for cell in [f"{o}/{a}" for o, _ in BANDS
                 for a in ("nohole", "eg", "inf")]:
        if cell not in R:
            continue
        per_cell[cell] = {m: {"step0": R[cell][m].get("0"),
                              "step35": R[cell][m].get("35")}
                          for m in REAS_MARKERS if m in R[cell]}
    return {"raw": raw, "rel": rel, "checks": checks, "per_cell": per_cell}


# ------------------------------------------------------- panels: band 1 & 2 --

def traj_panel(ax, opp, cells, q, xmax, ylim, note, show_win_labels=False):
    """Every seed's full trajectory, so the reader sees SHAPES not four points.

    The four analysis windows are shaded behind the lines: a window is a claim
    about where a number was read, and it should be visible where it was read.
    """
    for wi, (_, lo, hi, _, _) in enumerate(WINDOWS):
        a, b = (lo - 0.45, hi + 0.45) if hi > lo else (lo - 0.45, lo + 0.45)
        ax.axvspan(a, b, color=MUT, alpha=0.10 if wi % 2 == 0 else 0.06,
                   lw=0, zorder=0.5)

    key = QKEY[q]
    tags = []
    for arm, _, lab, col in ARMS:
        seeds = sorted(s for (o, a, s) in cells if o == opp and a == arm)
        if not seeds:
            continue
        endpoints = []
        for i, s in enumerate(seeds):
            rows = cells[(opp, arm, s)]
            ks = [k for k in sorted(rows) if rows[k].get(key) is not None]
            ys = [rows[k][key] for k in ks]
            if not ks:
                continue
            ax.plot(ks, ys, color=col, lw=1.15, alpha=0.80, zorder=3,
                    solid_capstyle="round")
            # a dot at the frontier: where this seed actually stops is part of
            # the evidence, not incidental
            ax.plot([ks[-1]], [ys[-1]], marker=SEED_MK[i % len(SEED_MK)],
                    ms=4.2, color=col, mec=SURF, mew=0.7, ls="none", zorder=4)
            endpoints.append((ks[-1], ys[-1]))
        if endpoints:
            xe, ye = max(endpoints)
            tags.append([ye, xe, lab, col])

    gap = (ylim[1] - ylim[0]) * 0.062
    for ye, xe, lab, col in stagger(tags, gap):
        ax.annotate(lab, (xe, ye), textcoords="offset points", xytext=(6, 0),
                    ha="left", va="center", fontsize=7.6, color=col,
                    fontweight="bold", annotation_clip=False)

    if show_win_labels:
        for _, lo, hi, tick, _ in WINDOWS:
            ax.annotate(tick.replace("\n", " "), ((lo + hi) / 2.0, ylim[1]),
                        textcoords="offset points", xytext=(0, -3),
                        ha="center", va="top", fontsize=6.2, color=MUT,
                        rotation=90, annotation_clip=False)

    # The pad is anchored at the GLOBAL deepest step and sized from the same
    # three arm labels in both bands, so the two bands come out with an
    # identical x-axis: a shared axis drawn at two scales is not a shared axis.
    fit_xlim(ax, -1.2, xmax, [],
             [(lab, 7.6, False) for _, _, lab, _ in ARMS])
    ax.set_ylim(*ylim)
    style(ax, "", "", note=note)


def window_panel(ax, opp, agg, q, ylim, note, hline=None):
    """The four windows side by side, one line per arm, between-seed SE.

    n=1 cells are drawn as an OPEN diamond with no bar and an explicit "n=1"
    tag; a cell no seed reaches is drawn as a red cross on the axis rather than
    left as a gap the eye will interpolate through.
    """
    xs = list(range(len(WINDOWS)))
    tags = []
    for arm, _, lab, col in ARMS:
        px, py, single, absent = [], [], [], []
        for xi, wname in enumerate(WNAMES):
            m, s, n = get(agg, opp, arm, wname, q)
            if m is None:
                absent.append(xi)
                continue
            px.append(xi)
            py.append(m)
            if n >= 2:
                ax.errorbar([xi], [m], yerr=[s], color=col, lw=0,
                            elinewidth=2.0, capsize=5, capthick=2.0,
                            marker="o", ms=7.0, mec=SURF, mew=1.1, zorder=5)
            else:
                single.append((xi, m))
        if px:
            ax.plot(px, py, color=col, lw=1.7, alpha=0.9, zorder=4)
            tags.append([py[-1], px[-1], lab, col])
        for xi, m in single:
            ax.plot([xi], [m], marker="D", ms=8.5, mfc=SURF, mec=col, mew=2.2,
                    ls="none", zorder=6)
            ax.annotate("n=1", (xi, m), textcoords="offset points",
                        xytext=(0, 11), ha="center", fontsize=6.4, color=col,
                        fontweight="bold", annotation_clip=False)
        for xi in absent:
            # Above the marker, not below it: below, the label fell outside the
            # axes and was clipped by the x tick labels.
            yx = ylim[0] + (ylim[1] - ylim[0]) * 0.045
            ax.plot([xi], [yx], marker="x", ms=8, color=RED, mew=2.2,
                    ls="none", zorder=6)
            ax.annotate("no seed reaches\nthis window", (xi, yx),
                        textcoords="offset points", xytext=(0, 9),
                        ha="center", va="bottom", fontsize=6.2, color=RED,
                        linespacing=1.25, annotation_clip=False)

    gap = (ylim[1] - ylim[0]) * 0.075
    for ye, xe, lab, col in stagger(tags, gap):
        ax.annotate(lab, (xe, ye), textcoords="offset points", xytext=(8, 0),
                    ha="left", va="center", fontsize=7.6, color=col,
                    fontweight="bold", annotation_clip=False)

    if hline is not None:
        # The line is explained in the PANEL NOTE, not beside itself: every
        # interior position along y=1.0 is either on a drawn line or on an
        # arm's direct label, and the note's top-left corner is the one region
        # of this panel that no series enters.
        ax.axhline(hline, color=INK, lw=1.2, ls=(0, (5, 3)), zorder=2)
        ax.annotate(f"{hline:.1f}", (-0.40, hline), textcoords="offset points",
                    xytext=(0, -3), ha="left", va="top", fontsize=7.0,
                    color=INK, fontweight="bold")

    # Room for the direct labels INSIDE the axes: at the default right margin
    # "endgame penalty" ran off the edge of the paper.
    fit_xlim(ax, -0.45, max([t[1] for t in tags], default=len(WINDOWS) - 1),
             [], [(t[2], 7.6, False) for t in tags])
    ax.set_ylim(*ylim)
    ax.set_xticks(xs)
    ax.set_xticklabels([w[3] for w in WINDOWS], fontsize=7.8, color=INK2)
    ax.get_xticklabels()[0].set_color(INK)
    ax.get_xticklabels()[0].set_fontweight("bold")
    style(ax, "", "", note=note)


# ------------------------------------------------------------ panel: band 3 --

def change_rows(agg, q):
    """One row per arm: step-0 level, deepest level reached, relative change.

    `deepest` names the window each arm actually got to, because they did not
    all get to the same one -- no grim/inf cell reaches 30-37 and the tft/inf
    cell there is a single seed.
    """
    rows = []
    for opp, _ in BANDS:
        for arm, _, _, col in ARMS:
            a, _, _ = get(agg, opp, arm, "step0", q)
            wn, b, _, n = deepest(agg, opp, arm, q)
            if a is None or b is None or not a:
                continue
            rows.append({"q": q, "opp": opp, "arm": arm, "col": col,
                         "start": a, "end": b, "window": wn, "n_end": n,
                         "rel": b / a - 1.0})
    return rows


def change_panel(ax, agg, q, record, show_labels):
    """THE HEADLINE, one quantity at a time.

    Relative change rather than absolute, because the claim is about the three
    quantities MOVING DIFFERENTLY: defection overall halves, endgame defection
    does not, so the index doubles. Each bar prints the absolute endpoints it
    was formed from, so the relative framing never hides its own levels.

    ONE X-SCALE PER QUANTITY, three panels rather than one. On a single shared
    scale the concentration group runs to +414% (tft/inf, one seed) while the
    whole endgame_rate group lives inside +/-52%, which squeezes the headline
    contrast -- exploit_rate falling while endgame_rate does not -- into a few
    pixels. The cost is that the comparison is across panels, and it is paid
    back by every bar carrying its own numbers.
    """
    rows = change_rows(agg, q)
    lo = min([0.0] + [r["rel"] for r in rows])
    hi = max([0.0] + [r["rel"] for r in rows])

    FS = 6.8
    left_t, right_t = [], []
    for i, r in enumerate(rows):
        one = r["n_end"] < 2
        ax.barh(i, r["rel"], height=0.62, color=r["col"],
                alpha=0.30 if one else 0.85,
                edgecolor=r["col"], lw=2.0 if one else 0.0,
                hatch="////" if one else None, zorder=3)
        side = 1 if r["rel"] >= 0 else -1
        txt = f"{r['start']:.3f}->{r['end']:.3f} {r['rel'] * 100:+.0f}%"
        (right_t if side > 0 else left_t).append((txt, FS, True))
        ax.annotate(txt, (r["rel"], i), textcoords="offset points",
                    xytext=(6 * side, 0), ha="left" if side > 0 else "right",
                    va="center", fontsize=FS, color=INK2,
                    family="monospace", annotation_clip=False)
        record[f"{r['opp']}/{r['arm']}/{r['q']}"] = {
            "step0": r["start"], "end_window": r["window"], "end": r["end"],
            "relative_change": r["rel"], "n_seeds_at_end": r["n_end"]}

    ax.set_yticks(range(len(rows)))
    if show_labels:
        # The endpoint window rides on the ROW label, once, rather than on
        # every bar in all three panels: it is a property of the arm's
        # coverage, identical across the three quantities.
        wlab = {w[0]: w[3].replace("\n", " ") for w in WINDOWS}
        ax.set_yticklabels(
            [f"{r['opp']}/{r['arm']}  to {wlab[r['window']]}"
             + ("  n=1" if r["n_end"] < 2 else "") for r in rows],
            fontsize=7.3, color=INK2)
        for t, r in zip(ax.get_yticklabels(), rows):
            t.set_color(r["col"])
    else:
        ax.set_yticklabels([])
    ax.invert_yaxis()
    ax.axvline(0, color=INK, lw=1.5, zorder=4)
    fit_xlim(ax, lo, hi, left_t, right_t)
    # top padding leaves the panel note a clear strip: the note is the only
    # place several of these panels state what they are
    ax.set_ylim(len(rows) - 0.4, -1.85)
    ax.grid(True, axis="x", color=GRID, lw=0.8, zorder=0)
    ax.grid(False, axis="y")
    return rows


def trained_panel(ax, agg, record, note):
    """The one strand that IS trained: the endgame penalty against tft.

    Per-seed points as well as arm means, because the claim is not only that
    the means separate but that ALL THREE seeds move the same way -- which a
    mean with an error bar cannot show and a per-seed point can.
    """
    opp = "tft"
    tags = []
    for arm in ("base", "eg"):
        col = ARM_COL[arm]
        px, py = [], []
        for xi, wname in enumerate(WNAMES):
            c = (agg.get(f"{opp}/{arm}/{wname}") or {}).get("endgame_rate")
            if not c:
                continue
            px.append(xi)
            py.append(c["mean"])
            for i, v in enumerate(c["per_seed"]):
                ax.plot([xi + 0.13], [v], marker=SEED_MK[i % len(SEED_MK)],
                        ms=4.4, color=col, alpha=0.70, mec=SURF, mew=0.6,
                        ls="none", zorder=4)
            if c["se"] is not None:
                ax.errorbar([xi], [c["mean"]], yerr=[c["se"]], color=col, lw=0,
                            elinewidth=2.0, capsize=5, capthick=2.0,
                            marker="o", ms=7.0, mec=SURF, mew=1.1, zorder=5)
        if px:
            ax.plot(px, py, color=col, lw=1.8, zorder=3)
            tags.append([py[-1], px[-1], ARM_LAB[arm], col])
        record[arm] = {
            w: (lambda c: None if not c else
                {"mean": c["mean"], "se": c["se"], "per_seed": c["per_seed"],
                 "n": c["n"]})(
                    (agg.get(f"{opp}/{arm}/{w}") or {}).get("endgame_rate"))
            for w in WNAMES}

    b0 = (agg.get(f"{opp}/base/step0") or {}).get("endgame_rate")
    e0 = (agg.get(f"{opp}/eg/step0") or {}).get("endgame_rate")
    bl = (agg.get(f"{opp}/base/late") or {}).get("endgame_rate")
    el = (agg.get(f"{opp}/eg/late") or {}).get("endgame_rate")
    if b0 and e0 and bl and el:
        record["gap_step0"] = b0["mean"] - e0["mean"]
        record["gap_late"] = bl["mean"] - el["mean"]
        record["all_eg_seeds_fall_step0_to_late"] = bool(
            len(e0["per_seed"]) == len(el["per_seed"])
            and all(b < a for a, b in zip(e0["per_seed"], el["per_seed"])))
        # Thrown DOWN-right into the empty lower-left quadrant. Up and to the
        # right the second line is long enough to reach the 8-16 error bar,
        # and higher still it reaches the panel note.
        ax.annotate(f"step 0: {b0['mean']:.3f} vs {e0['mean']:.3f}\n"
                    f"gap {record['gap_step0']:+.3f} -- indistinguishable",
                    (0, min(b0["mean"], e0["mean"])),
                    textcoords="offset points", xytext=(6, -52),
                    fontsize=6.8, color=INK2, ha="left", va="top",
                    annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color=MUT, lw=0.8,
                                    shrinkB=4))
        ax.annotate(f"30-37: {bl['mean']:.3f} vs {el['mean']:.3f}\n"
                    f"gap {record['gap_late']:+.3f}"
                    + ("\nall 3 eg seeds moved down"
                       if record["all_eg_seeds_fall_step0_to_late"] else ""),
                    (3, el["mean"]), textcoords="offset points",
                    xytext=(-6, -30), fontsize=6.8, color=INK2, ha="right",
                    va="top", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color=MUT, lw=0.8))

    gap = 0.030
    for ye, xe, lab, col in stagger(tags, gap):
        ax.annotate(lab, (xe, ye), textcoords="offset points", xytext=(8, 0),
                    ha="left", va="center", fontsize=7.6, color=col,
                    fontweight="bold", annotation_clip=False)
    fit_xlim(ax, -0.45, max([t[1] for t in tags], default=len(WINDOWS) - 1),
             [], [(t[2], 7.6, False) for t in tags])
    ax.set_ylim(0, 0.48)
    ax.set_xticks(range(len(WINDOWS)))
    ax.set_xticklabels([w[3] for w in WINDOWS], fontsize=7.8, color=INK2)
    ax.get_xticklabels()[0].set_color(INK)
    ax.get_xticklabels()[0].set_fontweight("bold")
    style(ax, "", "", note=note)


# ------------------------------------------------------------ panel: band 4 --

def marker_panel(ax, reas, note):
    """How much of the published marker suppression was there before training.

    The solid segment is the relative delta AT STEP 0; the open extension runs
    on to the pooled 0-35 value the reasoning log published. Bar length is the
    published effect; the SOLID part is the share of it the untrained policy
    already had. For tft's `endgame_defect_plan` there is no extension at all.
    """
    rows = [(opp, m, lab) for opp, _ in BANDS for m, lab in MARKERS
            if f"{opp}/{m}" in reas["rel"]]
    if not rows:
        return {}
    out = {}
    lo, hi = 0.0, 0.0
    left_t, right_t = [], []
    for xi, (opp, m, lab) in enumerate(rows):
        r = reas["rel"][f"{opp}/{m}"]
        r0 = r["rel_at_step0"] * 100.0
        rp = r["rel_pooled_0_%d" % POOL_HI] * 100.0
        lo = min(lo, r0, rp)
        hi = max(hi, r0, rp)
        ax.barh(xi, r0, height=0.52, color=BLUE, alpha=0.85, lw=0, zorder=3)
        ax.barh(xi, rp - r0, left=r0, height=0.52, color=SURF,
                edgecolor=BLUE, lw=1.6, hatch="////", zorder=3)
        ax.plot([rp], [xi], marker="|", ms=15, color=INK, mew=2.0, zorder=5)
        share = r["share_of_pooled_effect_present_at_step0"]
        num = (f"step 0 {r0:+.1f}%   published {rp:+.1f}%"
               + (f"   ({share * 100:.0f}% already there)"
                  if share is not None else ""))
        left_t.append((num, 6.9, True))
        ax.annotate(num, (min(r0, rp), xi), textcoords="offset points",
                    xytext=(-7, 0), ha="right", va="center", fontsize=6.9,
                    color=INK2, family="monospace", annotation_clip=False)
        # Row identity DIRECT-LABELLED inside the panel. Every bar is negative,
        # so the whole x > 0 half is empty; as y-tick labels these ran off the
        # left edge of the paper.
        name = f"{opp}  {lab}"
        right_t.append((name, 7.4, False))
        ax.annotate(name, (0, xi), textcoords="offset points",
                    xytext=(8, 0), ha="left", va="center", fontsize=7.4,
                    color=INK2)
        out[f"{opp}/{m}"] = {"rel_at_step0": r["rel_at_step0"],
                             "rel_pooled": r["rel_pooled_0_%d" % POOL_HI],
                             "share_present_at_step0": share}
    ax.set_yticks([])
    ax.invert_yaxis()
    ax.axvline(0, color=INK, lw=1.5, zorder=4)
    fit_xlim(ax, lo, hi, left_t, right_t)
    ax.set_ylim(len(rows) - 0.4, -1.9)
    ax.grid(True, axis="x", color=GRID, lw=0.8, zorder=0)
    ax.grid(False, axis="y")
    style(ax, "", "", note=note)
    return out


def check_panel(ax, reas, note):
    """The manipulation check, as a LEVEL: does the policy notice the horizon
    is gone? The horizon-visible arms sit at exactly 0.000 at every checkpoint,
    so there is no relative delta to take and none is invented."""
    ch = reas["checks"]
    xs, out = [], {}
    for oi, (opp, _) in enumerate(BANDS):
        if opp not in ch:
            continue
        c = ch[opp]
        xs.append((oi, opp))
        for dx, key, mfc, tag in ((-0.16, "inf_step0", BLUE, "step 0"),
                                  (0.16, "inf_pooled", SURF, "pooled 0-35")):
            ax.plot([oi + dx], [c[key]], marker="o", ms=11, mfc=mfc,
                    mec=BLUE, mew=2.2, ls="none", zorder=5)
            ax.annotate(f"{c[key]:.3f}\n{tag}", (oi + dx, c[key]),
                        textcoords="offset points", xytext=(0, 13),
                        ha="center", fontsize=6.9, color=BLUE,
                        annotation_clip=False)
        ax.plot([oi - 0.16, oi + 0.16], [c["visible_step0"],
                                         c["visible_pooled"]],
                color=PURPLE, lw=2.4, zorder=4)
        ax.annotate("horizon-visible arms: 0.000 at EVERY checkpoint",
                    (oi, c["visible_step0"]), textcoords="offset points",
                    xytext=(0, -7), ha="center", va="top", fontsize=6.4,
                    color=PURPLE, annotation_clip=False)
        out[opp] = c
    ax.set_xticks([i for i, _ in xs])
    ax.set_xticklabels([o for _, o in xs], fontsize=8.6, color=INK2)
    ax.set_xlim(-0.55, len(BANDS) - 0.45)
    ax.set_ylim(-0.045, 0.235)
    style(ax, "", "", note=note)
    return out


# ------------------------------------------------------------------- text --

def page_text(agg, reas, prov, missing, live, args):
    """Suptitle, header block, footer block. Every number read from the data.

    A stale hardcoded string is the worst defect this repo's figure audits
    find, so nothing here is written by hand: the headline claim, the coverage
    line and every caveat's numbers are formatted from the arguments.
    """
    def g(opp, arm, w, q):
        m, s, n = get(agg, opp, arm, w, q)
        return m

    gb0, gbl = g("grim", "base", "step0", "concentration"), \
        g("grim", "base", "late", "concentration")
    tb0, tbl = g("tft", "base", "step0", "concentration"), \
        g("tft", "base", "late", "concentration")
    gx0, gxl = g("grim", "base", "step0", "exploit_rate"), \
        g("grim", "base", "late", "exploit_rate")
    ge0, gel = g("grim", "base", "step0", "endgame_rate"), \
        g("grim", "base", "late", "endgame_rate")
    tx0, txl = g("tft", "base", "step0", "exploit_rate"), \
        g("tft", "base", "late", "exploit_rate")
    te0, tel = g("tft", "base", "step0", "endgame_rate"), \
        g("tft", "base", "late", "endgame_rate")
    gi0, gie = g("grim", "inf", "step0", "endgame_rate"), \
        g("grim", "inf", "early", "endgame_rate")
    ti0, tie = g("tft", "inf", "step0", "endgame_rate"), \
        g("tft", "inf", "early", "endgame_rate")
    gic, tic = g("grim", "inf", "step0", "concentration"), \
        g("tft", "inf", "step0", "concentration")

    title = (
        "The conclusion of 0830-endgame-summary.md 7 survives; its attribution "
        "to TRAINING does not. The hidden-horizon endgame collapse, the "
        "inverted concentration ratio and the notices_unknown manipulation "
        f"check are ALL fully present at STEP 0 -- the untrained policy.\nWhat "
        f"training actually does is prune NON-endgame defection and spare the "
        f"endgame: exploit_rate {gx0:.3f} -> {gxl:.3f} (grim) and "
        f"{tx0:.3f} -> {txl:.3f} (tft) while endgame_rate holds at "
        f"{ge0:.3f} -> {gel:.3f} and {te0:.3f} -> {tel:.3f}, so the "
        f"concentration index roughly doubles ({gb0:.2f} -> {gbl:.2f}, "
        f"{tb0:.2f} -> {tbl:.2f}).")

    n_runs = len(prov)
    depths = ", ".join(
        f"{k} to step {v['max_step']}"
        for k, v in sorted(prov.items()) if "/inf/" in k)
    lines = [
        "Qwen3.8-27B, thinking on, iterated prisoner's dilemma, local PEFT LoRA "
        "(see 0830-endgame-summary.md 8). Source is the DENSE TRAINING LOG, "
        f"metrics.jsonl, over {n_runs} runs: two opponents x three arms x up to "
        "three seeds, deduped by step with last write wins. Arms differ in one "
        "thing each: orange adds a hidden reward charge on late betrayal, blue "
        "scrubs the stated round total from the prompt (core.scrub_horizon) and "
        "changes nothing else.",

        "WHY STEP 0 IS THE UNTRAINED POLICY, WHICH IS THE WHOLE ARGUMENT. "
        "hole_exp/train_mixed.py samples rollouts, applies the gradient at "
        "tc.optim_step(...) on L844, and only then logs m = {\"step\": step, "
        "...} on L898 from step_metrics_mixed(recs, ...) -- where recs are the "
        "PRE-UPDATE rollouts it just sampled. So the row keyed step N describes "
        "the policy at the START of step N, and the row keyed step 0 describes "
        "a policy that has taken zero gradient steps. A gap already present at "
        "step 0 was not installed by this training run. Every claim on this "
        "page is downstream of that one fact.",

        "THE CONCENTRATION INDEX IS AN INDEX, NOT A PROBABILITY. It is "
        "endgame_rate / exploit_rate, formed PER SEED and then averaged across "
        "seeds -- never as a ratio of the two arm means, which would silently "
        "weight seeds by their exploit_rate. endgame_rate divides late "
        "betrayals by the EXOGENOUS late window; exploit_rate is over ALL "
        "rounds. They are not the same denominator, so the ratio cannot be "
        "read as 'the chance a late decision is a betrayal'. It also inherits "
        "the warning at hole_exp/core.py L725 that endgame_rate is NOT "
        "comparable across counterparts: against a never-forgiving counterpart "
        "the timeline terminates after the first betrayal, so an episode that "
        "defected early never reaches the window and is scored 0.0 rather than "
        "undefined. THE RELIABLE READ IS THE WITHIN-ARM CHANGE OVER TRAINING, "
        "where that artefact is held fixed. Between-arm level differences are "
        "weaker evidence and should not be quoted as effect sizes.",

        f"WINDOWS, AND WHY THESE FOUR. step 0 is the untrained policy. 8-16 is "
        f"the window 7.1 published and the deepest one every inf seed reaches. "
        f"16-19 is the deepest three of the four inf seeds reach. 30-37 is the "
        f"deepest window ALL base/eg seeds reach -- the grim base/eg cells were "
        f"stopped at step 34-50 once their effect went flat (7.2), so 30-37 is "
        f"the deepest MATCHED window and it is not extended past that even "
        f"though the tft runs go further. Error bars are BETWEEN-TRAINING-SEED "
        f"SE on the arm level: sd(per-seed values, ddof=1)/sqrt(n). They are "
        f"not intervals on any difference.",
    ]

    foot = []

    foot.append((RED,
        "INF COVERAGE IS THIN AND UNEVEN, AND THE FIGURE SHOULD NOT BE READ "
        "PAST IT. Only TWO seeds exist per inf cell, against three for every "
        f"other arm. Depths reached: {depths}. The 30-37 window therefore has "
        "NO grim/inf cell at all -- drawn as a red cross on the axis, never as "
        "an interpolated gap -- and its tft/inf cell rests on ONE seed, drawn "
        "as an open diamond with an explicit n=1 tag and NO error bar, because "
        "a one-seed cell has no between-run spread to draw. The same convention "
        "governs the hatched n=1 bar in panel D. Treat every inf point past "
        "step 19 as a single run's trajectory, not as a measured arm."
        + (f"\nFOUR CELLS WERE STILL BEING WRITTEN when this was rendered: "
           + ", ".join(sorted(live))
           + ". Their max_step is a FRONTIER, not a stopping point, and the "
             "30-37 inf coverage in particular will change as they advance. "
             "Every run's mtime and row count is recorded in the paired JSON, "
             "and --max-step pins the frontier for an exactly reproducible "
             "render." if live else "")))

    foot.append((INK2,
        "WHAT THIS REVISES AND WHAT IT LEAVES ALONE. It does NOT contradict "
        "0830-endgame-summary.md 7. That section concludes the endgame is a CUE "
        "rather than a DISPOSITION, and finding the cue effect already complete "
        "in the untrained policy makes that conclusion stronger, not weaker. "
        "What it revises is the EVIDENCE. 7.1's numbers were read at steps 8-16 "
        "and presented as though training had produced them; the step-0 column "
        "this figure adds shows it had not. 7.2 (the prompt swap on the step-35 "
        f"tft/inf adapter) and 7.3 (marker counts at that same checkpoint) are "
        f"single-checkpoint contrasts and could never have spoken to training "
        f"either way -- that is a property of their design, not a fault in "
        f"their execution. THE CONCLUSION STANDS. THE ATTRIBUTION TO TRAINING "
        f"DOES NOT."))

    if reas:
        edp = (reas["rel"].get("tft/endgame_defect_plan") or {})
        s0 = edp.get("rel_at_step0")
        sp = edp.get("rel_pooled_0_%d" % POOL_HI)
        bi = (reas["rel"].get("tft/backward_induction") or {})
        gch = reas["checks"].get("grim", {})
        tch = reas["checks"].get("tft", {})
        foot.append((ORANGE,
            "THE REASONING PANELS ARE ONE SEED AND ARE DIRECTIONAL ONLY. Every "
            "point in F and G is a single training seed at 192 reasoning "
            "blocks, so binomial noise alone is about +/-0.03 on a rate near "
            "0.15 -- comparable to several of the gaps drawn. They are crude "
            "regexes over raw chain-of-thought text and will both miss "
            "paraphrases and catch mentions that are not endgame reasoning. No "
            "between-seed error bar exists for any of them and none is drawn. "
            "Read the ORDERING and the SIGN, never the level."
            + (f"\nEven so the pattern is hard to miss: tft's "
               f"endgame_defect_plan is {s0*100:+.1f}% at step 0 against the "
               f"{sp*100:+.1f}% pooled 0-35 value the reasoning log published, "
               f"i.e. the entire published effect is present before training. "
               f"tft's backward_induction is the one marker that mostly does "
               f"arrive over training "
               f"({bi.get('rel_at_step0', 0)*100:+.1f}% at step 0 against "
               f"{bi.get('rel_pooled_0_%d' % POOL_HI, 0)*100:+.1f}% pooled). "
               f"And notices_unknown, the manipulation check, is fully present "
               f"at step 0: grim {gch.get('visible_step0', 0):.3f} -> "
               f"{gch.get('inf_step0', 0):.3f} and tft "
               f"{tch.get('visible_step0', 0):.3f} -> "
               f"{tch.get('inf_step0', 0):.3f}, against pooled "
               f"{gch.get('inf_pooled', 0):.3f} and "
               f"{tch.get('inf_pooled', 0):.3f}."
               if s0 is not None and sp else "")))

    gic_m = g("grim", "inf", "mid", "concentration")
    tic_l = g("tft", "inf", "late", "concentration")
    foot.append((INK,
        f"THE ONE GENUINELY NEW AND GENUINELY WEAK CLAIM. The concentration "
        f"index rises in the inf arms too, from a much lower start: grim/inf "
        f"{gic:.2f} -> {gic_m:.2f} by step 19, tft/inf {tic:.2f} -> "
        f"{tic_l:.2f} at n=1. If that holds it means training installs "
        f"something endgame-shaped even with NO stated horizon to key on, which "
        f"nothing in 7 predicts. IT IS THE WEAKEST CLAIM ON THIS PAGE and is "
        f"flagged rather than argued: three of the four inf cells stop at step "
        f"18-20, so the rise is measured over at most twenty gradient steps, "
        f"the deepest point rests on one seed, and the index's own "
        f"cross-counterpart caveat applies with full force to a comparison "
        f"between arms whose early-betrayal rates differ this much. It needs "
        f"the inf runs to reach the depth the base/eg runs already have."
        + (f"\nRun directories with no metrics.jsonl, skipped rather than "
           f"imputed: {', '.join(missing)}." if missing else "")))

    return title, lines, foot


# ------------------------------------------------------------------- main --

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default=RUNS_DEFAULT,
                    help="root holding the per-cell run directories")
    ap.add_argument("--markers", default=str(
        HERE.parent / "0826_think_curves" / "reasoning_markers.json"),
        help="reasoning marker curves for panels F and G (ONE SEED)")
    ap.add_argument("--outdir", default=str(HERE))
    ap.add_argument("--max-step", type=int, default=None,
                    help="drop every logged step above this. Four inf cells "
                         "are still training, so this pins the data frontier "
                         "for an exactly reproducible render.")
    a = ap.parse_args()          # --help exits here, before anything renders

    root, outdir = Path(a.runs), Path(a.outdir)
    if not root.exists():
        print(f"[fig] missing {root}")
        return 1

    cells, missing, prov = load_runs(root, a.max_step)
    if not cells:
        print(f"[fig] no metrics.jsonl under {root}")
        return 1
    agg, seeds_of = aggregate(cells)
    reas = reasoning(Path(a.markers))
    if reas is None:
        print(f"[fig] ** {a.markers} missing: no reasoning panels **")

    # "still being written" without consulting the wall clock, so the JSON
    # stays byte-stable across a re-run: a run counts as live if its mtime is
    # within two hours of the NEWEST mtime in the wave. The frozen base/eg
    # cells sit hours behind the inf cells that are still advancing.
    newest = max(p["mtime_utc"] for p in prov.values())
    tmax = dt.datetime.strptime(newest, "%Y-%m-%dT%H:%M:%SZ")
    live = sorted(k for k, p in prov.items()
                  if (tmax - dt.datetime.strptime(
                      p["mtime_utc"], "%Y-%m-%dT%H:%M:%SZ")).total_seconds()
                  < 7200)
    now = dt.datetime.now(dt.timezone.utc)
    for k in live:
        age = (now - dt.datetime.strptime(
            prov[k]["mtime_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(
                tzinfo=dt.timezone.utc)).total_seconds() / 60.0
        print(f"[fig] LIVE {k}: max_step {prov[k]['max_step']}, last written "
              f"{age:.0f} min ago -- frontier will move")

    # -------------------------------------------------------------- render --
    # PAGE TEXT IS BUILT BEFORE THE PANELS, because the bands are positioned
    # from its MEASURED height. Every block wraps to a number of lines that
    # depends on the data in it, so fixed y offsets are what let a header line
    # land on top of a band heading.
    FIG_W, FIG_H = 22.0, 31.0
    TITLE_PT, HEAD_PT, FOOT_PT = 13.5, 8.4, 8.2
    PT = 1.0 / (FIG_H * 72.0)

    def cols(pt):
        # DejaVu Sans averages ~0.555 em of advance per character; the text
        # column runs from x=0.008 to x=0.99.
        return int(0.982 * FIG_W * 72.0 / (0.555 * pt))

    title, lines, foot = page_text(agg, reas, prov, missing, live, a)
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

    BAND_HEAD, BAND_GAP = 0.020, 0.030
    page_top = 0.997 - head_h - BAND_HEAD
    page_bot = 0.010 + foot_h + 0.030
    # Bands 1 and 2 are given IDENTICAL heights: they share all three y-axes,
    # and a shared axis drawn at two different scales is not a shared axis.
    ratios = [1.0, 1.0, 0.92, 0.72]
    avail = page_top - page_bot - BAND_GAP * (len(ratios) - 1) \
        - BAND_HEAD * (len(ratios) - 1)
    if avail < 0.30:
        print(f"[fig] ** only {avail:.3f} of figure height left for "
              f"{len(ratios)} bands; page text has outgrown FIG_H={FIG_H} **")
    unit = avail / sum(ratios)
    spans, y = [], page_top
    for r in ratios:
        spans.append((y, y - unit * r))
        y = y - unit * r - BAND_GAP - BAND_HEAD

    # Band 3 needs FOUR slots: the headline is split into one panel per
    # quantity so a +414% one-seed bar cannot squash the two rate scales.
    # Band 3's left margin is wider because its row labels carry the endpoint
    # window as well as the arm.
    NCOL = [3, 3, 4, 3]
    LEFT = [0.052, 0.052, 0.112, 0.052]
    WSP = [0.30, 0.30, 0.42, 0.26]
    grids = [fig.add_gridspec(1, NCOL[i], top=t, bottom=b, wspace=WSP[i],
                              left=LEFT[i], right=0.975)
             for i, (t, b) in enumerate(spans)]

    # ---- shared y-limits, computed from the data actually drawn ----------
    ylim = {}
    for q, _ in QUANTS:
        hi = 0.0
        for (opp, arm, s), rows in cells.items():
            key = QKEY.get(q)
            v = [r[key] for r in rows.values()
                 if key and r.get(key) is not None]
            if v:
                hi = max(hi, max(v))
        for opp, _ in BANDS:
            for arm, _, _, _ in ARMS:
                for w in WNAMES:
                    m, sd, n = get(agg, opp, arm, w, q)
                    if m is not None:
                        hi = max(hi, m + (sd or 0.0))
        # The two rate panels need more headroom than the index panel: they
        # carry a four-line panel note over a series that climbs into the
        # top-left corner, and the note is where their caveats live.
        ylim[q] = (0.0, hi * (1.44 if q in QKEY else 1.20))
    # concentration is only ever formed over a window, never per step
    ylim["concentration"] = (0.0, ylim["concentration"][1])
    xmax = max(max(r) for r in cells.values())

    # ---- bands 1 and 2: one opponent each ---------------------------------
    for bi, (opp, _) in enumerate(BANDS):
        gs = grids[bi]
        L = "AB"[bi]
        ax = fig.add_subplot(gs[0, 0])
        traj_panel(ax, opp, cells, EG_KEY.split("/")[1], xmax,
                   ylim["endgame_rate"],
                   "every seed's full trajectory. shaded columns are the four\n"
                   "windows below -- a window is a claim about WHERE a number\n"
                   "was read, so it is drawn where it was read",
                   show_win_labels=(bi == 0))
        style(ax, f"{L}1  -  endgame_rate over training, per seed",
              "betrayals in the late window / exogenous window",
              xlab="training step")

        ax = fig.add_subplot(gs[0, 1])
        traj_panel(ax, opp, cells, XP_KEY.split("/")[1], xmax,
                   ylim["exploit_rate"],
                   "the SAME runs on the denominator that covers all rounds.\n"
                   "this is what training halves, in every arm")
        style(ax, f"{L}2  -  exploit_rate over training, per seed",
              "betrayals / all scored decisions", xlab="training step")

        ax = fig.add_subplot(gs[0, 2])
        window_panel(ax, opp, agg, "concentration", ylim["concentration"],
                     "index = endgame_rate / exploit_rate, formed PER SEED\n"
                     "then averaged. NOT a probability -- the two rates have\n"
                     "different denominators. read the WITHIN-ARM change.\n"
                     "dashed 1.0 = defects at the same rate in the final\n"
                     "window as it does over the whole game; below it, LESS",
                     hline=1.0)
        style(ax, f"{L}3  -  concentration index by window",
              "endgame_rate / exploit_rate  (index)",
              xlab="training-step window")

    # ---- band 3: what changed ---------------------------------------------
    gs = grids[2]
    change_rec = {}
    CNOTE = {
        "endgame_rate":
            "the horizon-visible BASELINES barely move: this is\n"
            "the defection training does NOT prune",
        "exploit_rate":
            "the same runs, all rounds. roughly HALVES in every\n"
            "arm -- this is what training does prune",
        "concentration":
            "so the index roughly doubles. training does not\n"
            "teach the endgame; it removes everything else.\n"
            "hatched = endpoint rests on ONE seed",
    }
    for qi, (q, qlab) in enumerate(QUANTS):
        ax = fig.add_subplot(gs[0, qi])
        change_panel(ax, agg, q, change_rec, show_labels=(qi == 0))
        style(ax, f"C{qi + 1}  -  {qlab}", "", note=CNOTE[q])
        ax.set_xlabel("relative change from step 0", fontsize=8.6, color=INK2)
        ax.xaxis.set_major_formatter(
            mticker.FuncFormatter(lambda v, _: f"{v * 100:+.0f}%"))

    ax = fig.add_subplot(gs[0, 3])
    trained_rec = {}
    trained_panel(ax, agg, trained_rec,
                  "the ONE strand of 7 that IS trained. small glyphs are\n"
                  "individual seeds: the claim is not only that the means\n"
                  "separate but that every seed moves the same way")
    style(ax, "D  -  endgame penalty vs baseline, vs tft",
          "train/endgame_rate", xlab="training-step window")

    # ---- band 4: the reasoning side ---------------------------------------
    marker_rec, check_rec = {}, {}
    if reas:
        gs = grids[3]
        ax = fig.add_subplot(gs[0, 0:2])
        marker_rec = marker_panel(
            ax, reas,
            "SOLID = the relative delta at STEP 0. HATCHED = the rest of the\n"
            "way to the pooled 0-35 value 0830-endgame-reasoning.md 3\n"
            "published. bar length is the published effect; the solid part is\n"
            "what the UNTRAINED policy already had")
        style(ax, "E  -  hidden horizon vs horizon-visible, reasoning markers."
                  "  ONE SEED, 192 BLOCKS PER POINT, DIRECTIONAL ONLY",
              "", xlab="relative delta, (inf - nohole) / nohole  (%)")

        ax = fig.add_subplot(gs[0, 2])
        check_rec = check_panel(
            ax, reas,
            "the MANIPULATION CHECK: does the policy notice the horizon is\n"
            "gone? reported as a LEVEL, not a relative delta -- the\n"
            "horizon-visible arms are exactly 0.000, so no ratio exists")
        style(ax, "F  -  notices_unknown  (ONE SEED)",
              "share of reasoning blocks", xlab="opponent")

    # ---- band headings, read off the finished layout ----------------------
    heads = [BANDS[0][1], BANDS[1][1],
             "THE HEADLINE  -  what training actually changed, step 0 to the "
             "deepest window each arm reaches. Both opponents together",
             "THE REASONING SIDE  -  ONE SEED, DIRECTIONAL ONLY"]
    for bi, heading in enumerate(heads):
        if bi >= len(grids) or (bi == 3 and not reas):
            continue
        top = spans[bi][0]
        fig.text(0.012, top + BAND_HEAD * 0.78, heading, fontsize=13.0,
                 color=INK, fontweight="bold", va="bottom", ha="left")
        fig.add_artist(plt.Line2D([0.012, 0.99], [top + BAND_HEAD * 0.60] * 2,
                                  color=GRID, lw=1.1))

    fig.suptitle(title, fontsize=TITLE_PT, color=INK, x=0.008, ha="left",
                 y=0.997, va="top", linespacing=1.4)
    y = 0.997 - nlines(title) * title_lh - 0.010
    for t in lines:
        fig.text(0.008, y, t, fontsize=HEAD_PT, color=INK2, ha="left",
                 va="top", linespacing=1.5)
        y -= nlines(t) * head_lh + 0.0035
    y = page_bot - 0.030
    for col, t in foot:
        fig.text(0.008, y, t, fontsize=FOOT_PT, color=col, ha="left",
                 va="top", linespacing=1.5)
        y -= nlines(t) * foot_lh + 0.0055

    png = outdir / "fig1_training_vs_cue.png"
    fig.savefig(png, dpi=150, facecolor=fig.get_facecolor())
    print(f"[fig] wrote {png}")

    # ---------------------------------------------------------------- json --
    windows_doc = {w[0]: {"lo": w[1], "hi": w[2], "why": w[4]}
                   for w in WINDOWS}
    out = {
        "figure": png.name,
        "question": "0830-endgame-summary.md 7 argues the endgame is a cue "
                    "rather than a disposition. Which of its three strands is "
                    "a TRAINING effect, and which was already true of the "
                    "untrained policy?",
        "load_bearing_premise":
            "hole_exp/train_mixed.py samples rollouts, applies the gradient at "
            "tc.optim_step(...) (L844), then logs m = {\"step\": step, ...} "
            "(L898) from step_metrics_mixed(recs, ...) where recs are the "
            "PRE-UPDATE rollouts. The row keyed step N therefore describes the "
            "policy at the START of step N, and step 0 is the UNTRAINED "
            "policy. A gap already present at step 0 was not installed by "
            "training.",
        "answer": {
            "headline": title.replace("\n", " "),
            "already_true_at_step_0": [
                "the inf endgame collapse: endgame_rate "
                f"{get(agg, 'grim', 'inf', 'step0', 'endgame_rate')[0]:.3f} "
                f"(grim) / "
                f"{get(agg, 'tft', 'inf', 'step0', 'endgame_rate')[0]:.3f} "
                f"(tft) at step 0 against "
                f"{get(agg, 'grim', 'inf', 'early', 'endgame_rate')[0]:.3f} / "
                f"{get(agg, 'tft', 'inf', 'early', 'endgame_rate')[0]:.3f} at "
                "steps 8-16, the window 7.1 published. Flat.",
                "the concentration inversion: inf sits at "
                f"{get(agg, 'grim', 'inf', 'step0', 'concentration')[0]:.2f} / "
                f"{get(agg, 'tft', 'inf', 'step0', 'concentration')[0]:.2f} at "
                "step 0 against "
                f"{get(agg, 'grim', 'base', 'step0', 'concentration')[0]:.2f} / "
                f"{get(agg, 'tft', 'base', 'step0', 'concentration')[0]:.2f} "
                "for the horizon-visible baselines.",
                "notices_unknown, the manipulation check, is fully present at "
                "step 0 against 0.000 for every horizon-visible arm.",
                "most of the 3 marker suppression, and for tft's "
                "endgame_defect_plan all of it.",
            ],
            "genuinely_trained": [
                "overall defection roughly halves in every arm (exploit_rate).",
                "final-window defection does NOT fall with it in the "
                "horizon-visible baselines, so the concentration index roughly "
                "doubles. Training prunes non-endgame defection and spares the "
                "endgame. THIS IS THE HEADLINE.",
                "the endgame penalty's suppression against tft: "
                "indistinguishable from baseline at step 0, clearly separated "
                "by steps 30-37, all three seeds moving down.",
            ],
            "weakest_claim":
                "The concentration index also rises in the inf arms from a far "
                "lower start, which would mean training installs something "
                "endgame-shaped with no stated horizon. Three of the four inf "
                "cells stop at step 18-20 and the deepest point is n=1, so "
                "this is flagged, not argued.",
            "what_this_revises":
                "It does NOT contradict 7. Finding the cue effect complete in "
                "the untrained policy strengthens 'the endgame is a cue'. What "
                "it revises is the evidence: 7.1's numbers were read at steps "
                "8-16 and presented as though training produced them, and "
                "7.2/7.3 are single-checkpoint by construction and never could "
                "have spoken to training. THE CONCLUSION STANDS; THE "
                "ATTRIBUTION TO TRAINING DOES NOT.",
        },
        "index_definition_and_caveat":
            "concentration = train/endgame_rate / train/exploit_rate, computed "
            "PER SEED over the window and only then averaged across seeds -- "
            "never a ratio of means. endgame_rate divides by the exogenous "
            "late window while exploit_rate is over all rounds, so this is an "
            "INDEX, not a probability. It inherits hole_exp/core.py L725: "
            "endgame_rate is not comparable across counterparts, because "
            "against a never-forgiving counterpart the timeline terminates "
            "after the first betrayal and an episode that never reaches the "
            "window is scored 0.0 rather than undefined. The reliable read is "
            "the WITHIN-ARM change over training; between-arm level "
            "differences are weaker.",
        "error_bar_definition":
            "BETWEEN-TRAINING-SEED SE ON THE ARM LEVEL: sd(per-seed window "
            "values, ddof=1)/sqrt(n_seeds). Null at n=1, and no bar is drawn "
            "there. Not an interval on any difference.",
        "windows": windows_doc,
        "cells": agg,
        "coverage": {
            "seeds_per_arm": seeds_of,
            "run_dirs_without_metrics_skipped": missing,
            "inf_caveat":
                "Only 2 seeds per inf cell against 3 elsewhere. No grim/inf "
                "cell reaches the 30-37 window and only tft/inf s1 does, so "
                "that cell is n=1 and carries no error bar.",
            "grim_stop_caveat":
                "The grim base/eg cells were stopped at step 34-50 (see "
                "0830-endgame-summary.md 2), so 30-37 is the deepest window "
                "matched across all base/eg seeds and is deliberately not "
                "extended even though the tft runs go further.",
            "still_being_written": live,
            "liveness_rule":
                "A run counts as live if its metrics.jsonl mtime is within 2h "
                "of the newest mtime in the wave. Wall-clock-free so this JSON "
                "stays byte-stable across a re-run.",
        },
        "provenance": {
            "runs_root": str(root),
            "run_template": RUN_TMPL,
            "metric_keys": [EG_KEY, XP_KEY],
            "dedupe": "by step, last write wins",
            "max_step_cap_applied": a.max_step,
            "runs": prov,
        },
        "training_change_step0_to_deepest": change_rec,
        "endgame_penalty_vs_baseline_tft": trained_rec,
        "reasoning_relative_deltas_ONE_SEED": marker_rec,
        "reasoning_manipulation_check_ONE_SEED": check_rec,
        "reasoning_source": {
            "file": str(Path(a.markers)),
            "pooled_window": [0, POOL_HI],
            "pooling": "unweighted mean over the checkpoints shared by the "
                       "inf and nohole cells in [0, 35]; recomputed here from "
                       "source rather than copied out of the log.",
            "caveat": "ONE SEED, 192 reasoning blocks per point. Binomial "
                      "noise alone is about +/-0.03 on a rate near 0.15. Crude "
                      "regexes over raw chain-of-thought. No between-seed "
                      "error bar exists and none is drawn. Directional only.",
            "detail": (reas or {}).get("raw", {}),
            "per_cell_step0_and_step35": (reas or {}).get("per_cell", {}),
        },
        "reasoning_step0_vs_35_ONE_SEED": (reas or {}).get("per_cell", {}),
    }
    js = outdir / "fig1_training_vs_cue.json"
    js.write_text(json.dumps(out, indent=1, sort_keys=False))
    print(f"[fig] wrote {js}")

    for opp, _ in BANDS:
        for arm, _, _, _ in ARMS:
            bits = []
            for w in WNAMES:
                m, s, n = get(agg, opp, arm, w, "concentration")
                bits.append("      --      " if m is None else
                            (f"{m:.3f}+/-{s:.3f}" if s is not None
                             else f"{m:.3f} (n=1)"))
            print(f"[fig] {opp+'/'+arm:>10} concentration  "
                  + "  ".join(f"{b:>16}" for b in bits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
