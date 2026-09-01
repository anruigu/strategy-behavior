"""/home/allie/venvs/tinker-ipd/bin/python fig4_knob_by_opponent.py

Figure 4 -- the opponent only matters as an interaction with the endgame penalty.

Sibling figures (fig1/fig2/fig3) establish that training against grim versus
tit-for-tat, on its own, produces no measurable difference in the learned policy.
This figure shows the one place the opponent does matter: the endgame penalty
suppresses late betrayal against both scripted opponents, but several times more
strongly against tit-for-tat, and the resulting policies then differ on envs where
the opponent was never manipulated at all.

COLOUR ENCODING IS INVERTED RELATIVE TO THE SIBLING FIGURES.  Here the ARM is the
contrast, so colour encodes the arm (PURPLE base / ORANGE eg / BLUE inf) and the
opponent is carried by panel position, marker shape and line style.  The siblings
do the reverse because there the opponent is the contrast.

Reads (never writes) train_strategy.json and eval_strategy.json.
"""

from __future__ import annotations
import argparse, json, textwrap
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
PURPLE, ORANGE, BLUE = "#7a5bd6", "#eb6834", "#2a78d6"   # arm palette: base / eg / inf
GRIM, TFT = "#00918f", "#b8236f"                          # opponent palette (siblings only)
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
PAPER, RED = "#f9f9f7", "#b5342a"

TRAIN_JSON = HERE / "train_strategy.json"
EVAL_JSON = HERE / "eval_strategy.json"

ARM_COLOR = {"base": PURPLE, "eg": ORANGE, "inf": BLUE}
OPP_MARKER = {"grim": "o", "tft": "s"}
OPP_LS = {"grim": "-", "tft": "--"}

DELTA_STEP_MIN = 8          # panel A averages the endgame-rate curve over steps >= this
FLOOR_EPS = 0.02            # a marker below this in every arm is called floor-limited


# --------------------------------------------------------------------------- #
# house style
# --------------------------------------------------------------------------- #
def style(ax, title, ylab, xlab=None, note=None):
    ax.set_title(title, fontsize=10.5, color=INK, loc="left", pad=8)
    ax.set_ylabel(ylab, fontsize=9, color=INK2)
    if xlab:
        ax.set_xlabel(xlab, fontsize=9, color=INK2)
    ax.set_facecolor(SURF)
    ax.grid(True, axis="y", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.tick_params(colors=MUT, labelsize=8, length=0)
    if note:
        ax.text(0.015, 0.965, note, transform=ax.transAxes, fontsize=7.5,
                color=MUT, va="top")


def hgrid(ax):
    """Horizontal-dumbbell panels grid on x, not y."""
    ax.grid(False, axis="y")
    ax.grid(True, axis="x", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)


# --------------------------------------------------------------------------- #
# small numeric helpers -- every SE here is BETWEEN TRAINING SEED
# --------------------------------------------------------------------------- #
def between_seed(vals):
    """(mean, se, n) over seeds. se is None when n < 2 -- never 0-by-fiat."""
    v = [float(x) for x in vals if x is not None and np.isfinite(float(x))]
    if not v:
        return None, None, 0
    m = float(np.mean(v))
    if len(v) < 2:
        return m, None, 1
    return m, float(np.std(v, ddof=1) / np.sqrt(len(v))), len(v)


def paired_delta(a_per_seed, b_per_seed, denominator=None):
    """b minus a, paired on seed index (both arms launched with the same seed).

    denominator travels with the delta so a rate difference is never reported without
    the count each side of it was taken over.
    """
    keys = sorted(set(a_per_seed) & set(b_per_seed))
    d = {k: b_per_seed[k] - a_per_seed[k] for k in keys
         if a_per_seed.get(k) is not None and b_per_seed.get(k) is not None}
    m, se, n = between_seed(d.values())
    out = {"per_seed": d, "mean": m, "se": se, "n_seeds": n}
    if denominator is not None:
        out["denominator"] = denominator
    return out


def unpaired_se(se_a, se_b):
    if se_a is None or se_b is None:
        return None
    return float(np.hypot(se_a, se_b))


def f(v, nd=3):
    return "--" if v is None else f"{v:.{nd}f}"


def pm(m, se, nd=3):
    return f(m, nd) if se is None else f"{f(m, nd)} +/- {f(se, nd)}"


def ebar(ax, x, y, se, color, horizontal=False, lw=1.6, z=5, capsize=0):
    """A null SE draws NO bar. Never a zero-length stand-in for missing spread."""
    if se is None:
        return
    if horizontal:
        ax.errorbar(x, y, xerr=se, fmt="none", ecolor=color, elinewidth=lw,
                    capsize=capsize, zorder=z)
    else:
        ax.errorbar(x, y, yerr=se, fmt="none", ecolor=color, elinewidth=lw,
                    capsize=capsize, zorder=z)


# --------------------------------------------------------------------------- #
# panel A -- the knob over training, both opponents
# --------------------------------------------------------------------------- #
def curve_window_mean(rec, step_min):
    """Per-seed mean of a dense curve over steps >= step_min, plus the per-seed count
    of optimizer steps that mean was actually taken over.

    The count is the denominator of the window mean.  train/endgame_rate is logged once
    per optimizer step as an episode-weighted average the trainer has already reduced,
    so the unit being averaged here is the STEP, not the episode.
    """
    steps = np.asarray(rec["steps"], dtype=float)
    out, n = {}, {}
    for seed, series in rec["per_seed"].items():
        a = np.array([np.nan if v is None else float(v) for v in series], dtype=float)
        m = (steps >= step_min) & ~np.isnan(a)
        out[seed] = float(a[m].mean()) if m.any() else None
        n[seed] = int(m.sum())
    return out, n


ENDGAME_DENOM_WHAT = (
    "optimizer steps x training seeds, NOT episodes. train/endgame_rate is emitted once per "
    "optimizer step, already reduced by the trainer to a single episode-weighted number over "
    "that step's rollout batch. The window statistic averages those per-step numbers over the "
    "window within a seed, then averages seeds, so its denominator is the number of logged "
    "optimizer steps in the window per seed and the number of seeds.")


def last_step_with_n_seeds(rec, k):
    steps = np.asarray(rec["steps"], dtype=float)
    ns = np.asarray([0 if v is None else int(v) for v in rec["n_seeds"]])
    ok = ns >= k
    return int(steps[ok].max()) if ok.any() else None


def panel_a(ax, T, out):
    curves = T["metrics_curves"]
    labels = []
    ymax = 0.0
    for opp in ("grim", "tft"):
        for arm in ("base", "eg", "inf"):
            rec = curves.get(f"{opp}/{arm}", {}).get("train/endgame_rate")
            if rec is None:
                continue
            col = ARM_COLOR[arm]
            steps = np.asarray(rec["steps"], dtype=float)
            mean = np.array([np.nan if v is None else float(v) for v in rec["mean"]])
            se = np.array([np.nan if v is None else float(v) for v in rec["se"]])

            # drawn only while the cell still carries >= 2 seeds: a single surviving
            # seed has no between-seed spread and the house rule draws no bar for it,
            # so drawing its mean as if it were a cell mean would overstate the run
            ceil = last_step_with_n_seeds(rec, 2)
            keep = steps <= (ceil if ceil is not None else -1)
            mean = np.where(keep, mean, np.nan)
            se = np.where(keep, se, np.nan)
            out.setdefault("drawn_step_ceiling_n_seeds_ge_2", {})[f"{opp}/{arm}"] = ceil
            out.setdefault("last_step_all_3_seeds", {})[f"{opp}/{arm}"] = \
                last_step_with_n_seeds(rec, 3)

            for series in rec["per_seed"].values():
                a = np.where(keep, np.array([np.nan if v is None else float(v) for v in series]), np.nan)
                ax.plot(steps, a, ls=OPP_LS[opp], color=col,
                        lw=0.7, alpha=0.22, zorder=2, solid_capstyle="round")
                if np.isfinite(a).any():
                    ymax = max(ymax, float(np.nanmax(a)))

            band = ~np.isnan(mean) & ~np.isnan(se)
            if band.any():
                ymax = max(ymax, float(np.nanmax((mean + se)[band])))
            ax.fill_between(steps, mean - se, mean + se, where=band, color=col,
                            alpha=0.13, lw=0, zorder=2)
            ax.plot(steps, mean, ls=OPP_LS[opp], color=col,
                    lw=2.1 if arm != "inf" else 1.5, alpha=1.0 if arm != "inf" else 0.85,
                    zorder=3, solid_capstyle="round")

            good = ~np.isnan(mean)
            if good.any():
                labels.append([float(steps[good][-1]), float(mean[good][-1]),
                               f"{opp}/{arm}", col])

    labels.sort(key=lambda r: r[1])
    for i in range(1, len(labels)):
        if labels[i][1] - labels[i - 1][1] < 0.028:
            labels[i][1] = labels[i - 1][1] + 0.028
    for xe, ye, txt, col in labels:
        ax.plot([xe], [ye], marker=OPP_MARKER[txt.split("/")[0]], ms=4.6, color=col,
                mec=PAPER, mew=0.8, zorder=4)
        ax.text(xe + 1.0, ye, " " + txt, fontsize=8.4, color=col, va="center",
                ha="left", zorder=6,
                bbox=dict(boxstyle="square,pad=0.12", facecolor=PAPER,
                          edgecolor="none", alpha=0.8))

    # the deltas, computed here and read off nothing
    lines, denom_lines = [], []
    for opp in ("grim", "tft"):
        b, bn = curve_window_mean(curves[f"{opp}/base"]["train/endgame_rate"], DELTA_STEP_MIN)
        e, en = curve_window_mean(curves[f"{opp}/eg"]["train/endgame_rate"], DELTA_STEP_MIN)
        d = paired_delta(b, e)
        bm, bse, _ = between_seed(b.values())
        em, ese, _ = between_seed(e.values())

        pair = sorted(d["per_seed"])
        d["window"] = (f"steps >= {DELTA_STEP_MIN}; every logged step at or above it that the "
                       f"seed actually reached is included, so the count differs by seed")
        d["pairing"] = (
            "PAIRED on seed index: {opp}/base/sN and {opp}/eg/sN were launched with the same "
            "seed, so the per-seed difference is formed first and the SE is the between-seed SE "
            "of those differences. The UNPAIRED quadrature alternative sqrt(se_base^2+se_eg^2) "
            "is carried beside this block as delta_se_if_unpaired; the two agree on the mean by "
            "construction and differ only in the SE.".replace("{opp}", opp))
        d["denominator"] = ENDGAME_DENOM_WHAT
        d["steps_per_seed"] = {s: {"base": bn.get(s), "eg": en.get(s)} for s in pair}
        d["steps_total"] = {"base": int(sum(bn.get(s, 0) for s in pair)),
                            "eg": int(sum(en.get(s, 0) for s in pair))}

        out[opp] = {
            "base_per_seed": b, "base_mean": bm, "base_se": bse,
            "base_steps_per_seed": bn,
            "eg_per_seed": e, "eg_mean": em, "eg_se": ese,
            "eg_steps_per_seed": en,
            "delta_eg_minus_base": d,
            "delta_se_if_unpaired": unpaired_se(bse, ese),
            "denominator": {
                "what": ENDGAME_DENOM_WHAT,
                "step_window": f"steps >= {DELTA_STEP_MIN}",
                "n_steps_in_window_per_seed": {"base": bn, "eg": en},
                "n_steps_in_window_total": {"base": int(sum(bn.values())),
                                            "eg": int(sum(en.values()))},
                "n_seeds": {"base": sum(v is not None for v in b.values()),
                            "eg": sum(v is not None for v in e.values()),
                            "paired": d["n_seeds"]},
                "grid_steps_at_or_above_window": int(
                    (np.asarray(curves[f"{opp}/base"]["train/endgame_rate"]["steps"],
                                dtype=float) >= DELTA_STEP_MIN).sum()),
                "source": ("train_strategy.json metrics_curves['{opp}/base' and '{opp}/eg']"
                           "['train/endgame_rate'].steps / .per_seed / .n_seeds"
                           .replace("{opp}", opp)),
            },
            "last_all_seed_step_base": out["last_step_all_3_seeds"][f"{opp}/base"],
            "last_all_seed_step_eg": out["last_step_all_3_seeds"][f"{opp}/eg"],
        }
        sfmt = lambda c: "/".join(str(c.get(s, 0)) for s in pair)   # noqa: E731
        lines.append(f"  {opp:<5s} {d['mean']:+.3f} +/- {f(d['se'])}   (n={d['n_seeds']} seeds)")
        denom_lines.append(f"  {opp:<5s} {sfmt(bn)} base, {sfmt(en)} eg  steps in window")

    ratio = out["tft"]["delta_eg_minus_base"]["mean"] / out["grim"]["delta_eg_minus_base"]["mean"]
    out["tft_over_grim_delta_ratio"] = ratio

    box = (f"eg minus base, mean train/endgame_rate over steps >= {DELTA_STEP_MIN}\n"
           "paired on seed index, SE between training seed\n"
           + "\n".join(lines)
           + f"\n  the tft knob is {abs(ratio):.1f}x the grim knob\n"
           + "DENOMINATOR: optimizer steps x seeds, not episodes\n"
           + "\n".join(denom_lines))
    ax.text(0.985, 0.960, box, transform=ax.transAxes, fontsize=8.4, color=INK2,
            va="top", ha="right", linespacing=1.55, zorder=6, family="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor=PAPER, edgecolor=GRID, lw=0.8))

    # top 40% of the panel is reserved for the note, legend and delta box
    ytop = ymax / 0.60
    for opp in ("grim", "tft"):
        s = min(out[opp]["last_all_seed_step_base"], out[opp]["last_all_seed_step_eg"])
        ax.axvline(s, color=MUT, lw=0.8, ls=(0, (2, 3)), alpha=0.6, zorder=1)
        ax.text(s + 0.5, 0.006 * ytop, f"3-seed ceiling, {opp}", fontsize=7.2,
                color=MUT, va="bottom", ha="left", zorder=6)

    xmax = max(r[0] for r in labels)
    ax.set_xlim(-1.5, xmax + 14)
    ax.set_ylim(0, ytop)
    ax.set_yticks(np.arange(0, ymax, 0.1))
    style(ax, "A.  The endgame penalty pulls late betrayal down against both opponents, "
              "much harder against tit-for-tat",
          "train/endgame_rate  (pooled over all 7 trained envs)", "training step",
          note="Colour = ARM (purple base / orange eg / blue inf);\n"
               "opponent = line style and end marker (solid o grim,\n"
               "dashed s tft).  Band = between-seed SE, faint traces\n"
               "= individual seeds.  A curve stops where its cell falls\n"
               "below 2 seeds and therefore has no spread to show.")


# --------------------------------------------------------------------------- #
# panel B -- what the knob does behaviourally
# --------------------------------------------------------------------------- #
STATS_B = ["coop_rate", "ever_defect", "defects_last_round",
           "defect_before_last", "first_defect_from_end"]


def panel_b(ax, T, out):
    late, alls = T["pooled_late"], T["pooled_all"]
    rows, y = [], 0.0
    n_stats = len(STATS_B)
    for opp in ("grim", "tft"):
        for st in STATS_B:
            rows.append((opp, st, y))
            y -= 1.0
        y -= 0.7                     # hairline gap between the two opponent blocks
    ymin = y + 0.7

    label_x = 1.045
    for opp, st, yy in rows:
        b = late[f"{opp}/base"][st]
        e = late[f"{opp}/eg"][st]
        rec = {"opponent": opp, "stat": st,
               "base": {k: b[k] for k in ("mean", "se", "n_seeds", "n_episodes", "per_seed")},
               "eg": {k: e[k] for k in ("mean", "se", "n_seeds", "n_episodes", "per_seed")}}
        d = paired_delta(b["per_seed"], e["per_seed"], denominator={
            "unit": f"ipd trace episodes at steps >= {T['meta']['late_step']}",
            "base": b["n_episodes"], "eg": e["n_episodes"]})
        rec["delta_eg_minus_base"] = d
        rec["delta_se_if_unpaired"] = unpaired_se(b["se"], e["se"])

        # per-seed base->eg segments, one faint line each
        seeds = sorted(set(b["per_seed"]) & set(e["per_seed"]))
        for i, s in enumerate(seeds):
            bv, ev = b["per_seed"].get(s), e["per_seed"].get(s)
            if bv is None or ev is None:
                continue
            oy = yy + (i - (len(seeds) - 1) / 2) * 0.19
            ax.plot([bv, ev], [oy, oy], color=MUT, lw=0.7, alpha=0.45, zorder=2)
            ax.plot([bv], [oy], marker=OPP_MARKER[opp], ms=2.9, color=PURPLE,
                    alpha=0.5, mec="none", zorder=2)
            ax.plot([ev], [oy], marker=OPP_MARKER[opp], ms=2.9, color=ORANGE,
                    alpha=0.5, mec="none", zorder=2)

        if b["mean"] is not None and e["mean"] is not None:
            ax.annotate("", xy=(e["mean"], yy), xytext=(b["mean"], yy),
                        arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.5,
                                        shrinkA=3.0, shrinkB=3.0, alpha=0.85),
                        zorder=3)
        for val, col in ((b["mean"], PURPLE), (e["mean"], ORANGE)):
            if val is None:
                continue
            ax.plot([val], [yy], marker=OPP_MARKER[opp], ms=7.2, color=col,
                    mec=PAPER, mew=0.9, zorder=3)
        ebar(ax, b["mean"], yy, b["se"], PURPLE, horizontal=True, lw=1.5, z=4)
        ebar(ax, e["mean"], yy, e["se"], ORANGE, horizontal=True, lw=1.5, z=4)

        # inf reference, pooled over ALL trained steps: grim/inf has no late episodes
        iv = alls[f"{opp}/inf"][st]
        rec["inf_pooled_all"] = {k: iv[k] for k in ("mean", "se", "n_seeds", "n_episodes", "per_seed")}
        if iv["mean"] is not None:
            # offset off the paired row: inf is a reference, not a third point of the pair,
            # and it lands exactly on top of eg wherever both have bottomed out at zero
            ax.plot([iv["mean"]], [yy + 0.33], marker=OPP_MARKER[opp], ms=5.0, color=BLUE,
                    alpha=0.9, mec=PAPER, mew=0.8, zorder=3)
            ebar(ax, iv["mean"], yy + 0.33, iv["se"], BLUE, horizontal=True, lw=1.2, z=4)

        dtxt = f"{d['mean']:+.3f}" if d["mean"] is not None else "--"
        dse = f" +/- {f(d['se'])}" if d["se"] is not None else ""
        ax.text(label_x, yy, f"{f(b['mean'])} -> {f(e['mean'])}   d={dtxt}{dse}",
                fontsize=7.6, color=INK2, va="center", ha="left", zorder=6,
                family="monospace")
        out.setdefault("rows", []).append(rec)

    # is defects_last_round just ever_defect again?
    ident = all(
        late[f"{o}/{a}"]["ever_defect"]["per_seed"] == late[f"{o}/{a}"]["defects_last_round"]["per_seed"]
        for o in ("grim", "tft") for a in ("base", "eg"))
    out["defects_last_round_identical_to_ever_defect"] = bool(ident)

    ticklab = []
    for opp, st, yy in rows:
        lab = st
        if ident and st == "defects_last_round":
            lab = "defects_last_round (= ever_defect)"
        ticklab.append(lab)
    ax.set_yticks([r[2] for r in rows])
    ax.set_yticklabels(ticklab, fontsize=8)
    ax.set_ylim(ymin - 0.55, 3.7)
    ax.set_xlim(-0.045, 1.66)
    ax.set_xticks(np.arange(0, 1.05, 0.2))

    sep = rows[n_stats - 1][2] - 0.85
    ax.axhline(sep, color=GRID, lw=1.0, zorder=1)
    ax.text(-0.035, 0.78, "GRIM   (marker o)", fontsize=8.5, color=INK, va="center", zorder=6)
    ax.text(-0.035, sep - 0.42, "TFT   (marker s)", fontsize=8.5, color=INK, va="center", zorder=6)
    ax.text(label_x, 0.78, "base -> eg      delta (between-seed SE)", fontsize=7.4,
            color=MUT, va="center", ha="left", zorder=6, family="monospace")

    style(ax, "B.  The knob changes HOW OFTEN the buzzer-beater is taken, not WHEN defection starts",
          "", "rate / rounds  (ipd trace episodes, steps >= 25)",
          note="Purple = base, orange = eg, blue = inf reference.  Thin grey segments are the three individual\n"
               "seeds; the thick arrow is the between-seed mean shift and the bars are between-seed SE.\n"
               "inf is pooled over ALL trained steps -- grim/inf stopped at step 15 and has no late episodes.")
    hgrid(ax)


# --------------------------------------------------------------------------- #
# panel C -- the transfer test
# --------------------------------------------------------------------------- #
SHARED_ENV_WEIGHTING = (
    "The pooled number is an EQUAL-WEIGHT mean over the three per-env seed means, not an "
    "episode-weighted pool, so this episode count is the support the estimate rests on and "
    "NOT the weight it was formed with: an env contributing few episodes and an env "
    "contributing many count the same in the mean. The actual per-env spread is in "
    "n_episodes_by_env.")


def shared_env_episodes(T, opp, arm):
    """Episode counts behind pooled_three_envs, summed from the per-env cache blocks.

    pooled_three_envs carries no n_episodes of its own; the counts only exist per env under
    shared_opponent_envs['<opp>/<arm>/<env>'], so they are summed here at render time.
    """
    S = T["shared_opponent_envs"]
    envs = S["pooled_three_envs"][f"{opp}/{arm}"]["envs"]
    by_env, per_seed = {}, {}
    for env in envs:
        blk = S[f"{opp}/{arm}/{env}"]["pooled_late"]["exploit_rate"]
        psn = {str(k): int(v) for k, v in (blk.get("per_seed_n") or {}).items()}
        n = blk.get("n_episodes")
        if n is None and not psn:
            raise KeyError(
                f"shared_opponent_envs['{opp}/{arm}/{env}'].pooled_late.exploit_rate carries "
                "neither n_episodes nor per_seed_n, so the panel C denominator cannot be "
                "derived; refusing to report a rate without one")
        by_env[env] = int(n) if n is not None else int(sum(psn.values()))
        for s, v in psn.items():
            per_seed[s] = per_seed.get(s, 0) + v
    return {
        "n_episodes": int(sum(by_env.values())),
        "n_episodes_by_env": by_env,
        "n_episodes_per_seed": dict(sorted(per_seed.items())),
        "_weighting": SHARED_ENV_WEIGHTING,
        "_source": ("summed at render time over shared_opponent_envs['<opp>/<arm>/<env>']"
                    ".pooled_late.exploit_rate.n_episodes for env in "
                    + ", ".join(envs)),
    }


def panel_c(ax, axd, T, out):
    p3 = T["shared_opponent_envs"]["pooled_three_envs"]
    envs = T["meta"]["shared_opponent_envs"]
    xs = {("grim", "base"): 0.0, ("grim", "eg"): 1.0,
          ("tft", "base"): 2.45, ("tft", "eg"): 3.45}

    for (opp, arm), x in xs.items():
        blk = p3[f"{opp}/{arm}"]["exploit_rate"]
        col = ARM_COLOR[arm]
        seeds = sorted(blk["per_seed"])
        for i, s in enumerate(seeds):
            v = blk["per_seed"][s]
            if v is None:
                continue
            ax.plot([x + (i - (len(seeds) - 1) / 2) * 0.17], [v], marker=OPP_MARKER[opp],
                    ms=4.0, color=col, alpha=0.42, mec="none", zorder=2)
        if blk["mean"] is not None:
            ax.plot([x], [blk["mean"]], marker=OPP_MARKER[opp], ms=11.0, color=col,
                    mec=PAPER, mew=1.1, zorder=3)
            top = max([blk["mean"] + (blk["se"] or 0.0)]
                      + [v for v in blk["per_seed"].values() if v is not None])
            ax.text(x, top + 0.006, f(blk["mean"]), fontsize=8.4, color=col,
                    ha="center", va="bottom", zorder=6)
        ebar(ax, x, blk["mean"], blk["se"], col, lw=1.8, z=5)
        cell = {k: blk[k] for k in ("mean", "se", "n_seeds", "per_seed")}
        cell.update(shared_env_episodes(T, opp, arm))
        out.setdefault("cells", {})[f"{opp}/{arm}"] = cell

    ytop = max(v["mean"] + (v["se"] or 0.0)
               for v in (p3[f"{o}/{a}"]["exploit_rate"] for o in ("grim", "tft") for a in ("base", "eg")))
    bracket = ytop + 0.037

    # the within-opponent comparison brackets
    for opp, x0, x1 in (("grim", 0.0, 1.0), ("tft", 2.45, 3.45)):
        a = p3[f"{opp}/base"]["exploit_rate"]
        b = p3[f"{opp}/eg"]["exploit_rate"]
        d = paired_delta(a["per_seed"], b["per_seed"], denominator={
            "unit": (f"trace episodes at steps >= {T['meta']['late_step']}, summed over the "
                     "three shared-opponent envs"),
            "base": out["cells"][f"{opp}/base"]["n_episodes"],
            "eg": out["cells"][f"{opp}/eg"]["n_episodes"],
            "weighting": SHARED_ENV_WEIGHTING})
        out.setdefault("deltas", {})[opp] = {
            "delta_eg_minus_base": d,
            "delta_se_if_unpaired": unpaired_se(a["se"], b["se"]),
            "n_episodes": {"base": out["cells"][f"{opp}/base"]["n_episodes"],
                           "eg": out["cells"][f"{opp}/eg"]["n_episodes"]},
            "n_episodes_per_seed": {"base": out["cells"][f"{opp}/base"]["n_episodes_per_seed"],
                                    "eg": out["cells"][f"{opp}/eg"]["n_episodes_per_seed"]},
            "_weighting": SHARED_ENV_WEIGHTING,
        }
        z = abs(d["mean"] / d["se"]) if (d["mean"] is not None and d["se"]) else None
        out["deltas"][opp]["abs_z_paired"] = z
        ax.plot([x0, x0, x1, x1], [bracket - 0.007, bracket, bracket, bracket - 0.007],
                color=MUT, lw=0.9, zorder=3)
        ax.text((x0 + x1) / 2, bracket + 0.003,
                f"{d['mean']:+.3f} +/- {f(d['se'])}" + (f"  ({z:.1f} SE)" if z else ""),
                fontsize=8.2, color=INK, ha="center", va="bottom", zorder=6)

    # baseline-pair separation, the thing that must NOT be there
    for tag in ("base", "eg"):
        a = p3[f"grim/{tag}"]["exploit_rate"]
        b = p3[f"tft/{tag}"]["exploit_rate"]
        dm = a["mean"] - b["mean"]
        dse = unpaired_se(a["se"], b["se"])
        out.setdefault("grim_minus_tft_within_arm", {})[tag] = {
            "delta": dm, "se_unpaired": dse,
            "abs_z": abs(dm / dse) if dse else None,
            "_pairing": "UNPAIRED across opponents: seed index names different checkpoints",
            "n_episodes": {"grim": out["cells"][f"grim/{tag}"]["n_episodes"],
                           "tft": out["cells"][f"tft/{tag}"]["n_episodes"]},
            "_weighting": SHARED_ENV_WEIGHTING,
        }

    ax.set_xticks(list(xs.values()))
    ax.set_xticklabels([f"{o}\n{a}\nn={out['cells'][f'{o}/{a}']['n_episodes']}"
                        for (o, a) in xs], fontsize=8.5)
    ax.set_xlim(-0.62, 4.07)
    ax.set_ylim(0, 0.27)
    ax.set_yticks(np.arange(0, 0.16, 0.025))
    gm = out["grim_minus_tft_within_arm"]
    ax.text(0.015, 0.845,
            f"grim minus tft, same arm (UNPAIRED)\n"
            f"  base {gm['base']['delta']:+.3f} +/- {f(gm['base']['se_unpaired'])}"
            f"  ({gm['base']['abs_z']:.1f} SE) no separation\n"
            f"  eg   {gm['eg']['delta']:+.3f} +/- {f(gm['eg']['se_unpaired'])}"
            f"  ({gm['eg']['abs_z']:.1f} SE) SEPARATED",
            transform=ax.transAxes, fontsize=8.2, color=INK, va="top", ha="left",
            linespacing=1.55, zorder=6, family="monospace")
    late_step = T["meta"]["late_step"]
    ax.text(0.015, 0.015,
            textwrap.fill(
                f"n under each label = trace episodes at steps >= {late_step}, summed over "
                + " + ".join(envs) + ".  The pooled value is an EQUAL-WEIGHT mean over the "
                "three per-env seed means, so n is the support behind the estimate, not its "
                "weighting.", width=62),
            transform=ax.transAxes, fontsize=6.9, color=MUT, va="bottom", ha="left",
            linespacing=1.5, zorder=6)
    style(ax, "C.  The knob transfers off IPD, and differently by opponent",
          "exploit_rate, three shared-opponent envs pooled (equal weight per env)", None,
          note="public_goods, dond and trust draw from IDENTICAL opponent\n"
               "populations in both arms, so a grim-vs-tft gap here cannot be\n"
               "the environment: it is an unconfounded policy difference.")
    out["envs"] = envs
    out["denominator"] = {
        "what": ("trace episodes in the three shared-opponent envs at steps >= "
                 f"{late_step}, summed over envs; pooled_three_envs itself carries no "
                 "n_episodes, so the counts are summed at render time from the per-env blocks"),
        "n_episodes": {k: v["n_episodes"] for k, v in out["cells"].items()},
        "n_episodes_by_env": {k: v["n_episodes_by_env"] for k, v in out["cells"].items()},
        "n_episodes_per_seed": {k: v["n_episodes_per_seed"] for k, v in out["cells"].items()},
        "weighting": SHARED_ENV_WEIGHTING,
    }

    # -- the deltas get their own zero-centred axis; a difference is not a condition -- #
    axd.axhline(0.0, color=INK2, lw=1.0, zorder=1)
    span = []
    for i, opp in enumerate(("grim", "tft")):
        d = out["deltas"][opp]["delta_eg_minus_base"]
        for j, s in enumerate(sorted(d["per_seed"])):
            axd.plot([i + (j - 1) * 0.15], [d["per_seed"][s]], marker=OPP_MARKER[opp],
                     ms=3.8, color=INK, alpha=0.30, mec="none", zorder=2)
            span.append(d["per_seed"][s])
        axd.plot([i], [d["mean"]], marker=OPP_MARKER[opp], ms=10.0, color=INK,
                 mec=PAPER, mew=1.1, zorder=3)
        ebar(axd, i, d["mean"], d["se"], INK, lw=1.8, z=5)
        span += [d["mean"] - (d["se"] or 0), d["mean"] + (d["se"] or 0)]
        axd.text(i + 0.14, d["mean"], f"{d['mean']:+.3f}", fontsize=8.6, color=INK,
                 ha="left", va="center", zorder=6)
    lo, hi = min(span), max(span)
    pad = 0.22 * (hi - lo)
    axd.set_xticks([0, 1])
    axd.set_xticklabels(["grim", "tft"], fontsize=8.5)
    axd.set_xlim(-0.72, 2.00)
    axd.set_ylim(lo - pad, hi + 3.1 * pad)
    style(axd, "eg minus base", "delta exploit_rate", None,
          note="neutral INK: a difference\nis not a condition and does\nnot borrow a condition's hue")


# --------------------------------------------------------------------------- #
# panel D -- does the reasoning move with it?
# --------------------------------------------------------------------------- #
MARKERS_D = ["m_endgame_hold", "m_endgame_defect_plan", "m_backward_induction",
             "m_in_game_penalty", "m_assumes_finite", "m_notices_unknown",
             "m_shaping_awareness", "m_infinite_logic"]
EVAL_ARM = {"base": "nohole", "eg": "eg"}


def reasoning_blocks_per_arm(E):
    """(per_arm, common) block counts for the four arms this panel actually draws.

    common is the shared count when all four agree and None when they do not, so the single
    "N blocks per arm" phrase is never printed over arms that stopped agreeing after a cache
    rebuild.  Read per arm rather than off one arm for exactly that reason.
    """
    by_arm = E["reasoning_markers"]["by_arm"]
    per_arm = {f"{o}/{EVAL_ARM[a]}": by_arm[f"{o}/{EVAL_ARM[a]}"]["n_blocks"]
               for o in ("grim", "tft") for a in ("base", "eg")}
    vals = set(per_arm.values())
    return per_arm, (vals.pop() if len(vals) == 1 else None)


def blocks_phrase(per_arm, common):
    return (f"{common} reasoning blocks per arm" if common is not None
            else "reasoning blocks per arm " + ", ".join(f"{k} {v}" for k, v in per_arm.items()))


def panel_d(ax, E, out):
    by_arm = E["reasoning_markers"]["by_arm"]

    live, floor = [], []
    for mk in MARKERS_D:
        vals = [by_arm[f"{o}/{EVAL_ARM[a]}"][mk]["mean"]
                for o in ("grim", "tft") for a in ("base", "eg")]
        (floor if max(v for v in vals if v is not None) < FLOOR_EPS else live).append(mk)
    out["markers_drawn"] = live
    out["markers_floor_limited"] = floor
    out["floor_threshold"] = FLOOR_EPS
    out["panel_choice"] = (
        "Drew the reasoning-marker panel. The markers are NOT mostly at the floor: "
        f"{len(live)} of {len(MARKERS_D)} clear {FLOOR_EPS} in at least one arm, and they move "
        "base->eg with the same grim-vs-tft asymmetry as the behaviour, which is the point of the "
        f"figure. The remaining {len(floor)} ({', '.join(floor)}) sit at the floor and are named as "
        "floor-limited rather than drawn as meaningful nulls. The inf reference the brief offers as "
        "the fallback is instead carried in panel B, in behavioural units, where it belongs.")

    rows, y = [], 0.0
    for opp in ("grim", "tft"):
        for mk in live:
            rows.append((opp, mk, y))
            y -= 1.0
        y -= 0.7
    ymin = y + 0.7
    label_x = 0.665

    for opp, mk, yy in rows:
        b = by_arm[f"{opp}/{EVAL_ARM['base']}"][mk]
        e = by_arm[f"{opp}/{EVAL_ARM['eg']}"][mk]
        d = paired_delta(b["per_seed"], e["per_seed"], denominator={
            "unit": "reasoning blocks in the arm",
            "base": b.get("n_episodes"), "eg": e.get("n_episodes")})

        seeds = sorted(set(b["per_seed"]) & set(e["per_seed"]))
        for i, s in enumerate(seeds):
            bv, ev = b["per_seed"].get(s), e["per_seed"].get(s)
            if bv is None or ev is None:
                continue
            oy = yy + (i - (len(seeds) - 1) / 2) * 0.19
            ax.plot([bv, ev], [oy, oy], color=MUT, lw=0.7, alpha=0.45, zorder=2)
            ax.plot([bv], [oy], marker=OPP_MARKER[opp], ms=2.9, color=PURPLE,
                    alpha=0.5, mec="none", zorder=2)
            ax.plot([ev], [oy], marker=OPP_MARKER[opp], ms=2.9, color=ORANGE,
                    alpha=0.5, mec="none", zorder=2)

        ax.annotate("", xy=(e["mean"], yy), xytext=(b["mean"], yy),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.5,
                                    shrinkA=3.0, shrinkB=3.0, alpha=0.85), zorder=3)
        for val, col in ((b["mean"], PURPLE), (e["mean"], ORANGE)):
            ax.plot([val], [yy], marker=OPP_MARKER[opp], ms=7.2, color=col,
                    mec=PAPER, mew=0.9, zorder=3)
        ebar(ax, b["mean"], yy, b["se"], PURPLE, horizontal=True, lw=1.5, z=4)
        ebar(ax, e["mean"], yy, e["se"], ORANGE, horizontal=True, lw=1.5, z=4)

        ax.text(label_x, yy, f"{f(b['mean'])} -> {f(e['mean'])}   d={d['mean']:+.3f} +/- {f(d['se'])}",
                fontsize=7.6, color=INK2, va="center", ha="left", zorder=6, family="monospace")
        keys = ("mean", "se", "n_seeds", "per_seed")
        out.setdefault("rows", []).append({
            "opponent": opp, "marker": mk,
            "base_nohole": dict({k: b[k] for k in keys},
                                n_blocks=b.get("n_episodes"),
                                n_blocks_per_seed=b.get("n_episodes_per_seed")),
            "eg": dict({k: e[k] for k in keys},
                       n_blocks=e.get("n_episodes"),
                       n_blocks_per_seed=e.get("n_episodes_per_seed")),
            "delta_eg_minus_base": d,
            "delta_se_if_unpaired": unpaired_se(b["se"], e["se"]),
            "denominator": "reasoning blocks per arm (rate = blocks containing the marker / blocks)",
        })

    ax.set_yticks([r[2] for r in rows])
    ax.set_yticklabels([r[1] for r in rows], fontsize=8)
    ax.set_ylim(ymin - 2.05, 3.7)
    ax.set_xlim(-0.028, 1.06)
    ax.set_xticks(np.arange(0, 0.65, 0.1))

    sep = rows[len(live) - 1][2] - 0.85
    ax.axhline(sep, color=GRID, lw=1.0, zorder=1)
    ax.text(-0.02, 0.78, "GRIM   (marker o)", fontsize=8.5, color=INK, va="center", zorder=6)
    ax.text(-0.02, sep - 0.42, "TFT   (marker s)", fontsize=8.5, color=INK, va="center", zorder=6)
    ax.text(label_x, 0.78, "base -> eg      delta (between-seed SE)", fontsize=7.4,
            color=MUT, va="center", ha="left", zorder=6, family="monospace")

    fl = ",  ".join(
        f"{m} (max {max(by_arm[f'{o}/{EVAL_ARM[a]}'][m]['mean'] for o in ('grim', 'tft') for a in ('base', 'eg')):.3f})"
        for m in floor)
    ax.text(-0.02, ymin - 1.92,
            f"FLOOR-LIMITED, not drawn:  {fl}.\nThese sit at the detection floor in all four arms; their "
            "flatness is an absence of signal, not a measured null.",
            fontsize=7.4, color=MUT, va="bottom", ha="left", zorder=6, linespacing=1.5)

    per_arm_nb, nb = reasoning_blocks_per_arm(E)
    out["n_blocks_by_arm"] = per_arm_nb
    out["n_blocks_per_arm"] = nb
    style(ax, "D.  The reasoning moves the same way, with the same grim-vs-tft asymmetry",
          "", "fraction of reasoning blocks containing the marker",
          note=f"Frozen step-35 checkpoints, {blocks_phrase(per_arm_nb, nb)}, 3 train seeds.  DIAGONAL ONLY: each arm\n"
               "plays only the opponent it trained against, so a grim-vs-tft gap here is policy and environment\n"
               "together.  The baseline arm is named `nohole` in eval_strategy.json and `base` everywhere else.")
    hgrid(ax)


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)
    ap.add_argument("--outdir", type=Path, default=HERE)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--stem", type=str, default="fig4_knob_by_opponent")
    args = ap.parse_args()

    T = json.loads(TRAIN_JSON.read_text())
    E = json.loads(EVAL_JSON.read_text())
    meta = T["meta"]

    fig = plt.figure(figsize=(18.8, 12.4))
    fig.patch.set_facecolor(PAPER)
    # no hspace/wspace here: locally modified subplot params make tight_layout bail
    gs = fig.add_gridspec(2, 6)
    axA = fig.add_subplot(gs[0, 0:3])
    axB = fig.add_subplot(gs[0, 3:6])
    axC = fig.add_subplot(gs[1, 0:2])
    axCd = fig.add_subplot(gs[1, 2:3])
    axD = fig.add_subplot(gs[1, 3:6])

    pa, pb, pc, pd = {}, {}, {}, {}
    panel_a(axA, T, pa)
    panel_b(axB, T, pb)
    panel_c(axC, axCd, T, pc)
    panel_d(axD, E, pd)

    # legend on one panel only
    h = [plt.Line2D([], [], color=PURPLE, lw=2.4, label="base  (no manipulation)"),
         plt.Line2D([], [], color=ORANGE, lw=2.4, label="eg  (endgame penalty)"),
         plt.Line2D([], [], color=BLUE, lw=2.4, label="inf  (round count scrubbed)"),
         plt.Line2D([], [], color=INK2, lw=1.6, ls="-", marker="o", ms=5,
                    label="grim  (solid o)"),
         plt.Line2D([], [], color=INK2, lw=1.6, ls="--", marker="s", ms=5,
                    label="tft  (dashed s)")]
    axA.legend(handles=h, frameon=False, fontsize=8.5, labelcolor=INK2,
               loc="upper left", ncol=2, handlelength=2.4,
               bbox_to_anchor=(0.012, 0.795), columnspacing=1.4)

    # ---------------- header, every number computed above ---------------- #
    gd = pa["grim"]["delta_eg_minus_base"]
    td = pa["tft"]["delta_eg_minus_base"]
    ratio = pa["tft_over_grim_delta_ratio"]
    cg = pc["deltas"]["grim"]["delta_eg_minus_base"]
    ct = pc["deltas"]["tft"]["delta_eg_minus_base"]

    fig.suptitle(
        "The opponent only matters through the endgame penalty: the same knob cuts late betrayal "
        f"{abs(ratio):.1f}x harder against tit-for-tat "
        f"({td['mean']:+.3f} vs {gd['mean']:+.3f}), and only the penalised arms differ off IPD",
        fontsize=14.5, color=INK, x=0.006, ha="left", y=0.985)

    ep_late = {k: T["pooled_late"][k]["coop_rate"]["n_episodes"]
               for k in ("grim/base", "grim/eg", "tft/base", "tft/eg")}
    nb_by_arm, nb = reasoning_blocks_per_arm(E)

    g_ceil = min(pa["grim"]["last_all_seed_step_base"], pa["grim"]["last_all_seed_step_eg"])
    t_ceil = min(pa["tft"]["last_all_seed_step_base"], pa["tft"]["last_all_seed_step_eg"])

    blocks = [
        (INK2,
         "COLOUR ENCODING IS INVERTED HERE relative to sibling figures fig1-fig3.  In this figure the ARM is the "
         "contrast, so colour encodes the arm (purple base / orange eg / blue inf) and the OPPONENT is carried by "
         "panel position, marker shape (o grim, s tft) and line style (solid grim, dashed tft).  The siblings do the "
         "reverse because there the opponent is the contrast.  Neutral INK is reserved for differences, and blue for inf."),
        (INK2,
         f"Denominators.  A: dense per-step train/* curves pooled over all 7 trained envs, 3 seeds per opponent x arm "
         f"(inf: 2 seeds).  The steps >= {DELTA_STEP_MIN} delta is denominated in OPTIMIZER STEPS x SEEDS, not episodes -- "
         f"train/endgame_rate arrives already reduced by the trainer to one episode-weighted number per step -- and the "
         f"seeds reached different depths: " + ";  ".join(
             f"{o} base {'/'.join(str(v) for v in pa[o]['base_steps_per_seed'].values())}, "
             f"eg {'/'.join(str(v) for v in pa[o]['eg_steps_per_seed'].values())} steps"
             for o in ("grim", "tft"))
         + f".  B: ipd trace episodes at steps >= {meta['late_step']} ("
         + ", ".join(f"{k} n={v}" for k, v in ep_late.items())
         + f"), with the inf reference pooled over steps >= {meta['trained_step']} instead because grim/inf stopped at "
           f"step 15 and has no late episodes.  C: {', '.join(pc['envs'])} at steps >= {meta['late_step']}, the three envs "
           f"whose opponent populations are identical across arms ("
         + ", ".join(f"{k} n={v}" for k, v in pc["denominator"]["n_episodes"].items())
         + " episodes, summed from the per-env cache blocks because pooled_three_envs carries no count of its own); the "
           "pooled value is an EQUAL-WEIGHT mean over the three per-env seed means, so those counts are the support "
           f"behind the estimate rather than its weighting.  D: frozen step-35 checkpoints, "
           f"{blocks_phrase(nb_by_arm, nb)}.  Trace dumps are the first 24 episodes of every 5th step."),
        (INK2,
         "Error bars.  EVERY bar and band is BETWEEN TRAINING SEED: each seed is collapsed to one number first, then the "
         "spread is taken across seeds as sd(ddof=1)/sqrt(n).  n < 2 draws NO bar, never a zero-length one.  eg-minus-base "
         "deltas are paired on seed index, since both arms of an opponent were launched with the same seeds; the unpaired "
         "sqrt(se_a^2 + se_b^2) alternative is recorded beside every delta in the companion JSON.  grim-minus-tft "
         "differences are UNPAIRED, because seed index 0/1/2 names different checkpoints in the two opponents."),
        (RED,
         f"CAVEAT.  The grim base and eg cells were stopped around step 39-50 while the tft cells ran further: grim holds "
         f"all 3 seeds only to step {g_ceil} and tft to step {t_ceil}.  The grim-vs-tft contrast is therefore fixed at a "
         "shallower step ceiling and the tft knob has more training over which to act, so the size of the asymmetry is an "
         "upper bound on the tft side rather than a calibrated ratio.  The inf arm has at most two seeds in either "
         "opponent; it is a reference line, not a tested condition."),
    ]

    y, dy = 0.9565, 0.0107
    for color, text in blocks:
        for line in textwrap.wrap(text, width=298, break_long_words=False):
            fig.text(0.006, y, line, fontsize=8.4, color=color, ha="left")
            y -= dy
        y -= 0.0022

    fig.tight_layout(rect=[0.004, 0.006, 0.998, y + 0.004], h_pad=3.2, w_pad=3.4)

    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    png = outdir / f"{args.stem}.png"
    fig.savefig(png, dpi=args.dpi, facecolor=fig.get_facecolor())
    print(f"[fig] wrote {png}")

    payload = {
        "figure": args.stem,
        "question": (
            "Does the scripted IPD opponent (grim vs tit-for-tat) matter at all, once you account for "
            "its interaction with the endgame penalty? Specifically: is the penalty's effect on late "
            "betrayal the same size against both opponents, and do the resulting policies differ on "
            "envs where the opponent was never manipulated?"),
        "answer": {
            "headline": (
                "The opponent only matters through the endgame penalty. The penalty suppresses late "
                f"betrayal against both opponents but {abs(ratio):.1f}x more strongly against tit-for-tat "
                f"({td['mean']:+.3f} +/- {f(td['se'])}) than against grim ({gd['mean']:+.3f} +/- "
                f"{f(gd['se'])}). On the three shared-opponent envs the baseline arms do not separate by "
                f"opponent ({f(pc['grim_minus_tft_within_arm']['base']['delta'])} +/- "
                f"{f(pc['grim_minus_tft_within_arm']['base']['se_unpaired'])}, "
                f"{pc['grim_minus_tft_within_arm']['base']['abs_z']:.1f} SE) while the eg arms do "
                f"({f(pc['grim_minus_tft_within_arm']['eg']['delta'])} +/- "
                f"{f(pc['grim_minus_tft_within_arm']['eg']['se_unpaired'])}, "
                f"{pc['grim_minus_tft_within_arm']['eg']['abs_z']:.1f} SE). Because those three envs use "
                "identical opponent populations in both arms, that gap is a genuine policy difference, "
                "not an environment difference."),
            "endgame_rate_delta_eg_minus_base": {
                "grim": {"mean": gd["mean"], "se_paired": gd["se"], "n_seeds": gd["n_seeds"],
                         "se_unpaired": pa["grim"]["delta_se_if_unpaired"],
                         "n_steps_in_window_per_seed": gd["steps_per_seed"],
                         "n_steps_in_window_total": gd["steps_total"]},
                "tft": {"mean": td["mean"], "se_paired": td["se"], "n_seeds": td["n_seeds"],
                        "se_unpaired": pa["tft"]["delta_se_if_unpaired"],
                        "n_steps_in_window_per_seed": td["steps_per_seed"],
                        "n_steps_in_window_total": td["steps_total"]},
                "tft_over_grim_ratio": ratio,
                "window": f"steps >= {DELTA_STEP_MIN}, all steps available to each seed",
                "denominator": ENDGAME_DENOM_WHAT,
                "pairing": gd["pairing"].replace("grim/", "<opp>/"),
            },
            "shared_opponent_env_exploit_rate_delta_eg_minus_base": {
                "grim": {"mean": cg["mean"], "se_paired": cg["se"], "n_seeds": cg["n_seeds"],
                         "se_unpaired": pc["deltas"]["grim"]["delta_se_if_unpaired"],
                         "n_episodes": pc["deltas"]["grim"]["n_episodes"]},
                "tft": {"mean": ct["mean"], "se_paired": ct["se"], "n_seeds": ct["n_seeds"],
                        "se_unpaired": pc["deltas"]["tft"]["delta_se_if_unpaired"],
                        "n_episodes": pc["deltas"]["tft"]["n_episodes"]},
                "denominator": pc["denominator"]["what"],
                "weighting": SHARED_ENV_WEIGHTING,
            },
            "what_the_knob_moves": (
                "It moves how often the last-round defection is taken, not when defection begins. "
                "In the late window every defection is a last-round defection in every cell "
                f"(defects_last_round identical to ever_defect: "
                f"{pb['defects_last_round_identical_to_ever_defect']}), first_defect_from_end is already "
                "at or near zero in the base arms, and eg pushes ever_defect down while leaving the "
                "timing of the first defection essentially unchanged."),
        },
        "panel_a_endgame_rate_over_training": pa,
        "panel_b_pooled_late_behaviour": pb,
        "panel_c_shared_opponent_env_transfer": pc,
        "panel_d_reasoning_markers": pd,
        "error_bar_definitions": {
            "primary": ("BETWEEN TRAINING SEED. Each training seed is collapsed to a single number "
                        "first, then the spread is taken across seeds as sd(ddof=1)/sqrt(n_seeds)."),
            "null_se": "n_seeds < 2 yields se null and NO bar is drawn, never a zero-length bar.",
            "eg_minus_base": ("Paired on seed index: grim/base/s0 and grim/eg/s0 were launched with the "
                              "same seed, so the per-seed difference is taken first and the SE is the "
                              "between-seed SE of those differences. The unpaired alternative "
                              "sqrt(se_a^2+se_b^2) is recorded alongside every delta as "
                              "delta_se_if_unpaired; both agree on the mean by construction."),
            "grim_minus_tft": ("UNPAIRED. Seed index 0/1/2 names different checkpoints in the grim and "
                               "tft arms, so SE = sqrt(se_grim^2 + se_tft^2)."),
        },
        "colour_encoding_note": {
            "this_figure": {"PURPLE #7a5bd6": "base", "ORANGE #eb6834": "eg", "BLUE #2a78d6": "inf",
                            "opponent": "panel position + marker shape (o grim, s tft) + line style "
                                        "(solid grim, dashed tft)",
                            "INK #0b0b0b": "differences (eg minus base) -- a difference is not a "
                                           "condition and does not borrow a condition's hue"},
            "inversion": ("INVERTED relative to sibling figures fig1/fig2/fig3. There the OPPONENT is "
                          "the contrast and colour encodes it (GRIM #00918f / TFT #b8236f). Here the ARM "
                          "is the contrast, so colour encodes the arm and the opponent drops to shape "
                          "and line style. The inversion is stated on the figure itself so the two "
                          "conventions cannot be confused."),
            "reserved": "BLUE #2a78d6 is reserved for inf and is used for nothing else in this figure.",
        },
        "panel_d_choice": pd["panel_choice"],
        "provenance": {
            "train_cache": {
                "path": str(TRAIN_JSON), "mtime": TRAIN_JSON.stat().st_mtime,
                "size_bytes": TRAIN_JSON.stat().st_size,
                "generated_utc": meta.get("generated_utc"),
            },
            "eval_cache": {
                "path": str(EVAL_JSON), "mtime": EVAL_JSON.stat().st_mtime,
                "size_bytes": EVAL_JSON.stat().st_size,
                "generated_utc": E["meta"].get("built_utc"),
            },
            "blocks_read": [
                "train_strategy.json: metrics_curves[opp/arm]['train/endgame_rate']",
                "train_strategy.json: pooled_late[opp/arm][stat] (steps >= 25)",
                "train_strategy.json: pooled_all[opp/arm][stat] (steps >= 5, inf reference only)",
                "train_strategy.json: shared_opponent_envs['pooled_three_envs'][opp/arm]['exploit_rate']",
                ("train_strategy.json: shared_opponent_envs['opp/arm/env'].pooled_late.exploit_rate"
                 ".n_episodes and .per_seed_n (panel C denominators, summed over the three envs)"),
                "train_strategy.json: meta",
                "eval_strategy.json: reasoning_markers.by_arm[opp/{nohole,eg}]",
            ],
            "arm_naming": ("train_strategy.json calls the baseline arm `base`; eval_strategy.json calls "
                           "the same arm `nohole`. Panel D maps base -> nohole."),
            "denominators": {
                "train_endgame_rate_window": {
                    "panel": "A",
                    "what": ENDGAME_DENOM_WHAT,
                    "step_window": f"steps >= {DELTA_STEP_MIN}",
                    "n_steps_in_window_per_seed": {
                        f"{o}/{a}": pa[o][f"{a}_steps_per_seed"]
                        for o in ("grim", "tft") for a in ("base", "eg")},
                    "n_steps_in_window_total": {
                        f"{o}/{a}": int(sum(pa[o][f"{a}_steps_per_seed"].values()))
                        for o in ("grim", "tft") for a in ("base", "eg")},
                    "n_seeds": {f"{o}/{a}": pa[o]["denominator"]["n_seeds"][a]
                                for o in ("grim", "tft") for a in ("base", "eg")},
                    "why_it_differs_by_seed": (
                        "the seeds were stopped at different depths, so the number of logged steps "
                        "at or above the window start is not the same in every seed; see "
                        "caveat.step_ceiling"),
                    "source": ("train_strategy.json metrics_curves[opp/arm]['train/endgame_rate']"
                               ".steps, .per_seed and .n_seeds, counted at render time"),
                },
                "pooled_late_ipd_episodes": ep_late,
                "shared_env_episodes": {
                    "panel": "C",
                    "n_episodes": pc["denominator"]["n_episodes"],
                    "n_episodes_by_env": pc["denominator"]["n_episodes_by_env"],
                    "n_episodes_per_seed": pc["denominator"]["n_episodes_per_seed"],
                    "source": ("summed at render time over shared_opponent_envs"
                               "['<opp>/<arm>/<env>'].pooled_late.exploit_rate.n_episodes; "
                               "shared_opponent_envs['pooled_three_envs'] carries no n_episodes "
                               "of its own, which is why a figure that reads only the pooled "
                               "block has to report null there"),
                },
                "shared_env_pooling": ("per seed, each of the three envs is averaged over its episodes at "
                                       f"steps >= {meta['late_step']} and the three env means are then "
                                       "averaged with equal weight; the between-seed SE is taken over "
                                       "those three numbers. " + SHARED_ENV_WEIGHTING),
                "reasoning_blocks_per_arm": nb,
                "reasoning_blocks_by_arm": nb_by_arm,
                "reasoning_blocks_total": int(sum(nb_by_arm.values())),
                "reasoning_blocks_source": (
                    "eval_strategy.json reasoning_markers.by_arm[<opp>/<nohole|eg>].n_blocks, read "
                    "once per drawn arm at render time rather than off a single arm, so the shared "
                    "'per arm' number is only printed while the four arms still agree; it cross-"
                    "checks against reasoning_markers.n_blocks_kept = "
                    f"{E['reasoning_markers'].get('n_blocks_kept')} summed over the four diagonal arms"),
                "reasoning_blocks_agree_with_n_blocks_kept": (
                    sum(nb_by_arm.values()) == E["reasoning_markers"].get("n_blocks_kept")),
                "trace_sampling_note": meta.get("trace_sampling_note"),
                "every_rate_is_denominated": (
                    "A: optimizer steps x seeds (panel_a[opp].denominator). B: ipd trace episodes "
                    "(n_episodes on every base/eg/inf block). C: shared-opponent-env episodes "
                    "(n_episodes on every cell, summed from the per-env blocks). D: reasoning "
                    "blocks (n_blocks on every row). Every count is read from the caches at render "
                    "time, so it moves when the caches are rebuilt."),
            },
        },
        "caveat": {
            "step_ceiling": (
                "The grim base and eg cells were stopped around step 39-50 while the tft cells ran "
                f"further. grim/base holds 3 seeds only to step {pa['grim']['last_all_seed_step_base']} "
                f"and grim/eg to step {pa['grim']['last_all_seed_step_eg']}; tft/base to step "
                f"{pa['tft']['last_all_seed_step_base']} and tft/eg to step "
                f"{pa['tft']['last_all_seed_step_eg']}. The grim-vs-tft contrast is therefore fixed at a "
                "shallower step ceiling, and the tft knob has more training over which to act. The size "
                "of the asymmetry should be read as an upper bound on the tft side, not as a calibrated "
                "ratio."),
            "inf_seeds": ("The inf arm has at most two training seeds in either opponent and grim/inf "
                          "additionally stopped at step 15, so it has zero episodes in the steps >= 25 "
                          "late window. Panel B therefore draws the inf reference from pooled_all "
                          "(steps >= 5). inf is a reference line for what a large effect looks like in "
                          "these units, not a tested condition."),
            "diagonal_only_reasoning": E["reasoning_markers"].get("_diagonal_only"),
            "reasoning_staleness": E["reasoning_markers"].get("_staleness"),
            "ground_truth_warnings": meta.get("ground_truth_warnings"),
        },
    }

    js = outdir / f"{args.stem}.json"
    js.write_text(json.dumps(payload, indent=1))
    print(f"[fig] wrote {js}")


if __name__ == "__main__":
    main()
