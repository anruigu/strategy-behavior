"""/home/allie/venvs/tinker-ipd/bin/python fig3_opponent_or_policy.py

Did the grim/tft opponent split change the learned POLICY, or only the ENVIRONMENT
the policy was measured in?

Any difference measured in `ipd` is confounded: the opponent itself differs there.
This figure shows the three handles that break the confound.

  A  shared-opponent envs over training  -- public_goods / dond / trust draw IDENTICAL
     opponent populations in both arms, so the environment is held fixed
  B  the same test as a per-env endpoint comparison (pooled over steps >= 25)
  C  crossplay -- frozen step-35 adapters played BOTH opponents, so the PLAYED
     opponent can be held fixed while the TRAINING opponent varies
  D  held-out horizons -- frozen adapters replayed at N = 6, 10, 14

Reads results/0830_grim_vs_tft/{train_strategy.json,eval_strategy.json}; writes
fig3_opponent_or_policy.png and fig3_opponent_or_policy.json next to itself.
"""
from __future__ import annotations
import argparse, json, textwrap
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
PURPLE, ORANGE, BLUE = "#7a5bd6", "#eb6834", "#2a78d6"   # arm palette: base / eg / inf
GRIM, TFT = "#00918f", "#b8236f"                          # opponent palette
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
PAPER, RED = "#f9f9f7", "#b5342a"

TRAIN_CACHE = HERE / "train_strategy.json"
EVAL_CACHE = HERE / "eval_strategy.json"

SHARED_ENVS = ("public_goods", "dond", "trust")
ENV_LABEL = {"public_goods": "public_goods", "dond": "dond", "trust": "trust"}
# the training cache calls the baseline arm `base`; the eval cache calls it `nohole`
ARM_TRAIN_TO_EVAL = {"base": "nohole", "eg": "eg", "inf": "inf"}

POOLED_LABEL = f"POOLED ({len(SHARED_ENVS)} envs)"
MIN_SEEDS = 2            # a mean is drawn only where at least this many seeds survive
SE_INNER, SE_OUTER = 1, 2  # forest interval multipliers, and the thresholds quoted with them
# the sensitivity variant in the endgame cache; the seed number is read out of the key
# rather than written into any label
EXCL_KEY = "excl_grim_nohole_s1"
EXCL_ARM = "grim/nohole"
EXCL_SEED = EXCL_KEY.rsplit("_s", 1)[1]


def style(ax, title, ylab, xlab=None, note=None, gridaxis="y"):
    ax.set_title(title, fontsize=10.5, color=INK, loc="left", pad=8)
    if ylab:
        ax.set_ylabel(ylab, fontsize=9, color=INK2)
    if xlab:
        ax.set_xlabel(xlab, fontsize=9, color=INK2)
    ax.set_facecolor(SURF)
    if gridaxis == "x":
        ax.grid(True, axis="x", color=GRID, lw=0.8, zorder=0)
        ax.grid(False, axis="y")
    else:
        ax.grid(True, axis="y", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUT, labelsize=8, length=0)
    if note:
        ax.text(0.015, 0.965, note, transform=ax.transAxes, fontsize=7.5,
                color=MUT, va="top", zorder=6)


# ---------------------------------------------------------------- numerics

def between_seed(values):
    """Repo convention: collapse each training seed to one number, then spread
    ACROSS seeds. sd(ddof=1)/sqrt(n). Fewer than 2 seeds -> se is None, never 0."""
    vals = [float(v) for v in values if v is not None and np.isfinite(v)]
    n = len(vals)
    if n == 0:
        return None, None, 0
    mean = float(np.mean(vals))
    se = float(np.std(vals, ddof=1) / np.sqrt(n)) if n >= 2 else None
    return mean, se, n


def jnum(x):
    if x is None:
        return None
    if isinstance(x, (np.floating, np.integer)):
        x = x.item()
    if isinstance(x, float) and not np.isfinite(x):
        return None
    return x


def errbar_v(ax, x, y, se, color, **kw):
    """A null SE draws NO bar (never a zero-length one)."""
    if se is None or not np.isfinite(se):
        return False
    ax.errorbar([x], [y], yerr=[se], fmt="none", ecolor=color, elinewidth=kw.pop("lw", 1.6),
                capsize=kw.pop("capsize", 2.6), capthick=1.2, zorder=kw.pop("zorder", 4))
    return True


def label_above(ax, x, y, se, text, color, pad, fontsize=6.8, rotation=0):
    """Error-bar-aware placement: past the end of the bar, not on top of it.
    Rotated 90 deg the anchor is the START of the string, so ha="left" makes the
    label grow upward away from the bar cap instead of straddling it."""
    top = y + (se if (se is not None and np.isfinite(se)) else 0.0)
    ha, va = ("left", "center") if rotation else ("center", "bottom")
    ax.text(x, top + pad, text, ha=ha, va=va, fontsize=fontsize, color=color,
            rotation=rotation, rotation_mode="anchor", zorder=6)


def contrast_census(tvc):
    """Every condition x plays x metric contrast the eval cache holds, split into the
    ones a |z| can be formed on and the ones it cannot.

    A contrast is UNTESTABLE when the quadrature SE is exactly zero: every seed on
    both arms sits on the same value, so delta is 0.0 with se 0.0 and |z| = 0/0.
    Dropping those is right, but the headline count then runs over a subset of the
    file and the exclusion has to be stated, so it is derived here (the cache's
    `verdict` block records n_contrasts_tested but not WHICH contrasts it dropped)."""
    total, testable, excluded = 0, 0, []
    for cond in (k for k in tvc if not k.startswith("_")):
        for plays in (k for k in tvc[cond] if k.startswith("plays=")):
            cell = tvc[cond][plays]
            for metric, b in cell.items():
                if not (isinstance(b, dict) and "delta" in b):
                    continue
                total += 1
                se = b.get("se")
                if se is not None and np.isfinite(se) and se > 0:
                    testable += 1
                    continue
                excluded.append({
                    "name": f"{cond}/{plays}/{metric}",
                    "condition": cond, "plays": plays, "metric": metric,
                    "delta": jnum(b.get("delta")), "se": jnum(se),
                    "mean_a": jnum(b.get("mean_a")), "mean_b": jnum(b.get("mean_b")),
                    "n_seeds_a": b.get("n_seeds_a"), "n_seeds_b": b.get("n_seeds_b"),
                    "why": "both arms pinned at the same value; se == 0 so |z| is undefined",
                })
    return total, testable, excluded


def pinned_value_text(excluded):
    """The value both arms are pinned at, if the excluded contrasts agree on one."""
    vals = [e["mean_a"] for e in excluded] + [e["mean_b"] for e in excluded]
    vals = [v for v in vals if v is not None]
    if vals and max(vals) - min(vals) < 1e-12:
        return f"{vals[0]:.3f}"
    return "a single value"


def nudge(ys, min_gap):
    """Push direct labels apart so they never overlap, preserving order."""
    order = np.argsort(ys)
    out = list(ys)
    prev = -np.inf
    for i in order:
        v = max(out[i], prev + min_gap)
        out[i] = v
        prev = v
    return out


# ------------------------------------------------------- panel A: pooling

def pooled_by_step(shared, opponent, arm):
    """Per step, per seed: equal-weight mean over the three shared-opponent envs
    (an env with more episodes must not outweigh the others -- this is exactly the
    rule build_train_cache.py uses for pooled_three_envs, applied per step instead
    of pooled over steps >= 25). Then spread ACROSS seeds.

    A seed with no episode in some env at some step contributes a mean over the
    SURVIVING envs only. That point is still plotted -- dropping it would hide a
    real measurement -- but it is flagged `partial` so the renderer can mark it,
    and the per-seed env count travels into the JSON."""
    per_step: dict[int, dict[str, list[tuple[str, float]]]] = {}
    envs_used = []
    for env in SHARED_ENVS:
        key = f"{opponent}/{arm}/{env}"
        if key not in shared:
            continue
        envs_used.append(env)
        blk = shared[key]["by_step"]["exploit_rate"]
        steps = blk["steps"]
        for seed, series in blk["per_seed"].items():
            for st, val in zip(steps, series):
                if val is None:
                    continue
                per_step.setdefault(int(st), {}).setdefault(seed, []).append((env, float(val)))
    steps_sorted = sorted(per_step)
    rows = []
    for st in steps_sorted:
        cells = sorted(per_step[st].items())
        per_seed = {s: float(np.mean([v for _, v in lst])) for s, lst in cells}
        envs_per_seed = {s: [e for e, _ in lst] for s, lst in cells}
        partial = {s: es for s, es in envs_per_seed.items() if len(es) < len(envs_used)}
        mean, se, n = between_seed(per_seed.values())
        rows.append({"step": st, "mean": mean, "se": se, "n_seeds": n, "per_seed": per_seed,
                     "envs_per_seed": envs_per_seed,
                     "n_envs_per_seed": {s: len(es) for s, es in envs_per_seed.items()},
                     "partial_seeds": partial})
    return rows, envs_used


# ------------------------------------------------------------------ main

def main() -> None:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)
    ap.add_argument("--outdir", type=Path, default=HERE)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--stem", default="fig3_opponent_or_policy")
    args = ap.parse_args()

    train = json.loads(TRAIN_CACHE.read_text())
    ev = json.loads(EVAL_CACHE.read_text())
    shared = train["shared_opponent_envs"]
    pooled3 = shared["pooled_three_envs"]
    cross = ev["crossplay"]
    bap = cross["by_arm_plays"]
    tvc = cross["trained_vs_contrast"]
    verdict = cross["verdict"]
    endgame = ev["endgame_length"]

    late_step = train["meta"]["late_step"]
    eval_step = cross["_meta"]["steps"][0]

    payload: dict = {}

    fig = plt.figure(figsize=(18.8, 12.4))
    fig.patch.set_facecolor(PAPER)
    # one flat gridspec: A and B each span two columns, C is those two columns
    # split, D spans two. Nesting a subgridspec -- or setting hspace/wspace here --
    # marks the gridspec locally modified and silently disables tight_layout, so
    # the spacing is handed to tight_layout as h_pad / w_pad instead.
    gs = fig.add_gridspec(2, 4, width_ratios=[0.86, 1.26, 1.00, 1.00])
    axA = fig.add_subplot(gs[0, 0:2])
    axB = fig.add_subplot(gs[0, 2:4])
    axC1 = fig.add_subplot(gs[1, 0])
    axC2 = fig.add_subplot(gs[1, 1])
    axD = fig.add_subplot(gs[1, 2:4])

    # ============================================================ PANEL A
    aspec = [
        ("base", "grim", GRIM, "o", "solid", 2.4, 1.00, 5.0, "grim-trained\nbaseline"),
        ("base", "tft", TFT, "s", (0, (5, 2)), 2.4, 1.00, 4.6, "tft-trained\nbaseline"),
        ("eg", "grim", GRIM, "o", (0, (1, 1.6)), 1.15, 0.55, 3.0, "grim-trained\neg"),
        ("eg", "tft", TFT, "s", (0, (1, 1.6)), 1.15, 0.55, 2.8, "tft-trained\neg"),
    ]
    panel_a: dict = {
        "_metric": f"exploit_rate, pooled over {' / '.join(SHARED_ENVS)}",
        "_pooling": (f"per step, per seed: equal-weight mean over the {len(SHARED_ENVS)} shared-opponent "
                     "envs; then mean/se BETWEEN training seed"),
        "_truncation": f"curve drawn only where n_seeds >= {MIN_SEEDS}; SE band likewise",
        "_partial_env_points": (
            f"Where a seed has no episode in some env at some step its contribution is a mean "
            f"over the SURVIVING envs only, so the point is an average of fewer than "
            f"{len(SHARED_ENVS)} envs for that seed even though n_seeds is unchanged. Those points "
            f"are kept and marked in the figure with a hollow neutral ring; n_envs_per_seed below "
            f"records the count for every point."),
        "_partial_env_points_found": [],
        "series": {},
    }
    a_ends = []
    xmax_a, a_top = 0, 0.0
    for arm, opp, hue, mk, ls, lw, alpha, ms, lab in aspec:
        rows, envs_used = pooled_by_step(shared, opp, arm)
        panel_a["series"][f"{opp}/{arm}"] = {
            "label": lab, "envs": envs_used,
            "points": [{"step": r["step"], "mean": jnum(r["mean"]), "se": jnum(r["se"]),
                        "n_seeds": r["n_seeds"],
                        "per_seed": {k: jnum(v) for k, v in r["per_seed"].items()},
                        "n_envs_per_seed": r["n_envs_per_seed"],
                        "envs_per_seed": r["envs_per_seed"],
                        "partial_envs": bool(r["partial_seeds"])}
                       for r in rows],
        }
        for r in rows:
            for sd, es in sorted(r["partial_seeds"].items()):
                panel_a["_partial_env_points_found"].append({
                    "series": f"{opp}/{arm}", "step": r["step"], "seed": sd,
                    "envs_present": es, "n_envs": len(es), "n_envs_expected": len(envs_used),
                    "envs_missing": [e for e in envs_used if e not in es],
                    "seed_value": jnum(r["per_seed"][sd]), "point_mean": jnum(r["mean"]),
                    "drawn": r["n_seeds"] >= MIN_SEEDS})
        keep = [r for r in rows if r["n_seeds"] >= MIN_SEEDS]
        if not keep:
            continue
        xs = np.array([r["step"] for r in keep], float)
        ys = np.array([r["mean"] for r in keep], float)
        ss = np.array([r["se"] if r["se"] is not None else np.nan for r in keep], float)
        xmax_a = max(xmax_a, xs.max())

        # per-seed traces faint underneath (baseline arm only -- eg would clutter),
        # truncated to the same steps as the mean so no single-seed tail runs on
        last = keep[-1]["step"]
        if arm == "base":
            seeds = sorted({s for r in rows for s in r["per_seed"]})
            for sd in seeds:
                px = [r["step"] for r in rows if sd in r["per_seed"] and r["step"] <= last]
                py = [r["per_seed"][sd] for r in rows if sd in r["per_seed"] and r["step"] <= last]
                a_top = max(a_top, max(py))
                axA.plot(px, py, color=hue, lw=0.75, alpha=0.24, zorder=2, solid_capstyle="round")

        band = np.isfinite(ss)
        a_top = max(a_top, float(np.nanmax(ys + np.where(band, ss, 0.0))))
        axA.fill_between(xs[band], (ys - ss)[band], (ys + ss)[band], color=hue,
                         alpha=0.15 if arm == "base" else 0.07, lw=0, zorder=1)
        axA.plot(xs, ys, color=hue, lw=lw, ls=ls, marker=mk, ms=ms, alpha=alpha,
                 mec=hue, mfc=hue if arm == "base" else SURF, mew=1.1, zorder=3)
        # a point where some seed averaged fewer than all the envs is not the same
        # measurement as its neighbours -- ring it, neutrally (this is a data-coverage
        # mark, not a condition, so it may not borrow the arm's hue)
        for r in keep:
            if not r["partial_seeds"]:
                continue
            axA.plot([r["step"]], [r["mean"]], marker="o", ms=ms + 4.4, ls="none",
                     mfc="none", mec=INK, mew=1.15, zorder=5)
            axA.plot([r["step"], r["step"]], [r["mean"], r["mean"] + 0.030],
                     color=MUT, lw=0.9, zorder=4.6, solid_capstyle="butt")
        a_ends.append((xs[-1], ys[-1], hue, alpha, lab))

    axA.axvspan(late_step, xmax_a + 2.0, color=GRID, alpha=0.30, lw=0, zorder=0.5)
    axA.text(late_step + 0.7, 0.004, f"pooled-late window (steps >= {late_step}), panel B",
             fontsize=6.9, color=MUT, va="bottom", zorder=6)
    axA.set_xlim(-1.6, xmax_a + 17.5)
    # reserve the top ~16% for the note so no curve or band runs into it
    a_lo = -0.010
    axA.set_ylim(a_lo, a_lo + (a_top - a_lo) / 0.775)
    lab_x = xmax_a + 2.6
    lab_y = nudge([e[1] for e in a_ends], 0.046)
    for (x, y, hue, alpha, lab), ly in zip(a_ends, lab_y):
        axA.annotate(lab, xy=(x, y), xytext=(lab_x, ly), fontsize=8.2, color=hue,
                     alpha=max(alpha, 0.9), va="center", ha="left", linespacing=1.3,
                     zorder=6, arrowprops=dict(arrowstyle="-", color=hue, alpha=0.45,
                                               lw=0.7, shrinkA=1.5, shrinkB=2.5))
    n_partial_drawn = sum(1 for p in panel_a["_partial_env_points_found"] if p["drawn"])
    n_partial_cut = len(panel_a["_partial_env_points_found"]) - n_partial_drawn
    cut_txt = ("" if not n_partial_cut else
               f", {n_partial_cut} past the {MIN_SEEDS}-seed cut (unplotted)")
    style(axA, "A  Transfer test over training: exploit rate where the opponent is IDENTICAL in both arms",
          f"exploit rate ({len(SHARED_ENVS)} shared-opponent envs, equal weight)", "training step",
          note=(f"{', '.join(SHARED_ENVS[:-1])} and {SHARED_ENVS[-1]} draw the SAME opponent populations in both arms, so the environment is held fixed\n"
                "and only the training opponent differs. A gap here is a learned-policy difference; a flat pair is not one.\n"
                "Baseline pair drawn heavy, eg pair light -- the eg pair is where separation appears. Faint lines: individual seeds\n"
                f"(baseline only). Every curve stops at the last step with at least {MIN_SEEDS} surviving seeds; no single-seed tail is drawn.\n"
                f"Hollow ring + tick: at that step some seed had no episode in one of the {len(SHARED_ENVS)} envs, so its contribution is a mean over the\n"
                f"survivors only and n_seeds overstates the coverage. {n_partial_drawn} ringed here{cut_txt}; kept, not dropped; n_envs_per_seed is in the JSON."))

    # ============================================================ PANEL B
    groups = list(SHARED_ENVS) + [POOLED_LABEL]
    bspec = [("base", "grim", GRIM, "o", -0.255, 1.0), ("base", "tft", TFT, "s", -0.085, 1.0),
             ("eg", "grim", GRIM, "o", 0.085, 0.58), ("eg", "tft", TFT, "s", 0.255, 0.58)]
    panel_b: dict = {"_metric": f"exploit_rate pooled over steps >= {late_step}",
                     "_source": {"per_env": "shared_opponent_envs[<opp>/<arm>/<env>].pooled_late",
                                 "pooled": "shared_opponent_envs.pooled_three_envs"},
                     "cells": {}}
    b_top = 0.0
    for gi, grp in enumerate(groups):
        for arm, opp, hue, mk, dx, alpha in bspec:
            if grp.startswith("POOLED"):
                blk = pooled3[f"{opp}/{arm}"]["exploit_rate"]
                nep = None
            else:
                blk = shared[f"{opp}/{arm}/{grp}"]["pooled_late"]["exploit_rate"]
                nep = blk.get("n_episodes")
            mean, se = blk["mean"], blk["se"]
            ps = {k: v for k, v in blk["per_seed"].items() if v is not None}
            panel_b["cells"][f"{grp}|{opp}/{arm}"] = {
                "mean": jnum(mean), "se": jnum(se), "n_seeds": blk["n_seeds"],
                "n_episodes": nep, "per_seed": {k: jnum(v) for k, v in ps.items()}}
            if mean is None:
                continue
            x = gi + dx
            for si, (sd, v) in enumerate(sorted(ps.items())):
                axB.plot([x + (si - 1) * 0.030], [v], marker=mk, ms=2.9, color=hue,
                         alpha=0.34 * alpha + 0.16, mec="none", ls="none", zorder=2)
                b_top = max(b_top, v)
            errbar_v(axB, x, mean, se, hue, lw=1.7, zorder=4)
            axB.plot([x], [mean], marker=mk, ms=8.0 if arm == "base" else 6.2, color=hue,
                     alpha=alpha, mec=INK if arm == "base" else hue,
                     mfc=hue if arm == "base" else SURF, mew=0.9, ls="none", zorder=3)
            b_top = max(b_top, mean + (se or 0.0) + 0.040)
            label_above(axB, x, mean, se, f"{mean:.3f}", INK2 if arm == "base" else MUT,
                        pad=0.007, fontsize=7.1, rotation=90)
        # dumbbell connector inside each arm, neutral (a pairing, not a condition)
        for arm, dxa, dxb in (("base", -0.255, -0.085), ("eg", 0.085, 0.255)):
            ya = panel_b["cells"][f"{grp}|grim/{arm}"]["mean"]
            yb = panel_b["cells"][f"{grp}|tft/{arm}"]["mean"]
            if ya is None or yb is None:
                continue
            axB.plot([gi + dxa, gi + dxb], [ya, yb], color=MUT, lw=1.0,
                     alpha=0.55 if arm == "base" else 0.38, zorder=2.5,
                     ls="-" if arm == "base" else (0, (2, 1.6)))
        axB.text(gi - 0.17, -0.028, "baseline", ha="center", fontsize=6.9, color=MUT)
        axB.text(gi + 0.17, -0.028, "eg", ha="center", fontsize=6.9, color=MUT)
    for gi in range(len(groups) - 1):
        axB.axvline(gi + 0.5, color=GRID, lw=0.9, zorder=0.5)
    axB.set_xticks(range(len(groups)))
    axB.set_xticklabels(groups, fontsize=8.6, color=INK2)
    axB.set_xlim(-0.52, len(groups) - 0.44)

    # flag the one place the pair separates
    pg = panel_b["cells"][f"{POOLED_LABEL}|grim/eg"]
    pt = panel_b["cells"][f"{POOLED_LABEL}|tft/eg"]
    d_eg = pg["mean"] - pt["mean"]
    se_eg = float(np.hypot(pg["se"], pt["se"]))
    ybr = max(pg["mean"] + pg["se"], pt["mean"] + pt["se"]) + 0.070
    axB.plot([3.085, 3.085, 3.255, 3.255], [ybr - 0.010, ybr, ybr, ybr - 0.010],
             color=INK2, lw=0.9, zorder=5)
    axB.text(3.17, ybr + 0.005,
             f"eg pair separates\n{d_eg:+.3f} +/- {se_eg:.3f}  ({abs(d_eg)/se_eg:.1f} SE)",
             ha="center", va="bottom", fontsize=7.2, color=INK, linespacing=1.35, zorder=6)
    # reserve the top ~14% of the panel for the note so no value label runs into it
    b_lo, b_need = -0.055, max(b_top, ybr + 0.048)
    axB.set_ylim(b_lo, b_lo + (b_need - b_lo) / 0.815)
    pgb, ptb = panel_b["cells"][f"{POOLED_LABEL}|grim/base"], panel_b["cells"][f"{POOLED_LABEL}|tft/base"]
    d_b = pgb["mean"] - ptb["mean"]
    se_b = float(np.hypot(pgb["se"], ptb["se"]))
    panel_b["pooled_contrast"] = {
        "baseline": {"delta_grim_minus_tft": jnum(d_b), "se_quadrature": jnum(se_b),
                     "abs_z": jnum(abs(d_b) / se_b)},
        "eg": {"delta_grim_minus_tft": jnum(d_eg), "se_quadrature": jnum(se_eg),
               "abs_z": jnum(abs(d_eg) / se_eg)}}
    # the partial-env problem panel A has to mark cannot arise here unless some seed
    # is missing an env over the whole pooled-late window -- checked, not assumed
    seed_envs: dict[str, set] = {}
    for grp in SHARED_ENVS:
        for arm, opp, *_ in bspec:
            for sd in panel_b["cells"][f"{grp}|{opp}/{arm}"]["per_seed"]:
                seed_envs.setdefault(f"{opp}/{arm}|seed={sd}", set()).add(grp)
    b_partial = {k: sorted(v) for k, v in sorted(seed_envs.items()) if len(v) < len(SHARED_ENVS)}
    panel_b["_env_coverage"] = {
        "n_envs_expected": len(SHARED_ENVS), "n_arm_seed_cells": len(seed_envs),
        "partial": b_partial,
        "_reading": ("every arm x seed contributes all envs over the pooled-late window, so no "
                     "endpoint number here averages a partial set" if not b_partial else
                     "some arm x seed is missing an env over the whole window; see `partial`")}
    b_cov = (f"All {len(SHARED_ENVS)} envs are present for all {len(seed_envs) // len(bspec)} seeds in every "
             f"cell here, so no endpoint number averages a partial set -- unlike A, which marks {n_partial_drawn}."
             if not b_partial else
             f"{len(b_partial)} arm x seed cells cover fewer than {len(SHARED_ENVS)} envs here: "
             + "; ".join(f"{k} -> {'+'.join(v)}" for k, v in b_partial.items()))
    style(axB, "B  The same test as an endpoint, per env",
          "exploit rate", None,
          note=("Pooled over steps >= " + str(late_step) + ". Small dots are individual training seeds; bars are between-seed SE.\n"
                f"Baseline pooled pair: {d_b:+.3f} +/- {se_b:.3f} ({abs(d_b)/se_b:.1f} SE) -- indistinguishable. The eg pair is not.\n"
                + b_cov))

    # ============================================================ PANEL C1 (dumbbell)
    arm_rows = ["grim/nohole", "grim/eg", "tft/nohole", "tft/eg", "tft/inf"]
    panel_c: dict = {"_metric": "exploit_rate", "_step": eval_step,
                     "dumbbell": {}, "forest": [], "verdict": {}}
    yy = {a: len(arm_rows) - 1 - i for i, a in enumerate(arm_rows)}
    c_any = []
    for arm in arm_rows:
        hue = GRIM if arm.startswith("grim") else TFT
        y = yy[arm]
        pts = {}
        for plays in ("grim", "tft"):
            k = f"{arm}|plays={plays}"
            if k not in bap:
                continue
            b = bap[k]["exploit_rate"]
            pts[plays] = (b["mean"], b["se"], b["n_seeds"], b["n_episodes"], bap[k]["diagonal"])
            panel_c["dumbbell"][k] = {"mean": jnum(b["mean"]), "se": jnum(b["se"]),
                                      "n_seeds": b["n_seeds"], "n_episodes": b["n_episodes"],
                                      "diagonal": bap[k]["diagonal"]}
        if len(pts) == 2:
            axC1.plot([pts["grim"][0], pts["tft"][0]], [y, y], color=MUT, lw=1.4,
                      alpha=0.6, zorder=2.5)
        for plays, (m, se, ns, nep, diag) in pts.items():
            mk = "o" if plays == "grim" else "s"
            if se is not None and np.isfinite(se):
                axC1.errorbar([m], [y], xerr=[se], fmt="none", ecolor=hue, elinewidth=1.7,
                              capsize=2.6, capthick=1.2, zorder=4)
                c_any += [m - se, m + se]
            c_any.append(m)
            axC1.plot([m], [y], marker=mk, ms=7.6 if diag else 6.8, ls="none",
                      mfc=hue if diag else SURF, mec=INK if diag else hue,
                      mew=1.3 if diag else 1.45, zorder=3)
            va = "bottom" if plays == "grim" else "top"
            dy = 0.17 if plays == "grim" else -0.17
            tag = f"{m:.3f}" + ("" if se is None else "")
            axC1.text(m, y + dy, tag, ha="center", va=va, fontsize=6.9, color=INK2, zorder=6)
    inf_cell = panel_c["dumbbell"]["tft/inf|plays=grim"]
    m_inf, n_inf = inf_cell["mean"], inf_cell["n_seeds"]
    axC1.text(m_inf + 0.026, yy["tft/inf"],
              f"{n_inf} train seed -> no SE bar;\nnever defects, either opponent",
              va="center", fontsize=6.9, color=MUT, linespacing=1.35, zorder=6)
    axC1.set_yticks([yy[a] for a in arm_rows])
    axC1.set_yticklabels([a.replace("/", " / ") for a in arm_rows], fontsize=8.6, color=INK2)
    axC1.set_ylim(-0.72, len(arm_rows) + 1.05)
    axC1.set_xlim(-0.016, max(c_any) + 0.058)
    axC1.text(-0.020, len(arm_rows) + 0.90,
              "row = the arm, i.e. the opponent it TRAINED against\n"
              "marker = the opponent it PLAYS here: circle grim, square tft\n"
              "filled = on-diagonal (plays the opponent it trained against)",
              ha="left", va="top", fontsize=7.1, color=MUT, linespacing=1.45, zorder=6)
    style(axC1, "C  Crossplay: hold the PLAYED opponent fixed", None,
          "exploit rate at step " + str(eval_step), gridaxis="x")

    # ============================================================ PANEL C2 (forest)
    rows = []
    for cond in ("nohole", "eg"):
        for plays in ("plays=grim", "plays=tft"):
            b = tvc[cond][plays]["exploit_rate"]
            rows.append({"condition": cond, "plays": plays, "metric": "exploit_rate",
                         "delta": b["delta"], "se": b["se"], "mean_a": b["mean_a"],
                         "mean_b": b["mean_b"], "n_seeds_a": b["n_seeds_a"],
                         "n_seeds_b": b["n_seeds_b"], "arm_a": tvc[cond][plays]["arm_a"],
                         "arm_b": tvc[cond][plays]["arm_b"], "flagged": False})
    top = verdict["ranked_top"][0]
    tb = tvc[top["condition"]][top["plays"]][top["metric"]]
    rows.append({"condition": top["condition"], "plays": top["plays"], "metric": top["metric"],
                 "delta": tb["delta"], "se": tb["se"], "mean_a": tb["mean_a"],
                 "mean_b": tb["mean_b"], "n_seeds_a": tb["n_seeds_a"],
                 "n_seeds_b": tb["n_seeds_b"], "arm_a": tvc[top['condition']][top['plays']]["arm_a"],
                 "arm_b": tvc[top['condition']][top['plays']]["arm_b"], "flagged": True})
    n_r = len(rows)
    f_lo, f_hi = [], []
    for i, r in enumerate(rows):
        y = n_r - 1 - i
        d, se = r["delta"], r["se"]
        col = MUT if r["flagged"] else INK          # a difference is NOT a condition
        if se is not None and np.isfinite(se) and se > 0:
            axC2.plot([d - SE_OUTER * se, d + SE_OUTER * se], [y, y], color=INK2, lw=1.0,
                      alpha=0.75, zorder=4)
            axC2.plot([d - SE_INNER * se, d + SE_INNER * se], [y, y], color=INK2, lw=3.0,
                      alpha=0.95, zorder=5)
            f_lo.append(d - SE_OUTER * se); f_hi.append(d + SE_OUTER * se)
        f_lo.append(d); f_hi.append(d)
        axC2.plot([d], [y], marker="D", ms=6.2, ls="none", mfc=col, mec=INK, mew=0.9, zorder=5.5)
        r["abs_z"] = jnum(abs(d) / se) if (se and np.isfinite(se)) else None
        panel_c["forest"].append({k: jnum(v) if isinstance(v, float) else v for k, v in r.items()})
    axC2.axvline(0.0, color=INK2, lw=1.1, zorder=1.5)
    axC2.axhline(0.5, color=GRID, lw=1.0, ls=(0, (3, 2)), zorder=1.5)
    xlo, xhi = min(f_lo) - 0.055, max(f_hi) + 0.030
    span = xhi - xlo
    axC2.set_xlim(xlo, xhi + span * 0.72)
    axC2.set_ylim(-4.35, n_r + 1.35)   # room under the rows for the exclusion note
    ticks, lbls = [], []
    for i, r in enumerate(rows):
        y = n_r - 1 - i
        ticks.append(y)
        lbls.append(f"{r['condition']} | {r['plays'].replace('=', ' ')}"
                    + ("\n" + r["metric"] if r["flagged"] else ""))
        zt = "" if r["abs_z"] is None else f"  ({r['abs_z']:.2f} SE)"
        axC2.text(xhi + span * 0.045, y, f"{r['delta']:+.3f} +/- {r['se']:.3f}{zt}",
                  va="center", ha="left", fontsize=7.2,
                  color=MUT if r["flagged"] else INK2, zorder=6)
    axC2.set_yticks(ticks)
    axC2.set_yticklabels(lbls, fontsize=7.9, color=INK2)
    n_test, n2, n2v, n1 = (verdict["n_contrasts_tested"], verdict["n_over_2se"],
                           verdict["n_over_2se_with_both_sides_varying"], verdict["n_over_1se"])
    n_all, n_testable, excluded = contrast_census(tvc)
    n_excl = len(excluded)
    pin_txt = pinned_value_text(excluded)
    by_metric: dict[str, list[str]] = {}
    for e in excluded:
        by_metric.setdefault(e["metric"], []).append(f"{e['condition']} | {e['plays'].replace('=', ' ')}")
    excl_txt = "; ".join(f"{m} at " + " and ".join(v) for m, v in by_metric.items())
    n_plain = sum(1 for r in rows if not r["flagged"])
    top_z = verdict["largest_abs_z"]["abs_z"]
    flag_row = rows[-1]
    zv_side = verdict["largest_abs_z"].get("zero_variance_side") or []
    zv_arm = flag_row["arm_a"] if "a" in zv_side else flag_row["arm_b"]
    c2_note = (
        f"Rows 1-{n_plain} are exploit rate; row {n_r} is the largest |z| over ALL metrics. "
        f"{n2} of {n_testable} testable contrasts clears {SE_OUTER} SE; {n1} clear {SE_INNER} SE; "
        f"{n2v} clears {SE_OUTER} SE with BOTH sides varying. The other {n_excl} of {n_all} are "
        f"untestable and excluded: {excl_txt}, both arms pinned at {pin_txt}, so |z| is undefined. "
        f"In the one that clears, the {zv_arm} side has zero between-seed variance, so quadrature "
        f"understates it -- read {top_z:.2f} SE as optimistic.")
    axC2.text(xlo + span * 0.015, -1.16,
              "\n".join(textwrap.wrap(c2_note, width=74, break_long_words=False,
                                      break_on_hyphens=False)),
              fontsize=6.5, color=MUT, va="top", ha="left", linespacing=1.42, zorder=6)
    panel_c["verdict"] = {"n_contrasts_tested": n_test, "n_over_2se": n2,
                          "n_over_2se_with_both_sides_varying": n2v, "n_over_1se": n1,
                          "largest_abs_z": {k: jnum(v) if isinstance(v, float) else v
                                            for k, v in verdict["largest_abs_z"].items()},
                          "_reading": verdict["_reading"]}
    panel_c["exclusions"] = {
        "n_contrasts_in_cache": n_all,
        "n_testable": n_testable,
        "n_untestable": n_excl,
        "excluded_contrasts": excluded,
        "excluded_names": [e["name"] for e in excluded],
        "_why": (f"{n_excl} of the {n_all} condition x plays x metric contrasts in "
                 f"trained_vs_contrast have delta 0.0 with se 0.0 because every seed on BOTH "
                 f"arms is pinned at {pin_txt}; |z| = 0/0 is undefined, so no |z| threshold can "
                 f"be applied to them and they are excluded from every count below."),
        "_headline": (f"{n2} of {n_testable} testable contrasts clears {SE_OUTER} SE; {n_excl} of "
                      f"{n_all} are untestable (both arms pinned at {pin_txt}, |z| undefined)."),
        "_agrees_with_cache_verdict": n_testable == n_test,
        "_source": ("computed here from crossplay.trained_vs_contrast: the cache's verdict block "
                    "records n_contrasts_tested but not which contrasts it dropped.")}
    style(axC2, "     grim-trained MINUS tft-trained", None,
          f"delta, played opponent held fixed  (thick +/-{SE_INNER} SE, thin +/-{SE_OUTER} SE)",
          gridaxis="x",
          note=(f"UNPAIRED: train_seed {'/'.join(str(s) for s in cross['_meta']['train_seeds'])} index different checkpoints\n"
                "across arms, so the SE is quadrature, not a paired SE.\n"
                "Markers are neutral -- a difference is not a condition\nand must not borrow a condition's hue."))

    # ============================================================ PANEL D
    dspec = [("grim/nohole", GRIM, "o", "solid", 2.2, 1.0), ("grim/eg", GRIM, "o", (0, (1, 1.6)), 1.2, 0.6),
             ("tft/nohole", TFT, "s", (0, (5, 2)), 2.2, 1.0), ("tft/eg", TFT, "s", (0, (1, 1.6)), 1.2, 0.6)]
    Ns = sorted({int(k.split("|N=")[1]) for k in endgame["all_seeds"]["by_arm_length"]})
    panel_d: dict = {"_metric": "first_defect_index_given_defect", "_lengths": Ns,
                     "all_seeds": {}, EXCL_KEY: {}, "slopes": {}}
    axD.plot(Ns, [n - 1 for n in Ns], color=MUT, lw=1.1, ls=(0, (3, 2.4)), zorder=1.5)
    d_ends = []
    for arm, hue, mk, ls, lw, alpha in dspec:
        for tag, ax_alpha in (("all_seeds", 1.0), (EXCL_KEY, 0.0)):
            blk = endgame[tag]["by_arm_length"]
            xs, ys, ss = [], [], []
            for N in Ns:
                b = blk[f"{arm}|N={N}"]["first_defect_index_given_defect"]
                xs.append(N); ys.append(b["mean"]); ss.append(b["se"])
                panel_d[tag][f"{arm}|N={N}"] = {
                    "mean": jnum(b["mean"]), "se": jnum(b["se"]), "n_seeds": b["n_seeds"],
                    "n_episodes_defined": b["n_episodes_defined"]}
            if tag == "all_seeds":
                axD.plot(xs, ys, color=hue, lw=lw, ls=ls, alpha=alpha, zorder=3)
                for x, y, se in zip(xs, ys, ss):
                    errbar_v(axD, x, y, se, hue, lw=1.6, zorder=4)
                    axD.plot([x], [y], marker=mk, ms=7.4 if lw > 2 else 5.4, ls="none",
                             color=hue, alpha=alpha, mec=INK if lw > 2 else hue,
                             mfc=hue if lw > 2 else SURF, mew=0.9, zorder=3)
                d_ends.append((xs[-1], ys[-1], hue, alpha, arm))
    # sensitivity: only grim/nohole changes when the compromised seed is dropped
    for N in Ns:
        a = panel_d["all_seeds"][f"{EXCL_ARM}|N={N}"]["mean"]
        e = panel_d[EXCL_KEY][f"{EXCL_ARM}|N={N}"]["mean"]
        axD.plot([N + 0.26], [e], marker="o", ms=5.6, ls="none", mfc="none", mec=GRIM,
                 mew=1.3, alpha=0.85, zorder=3)
        panel_d[f"sensitivity_{EXCL_ARM.replace('/', '_')}_N{N}"] = {
            "all_seeds": jnum(a), EXCL_KEY: jnum(e), "shift": jnum(e - a)}
    axD.plot([], [], color=MUT, lw=1.1, ls=(0, (3, 2.4)), label="true final round (N - 1)")
    axD.plot([], [], marker="o", ms=5.6, ls="none", mfc="none", mec=GRIM, mew=1.3,
             label=f"{EXCL_ARM.replace('/', ' / ')} with the compromised seed {EXCL_SEED} excluded")
    axD.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc="lower right",
               bbox_to_anchor=(1.0, 0.015), handletextpad=0.8)
    lab_yd = nudge([e[1] for e in d_ends], 0.72)
    for (x, y, hue, alpha, arm), ly in zip(d_ends, lab_yd):
        axD.annotate(arm.replace("/", " / "), xy=(x, y), xytext=(x + 0.45, ly), fontsize=7.9,
                     color=hue, alpha=max(alpha, 0.9), va="center", zorder=6,
                     arrowprops=dict(arrowstyle="-", color=hue, alpha=0.45, lw=0.7,
                                     shrinkA=1.5, shrinkB=1.5))
    slope_lines = []
    for arm, hue, mk, ls, lw, alpha in dspec:
        s_all = endgame["all_seeds"]["first_defect_index_slope_vs_num_rounds"][arm]["per_seed_slope"]
        s_ex = endgame[EXCL_KEY]["first_defect_index_slope_vs_num_rounds"][arm]["per_seed_slope"]
        panel_d["slopes"][arm] = {
            "all_seeds": {"mean": jnum(s_all["mean"]), "se": jnum(s_all["se"]), "n_seeds": s_all["n_seeds"]},
            EXCL_KEY: {"mean": jnum(s_ex["mean"]), "se": jnum(s_ex["se"]), "n_seeds": s_ex["n_seeds"]}}
        txt = f"{arm:11s} {s_all['mean']:+.3f} +/- {s_all['se']:.3f}"
        if abs(s_ex["mean"] - s_all["mean"]) > 1e-9:
            txt += f"    excl s{EXCL_SEED}: {s_ex['mean']:+.3f} +/- {s_ex['se']:.3f}"
        slope_lines.append((txt, hue))
    axD.text(5.68, 12.55, "fitted slope of first-defection index vs N, between-seed SE",
             fontsize=7.7, color=INK2, va="top", zorder=6)
    for i, (txt, hue) in enumerate(slope_lines):
        axD.text(5.68, 12.00 - i * 0.56, txt, fontsize=7.6, color=hue, va="top",
                 family="DejaVu Sans Mono", zorder=6)
    axD.set_xticks(Ns)
    axD.set_xlim(5.30, 16.9)
    axD.set_ylim(3.6, 15.3)
    slope_means = [panel_d["slopes"][arm]["all_seeds"]["mean"] for arm, *_ in dspec]
    style(axD, "D  Held-out horizons: game lengths never trained on",
          "mean first-defection index (episodes with a defection)", "N (rounds in the game)",
          note=(f"All {len(dspec)} arms track the true final round, fitted slopes {min(slope_means):+.3f} to "
                f"{max(slope_means):+.3f}, and the grim and\n"
                "tft arms lie on top of each other. Both the all-seeds and the compromised-seed-\n"
                f"excluded value are shown for {EXCL_ARM.replace('/', ' / ')} rather than silently choosing one.\n"
                "Diagonal only: each arm plays the opponent it trained against here."))

    # ============================================================ header
    fig.suptitle("The opponent split changed the gradient, not the policy \u2014 except where it meets the endgame penalty",
                 fontsize=14.5, color=INK, x=0.006, ha="left", y=0.985)

    n_train_ep = sum(shared[f"{o}/{a}/{e}"]["pooled_late"]["exploit_rate"]["n_episodes"]
                     for o in ("grim", "tft") for a in ("base", "eg") for e in SHARED_ENVS)
    # the gate threshold is carried in the key name the eval cache counts drops under
    gate_key = next(k for k in cross["_meta"] if k.startswith("rows_dropped_invalid_gt_"))
    gate = gate_key.rsplit("_gt_", 1)[1]
    ep_seeds, tr_seeds = cross["_meta"]["episode_seeds"], cross["_meta"]["train_seeds"]
    seed_ids = "/".join(str(s) for s in tr_seeds)
    n_arm_seeds = len(train["meta"]["seeds"])
    env_list = f"{', '.join(SHARED_ENVS[:-1])} and {SHARED_ENVS[-1]}"
    paras = [
        ("Any grim-vs-tft difference measured in `ipd` is uninterpretable, because the opponent itself differs there. "
         "Three handles break that confound, and this figure shows all three.", INK2),
        (f"(1) SHARED-OPPONENT ENVS (A, B) -- {env_list} draw IDENTICAL opponent populations in both arms, verified against every trace file, "
         "so the environment is held fixed and only the training opponent varies; a gap there is a learned-policy difference and a flat pair is not. "
         "The shared populations are public_goods: strict_punisher / conditional_punisher / conditional_noisy;  dond: sceptic / auditor / verifier;  "
         "trust: responsive / impatient / responsive_exit. Only the ipd opponent differs by arm, which is why ipd is absent from this figure.", INK2),
        (f"(2) CROSSPLAY (C) -- frozen step-{eval_step} adapters played BOTH opponents, so the PLAYED opponent can be held fixed while the TRAINING opponent varies.      "
         f"(3) HELD-OUT HORIZONS (D) -- the same frozen adapters replayed at N = {', '.join(str(n) for n in Ns)}, game lengths never trained on.", INK2),
        (f"Contrast count in C. trained_vs_contrast holds {n_all} condition x plays x metric contrasts. {n_excl} of them are UNTESTABLE -- {excl_txt}, where every seed on both arms is "
         f"pinned at {pin_txt}, so delta and the quadrature SE are both exactly zero and |z| = 0/0 is undefined. They are excluded, and every count on this page runs over the "
         f"{n_testable} testable contrasts, not over all {n_all}: {n2} of {n_testable} clears {SE_OUTER} SE, {n1} clear {SE_INNER} SE, and {n2v} clears {SE_OUTER} SE with both sides varying.", INK2),
        (f"Denominators. A, B: {n_train_ep} training episodes, {n_arm_seeds} seeds per arm, pooled over steps >= {late_step}, each env weighted equally so a larger env cannot outweigh a smaller one.      "
         f"C: {cross['_meta']['rows_kept']} of {cross['_meta']['rows_read']} crossplay episodes kept after the invalid_rate > {gate} gate, {len(ep_seeds)} episode seeds x up to {len(tr_seeds)} training seeds per cell, all at step {eval_step}.      "
         f"D: {endgame['all_seeds']['n_episodes']} episodes, {endgame[EXCL_KEY]['n_episodes']} with the compromised seed excluded.", INK2),
        ("Error bars are BETWEEN TRAINING SEED everywhere: each checkpoint is collapsed to one number over its episode seeds first, then the spread is taken across "
         f"checkpoints as sd(ddof=1)/sqrt(n_seeds). A null SE (fewer than {MIN_SEEDS} seeds) draws no bar at all, never a zero-length one. The trained_vs_contrast SE in C is "
         f"UNPAIRED quadrature, sqrt(se_a^2 + se_b^2), because train_seed {seed_ids} index different checkpoints in the grim and the tft arm; the same applies to the "
         "pooled contrast quoted in B.", INK2),
        (f"A wide interval containing zero is a FAILURE TO DETECT a difference, not a demonstration that none exists. With {n_arm_seeds} training seeds per arm these data bound "
         f"the size of any baseline policy difference; they do not rule one out. Compromised checkpoint: {EXCL_ARM} train_seed {EXCL_SEED} emits an empty decision answer on "
         "the majority of turns while its invalid_rate reads clean, so the repo's gate is blind to it -- D draws both variants, and it is also one of the seeds "
         f"behind the {EXCL_ARM} rows in C.      "
         f"In A, {n_partial_drawn} plotted points average fewer than the {len(SHARED_ENVS)} shared envs for some seed and are ringed; B has none.", RED),
    ]
    hdr = []
    for txt, col in paras:
        wrapped = textwrap.wrap(txt, width=252, break_long_words=False, break_on_hyphens=False)
        hdr += [(w if i == 0 else "      " + w, col) for i, w in enumerate(wrapped)]
    y0, dy = 0.9635, 0.0134
    for i, (txt, col) in enumerate(hdr):
        fig.text(0.006, y0 - i * dy, txt, fontsize=8.2, color=col, ha="left", va="top")

    fig.tight_layout(rect=[0.006, 0.004, 0.997, y0 - len(hdr) * dy - 0.008],
                     h_pad=3.2, w_pad=2.6)

    # ============================================================ outputs
    outdir = args.outdir
    png = outdir / f"{args.stem}.png"
    jsn = outdir / f"{args.stem}.json"
    fig.savefig(png, dpi=args.dpi, facecolor=fig.get_facecolor())

    payload = {
        "figure": args.stem,
        "question": ("Did the grim/tft opponent split change the learned POLICY, or only the "
                     "ENVIRONMENT the policy was measured in?"),
        "answer": {
            "headline": ("The opponent split changed the gradient, not the policy -- except where "
                         "it meets the endgame penalty."),
            "handle_1_shared_opponent_envs": {
                "baseline": panel_b["pooled_contrast"]["baseline"],
                "eg": panel_b["pooled_contrast"]["eg"],
                "reading": (f"On the baseline arm the two policies are indistinguishable on the "
                            f"{len(SHARED_ENVS)} envs whose opponents are identical in both arms. On the eg "
                            "arm they separate, so the opponent split interacts with the endgame penalty "
                            "even though it does nothing on its own.")},
            "handle_2_crossplay": {
                "reading": (f"With the played opponent held fixed, every baseline exploit-rate contrast "
                            f"sits within {SE_INNER} between-seed SE of zero. Over all metrics, {n2} of "
                            f"{n_testable} TESTABLE contrasts clears {SE_OUTER} SE and {n2v} does so with both "
                            f"sides varying. {n_excl} of the {n_all} contrasts in the cache are untestable and "
                            f"are excluded from those counts: both arms are pinned at {pin_txt}, so delta and "
                            f"the quadrature SE are both zero and |z| is undefined ({excl_txt})."),
                "exclusions": panel_c["exclusions"],
                "verdict": panel_c["verdict"]},
            "handle_3_held_out_horizons": {
                "reading": (f"All {len(dspec)} arms track the true final round with fitted slopes "
                            f"{min(slope_means):+.3f} to {max(slope_means):+.3f} at game lengths never trained "
                            "on; the grim and tft arms lie on top of each other."),
                "slopes": panel_d["slopes"]}},
        "error_bar_definitions": {
            "primary": ("BETWEEN TRAINING SEED: each checkpoint collapsed to one number over its "
                        "episode seeds, then sd(ddof=1)/sqrt(n_seeds) across checkpoints."),
            "null_se": (f"se is null when n_seeds < {MIN_SEEDS}; a null SE draws NO bar, never a "
                        "zero-length one."),
            "zero_se": (f"se is 0.0 when every seed on both arms is pinned at the same value; that "
                        f"contrast carries no |z| and is excluded from the counts, listed under "
                        f"panels.C.exclusions."),
            "trained_vs_contrast": (f"UNPAIRED quadrature sqrt(se_a^2 + se_b^2): train_seed {seed_ids} "
                                    "index different checkpoints in the grim and the tft arm."),
            "panel_b_pooled_contrast": ("quadrature of the two between-seed SEs; also unpaired, seeds "
                                        "index different runs across arms."),
            "cache_conventions": {"train": train["meta"]["error_bar_convention"],
                                  "eval": ev["meta"]["error_bars"]}},
        "panels": {"A": panel_a, "B": panel_b, "C": panel_c, "D": panel_d},
        "provenance": {
            "caches": [{"path": str(p),
                        "mtime_utc": datetime.fromtimestamp(
                            p.stat().st_mtime, timezone.utc).isoformat(timespec="seconds"),
                        "size_bytes": p.stat().st_size} for p in (TRAIN_CACHE, EVAL_CACHE)],
            "train_generated_utc": train["meta"]["generated_utc"],
            "eval_built_utc": ev["meta"]["built_utc"],
            "wave": ev["meta"]["wave"],
            "shared_opponent_envs_why": shared["why"],
            "opponent_populations": train["meta"]["opponent_populations"],
            "eval_step": eval_step, "late_step": late_step,
            "crossplay_meta": cross["_meta"],
            "arm_naming": "the training cache calls the baseline arm `base`; the eval cache calls it `nohole`"},
        "caveat": {
            "compromised_checkpoint": endgame["_flagged_cell"],
            "endgame_restriction": endgame["_restriction"],
            "endgame_diagonal_only": endgame["_diagonal_only"],
            "ceiling": verdict["largest_abs_z"].get("_ceiling_caveat"),
            "tft_inf_degenerate": cross["_meta"]["tft_inf_is_degenerate"],
            "no_grim_inf_crossplay": tvc["_only_nohole_and_eg"],
            "untestable_contrasts": panel_c["exclusions"]["_why"],
            "partial_env_points": panel_a["_partial_env_points"],
            "defection_and_betrayal_rate": (f"null in the {len(SHARED_ENVS)} shared-opponent envs -- those "
                                            "keys do not exist in the non-ipd stats dicts and are not plotted.")},
        "not_an_equivalence_claim": (
            "This figure does NOT claim the grim-trained and tft-trained policies are identical. "
            "A wide interval containing zero is a failure to detect a difference, not a demonstration "
            f"that none exists. With {n_arm_seeds} training seeds per arm the resolvable claim is an UPPER BOUND on "
            "the size of any policy difference on the baseline arm, not its absence. The eg arm shows a "
            "difference at the same sample size, which is what makes the baseline null informative rather "
            "than merely underpowered."),
    }
    jsn.write_text(json.dumps(payload, indent=1))
    print(f"[fig] wrote {png}")
    print(f"[fig] wrote {jsn}")


if __name__ == "__main__":
    main()
