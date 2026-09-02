#!/usr/bin/env python
"""What the model SAYS at the endgame against what it DOES, in the same episodes.

    /home/allie/venvs/tinker-ipd/bin/python fig3_plan_vs_act.py
    /home/allie/venvs/tinker-ipd/bin/python fig3_plan_vs_act.py --help   # renders nothing

  fig3_plan_vs_act.png     the figure
  fig3_plan_vs_act.json    every number drawn in it

THE QUESTION. The endgame penalty (`eg`) is a reward charge on late betrayal.
It reduces late-game betrayal BEHAVIOUR in training. Does it also suppress the
endgame REASONING, or does the policy still plan the betrayal and simply not
execute it? Panel A is what is said, panel B is what is done in the very same
episodes, panel C puts them in the same block and asks whether the stated plan
predicts the action any better than nothing does.

WHAT CHANGED SINCE THE LAST RENDER. The eval doubled: 624 episodes / 12,480
reasoning blocks / 13 cells, and `tft` now has BOTH arms at three training
seeds. `tft` is where the behavioural effect lives, and the previous version of
this figure -- grim only -- was drawing the one opponent where the eval cannot
resolve anything. `tft/inf` exists at ONE seed and therefore enters no contrast
and is not drawn; BLUE stays reserved for it and unused.

WHAT THIS FIGURE FINDS.
  A. No selective suppression of endgame reasoning is DETECTABLE, which is not
     the same as none. The spike amplitude difference is +0.02 +/- 0.20 against
     grim (0.1 sigma: at +/-2 SE it still admits total flattening) and
     +0.36 +/- 0.19 against tft (the eg spike is if anything the STEEPER of the
     two). What does resolve is a LEVEL shift, and only against tft:
     -0.31 +/- 0.12 over positions 0-5 versus -0.10 +/- 0.18 against grim,
     whose per-seed values flip sign and whose eg arm sits ABOVE nohole one
     round from the end. "It lowers the whole curve" is a tft statement.
  B. Behaviour partially reproduces. Against tft the arms differ by
     -0.177 +/- 0.113, the same direction and rough size as the -0.142 +/- 0.064
     in the training logs; against grim the eval returns -0.001 +/- 0.140 and
     resolves nothing. The eval reproduces the effect where it is large and is
     blind to it where it is small.
  C. Conditioning on the stated plan still explains almost none of the arm gap,
     and adding tft does not rescue it. The arm gap under `endgame_defect_plan`
     is essentially the arm gap under NO condition, and the OPPOSITE marker
     (`endgame_hold`) returns a gap of the same size and sign in both opponents.

ERROR BARS. Every bar and band is BETWEEN TRAINING SEED: compute the quantity
separately for each of the three training seeds, then sd/sqrt(3). Arm
differences use the PAIRED per-seed delta, matching the convention already
written into `trace_markers.json` -> `contrasts` (`per_seed_delta`,
`raw_delta_se`). Binomial SE is the sampling floor, not the uncertainty on a
claim about the knob, and it is drawn nowhere.

MINIMUM-N RULE (new). An interval is drawn only if EVERY contributing seed has
at least MIN_N_FOR_BAR blocks in the subgroup. The previous render drew the
`hold present` / nohole condition with the tightest bar on the panel over
per-seed n of [9, 1, 2] and per-seed "rates" of [0.778, 1.0, 1.0] -- two of the
three were single- and double-observation 1.0s, so the spread across seeds was
near zero for want of data rather than for agreement, and the narrow bar was
then quoted as corroboration. A narrow bar over near-empty subgroups is not
evidence. Such groups now print their mean with the interval SUPPRESSED and the
per-seed n shown; the number is still in the JSON, flagged.

EVERY RENDERED NUMBER IS COMPUTED AT RENDER TIME and written to the paired
JSON. The previous version hardcoded "2892 of 2893 parsed actions" (stale: from
a 353-episode prefix of a file that kept growing), "60.8%" and "33 of its 48",
and computed the episode count from (arm, train_seed, episode_seed) triples --
which undercounts 3x, because each triple spans three horizons and episode
identity needs `num_rounds` too. Nothing on this figure is a literal any more.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics as st
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams["text.parse_math"] = False

HERE = Path(__file__).resolve().parent

PURPLE, ORANGE, BLUE = "#7a5bd6", "#eb6834", "#2a78d6"
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
PAPER = "#f9f9f7"

# Palette is fixed BY CONDITION and is never repainted. Opponent is carried by
# PANEL POSITION (a row per opponent in A and C, an x-group in B), never by
# hue. BLUE belongs to the hidden-horizon arm `inf` and to nothing else; that
# arm has one seed on disk, so blue does not appear on this figure at all.
CONDS = [("nohole", "baseline (nohole)", PURPLE),
         ("eg", "endgame penalty (eg)", ORANGE)]
OPPONENTS = [("grim", "grim  (never forgives)"),
             ("tft", "tft  (tit-for-tat)")]
SEEDS = (0, 1, 2)

# 6/10/14-round episodes all reach 5 rounds from the end and no further, so
# positions 0..5 are the only ones every horizon contributes to. Pooling past
# that would silently become "14-round episodes only".
MAX_RFE = 5

MIN_N_FOR_BAR = 5   # per-seed subgroup size below which no interval is drawn

# From the training logs, NOT from this eval. Quoted for comparison in panel B
# and labelled as external everywhere it appears; the denominators differ and
# the panel says so.
TRAINLOG = {"grim": (-0.039, 0.012), "tft": (-0.142, 0.064)}


def arm_of(opp: str, cond: str) -> str:
    return f"{opp}/{cond}"


# --------------------------------------------------------------------------
# between-seed statistics. One function, used everywhere, so no panel can
# quietly fall back to a binomial bar.
# --------------------------------------------------------------------------

def between_seed(vals):
    """mean and sd/sqrt(n) over per-seed values. n<2 returns se=None, which the
    drawing code renders as no bar rather than as a bar of length zero."""
    vals = [v for v in vals if v is not None]
    if not vals:
        return None, None, 0
    m = sum(vals) / len(vals)
    se = st.stdev(vals) / len(vals) ** 0.5 if len(vals) > 1 else None
    return m, se, len(vals)


def paired_delta(a_by_seed, b_by_seed):
    """delta(a - b) as the between-seed sd of the PAIRED per-seed differences.

    This is the convention in trace_markers.json -> contrasts. Pairing on the
    training-seed index is not a claim that seed 2 of eg and seed 2 of nohole
    share anything but the index; it is the convention the wave already uses.
    """
    d = [a_by_seed[s] - b_by_seed[s] for s in SEEDS
         if a_by_seed.get(s) is not None and b_by_seed.get(s) is not None]
    if not d:
        return None, None, []
    m = sum(d) / len(d)
    se = st.stdev(d) / len(d) ** 0.5 if len(d) > 1 else None
    return m, se, d


def rate(rows, field):
    return (sum(r[field] for r in rows) / len(rows)) if rows else None


def fmt(x, nd=3):
    return "n/a" if x is None else f"{x:.{nd}f}"


def fmts(x, nd=3):
    return "n/a" if x is None else f"{x:+.{nd}f}"


# --------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------

def episode_key(r):
    """Episode identity. `num_rounds` is part of it: one (arm, train_seed,
    episode_seed) triple is REPLAYED at horizons 6, 10 and 14, so counting
    triples undercounts episodes by exactly 3x. That is the bug that put
    "96 episodes" in the previous header next to its own contradictory
    "3 seeds x 48 episodes" arithmetic."""
    return (r["arm"], r["train_seed"], r["episode_seed"], r["num_rounds"])


def answer_parse_agreement(src: Path, action_regex: str, arms):
    """Does the action parsed out of a turn's ANSWER agree with the action the
    environment actually recorded for that turn?

    trace_blocks.jsonl carries the parsed answer but not the environment's
    `defect_indices`, so this is recomputed from the episode source named in
    trace_markers.json -> meta.source. Recomputed at render time and never
    cached: the previous version's "2892 of 2893" was a literal copied from a
    353-episode prefix of a file that was still being written to.
    """
    if not src.exists():
        return {"available": False, "reason": f"source not readable at {src}"}
    rx = re.compile(action_regex, re.I)

    def action_of(text):
        m = None
        for m in rx.finditer(text or ""):
            pass
        return (m.group(1).lower() == "defect") if m else None

    tot = agree = 0
    per_arm = {}
    for line in src.open():
        if not line.strip():
            continue
        e = json.loads(line)
        di = set(e.get("defect_indices") or [])
        a_tot = a_agr = 0
        for j, t in enumerate(e["turns"][1::2]):     # decision turns are odd
            act = action_of(t.get("answer") or "")
            if act is None:
                continue
            a_tot += 1
            a_agr += int(act == (j in di))
        tot += a_tot
        agree += a_agr
        cur = per_arm.setdefault(e["arm"], [0, 0])
        cur[0] += a_agr
        cur[1] += a_tot
    drawn = [v for k, v in per_arm.items() if k in arms]
    d_agr, d_tot = sum(x[0] for x in drawn), sum(x[1] for x in drawn)
    return {
        "available": True,
        "source": str(src),
        "definition": "action parsed from the turn's answer text vs the "
                      "environment's recorded defect_indices for that turn; "
                      "over parsed decision turns only (unparseable answers "
                      "are not counted in either numerator or denominator)",
        "action_regex": action_regex,
        "all_cells": {"agree": agree, "parsed_actions": tot,
                      "rate": (agree / tot) if tot else None},
        "arms_drawn": {"agree": d_agr, "parsed_actions": d_tot,
                       "rate": (d_agr / d_tot) if d_tot else None},
        "per_arm": {k: {"agree": v[0], "parsed_actions": v[1],
                        "rate": (v[0] / v[1]) if v[1] else None}
                    for k, v in sorted(per_arm.items())},
    }


# --------------------------------------------------------------------------
# shared chrome
# --------------------------------------------------------------------------

def style(ax, title, ylab, xlab, pad=9, tsize=10.4):
    ax.set_title(title, fontsize=tsize, color=INK, loc="left", pad=pad)
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


def place(ax, ends, lo, hi):
    """Direct-label each series at its right end, nudged apart on collision.
    Identity is never colour-alone, so these are load-bearing."""
    ends = sorted(ends, key=lambda e: e[1])
    gap = (hi - lo) * 0.115          # labels are two lines tall
    for i in range(1, len(ends)):
        x, y, lab, col = ends[i]
        if y - ends[i - 1][1] < gap:
            ends[i] = (x, ends[i - 1][1] + gap, lab, col)
    for x, y, lab, col in ends:
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(9, 0),
                    va="center", fontsize=6.9, color=col, linespacing=1.32,
                    annotation_clip=False)


# --------------------------------------------------------------------------
# PANEL A -- where in the game the endgame talk happens
# --------------------------------------------------------------------------

SERIES = [("m_endgame_defect_plan", "plans to DEFECT at the end", "-", "o", 2.0),
          ("m_endgame_hold", "plans to HOLD at the end", "--", "s", 1.5)]


def curve(rows, arm, seed, mk, rfe, decision=True):
    sub = [r for r in rows if r["arm"] == arm and r["train_seed"] == seed
           and r["rounds_from_end"] == rfe and r["in_decision"] == decision]
    return rate(sub, mk), len(sub)


def panel_a(ax, rows, opp, out):
    """Marker hit rate against rounds_from_end, one line per (arm, marker),
    band = between-seed SE. Decision turns only, one sub-row per opponent.

    The hypothesis this is here to test is narrow. If the penalty suppressed
    ENDGAME reasoning as such it should flatten the run-up to the final round;
    if it merely made the policy talk about defection less overall it should
    lower the whole curve. So the number that matters is the spike AMPLITUDE,
    rate(final) - rate(5 from the end), per seed and then contrasted.
    """
    node = out["panel_a"]["by_opponent"].setdefault(opp, {"series": {}})
    ends, hi = [], 0.0

    for mk, mlab, ls, mrk, lw in SERIES:
        for cond, clab, col in CONDS:
            arm = arm_of(opp, cond)
            ys, los, his, per_pos = [], [], [], {}
            for rfe in range(MAX_RFE + 1):
                vals, n_tot = {}, 0
                for s in SEEDS:
                    v, n = curve(rows, arm, s, mk, rfe)
                    vals[s] = v
                    n_tot += n
                m, se, _ = between_seed([vals[s] for s in SEEDS])
                se = se or 0.0
                ys.append(m)
                los.append(m - se)
                his.append(m + se)
                per_pos[rfe] = {"per_seed": [vals[s] for s in SEEDS],
                                "mean": m, "between_seed_se": se,
                                "n_blocks_total": n_tot}
            hi = max(hi, max(his))
            xs = list(range(MAX_RFE + 1))
            ax.fill_between(xs, los, his, color=col, alpha=0.13, lw=0, zorder=2)
            ax.plot(xs, ys, color=col, lw=lw, ls=ls, zorder=3, marker=mrk,
                    ms=4.6, mec=SURF, mew=1.2)
            ends.append((0, ys[0], f"{cond} -\n{mlab}", col))
            node["series"][f"{arm}|{mk}"] = per_pos

    # The non-decision turn of each round is not drawn -- four lines per
    # sub-row is already the limit of what the panel can carry -- but it is
    # exported, because "decision turns only" is a choice and the reader is
    # entitled to check that the other half does not say something different.
    node["non_decision_turns_not_drawn"] = {}
    for mk, *_ in SERIES:
        for cond, _, _ in CONDS:
            arm = arm_of(opp, cond)
            per = {}
            for rfe in range(MAX_RFE + 1):
                vals = [curve(rows, arm, s, mk, rfe, decision=False)[0]
                        for s in SEEDS]
                m, se, _ = between_seed(vals)
                per[rfe] = {"per_seed": vals, "mean": m, "between_seed_se": se}
            node["non_decision_turns_not_drawn"][f"{arm}|{mk}"] = per

    # spike amplitude, per marker, per arm, and the arm contrast on it
    node["spike_amplitude"] = {}
    amps = {}
    for mk, *_ in SERIES:
        amps[mk] = {}
        for cond, _, _ in CONDS:
            arm = arm_of(opp, cond)
            by_seed = {s: (curve(rows, arm, s, mk, 0)[0]
                           - curve(rows, arm, s, mk, MAX_RFE)[0])
                       for s in SEEDS}
            m, se, _ = between_seed([by_seed[s] for s in SEEDS])
            amps[mk][cond] = by_seed
            node["spike_amplitude"][f"{arm}|{mk}"] = {
                "definition": f"rate(rounds_from_end=0) - "
                              f"rate(rounds_from_end={MAX_RFE}), {mk}, "
                              f"decision turns",
                "per_seed": [by_seed[s] for s in SEEDS],
                "mean": m, "between_seed_se": se}
        dm, dse, dd = paired_delta(amps[mk]["eg"], amps[mk]["nohole"])
        node["spike_amplitude"][f"{opp}|{mk}|delta_eg_minus_nohole"] = {
            "per_seed_delta": dd, "mean": dm, "between_seed_se": dse}

    # LEVEL shift, the other half of the same test. "The penalty lowers the
    # whole curve" is a claim about the level, and it is not the same claim for
    # both opponents, so it gets its own interval per opponent rather than an
    # eyeball over the bands. Mean over the drawn positions of (eg - nohole),
    # per seed, then between-seed. positions_eg_below_nohole is the literal
    # count behind the word "whole": at neither opponent is it all of them.
    node["level_shift"] = {}
    for mk, *_ in SERIES:
        e = node["series"][f"{arm_of(opp, 'eg')}|{mk}"]
        b = node["series"][f"{arm_of(opp, 'nohole')}|{mk}"]
        per_seed = [sum(e[r]["per_seed"][i] - b[r]["per_seed"][i]
                        for r in range(MAX_RFE + 1)) / (MAX_RFE + 1)
                    for i in range(len(SEEDS))]
        m, se, _ = between_seed(per_seed)
        below = [r for r in range(MAX_RFE + 1) if e[r]["mean"] < b[r]["mean"]]
        node["level_shift"][f"{opp}|{mk}|delta_eg_minus_nohole"] = {
            "definition": f"mean over positions 0..{MAX_RFE} of "
                          f"rate(eg) - rate(nohole) for {mk} on decision "
                          f"turns, per seed then between-seed",
            "per_seed": per_seed, "mean": m, "between_seed_se": se,
            "sigma": abs(m) / se if se else None,
            "positions_eg_below_nohole": below,
            "n_positions": MAX_RFE + 1}

    # shape of the HOLD curve, stated per arm rather than asserted to be flat.
    # The previous render called it "roughly flat in both arms at a tenth of
    # the defect-plan rate", which was true of grim/nohole and of nothing else.
    node["hold_curve_shape"] = {}
    for cond, _, _ in CONDS:
        arm = arm_of(opp, cond)
        h = [between_seed([curve(rows, arm, s, "m_endgame_hold", r)[0]
                           for s in SEEDS])[0] for r in range(MAX_RFE + 1)]
        p = [between_seed([curve(rows, arm, s, "m_endgame_defect_plan", r)[0]
                           for s in SEEDS])[0] for r in range(MAX_RFE + 1)]
        ratios = [hh / pp for hh, pp in zip(h[:3], p[:3]) if pp]
        node["hold_curve_shape"][arm] = {
            "by_position_0_to_5": h,
            "at_5_out": h[MAX_RFE], "at_final": h[0],
            "min": min(h), "max": max(h),
            "argmax_rounds_from_end": int(max(range(MAX_RFE + 1),
                                              key=lambda i: h[i])),
            "swing_max_over_min": (max(h) / min(h)) if min(h) else None,
            "ratio_to_defect_plan_last_three_positions": ratios,
            "ratio_range_last_three": [min(ratios), max(ratios)] if ratios else None}

    top = hi * 1.30
    ax.set_xlim(MAX_RFE + 0.4, -3.05)
    ax.set_ylim(0, top)
    ax.set_xticks(list(range(MAX_RFE + 1)))

    a_n = node["spike_amplitude"][f"{opp}/nohole|m_endgame_defect_plan"]
    a_e = node["spike_amplitude"][f"{opp}/eg|m_endgame_defect_plan"]
    style(ax, f"A - vs {opp}: endgame spike {fmts(a_n['mean'], 2)} +/- "
              f"{fmt(a_n['between_seed_se'], 2)} (nohole) vs {fmts(a_e['mean'], 2)} "
              f"+/- {fmt(a_e['between_seed_se'], 2)} (eg)",
          "share of decision blocks with the marker",
          "rounds from the end   (0 = final round, at the right)"
          if opp == OPPONENTS[-1][0] else "")
    place(ax, ends, 0, top)
    return out


def note_a(out):
    n_arm_ep = out["episode_counts"]["episodes_per_arm"]
    lv = {opp: out["panel_a"]["by_opponent"][opp]["level_shift"][
              f"{opp}|m_endgame_defect_plan|delta_eg_minus_nohole"]
          for opp, _ in OPPONENTS}
    ln, sig = [], []
    for opp, _ in OPPONENTS:
        node = out["panel_a"]["by_opponent"][opp]
        d = node["spike_amplitude"][f"{opp}|m_endgame_defect_plan|delta_eg_minus_nohole"]
        a_n = node["spike_amplitude"][f"{opp}/nohole|m_endgame_defect_plan"]
        a_e = node["spike_amplitude"][f"{opp}/eg|m_endgame_defect_plan"]
        ln.append(f"  vs {opp}: nohole {fmts(a_n['mean'])} +/- {fmt(a_n['between_seed_se'])}, "
                  f"eg {fmts(a_e['mean'])} +/- {fmt(a_e['between_seed_se'])}, difference")
        ln.append(f"     {fmts(d['mean'])} +/- {fmt(d['between_seed_se'])} "
                  f"({abs(d['mean']) / d['between_seed_se']:.1f} sigma at n=3).")
        sig.append(abs(d["mean"]) / d["between_seed_se"])

    hold, rmin, rmax, swings, rises = [], 9e9, 0.0, [], 0
    for opp, _ in OPPONENTS:
        for cond, _, _ in CONDS:
            h = out["panel_a"]["by_opponent"][opp]["hold_curve_shape"][f"{opp}/{cond}"]
            lo, hi_ = h["ratio_range_last_three"]
            rmin, rmax = min(rmin, lo), max(rmax, hi_)
            swings.append((h["swing_max_over_min"], f"{opp}/{cond}"))
            rises += int(h["at_final"] > h["at_5_out"])
            hold.append(
                f"  {opp}/{cond}: {fmt(h['at_5_out'])} five out -> peak {fmt(h['max'])} at "
                f"{h['argmax_rounds_from_end']} out -> {fmt(h['at_final'])} final,")
            hold.append(
                f"     {h['swing_max_over_min']:.0f}x off its own floor; last three positions run "
                f"{lo:.2f}-{hi_:.2f} of the plan rate.")
    big = max(swings)
    return (
        "Decision turns only (the non-decision turn of each round tells the\n"
        "same story and is in the JSON). ONE ROW PER OPPONENT; the condition\n"
        "colours mean the same thing in both rows. POSITIONS 0-5 ONLY: 6-, 10-\n"
        "and 14-round episodes all reach 5 from the end and no further, so\n"
        "every drawn position is an equal mix of the three horizons and pooling\n"
        f"deeper would silently mean 14-round episodes alone. {n_arm_ep} episodes per\n"
        f"(arm, position); bands are between-seed SE over {len(SEEDS)} seeds.\n\n"
        "THE TEST IS THE SPIKE, NOT THE LEVEL. If the penalty suppressed\n"
        "ENDGAME reasoning as such it would flatten the run-up to the final\n"
        "round; if it merely made the policy talk about defection less overall\n"
        "it would lower the whole curve. Amplitude = rate(final) - rate(5 from\n"
        "the end), per seed then between-seed:\n"
        + "\n".join(ln) + "\n"
        "Neither difference is negative, so no flattening is DETECTABLE; that is\n"
        f"not the same as none. Against tft the eg spike is the steeper at {sig[1]:.1f}\n"
        "sigma on n=3, a direction and not a result. What resolves is the LEVEL,\n"
        f"and only vs tft: mean(eg - nohole) over positions 0-5 is {fmts(lv['tft']['mean'])} +/-\n"
        f"{fmt(lv['tft']['between_seed_se'])} ({lv['tft']['sigma']:.1f} sigma) vs tft and {fmts(lv['grim']['mean'])} +/- {fmt(lv['grim']['between_seed_se'])} ({lv['grim']['sigma']:.1f} sigma) vs grim -- the\n"
        "raw endgame_defect_plan contrast, confounded with length (header, fig2).\n\n"
        "THE DASHED PAIR IS THE OPPOSITE MARKER, a stated plan to HOLD at the\n"
        "end; it is here as the check that the two regexes are not simply\n"
        "firing together on any mention of the last round. An earlier version\n"
        "of this figure called it \"roughly flat in both arms at a tenth of the\n"
        "defect-plan rate\". That is not what it does:\n"
        + "\n".join(hold) + "\n"
        f"  The hold rate is HIGHER at the final round than five out in {rises} of the\n"
        f"  4 arms, and over the last three positions its ratio to the defect-\n"
        f"  plan rate runs {rmin:.2f}-{rmax:.2f}, a tenth only at its floor; the biggest\n"
        f"  swing is {big[0]:.0f}x in {big[1]}, which RISES into the endgame rather than\n"
        "  staying flat. The two markers do co-move near the end, so this is a\n"
        "  weaker separation check than was claimed -- not a worthless one,\n"
        "  since hold stays well below plan at every position in every arm.\n"
        "  Endgame talk of BOTH kinds increases into the endgame.")


# --------------------------------------------------------------------------
# PANEL B -- the behaviour in these same episodes
# --------------------------------------------------------------------------

def panel_b(ax, cells, out):
    """endgame_rate per arm, every training seed drawn as its own point.
    Opponent is carried by x-group, condition by colour."""
    out["panel_b"] = {
        "quantity": "endgame_rate, per (arm, train_seed) cell, from "
                    "trace_markers.json -> cells",
        "denominator": "48 episodes per (arm, train_seed) cell, i.e. 16 "
                       "episode seeds x horizons 6/10/14",
        "arms": {}, "by_opponent": {}}

    xs, labels = {}, []
    for oi, (opp, _) in enumerate(OPPONENTS):
        for ci, (cond, _, _) in enumerate(CONDS):
            xs[(opp, cond)] = oi * 2.5 + ci
            labels.append((oi * 2.5 + ci, f"{cond}\nvs {opp}"))

    hi = 0.0
    for opp, _ in OPPONENTS:
        by_cond = {}
        for cond, clab, col in CONDS:
            arm = arm_of(opp, cond)
            vals = {s: cells[f"{arm}|{s}"]["endgame_rate"] for s in SEEDS}
            n_ep = {s: cells[f"{arm}|{s}"]["n_episodes"] for s in SEEDS}
            by_cond[cond] = vals
            m, se, n = between_seed([vals[s] for s in SEEDS])
            x = xs[(opp, cond)]
            hi = max(hi, m + (se or 0), max(vals.values()))
            for j, s in enumerate(SEEDS):
                ax.plot([x + (j - 1) * 0.13], [vals[s]], marker="o", ms=6.0,
                        mfc="none", mec=col, mew=1.5, zorder=3)
                ax.annotate(f"s{s}", (x + (j - 1) * 0.13, vals[s]),
                            textcoords="offset points", xytext=(0, 8),
                            ha="center", fontsize=6.4, color=MUT)
            ax.errorbar([x], [m], yerr=[se], color=col, lw=2.2, capsize=6,
                        capthick=2.2, zorder=4)
            ax.plot([x - 0.24, x + 0.24], [m, m], color=col, lw=2.8, zorder=5,
                    solid_capstyle="butt")
            ax.annotate(f"{m:.3f}\n+/- {fmt(se)}", (x + 0.27, m),
                        textcoords="offset points", xytext=(2, 0), va="center",
                        fontsize=7.2, color=col)
            out["panel_b"]["arms"][arm] = {
                "per_seed": [vals[s] for s in SEEDS], "mean": m,
                "between_seed_se": se, "n_seeds": n,
                "n_episodes_per_seed": [n_ep[s] for s in SEEDS]}
        dm, dse, dd = paired_delta(by_cond["eg"], by_cond["nohole"])
        tl_m, tl_se = TRAINLOG[opp]
        # leave-one-out on the most extreme per-seed delta, so "carried by one
        # seed" is a number on the figure rather than an impression from it
        drop = max(range(len(dd)), key=lambda i: abs(dd[i]))
        rest = [d for j, d in enumerate(dd) if j != drop]
        out["panel_b"]["by_opponent"][opp] = {
            "delta_eg_minus_nohole": {"per_seed_delta": dd, "mean": dm,
                                      "between_seed_se": dse,
                                      "sigma": abs(dm) / dse if dse else None},
            "delta_dropping_most_extreme_seed": {
                "dropped_train_seed": SEEDS[drop],
                "remaining_per_seed_delta": rest,
                "mean": sum(rest) / len(rest) if rest else None},
            "training_log_reference": {
                "mean": tl_m, "se": tl_se, "source": "training logs, EXTERNAL "
                "to this eval", "denominator": "endgame_rate over 7 "
                "environments across all training steps"},
            "this_eval_denominator": "ipd alone, checkpoint step 35, horizons "
                                     "6/10/14 which the policy never trained on"}
        xm = (xs[(opp, "nohole")] + xs[(opp, "eg")]) / 2
        ax.annotate(f"{fmts(dm)} +/- {fmt(dse)}", (xm, 0.0),
                    textcoords="offset points", xytext=(0, -34), ha="center",
                    fontsize=7.6, color=INK2, annotation_clip=False)
        ax.annotate(f"training log {fmts(tl_m)} +/- {fmt(tl_se)}", (xm, 0.0),
                    textcoords="offset points", xytext=(0, -46), ha="center",
                    fontsize=6.8, color=MUT, annotation_clip=False)

    ax.axvline(1.75, color=GRID, lw=1.0, zorder=1)
    ax.set_xlim(-0.75, 4.35)
    ax.set_ylim(0, max(0.60, hi * 1.22))
    ax.set_xticks([x for x, _ in labels])
    ax.set_xticklabels([t for _, t in labels], fontsize=7.4)
    g = out["panel_b"]["by_opponent"]["grim"]["delta_eg_minus_nohole"]
    t = out["panel_b"]["by_opponent"]["tft"]["delta_eg_minus_nohole"]
    style(ax, f"B - Behaviour: vs tft {fmts(t['mean'], 2)} +/- {fmt(t['between_seed_se'], 2)},"
              f"\nvs grim {fmts(g['mean'], 2)} +/- {fmt(g['between_seed_se'], 2)}",
          "endgame_rate", "", tsize=9.8)
    return out


def note_b(out):
    g = out["panel_b"]["by_opponent"]["grim"]["delta_eg_minus_nohole"]
    t = out["panel_b"]["by_opponent"]["tft"]["delta_eg_minus_nohole"]
    loo = out["panel_b"]["by_opponent"]["tft"]["delta_dropping_most_extreme_seed"]
    tg, tgs = TRAINLOG["grim"]
    tt, tts = TRAINLOG["tft"]
    ds = loo["dropped_train_seed"]
    e_ps = out["panel_b"]["arms"]["tft/eg"]["per_seed"]
    others = ", ".join(f"{v:.3f}" for i, v in enumerate(e_ps) if i != ds)
    n_ep = out["panel_b"]["arms"]["tft/eg"]["n_episodes_per_seed"][0]
    spans = []
    for opp, _ in OPPONENTS:
        for cond, _, _ in CONDS:
            v = out["panel_b"]["arms"][f"{opp}/{cond}"]["per_seed"]
            spans.append(f"  {opp}/{cond}: {min(v):.3f}-{max(v):.3f}")
    hz = out["data_hazard"]["cells"]
    return (
        "One hollow ring per training seed (s0/s1/s2), thick dash = arm mean,\n"
        "whisker = between-seed SE, difference = the paired per-seed delta.\n"
        "Opponent is the x-group; the colours keep their meaning across both.\n\n"
        "A PARTIAL REPRODUCTION, and it is worth saying plainly which half is\n"
        f"which. Against tft the eval returns {fmts(t['mean'])} +/- {fmt(t['between_seed_se'])}, "
        f"the same direction\nand rough magnitude as the training log's {fmts(tt)} +/- {fmt(tts)}. "
        f"Against grim\nit returns {fmts(g['mean'])} +/- {fmt(g['between_seed_se'])} "
        f"against a training-log {fmts(tg)} +/- {fmt(tgs)}: the eval\n"
        "cannot resolve an effect that small and does not claim to. The eval\n"
        "reproduces the behavioural effect where it is large and is blind to it\n"
        "where it is small. That is not the same as a null against grim.\n\n"
        f"DO NOT READ THE TFT NUMBER AS TIGHT. Its SE is {fmt(t['between_seed_se'])} on n=3 and it\n"
        f"is carried by tft/eg seed {ds}, an extreme value at {e_ps[ds]:.3f} against {others}\n"
        f"in the other two seeds. Drop it and the remaining two per-seed deltas\n"
        f"average {fmts(loo['mean'])}, about a third of the headline. Per-seed spans:\n"
        + "\n".join(spans) + "\n\n"
        "THE DENOMINATORS ARE NOT THE SAME. The training-log figure is\n"
        "endgame_rate over 7 environments across every training step. This\n"
        "panel is ipd alone, at checkpoint step 35, at horizons 6/10/14 that\n"
        f"the policy was never trained on, {n_ep} episodes per (arm, seed). A\n"
        "disagreement here is not evidence against the training-log result; an\n"
        "agreement is evidence the effect transfers to unseen horizons in this\n"
        "one environment at this one step.\n\n"
        "DATA HAZARD, carried from panel C: grim/nohole seed 1 has an empty\n"
        f"answer on {hz['grim/nohole|1']['decision_turn_empty_rate']:.1%} of its DECISION turns, and it is the "
        f"{hz['grim/nohole|1']['endgame_rate']:.3f} low\n"
        f"outlier in the grim/nohole group. tft/nohole seed 0 is at "
        f"{hz['tft/nohole|0']['decision_turn_empty_rate']:.1%},\n"
        f"on an endgame_rate of {hz['tft/nohole|0']['endgame_rate']:.3f}. Neither is caught by the repo's\n"
        "usual invalid_rate gate, which is episode-level and reads near zero\n"
        "for both.")


# --------------------------------------------------------------------------
# PANEL C -- the faithfulness test
# --------------------------------------------------------------------------

# (label, marker field, required value, x). None/None is the unconditional
# group, and it is the control that decides the panel: if the arm gap is the
# same there as it is under `plan present`, conditioning on the plan bought
# nothing. The x offsets leave a clear column on the far left for the
# "delta(eg - nohole)" caption.
GROUPS = [("plan\npresent", "m_endgame_defect_plan", 1, 0.80),
          ("plan\nabsent", "m_endgame_defect_plan", 0, 1.80),
          ("hold\npresent", "m_endgame_hold", 1, 3.30),
          ("hold\nabsent", "m_endgame_hold", 0, 4.30),
          ("ALL blocks\n(no condition)", None, None, 5.80)]


def panel_c(ax, rows, opp, out):
    fin = [r for r in rows if r["rounds_from_end"] == 0 and r["in_decision"]
           and r["opponent"] == opp]
    kept = [r for r in fin if r["answer_defect"] is not None]

    node = out["panel_c"]["by_opponent"].setdefault(opp, {})
    node["population"] = ("final-round (rounds_from_end == 0) decision blocks, "
                          f"opponent {opp}, both arms")
    node["n_final_decision_blocks"] = len(fin)
    node["n_excluded_null_answer"] = len(fin) - len(kept)
    node["exclusion_rate"] = (len(fin) - len(kept)) / len(fin) if fin else None
    node["exclusion_by_arm"] = {}
    for cond, _, _ in CONDS:
        arm = arm_of(opp, cond)
        a_fin = [r for r in fin if r["arm"] == arm]
        a_kept = [r for r in a_fin if r["answer_defect"] is not None]
        per_seed = []
        for s in SEEDS:
            t = [r for r in a_fin if r["train_seed"] == s]
            k = [r for r in t if r["answer_defect"] is not None]
            per_seed.append({"train_seed": s, "n_final_decision_blocks": len(t),
                             "n_excluded": len(t) - len(k), "n_kept": len(k),
                             "exclusion_rate": (len(t) - len(k)) / len(t) if t else None})
        node["exclusion_by_arm"][arm] = {
            "denominator": "final-round decision blocks for this arm",
            "n_final_decision_blocks": len(a_fin),
            "n_excluded": len(a_fin) - len(a_kept),
            "exclusion_rate": (len(a_fin) - len(a_kept)) / len(a_fin) if a_fin else None,
            "per_seed": per_seed}
    node["groups"] = {}

    thin, suppressed = [], []
    stats = {}
    for glab, mk, want, gx in GROUPS:
        key = glab.replace("\n", " ")
        stats[glab] = {}
        node["groups"][key] = {}
        for cond, clab, col in CONDS:
            arm = arm_of(opp, cond)
            by_seed, ns = {}, {}
            for s in SEEDS:
                sub = [r for r in kept if r["arm"] == arm and r["train_seed"] == s]
                if mk is not None:
                    sub = [r for r in sub if r[mk] == want]
                by_seed[s] = rate(sub, "answer_defect")
                ns[s] = len(sub)
                if len(sub) < MIN_N_FOR_BAR:
                    thin.append(f"{opp}/{cond} s{s} {key} n={len(sub)}")
            m, se, n = between_seed([by_seed[s] for s in SEEDS])
            draw_bar = min(ns.values()) >= MIN_N_FOR_BAR and n >= 2
            if not draw_bar:
                suppressed.append(f"{opp}/{cond} {key} n={list(ns.values())}")
            stats[glab][cond] = (by_seed, ns, m, se, draw_bar)
            node["groups"][key][arm] = {
                "per_seed_p_defect": [by_seed[s] for s in SEEDS],
                "per_seed_n_blocks": [ns[s] for s in SEEDS],
                "mean": m, "between_seed_se": se, "n_seeds": n,
                "n_blocks_pooled": sum(ns.values()),
                "interval_drawn": draw_bar,
                "interval_suppressed_reason":
                    None if draw_bar else
                    f"min per-seed n = {min(ns.values())} < {MIN_N_FOR_BAR}; a "
                    "narrow between-seed bar over single-observation subgroups "
                    "measures the absence of data, not agreement"}

            x = gx + (0.19 if cond == "eg" else -0.19)
            for j, s in enumerate(SEEDS):
                ax.plot([x + (j - 1) * 0.055], [by_seed[s]], marker="o", ms=4.8,
                        mfc="none" if ns[s] >= MIN_N_FOR_BAR else col, mec=col,
                        mew=1.3, alpha=0.95, zorder=3)
            if draw_bar:
                ax.errorbar([x], [m], yerr=[se], color=col, lw=2.0, capsize=5,
                            capthick=2.0, zorder=4)
                ax.plot([x - 0.15, x + 0.15], [m, m], color=col, lw=3.0,
                        zorder=5, solid_capstyle="butt")
            else:
                # no interval: hollow, dashed, and labelled down at the panel
                # floor on a leader line, so the eye cannot read it as a tight
                # estimate and the label cannot land on a neighbour's data.
                ax.plot([x - 0.15, x + 0.15], [m, m], color=col, lw=1.6,
                        ls=(0, (2, 1.6)), zorder=5, solid_capstyle="butt")
                ax.plot([x, x], [0.16, m - 0.03], color=col, lw=0.7,
                        ls=(0, (1, 2.2)), zorder=2)
                ax.text(x, 0.12, "no interval, n="
                        + ",".join(str(ns[s]) for s in SEEDS),
                        ha="center", va="top", fontsize=5.9, color=col)
            ax.text(x, 1.055, f"n={sum(ns.values())}", ha="center",
                    fontsize=6.4, color=col)

        dm, dse, dd = paired_delta(stats[glab]["eg"][0], stats[glab]["nohole"][0])
        both_drawn = stats[glab]["eg"][4] and stats[glab]["nohole"][4]
        node["groups"][key]["delta_eg_minus_nohole"] = {
            "per_seed_delta": dd, "mean": dm, "between_seed_se": dse,
            "sigma": abs(dm) / dse if dse else None,
            "both_arms_meet_min_n": both_drawn}
        ax.text(gx, 1.155, f"{fmts(dm)}\n+/- {fmt(dse)}"
                           + ("" if both_drawn else "\n(thin)"),
                ha="center", va="bottom", fontsize=7.0,
                color=INK2 if both_drawn else MUT)

    ax.text(-0.50, 1.155, "delta(eg - nohole),\nbetween-seed SE:", ha="left",
            va="bottom", fontsize=7.0, color=INK2)

    g_plan = node["groups"]["plan present"]["delta_eg_minus_nohole"]
    g_all = node["groups"]["ALL blocks (no condition)"]["delta_eg_minus_nohole"]
    g_hold = node["groups"]["hold present"]["delta_eg_minus_nohole"]
    node["verdict"] = {
        "delta_conditioned_on_plan": g_plan["mean"],
        "delta_unconditional": g_all["mean"],
        "explained_by_conditioning_on_plan": g_plan["mean"] - g_all["mean"],
        "delta_conditioned_on_opposite_marker_hold": g_hold["mean"],
        "plan_gap_sigma": g_plan["sigma"],
        "unconditional_gap_sigma": g_all["sigma"],
        "survives_between_seed_se_at_2_sigma":
            bool(g_plan["sigma"] and g_plan["sigma"] > 2),
        "note": "conditioning on the stated plan moves the arm gap by "
                f"{fmts(g_plan['mean'] - g_all['mean'])} out of {fmts(g_all['mean'])}; "
                "the OPPOSITE marker gives a gap of the same size and sign, "
                "which is what you see when the marker is doing no work and "
                "the whole difference is the arm's overall final-round rate."}
    node["thin_subgroups"] = thin
    node["intervals_suppressed"] = suppressed

    # The y headroom above 1.0 is where the two annotation rows live: subgroup
    # n at 1.055 and the arm delta at 1.155.
    ax.set_xlim(-0.55, 6.45)
    ax.set_ylim(-0.06, 1.44)
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_xticks([g[3] for g in GROUPS])
    ax.set_xticklabels([g[0] for g in GROUPS] if opp == OPPONENTS[-1][0]
                       else ["" for _ in GROUPS], fontsize=7.6)
    style(ax, f"C - vs {opp}: gap under the plan {fmts(g_plan['mean'], 2)}, under "
              f"NOTHING {fmts(g_all['mean'], 2)}, under the OPPOSITE marker "
              f"{fmts(g_hold['mean'], 2)}",
          "P(the block's answer actually defects)",
          "what the same final-round reasoning block was conditioned on"
          if opp == OPPONENTS[-1][0] else "")
    for gx in (2.55, 4.80):
        ax.axvline(gx, color=GRID, lw=1.0, zorder=1)
    ax.axvspan(4.80, 6.45, color=GRID, alpha=0.35, lw=0, zorder=0)

    # The legend is drawn on the first opponent row only. On the tft row the
    # floor of the panel is where eg seed 2 lives, and a legend there would sit
    # on top of the panel's most consequential data point.
    if opp == OPPONENTS[0][0]:
        for cond, clab, col in CONDS:
            ax.plot([], [], color=col, lw=3.0, label=clab)
        leg = ax.legend(loc="lower right", fontsize=7.2, frameon=False,
                        bbox_to_anchor=(0.997, 0.005), ncol=2)
        for t, (_, _, col) in zip(leg.get_texts(), CONDS):
            t.set_color(col)
    return out


def note_c(out):
    lines, excl, thin, supp = [], [], [], []
    worst = None      # the suppressed group with the emptiest seed, quoted below
    thinnest_seed = None
    for opp, _ in OPPONENTS:
        node = out["panel_c"]["by_opponent"][opp]
        for key, grp in node["groups"].items():
            for cond, _, _ in CONDS:
                e = grp.get(f"{opp}/{cond}")
                if e and not e["interval_drawn"]:
                    mn = min(e["per_seed_n_blocks"])
                    if worst is None or mn < worst[0]:
                        worst = (mn, f"{opp} {key} / {cond}", e)
        for cond, _, _ in CONDS:
            for key, grp in node["groups"].items():
                e = grp.get(f"{opp}/{cond}")
                if e:
                    for n, r in zip(e["per_seed_n_blocks"], e["per_seed_p_defect"]):
                        if thinnest_seed is None or n < thinnest_seed:
                            thinnest_seed = n
    w_ns = ", ".join(str(n) for n in worst[2]["per_seed_n_blocks"]) if worst else ""
    w_ps = ", ".join(fmt(r) for r in worst[2]["per_seed_p_defect"]) if worst else ""
    w_lab = worst[1] if worst else "none"
    for opp, _ in OPPONENTS:
        node = out["panel_c"]["by_opponent"][opp]
        v = node["verdict"]
        lines.append(
            f"  vs {opp}: plan {fmts(v['delta_conditioned_on_plan'])}, nothing "
            f"{fmts(v['delta_unconditional'])}, opposite marker "
            f"{fmts(v['delta_conditioned_on_opposite_marker_hold'])};")
        lines.append(
            f"     the plan buys {fmts(v['explained_by_conditioning_on_plan'])} of "
            f"{fmts(v['delta_unconditional'])}. Unconditional gap "
            f"{v['unconditional_gap_sigma']:.1f} sigma at n=3.")
        for cond, _, _ in CONDS:
            e = node["exclusion_by_arm"][f"{opp}/{cond}"]
            excl.append(f"  {opp}/{cond}: {e['n_excluded']} of "
                        f"{e['n_final_decision_blocks']} ({e['exclusion_rate']:.1%}); "
                        "per seed "
                        + ", ".join(f"s{p['train_seed']} {p['n_excluded']}/"
                                    f"{p['n_final_decision_blocks']}"
                                    for p in e["per_seed"]))
        thin += node["thin_subgroups"]
        supp += node["intervals_suppressed"]
    gn = out["panel_c"]["by_opponent"]["grim"]["exclusion_by_arm"]["grim/nohole"]
    thinnest = min(gn["per_seed"], key=lambda p: p["n_kept"])
    worst_kept, worst_tot = thinnest["n_kept"], thinnest["n_final_decision_blocks"]
    return (
        "One ring per training seed, thick dash = mean of the three, whisker =\n"
        "between-seed SE. One row per opponent; colours keep their meaning.\n\n"
        f"MINIMUM-N RULE. A FILLED ring means that seed's subgroup holds fewer\n"
        f"than {MIN_N_FOR_BAR} blocks. If ANY of the three seeds is that thin the interval is\n"
        "NOT DRAWN at all -- the mean appears as a hollow dashed rule with its\n"
        "per-seed n printed, and its delta is marked (thin). This is a fix, not\n"
        f"a decoration: the previous render gave {w_lab} the tightest bar on the\n"
        f"panel over per-seed n of [{w_ns}] with per-seed rates [{w_ps}], then\n"
        f"quoted that bar as corroboration. The thinnest cell anywhere on this\n"
        f"panel is n={thinnest_seed}, so some of those 'rates' are one and two observations\n"
        "and the spread across seeds was near zero for want of data. A narrow\n"
        "bar over near-empty subgroups is not evidence of anything.\n"
        "  intervals suppressed: " + ("; ".join(supp) if supp else "none") + "\n"
        "  thin per-seed cells: " + ("; ".join(thin) if thin else "none") + "\n\n"
        "THE ARGUMENT IS THE SHADED GROUP ON THE RIGHT. If the penalty left the\n"
        "plan intact and intercepted only the act, the arm gap under \"plan\n"
        "present\" would have to be LARGER than the gap with no conditioning at\n"
        "all. In neither opponent is it:\n"
        + "\n".join(lines) + "\n"
        "Adding tft did not rescue the plan-specific story; it made the gap\n"
        "bigger and left the plan explaining just as little of it. A marker\n"
        "that predicts the same thing as its own negation is not predicting\n"
        "anything. What differs between the arms is the overall final-round\n"
        "defect rate, and against tft that difference is carried by eg seed 2.\n\n"
        "NULL-ANSWER EXCLUSION -- blocks whose answer was empty or truncated so\n"
        "no action could be parsed. The env falls back to a library default\n"
        "move there, and scoring that as \"planned to defect, cooperated\n"
        "instead\" would manufacture unfaithfulness out of the token budget.\n"
        "Denominator is that arm's final-round DECISION blocks:\n"
        + "\n".join(excl) + "\n"
        f"The drop is badly uneven: grim/nohole s1 keeps only {worst_kept} of its\n"
        f"{worst_tot} final-round decision blocks, so every grim/nohole estimate above\n"
        "leans on that one thin seed and could be selection-biased if\n"
        "truncation correlates with the action.")


# --------------------------------------------------------------------------

def build(out_dir: Path, dpi: int, source: Path | None) -> int:
    blocks_p = out_dir / "trace_blocks.jsonl"
    cells_p = out_dir / "trace_markers.json"
    markers = json.loads(cells_p.read_text())
    cells, meta = markers["cells"], markers["meta"]
    all_rows = [json.loads(l) for l in blocks_p.read_text().splitlines() if l.strip()]

    drawn_arms = [arm_of(o, c) for o, _ in OPPONENTS for c, _, _ in CONDS]
    rows = [r for r in all_rows if r["arm"] in set(drawn_arms)]

    # --- episode counts, with the identity bug fixed -----------------------
    n_ep_drawn = len({episode_key(r) for r in rows})
    n_ep_all = len({episode_key(r) for r in all_rows})
    n_triples = len({(r["arm"], r["train_seed"], r["episode_seed"]) for r in rows})
    per_cell = {len({episode_key(r) for r in rows
                     if r["arm"] == a and r["train_seed"] == s})
                for a in drawn_arms for s in SEEDS}
    n_ep_cell = per_cell.pop() if len(per_cell) == 1 else None
    n_ep_arm = n_ep_cell * len(SEEDS) if n_ep_cell else n_ep_drawn // len(drawn_arms)

    src = source or Path(meta.get("source", ""))
    agreement = answer_parse_agreement(src, meta["action_regex"], set(drawn_arms))

    out = {
        "figure": "fig3_plan_vs_act.png",
        "source_blocks": str(blocks_p),
        "source_cells": str(cells_p),
        "source_episodes": str(src),
        "arms_plotted": drawn_arms,
        "opponents": dict(OPPONENTS),
        "train_seeds": list(SEEDS),
        "episode_counts": {
            "identity": "an episode is (arm, train_seed, episode_seed, "
                        "num_rounds). num_rounds is PART OF THE IDENTITY: each "
                        "(arm, train_seed, episode_seed) triple is replayed at "
                        "horizons 6, 10 and 14, so counting triples undercounts "
                        "episodes by exactly 3x.",
            "n_episodes_drawn_arms": n_ep_drawn,
            "n_episodes_all_cells": n_ep_all,
            "n_triples_drawn_arms_WRONG_DENOMINATOR": n_triples,
            "previous_render_reported": 96,
            "correct_value_for_the_previous_grim_only_figure": 288,
            "n_blocks_drawn_arms": len(rows),
            "n_blocks_all_cells": len(all_rows),
            "episodes_per_cell": n_ep_cell,
            "episodes_per_arm": n_ep_arm,
            "cross_check": f"{len(drawn_arms)} arms x {len(SEEDS)} seeds x "
                           f"{n_ep_cell} episodes = "
                           f"{len(drawn_arms) * len(SEEDS) * n_ep_cell}, drawn = "
                           f"{n_ep_drawn}"},
        "answer_parse_agreement": agreement,
        "coverage_note": "grim and tft each have both arms at 3 training "
                         "seeds. tft/inf exists at ONE seed (train_seed 1) and "
                         "grim/inf at none, so no inf contrast is computable; "
                         "inf is excluded from every panel and BLUE, which is "
                         "reserved for it, appears nowhere on this figure.",
        "error_bar_definition": "all bars and bands are BETWEEN TRAINING SEED: "
                                "per-seed value, then sd/sqrt(3). Arm "
                                "differences use the paired per-seed delta. "
                                "Binomial SE is the sampling floor and is not "
                                "drawn.",
        "minimum_n_rule": f"an interval is drawn only if every contributing "
                          f"seed has >= {MIN_N_FOR_BAR} blocks in the subgroup; "
                          f"otherwise the mean is drawn without an interval and "
                          f"flagged. Means are still reported here.",
        "panel_a": {"turns": "decision turns only (in_decision true)",
                    "positions": list(range(MAX_RFE + 1)),
                    "position_restriction": "0..5 only: every horizon (6, 10, "
                                            "14) reaches 5 from the end and no "
                                            "further, so each drawn position is "
                                            "an equal mix of the three horizons",
                    "by_opponent": {}},
        "panel_c": {"by_opponent": {}},
    }

    # --- the data hazard ----------------------------------------------------
    # Two different empty-answer denominators exist and neither was stated
    # before, which made them look like a rounding disagreement.
    hz = {"denominators": {
        "n_empty_answer_rate": "trace_markers.json -> cells -> "
                               "n_empty_answer_rate is over ALL turns in the "
                               "cell; the denominator is the cell's n_blocks, "
                               "reported per cell below as n_blocks_all_turns",
        "decision_turn_empty_rate": "computed here over DECISION blocks only "
                                    "(half as many; reported per cell below as "
                                    "n_decision_blocks): the share whose "
                                    "answer_defect is null",
        "invalid_rate": "episode-level, from the env; this is the repo's usual "
                        "gate and it does NOT catch empty answers"},
        "cells": {}}
    for opp, _ in OPPONENTS:
        for cond, _, _ in CONDS:
            arm = arm_of(opp, cond)
            for s in SEEDS:
                k = f"{arm}|{s}"
                dec = [r for r in rows if r["arm"] == arm
                       and r["train_seed"] == s and r["in_decision"]]
                emp = sum(1 for r in dec if r["answer_defect"] is None)
                c = cells[k]
                hz["cells"][k] = {
                    "n_decision_blocks": len(dec),
                    "n_decision_blocks_empty_answer": emp,
                    "decision_turn_empty_rate": emp / len(dec) if dec else None,
                    "n_empty_answer_rate_all_turns": c["n_empty_answer_rate"],
                    "n_blocks_all_turns": c["n_blocks"],
                    "invalid_rate": c["invalid_rate"],
                    "endgame_rate": c["endgame_rate"],
                    "mean_chars": c["mean_chars"]}
    worst = sorted(hz["cells"].items(),
                   key=lambda kv: -kv[1]["decision_turn_empty_rate"])[:3]
    hz["flagged"] = [{"cell": k, **v} for k, v in worst
                     if v["decision_turn_empty_rate"] > 0.20]
    out["data_hazard"] = hz

    # --- figure -------------------------------------------------------------
    fig = plt.figure(figsize=(21.4, 15.0))
    fig.patch.set_facecolor(PAPER)
    gs = fig.add_gridspec(2, 3, width_ratios=[1.12, 0.60, 1.72],
                          height_ratios=[1.0, 1.0],
                          left=0.038, right=0.988, top=0.770, bottom=0.452,
                          wspace=0.235, hspace=0.290)

    ax_a = [fig.add_subplot(gs[i, 0]) for i in range(2)]
    ax_b = fig.add_subplot(gs[:, 1])
    ax_c = [fig.add_subplot(gs[i, 2]) for i in range(2)]

    for i, (opp, _) in enumerate(OPPONENTS):
        out = panel_a(ax_a[i], rows, opp, out)
    out = panel_b(ax_b, cells, out)
    for i, (opp, _) in enumerate(OPPONENTS):
        out = panel_c(ax_c[i], rows, opp, out)

    # Footer columns are pinned to the finished axes positions, so a change to
    # the width ratios cannot slide a note out from under its panel.
    for ax, note in ((ax_a[1], note_a(out)),
                     (ax_b, note_b(out)),
                     (ax_c[1], note_c(out))):
        pos = ax.get_position()
        fig.text(pos.x0, 0.398, note, fontsize=7.0, color=MUT, va="top",
                 ha="left", linespacing=1.36)

    v_t = out["panel_c"]["by_opponent"]["tft"]["verdict"]
    v_g = out["panel_c"]["by_opponent"]["grim"]["verdict"]
    b_t = out["panel_b"]["by_opponent"]["tft"]["delta_eg_minus_nohole"]
    b_g = out["panel_b"]["by_opponent"]["grim"]["delta_eg_minus_nohole"]

    # The previous title read "The endgame penalty does not suppress endgame
    # reasoning selectively: it lowers the whole reasoning curve, ...". Both
    # halves overreached. "Does not suppress selectively" was an equivalence
    # claim resting on a grim spike difference of 0.1 sigma, and "lowers the
    # whole curve" is false of grim, whose eg arm sits ABOVE nohole one round
    # from the end. Only the LEVEL shift against tft clears the figure's own
    # 2-sigma bar, so only it is called a result.
    mk0 = SERIES[0][0]
    sp = {o: out["panel_a"]["by_opponent"][o]["spike_amplitude"][
              f"{o}|{mk0}|delta_eg_minus_nohole"] for o, _ in OPPONENTS}
    lv = {o: out["panel_a"]["by_opponent"][o]["level_shift"][
              f"{o}|{mk0}|delta_eg_minus_nohole"] for o, _ in OPPONENTS}

    title = (
        f"No DETECTABLE selective suppression: spike difference "
        f"{fmts(sp['tft']['mean'], 2)} +/- {fmt(sp['tft']['between_seed_se'], 2)} vs tft, "
        f"{fmts(sp['grim']['mean'], 2)} +/- {fmt(sp['grim']['between_seed_se'], 2)} vs grim; "
        f"the level drop is a tft result ({fmts(lv['tft']['mean'], 2)} +/- "
        f"{fmt(lv['tft']['between_seed_se'], 2)}), not a grim one; and the stated plan "
        f"predicts the action no better than nothing does")
    fig.suptitle(title, fontsize=12.6, color=INK, x=0.006, ha="left", y=0.988)
    out["headline"] = title

    ag = agreement.get("arms_drawn") if agreement.get("available") else None
    ag_txt = (f"agreed with the recorded episode defect_indices on "
              f"{ag['agree']:,} of {ag['parsed_actions']:,} parsed actions "
              f"({ag['rate']:.4%}), recomputed at render time"
              if ag else "agreement with defect_indices not recomputed: the "
                         "episode source was not readable")
    header = [
        f"EVERY ERROR BAR AND BAND IS BETWEEN TRAINING SEED: the quantity is computed separately for each of the "
        f"{len(SEEDS)} training seeds, then sd/sqrt({len(SEEDS)}); arm differences are the paired per-seed delta, "
        "the convention already written into trace_markers.json -> contrasts. Binomial SE is the",
        f"sampling FLOOR, not the uncertainty on a claim about the knob, and it is drawn nowhere here. At "
        f"n={len(SEEDS)} these "
        f"intervals are wide and nothing under 2 sigma is called a result: the behaviour gap in panel B is "
        f"{b_t['sigma']:.1f} sigma vs tft and {b_g['sigma']:.1f} sigma vs grim, and the plan-conditioned gap in panel C is "
        f"{v_t['plan_gap_sigma']:.1f} sigma vs tft,",
        f"{v_g['plan_gap_sigma']:.1f} sigma vs grim. Qwen3.8-27B, thinking on, ipd only, checkpoint step 35, horizons "
        "6/10/14, none of which is the training horizon. AN EPISODE IS (arm, train_seed, episode_seed, num_rounds): "
        "num_rounds is part of the identity because each triple is replayed at all",
        f"three horizons, so counting triples undercounts 3x -- which is how the previous render printed "
        f"\"96 episodes\" beside its own \"3 seeds x 48 episodes\". Drawn here: {len(drawn_arms)} arms x "
        f"{len(SEEDS)} seeds x {n_ep_cell} = {n_ep_drawn} episodes and {len(rows):,} reasoning blocks, out of "
        f"{n_ep_all} episodes and {len(all_rows):,} blocks on disk.",
        "tft/inf has ONE seed and grim/inf none, so inf enters no contrast, is not drawn, and BLUE -- which is "
        "reserved for it -- appears nowhere. A marker hit is binary per reasoning block; answer_defect is the action "
        f"parsed from that same turn's answer and {ag_txt}.",
    ]
    for i, line in enumerate(header):
        fig.text(0.006, 0.960 - i * 0.0148, line, fontsize=7.9, color=INK2,
                 ha="left")

    n_dec_set = sorted({v["n_decision_blocks"] for v in hz["cells"].values()})
    n_all_set = sorted({v["n_blocks_all_turns"] for v in hz["cells"].values()})
    dens = (f"{n_all_set[0]} per cell" if len(n_all_set) == 1 else "per cell",
            f"{n_dec_set[0]} per cell" if len(n_dec_set) == 1 else "per cell")
    hz_lines = ["DATA HAZARD -- EMPTY ANSWERS, AND THE TWO DENOMINATORS THAT MAKE THEM LOOK LIKE A ROUNDING "
                f"DISAGREEMENT. trace_markers.json -> cells -> n_empty_answer_rate is over ALL turns in the cell "
                f"({dens[0]}); the rate quoted below is over DECISION turns only ({dens[1]}). Both are correct."]
    for k, v in worst:
        if v["decision_turn_empty_rate"] <= 0.20:
            continue
        hz_lines.append(
            f"  {k}: {v['decision_turn_empty_rate']:.1%} of its "
            f"{v['n_decision_blocks']} DECISION turns have an empty answer "
            f"({v['n_empty_answer_rate_all_turns']:.1%} over all "
            f"{v['n_blocks_all_turns']} turns), mean reasoning "
            f"{v['mean_chars']:.0f} chars, endgame_rate {v['endgame_rate']:.3f} "
            f"-- and its episode-level invalid_rate reads "
            f"{v['invalid_rate']:.3f}, so the repo's usual gate does not see "
            f"it at all.")
    hz_lines.append("  Truncation is not random with respect to the action, so every cell above is a candidate "
                    "selection bias in panels B and C, not merely a smaller n.")
    for i, line in enumerate(hz_lines):
        fig.text(0.006, 0.879 - i * 0.0142, line, fontsize=7.4,
                 color=INK2 if i == 0 else MUT, ha="left")

    # --- the disclaimer fig1 carries and this figure did not ----------------
    # Collect every arm-difference interval the figure puts on the page, name
    # the widest, and say what it admits. Intervals over subgroups that fail
    # the minimum-n rule are printed "(thin)" and no bar is drawn for them, so
    # the widest DRAWN interval excludes those; the widest including them is
    # in the JSON. The least resolved of the two spike differences is quoted
    # separately because that is the one the headline rests on.
    iv = []
    for opp, _ in OPPONENTS:
        pa = out["panel_a"]["by_opponent"][opp]
        for k, v in pa["spike_amplitude"].items():
            if k.endswith("|delta_eg_minus_nohole"):
                iv.append((f"panel A spike difference, {k.split('|')[1]} vs "
                           f"{opp}", v, False))
        for k, v in pa["level_shift"].items():
            iv.append((f"panel A level shift, {k.split('|')[1]} vs {opp}",
                       v, False))
        iv.append((f"panel B behaviour gap vs {opp}",
                   out["panel_b"]["by_opponent"][opp]["delta_eg_minus_nohole"],
                   False))
        for g, gv in out["panel_c"]["by_opponent"][opp]["groups"].items():
            d = gv["delta_eg_minus_nohole"]
            iv.append((f"panel C arm gap under \"{g}\" vs {opp}", d,
                       not d["both_arms_meet_min_n"]))
    iv = [t for t in iv if t[1]["between_seed_se"] is not None]
    wide_all = max(iv, key=lambda t: t[1]["between_seed_se"])
    wide = max([t for t in iv if not t[2]] or iv,
               key=lambda t: t[1]["between_seed_se"])
    weak = min(sp, key=lambda o: abs(sp[o]["mean"]) / sp[o]["between_seed_se"])
    wm, wse = sp[weak]["mean"], sp[weak]["between_seed_se"]

    disc = [
        f"THIS IS NOT AN EQUIVALENCE RESULT, AND THE {weak.upper()} HALF OF THIS FIGURE IS NOT ONE. Every arm "
        f"difference here is between-seed on n={len(SEEDS)} and correspondingly wide: the widest drawn is the "
        f"{wide[0]} at {fmts(wide[1]['mean'])} +/- {fmt(wide[1]['between_seed_se'])}. The difference the headline "
        f"rests on, the {weak} spike difference,",
        f"is {fmts(wm)} +/- {fmt(wse)} -- {abs(wm) / wse:.1f} sigma, admitting anything from {fmts(wm - 2 * wse)} to "
        f"{fmts(wm + 2 * wse)} at +/-2 SE, the complete flattening of the {weak} endgame spike included. A WIDE "
        f"INTERVAL CONTAINING ZERO IS A FAILURE TO DETECT, NOT A DEMONSTRATION OF ABSENCE. No panel here shows that "
        f"the penalty leaves endgame reasoning alone.",
    ]
    y0 = 0.879 - (len(hz_lines) - 1) * 0.0142 - 0.0072
    for i, line in enumerate(disc):
        fig.text(0.006, y0 - i * 0.0090, line, fontsize=7.4, color=INK,
                 ha="left", va="top")

    out["not_an_equivalence_claim"] = True
    out["interval_width_disclaimer"] = {
        "not_an_equivalence_claim": True,
        "rendered_text": " ".join(disc),
        "definition": "the arm-difference intervals scanned are every "
                      "delta_eg_minus_nohole this figure prints: the panel A "
                      "spike differences and level shifts, the panel B "
                      "behaviour gaps, and the panel C per-subgroup gaps",
        "widest_interval_drawn": {
            "what": wide[0], "mean": wide[1]["mean"],
            "between_seed_se": wide[1]["between_seed_se"]},
        "widest_interval_including_min_n_flagged": {
            "what": wide_all[0], "mean": wide_all[1]["mean"],
            "between_seed_se": wide_all[1]["between_seed_se"],
            "fails_minimum_n_rule": wide_all[2]},
        "least_resolved_spike_difference": {
            "opponent": weak, "marker": mk0, "mean": wm,
            "between_seed_se": wse, "sigma": abs(wm) / wse,
            "two_se_interval": [wm - 2 * wse, wm + 2 * wse]},
        "note": "a wide interval containing zero is a failure to detect, not "
                "a demonstration of absence. The one claim on this figure "
                "that clears the 2-sigma bar it sets for itself is the tft "
                "LEVEL shift; the spike differences and the plan-conditioned "
                "gaps do not, and panel C records "
                "survives_between_seed_se_at_2_sigma false for both "
                "opponents."}

    png = out_dir / "fig3_plan_vs_act.png"
    fig.savefig(png, dpi=dpi, facecolor=fig.get_facecolor())
    print(f"[fig3] wrote {png}")

    js = out_dir / "fig3_plan_vs_act.json"
    js.write_text(json.dumps(out, indent=1))
    print(f"[fig3] wrote {js}")

    print(f"[fig3] episodes drawn {n_ep_drawn} (triples would say {n_triples}), "
          f"blocks {len(rows)}")
    if ag:
        print(f"[fig3] answer/defect_indices agreement {ag['agree']}/"
              f"{ag['parsed_actions']} = {ag['rate']:.6f}")
    for opp, _ in OPPONENTS:
        v = out["panel_c"]["by_opponent"][opp]["verdict"]
        print(f"[fig3] panel C {opp}: delta|plan = "
              f"{v['delta_conditioned_on_plan']:+.4f}, delta|nothing = "
              f"{v['delta_unconditional']:+.4f}, delta|hold = "
              f"{v['delta_conditioned_on_opposite_marker_hold']:+.4f}, "
              f"plan buys {v['explained_by_conditioning_on_plan']:+.4f}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out-dir", type=Path, default=HERE,
                   help="directory holding trace_blocks.jsonl and "
                        "trace_markers.json, and where the png/json are "
                        "written (default: the script's own directory)")
    p.add_argument("--dpi", type=int, default=150, help="PNG dpi (default 150)")
    p.add_argument("--source", type=Path, default=None,
                   help="episode jsonl used to recompute answer/defect_indices "
                        "agreement (default: trace_markers.json -> meta.source)")
    a = p.parse_args()
    return build(a.out_dir, a.dpi, a.source)


if __name__ == "__main__":
    raise SystemExit(main())
