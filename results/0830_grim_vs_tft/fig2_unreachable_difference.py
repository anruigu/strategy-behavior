#!/usr/bin/env python
"""Where in the game do grim and tit-for-tat differ, and does the policy go there?

    /home/allie/venvs/tinker-ipd/bin/python fig2_unreachable_difference.py

  fig2_unreachable_difference.png    the four panels
  fig2_unreachable_difference.json   every number drawn

THE QUESTION. grim trigger and tit-for-tat are the SAME opponent until the model
defects with rounds still to play. A defection in the final round leaves neither
of them a round in which to answer it, so it cannot discriminate them. Everything
that makes grim grim -- the refusal to forgive -- lives strictly after a mid-game
defection. So before asking whether the two trained policies differ, ask whether
the policy ever visits the region of the game in which the opponents differ.

WHY THIS IS THE MECHANISM, NOT A SIDE OBSERVATION. crossplay finds no policy
difference between the grim-trained and tft-trained arms. That null has two very
different readings: the RL either could not learn the distinction, or was never
shown it. This figure separates them. The distinguishing training signal is
delivered only along the path defect-early -> get punished -> return to
cooperating -> observe whether the opponent forgives. Panel D counts how many
episodes walked that path. Panels A and B locate the defections in the game.
Panel C measures the share of rounds spent in the punished regime at all.

TWO CACHES, AND THREE WINDOWS -- NEVER DIVIDED BY ONE ANOTHER. Panels A, C and D
all read `train_strategy.json`, ipd only, but they do NOT share a window, and
each panel is labelled with the window it actually uses:

  A, C   steps >= meta["late_step"]   the LATE window, converged policy only.
  D      steps >= meta["trained_step"]  EVERY trained step. The cache builds the
         repair funnel at this floor and no other, so the funnel is reported at
         this floor. It is also the conservative choice: the claim panel D makes
         is "this path is almost never walked", and the wider window roughly
         doubles the denominator that claim has to survive. Panel D carries a
         second line with the late-window counts so the claim can be checked in
         both windows.
  B      `eval_strategy.json`: frozen step-35 adapters replayed at N = 6, 10,
         14, lengths the arms never trained on. Panel B exists to rule out the
         reading that panel A is an artefact of the fixed 10-round horizon.

Per the training cache's own note the traces are the FIRST 24 episodes of every
5th step, so every train panel is a sample of training, not the dense log.

NO WINDOW BOUND IS WRITTEN AS A LITERAL. Every step floor on the page and in the
companion JSON is read out of `train_strategy.json["meta"]`.

ERROR BARS. Every bar is BETWEEN TRAINING SEED, sd(ddof=1)/sqrt(n_seeds), in
both caches. A cell with n_seeds < 2 carries se = null and gets NO bar drawn --
never a zero-length bar, which would read as a measured zero spread.

PALETTE. Opponent identity is #00918f grim / #b8236f tft, and every series is
direct-labelled as well as coloured: these two hues separate only at the CVD
floor, so identity never rests on colour alone. Arm identity, where it appears,
is the study's fixed trio #7a5bd6 base / #eb6834 endgame-penalty / #2a78d6
hidden-horizon.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
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

TRAIN = HERE / "train_strategy.json"
EVAL = HERE / "eval_strategy.json"

OPP = [("grim", GRIM, "o", "-", "grim trigger"),
       ("tft", TFT, "s", (0, (5, 2)), "tit-for-tat")]

EARMS = [("grim/nohole", GRIM, "o", "-", 2.2, "grim / base", 1.00),
         ("tft/nohole", TFT, "s", (0, (5, 2)), 2.2, "tit-for-tat / base", 1.00),
         ("grim/eg", GRIM, "o", (0, (1, 1.6)), 1.5, "grim / endgame-penalty", 0.60),
         ("tft/eg", TFT, "s", (0, (1, 1.6)), 1.5, "tit-for-tat / endgame-penalty", 0.60)]

CELLS = [("grim/base", GRIM), ("tft/base", TFT), ("grim/eg", GRIM),
         ("tft/eg", TFT), ("grim/inf", GRIM), ("tft/inf", TFT)]

STAGES = [
    ("all", "all episodes"),
    ("f_defect_before_last", "model defected BEFORE the final round"),
    ("f_opp_retaliated", "opponent retaliated"),
    ("f_model_returned", "model returned to cooperating"),
    ("f_opp_forgave", "opponent forgave"),
]
FCELLS = [("grim/base", GRIM, "grim / base", 0.80),
          ("tft/base", TFT, "tit-for-tat / base", 0.80)]
# The endgame-penalty arm runs the same funnel. Four bars per stage row leaves
# ~10pt per label at this figure size, which is not legible, so eg is carried as
# an explicit count line instead of a bar it would be impossible to read.
ECELLS = [("grim/eg", GRIM, "grim / endgame-penalty"),
          ("tft/eg", TFT, "tit-for-tat / endgame-penalty")]
SLOT = [0.19, -0.19]
BH, BH2 = 0.34, 0.30


def style(ax, title, ylab, xlab=None, note=None):
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
        ax.text(0.015, 0.965, note, transform=ax.transAxes, fontsize=7.5,
                color=MUT, va="top")


def hbar_style(ax, title, ylab, xlab=None, note=None):
    """Same helper, x-gridded: the vertical grid is the readable one on barh."""
    style(ax, title, ylab, xlab, note)
    ax.grid(False, axis="y")
    ax.grid(True, axis="x", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)


def errbar(ax, x, y, se, color, horizontal=False):
    """A null SE draws NOTHING. A genuine 0.0 from >=2 seeds does draw."""
    if se is None:
        return False
    if horizontal:
        ax.errorbar(y, x, xerr=se, fmt="none", ecolor=color, elinewidth=1.3,
                    capsize=2.6, capthick=1.3, zorder=4)
    else:
        ax.errorbar(x, y, yerr=se, fmt="none", ecolor=color, elinewidth=1.3,
                    capsize=2.6, capthick=1.3, zorder=4)
    return True


def all_stage(n_episodes: int) -> dict:
    """Stage 1 of the funnel: the cell's own denominator, so the rate is 1.0.

    Both cell groups are built through this one constructor. The quantity is the
    same trivial one in every cell, so it must not read 1.0 where a bar is drawn
    and null where only a count line is, purely because two code paths built it.
    """
    return {"num": n_episodes, "den": n_episodes, "pooled_rate": 1.0,
            "se": None, "n_seeds": None, "per_seed": None,
            "structurally_impossible": False}


def funnel_stage(f: dict, cell: str, key: str) -> dict:
    """One cached funnel stage, flattened to the shape the JSON publishes."""
    st = f[key]
    return {"num": st["num"], "den": st["den"], "pooled_rate": st["pooled_rate"],
            "se": st["se"], "n_seeds": st["n_seeds"], "per_seed": st["per_seed"],
            "structurally_impossible": (key == "f_opp_forgave"
                                        and cell.startswith("grim"))}


def late_funnel_entry(T: dict, cell: str) -> tuple[int, int]:
    """(episodes, episodes that defected before the final round) in the LATE window.

    The cache builds the funnel at the trained-step floor only, but stage 2 is a
    plain per-episode boolean that `pooled_late` also carries, so the late-window
    entry count is recoverable exactly: per_seed holds k/n and per_seed_n holds n.
    Stages 3-5 are conditional chains and are NOT recoverable from the cache --
    for those the late window is a subset of the panel's window, which bounds
    them from above by the counts the panel already draws.
    """
    d = T["pooled_late"][cell]["defect_before_last"]
    num = sum(int(round(d["per_seed"][s] * d["per_seed_n"][s]))
              for s in d["per_seed"])
    return d["n_episodes"], num


def eg_line(T: dict, dens: dict, cell: str) -> str:
    f = T["funnel"][cell]
    bits = ["%d ep" % dens[cell]]
    for key, _ in STAGES[1:]:
        st = f[key]
        if key == "f_opp_forgave" and cell.startswith("grim"):
            bits.append("n/a by construction")
        elif st["den"] == 0:
            bits.append("0 / 0 never reached")
        else:
            bits.append("%d / %d" % (st["num"], st["den"]))
    return "  ->  ".join(bits)


def main() -> int:
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)
    ap.add_argument("--outdir", type=Path, default=HERE)
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--stem", default="fig2_unreachable_difference")
    args = ap.parse_args()

    T = json.loads(TRAIN.read_text())
    E = json.loads(EVAL.read_text())

    # The two step floors this figure reports at. Both come out of the cache
    # meta; neither is ever written as a literal anywhere on the page.
    LATE = T["meta"]["late_step"]        # panels A and C
    TRAINED = T["meta"]["trained_step"]  # panel D, the window the funnel is built at

    REC: dict = {
        "figure": "fig2_unreachable_difference",
        "question": (
            "grim trigger and tit-for-tat are behaviourally identical until the "
            "model defects with rounds still to play. Where in the game does the "
            "policy defect, and how often does it walk the defect -> punished -> "
            "return -> forgiven path that is the only place the two opponents "
            "differ?"
        ),
        "answer": None,
        "windows": {
            "_what": (
                "The train panels do NOT share a window. Every bound here is read "
                "from train_strategy.json['meta']; none is written as a literal."
            ),
            "A_hazard_by_round_index_train": "steps >= %d (late window)" % LATE,
            "B_hazard_by_rounds_from_end_eval":
                "frozen step-35 adapters replayed at N = 6, 10, 14",
            "C_exposure": "steps >= %d (late window)" % LATE,
            "D_repair_funnel": "steps >= %d (every trained step)" % TRAINED,
            "why_panel_D_is_wider": (
                "The cache builds the repair funnel over steps >= %d and at no "
                "other floor, so that is the window panel D reports. It is also "
                "the conservative denominator for a 'this path is almost never "
                "walked' claim: narrowing to steps >= %d would roughly halve the "
                "number of episodes the claim has to survive. Panel D therefore "
                "keeps the wider window and states it, and carries the "
                "late-window counts as a secondary check."
                % (TRAINED, LATE)
            ),
        },
        "error_bar_definitions": {
            "all_panels": (
                "BETWEEN TRAINING SEED. Each training seed (checkpoint lineage) is "
                "collapsed to one number over its episodes first, then the spread "
                "is taken across seeds: sample sd (ddof=1) / sqrt(n_seeds)."
            ),
            "null_policy": (
                "n_seeds < 2 carries se = null and draws NO bar. A drawn bar of "
                "length 0.0 is a real between-seed spread of zero on >= 2 seeds, "
                "not a missing value."
            ),
            "train_window_panels_A_C": "training traces pooled over steps >= %d, "
                                       "env = ipd only" % LATE,
            "train_window_panel_D": "training traces pooled over steps >= %d, "
                                    "every trained step, env = ipd only" % TRAINED,
            "eval_window": "frozen step-35 adapters replayed at N = 6, 10, 14",
        },
        "provenance": {},
        "caveat": None,
        "panels": {},
    }

    for label, p in (("train_strategy", TRAIN), ("eval_strategy", EVAL)):
        st = p.stat()
        REC["provenance"][label] = {
            "path": str(p),
            "bytes": st.st_size,
            "mtime_utc": dt.datetime.fromtimestamp(
                st.st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    REC["provenance"]["train_cache_meta"] = {
        "late_step": LATE,
        "trained_step": TRAINED,
        "shape_env": T["meta"]["shape_env"],
        "trace_sampling_note": T["meta"]["trace_sampling_note"],
        "episodes_kept_ipd": T["meta"]["episodes_kept_ipd"],
        "invalid_rate_rule": T["meta"]["invalid_rate_rule"],
    }
    REC["provenance"]["eval_cache_meta"] = {
        "what": E["meta"]["_what"],
        "wave": E["meta"]["wave"],
        "error_bars": E["meta"]["error_bars"],
        "restriction": E["endgame_length"]["_restriction"],
        "diagonal_only": E["endgame_length"]["_diagonal_only"],
        "flagged_cell": E["endgame_length"]["_flagged_cell"],
        "nohole_is_base": "this file names the baseline arm `nohole`; the training "
                          "cache names it `base`",
    }

    # ======================================================================
    fig, axes = plt.subplots(2, 2, figsize=(18.4, 12.0))
    fig.patch.set_facecolor(PAPER)
    axA, axB = axes[0]
    axC, axD = axes[1]

    # ----------------------------------------------------------------------
    # PANEL A -- defection hazard by round index, training traces, base arm
    # ----------------------------------------------------------------------
    panelA: dict = {
        "what": "P(model defects in round r), training traces, base arm, "
                "steps >= %d (late window)" % LATE,
        "window": "steps >= %d" % LATE,
        "x": "round index, 1-based",
        "series": {},
    }
    n_rounds = None
    for opp, col, mk, ls, nice in OPP:
        h = T["hazard"][f"{opp}/base"]["by_round_index"]
        x = np.asarray(h["x"], float) + 1.0          # cache is 0-based
        y = np.asarray(h["mean"], float)
        se = h["se"]
        n_rounds = len(x)
        axA.plot(x, y, color=col, marker=mk, ls=ls, lw=2.2, ms=6.5,
                 mec=col, mfc=col if opp == "grim" else PAPER, mew=1.6, zorder=3)
        for xi, yi, si in zip(x, y, se):
            errbar(axA, xi, yi, si, col)
        panelA["series"][f"{opp}/base"] = {
            "round_index": x.tolist(), "hazard_mean": y.tolist(), "se": se,
            "n_episodes_per_point": h["n"], "per_seed": h["per_seed"],
            "n_seeds": len(h["per_seed"]),
        }

    last = int(n_rounds)
    axA.axvspan(0.4, last - 0.5, color=GRID, alpha=0.55, zorder=0.5, lw=0)
    axA.axvline(last - 0.5, color=MUT, lw=0.9, ls=(0, (2, 2)), zorder=0.6)

    axA.text((0.4 + last - 0.5) / 2.0, 1.045,
             "ROUNDS 1-%d  -  grim and tit-for-tat differ here" % (last - 1),
             fontsize=8.6, color=INK2, ha="center", va="bottom")
    axA.text(last, 1.045, "ROUND %d" % last, fontsize=8.6, color=INK,
             ha="center", va="bottom")
    axA.text(1.30, 1.000,
             "In the final round neither opponent has a round left in\n"
             "which to answer a defection, so grim and tit-for-tat are\n"
             "literally the same opponent there. Everything that makes\n"
             "them different lives LEFT of the dashed line.",
             fontsize=8.2, color=INK, ha="left", va="top", linespacing=1.5)

    # direct labels, dropped into the dead space rounds 1-7 leave behind
    lab_y = {"grim": 0.53, "tft": 0.35}
    for opp, col, mk, ls, nice in OPP:
        h = T["hazard"][f"{opp}/base"]["by_round_index"]
        y = np.asarray(h["mean"], float)
        yl = lab_y[opp]
        axA.plot([1.35, 2.35], [yl, yl], color=col, ls=ls, lw=2.2, zorder=3)
        axA.plot([1.85], [yl], color=col, marker=mk, ms=6.5, mec=col,
                 mfc=col if opp == "grim" else PAPER, mew=1.6, zorder=3)
        axA.text(2.6, yl, "%s  (base arm, n=%d episodes, 3 seeds)\n"
                          "round %d: %.3f      round %d: %.3f"
                 % (nice, h["n"][0], last - 1, y[-2], last, y[-1]),
                 fontsize=8.6, color=INK, va="center", linespacing=1.5)

    zero_upto = {}
    for opp, col, mk, ls, nice in OPP:
        y = np.asarray(T["hazard"][f"{opp}/base"]["by_round_index"]["mean"], float)
        nz = np.nonzero(y)[0]
        zero_upto[opp] = int(nz[0]) if len(nz) else len(y)   # 0-based first nonzero
    first_nz = min(zero_upto.values())
    axA.annotate("rounds 1-%d are EXACTLY 0.000 in every seed of both arms:\n"
                 "not a small number, no episode defects there at all" % first_nz,
                 xy=(first_nz / 2.0 + 0.5, 0.0), xycoords="data",
                 xytext=(1.30, 0.155), textcoords="data",
                 fontsize=8.2, color=RED, va="bottom",
                 arrowprops=dict(arrowstyle="-", color=RED, lw=0.9,
                                 shrinkA=2, shrinkB=2))
    panelA["rounds_exactly_zero_both_arms"] = list(range(1, first_nz + 1))

    for opp, col, mk, ls, nice in OPP:
        h = T["hazard"][f"{opp}/base"]["by_round_index"]
        y = np.asarray(h["mean"], float)
        se = h["se"]
        # The two spike tips and the two round-9 points sit inside each other's
        # error bars, so neither pair can be labelled by stacking upward.
        i = last - 2
        axA.text(i + 1 - (0.12 if opp == "grim" else 0.30),
                 y[i] + ((se[i] or 0.0) + 0.030 if opp == "grim" else 0.0),
                 "%.3f" % y[i], fontsize=8.4, color=col, ha="right",
                 va="center", zorder=6)
        j = last - 1
        axA.text(last + 0.22, y[j], "%.3f" % y[j], fontsize=8.4, color=col,
                 ha="left", va="center", zorder=6)

    axA.set_xlim(0.35, last + 1.30)
    axA.set_ylim(-0.035, 1.28)
    axA.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    axA.set_xticks(range(1, last + 1))
    style(axA, "A.  Training traces: when does the policy defect?",
          "P(model defects in this round)",
          "round index within the 10-round episode",
          note="ipd, base arm, LATE window: steps >= %d, pooled per seed then "
               "across 3 seeds" % LATE)
    REC["panels"]["A_hazard_by_round_index_train"] = panelA

    # ----------------------------------------------------------------------
    # PANEL B -- same hazard, frozen step-35 adapters at held-out lengths
    # ----------------------------------------------------------------------
    panelB: dict = {
        "what": "P(model defects | rounds_from_end = k), frozen step-35 adapters, "
                "pooled over N = 6, 10, 14 (lengths never trained on)",
        "window": "frozen step-35 adapters at N = 6, 10, 14",
        "x": "rounds from the end of the episode (0 = final round)",
        "block": "all_seeds",
        "series": {}, "sensitivity_excl_grim_nohole_s1": {},
        "lengths": E["endgame_length"]["all_seeds"]["by_arm"]["grim/nohole"]["num_rounds_present"],
    }
    kmax = 0
    for arm, col, mk, ls, lw, nice, al in EARMS:
        h = E["endgame_length"]["all_seeds"]["by_arm"][arm]["hazard_by_rounds_from_end_pooled"]
        ks = sorted(int(k) for k in h)
        kmax = max(kmax, ks[-1])
        y = np.array([h[str(k)]["mean"] for k in ks], float)
        se = [h[str(k)]["se"] for k in ks]
        axB.plot(ks, y, color=col, marker=mk, ls=ls, lw=lw,
                 ms=6.0 if al == 1.0 else 4.6,
                 alpha=al, mec=col, mfc=col if arm.startswith("grim") else PAPER,
                 mew=1.5, zorder=3)
        for ki, yi, si in zip(ks, y, se):
            errbar(axB, ki, yi, si, col)
        panelB["series"][arm] = {
            "rounds_from_end": ks, "hazard_mean": y.tolist(), "se": se,
            "n_decisions": [h[str(k)]["n_decisions"] for k in ks],
            "n_seeds": [h[str(k)]["n_seeds"] for k in ks],
            "per_seed_at_final_round": h["0"]["per_seed"],
            "frac_defect_before_last": E["endgame_length"]["all_seeds"]["by_arm"][arm]
                ["pooled_over_lengths"]["frac_defect_before_last"],
        }

    axB.axvspan(0.5, kmax + 0.6, color=GRID, alpha=0.55, zorder=0.5, lw=0)
    axB.axvline(0.5, color=MUT, lw=0.9, ls=(0, (2, 2)), zorder=0.6)
    axB.text(0.7, 1.045, "ROUNDS 1+ FROM THE END  -  the two opponents differ here",
             fontsize=8.6, color=INK2, ha="left", va="bottom")

    # direct labels: the whole right half of this panel is exactly zero
    ylad = 0.98
    for arm, col, mk, ls, lw, nice, al in EARMS:
        h = E["endgame_length"]["all_seeds"]["by_arm"][arm]["hazard_by_rounds_from_end_pooled"]
        axB.plot([3.4, 4.5], [ylad, ylad], color=col, ls=ls, lw=lw, alpha=al, zorder=3)
        axB.plot([3.95], [ylad], color=col, marker=mk, ms=6.0, alpha=al, mec=col,
                 mfc=col if arm.startswith("grim") else PAPER, mew=1.5, zorder=3)
        axB.text(4.8, ylad, "%s      final round %.3f      1 from end %.3f"
                 % (nice, h["0"]["mean"], h["1"]["mean"]),
                 fontsize=8.5, color=INK, va="center")
        ylad -= 0.105

    gs = E["endgame_length"]["excl_grim_nohole_s1"]["by_arm"]["grim/nohole"]
    gsh = gs["hazard_by_rounds_from_end_pooled"]
    panelB["sensitivity_excl_grim_nohole_s1"]["grim/nohole"] = {
        "hazard_final_round": gsh["0"], "hazard_1_from_end": gsh["1"],
        "n_episodes": gs["pooled_over_lengths"]["n_episodes"],
        "frac_defect_before_last": gs["pooled_over_lengths"]["frac_defect_before_last"],
    }
    axB.plot([0], [gsh["0"]["mean"]], marker="D", ms=7.5, mfc=PAPER, mec=GRIM,
             mew=1.8, zorder=5)
    errbar(axB, 0, gsh["0"]["mean"], gsh["0"]["se"], GRIM)
    axB.annotate("SENSITIVITY  grim/base with the compromised seed 1 dropped:\n"
                 "final-round hazard %.3f -> %.3f  (n=%d -> %d episodes, 3 -> %d seeds).\n"
                 "The spike does not depend on that checkpoint."
                 % (E["endgame_length"]["all_seeds"]["by_arm"]["grim/nohole"]
                     ["hazard_by_rounds_from_end_pooled"]["0"]["mean"],
                    gsh["0"]["mean"],
                    E["endgame_length"]["all_seeds"]["by_arm"]["grim/nohole"]
                     ["pooled_over_lengths"]["n_episodes"],
                    gs["pooled_over_lengths"]["n_episodes"],
                    gsh["0"]["n_seeds"]),
                 xy=(0.06, gsh["0"]["mean"]), xycoords="data",
                 xytext=(3.4, 0.315), textcoords="data",
                 fontsize=8.2, color=RED, va="center",
                 arrowprops=dict(arrowstyle="-", color=RED, lw=0.9,
                                 shrinkA=2, shrinkB=3))

    axB.text(3.4, 0.115,
             "Beyond 2 rounds from the end every arm is exactly 0.000, at every one\n"
             "of the three horizons. The spike tracks the END of the game, not the\n"
             "round number: N = 6, 10 and 14 were never trained on.",
             fontsize=8.2, color=INK2, va="center", linespacing=1.5)

    axB.set_xlim(-0.65, kmax + 0.6)
    axB.set_ylim(-0.035, 1.28)
    axB.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    axB.set_xticks(range(0, kmax + 1))
    style(axB, "B.  Frozen step-35 adapters at horizons never trained on",
          "P(model defects at this distance from the end)",
          "rounds from the end  (0 = final round)",
          note="pooled over N = 6, 10, 14; all_seeds block; base solid, "
               "endgame-penalty dotted")
    REC["panels"]["B_hazard_by_rounds_from_end_eval"] = panelB

    # ----------------------------------------------------------------------
    # PANEL C -- exposure to the only regime in which the opponents differ
    # ----------------------------------------------------------------------
    panelC: dict = {
        "what": "share of ipd rounds played in each regime, training traces, "
                "steps >= %d (late window)" % LATE,
        "window": "steps >= %d" % LATE,
        "statistics": {
            "rounds_in_punishment": "share of rounds played AFTER the opponent has "
                                    "defected at least once -- the only regime in "
                                    "which grim and tit-for-tat behave differently",
            "opp_defect_share": "1 - opp_coop_rate: share of rounds in which the "
                                "opponent defected at all",
        },
        "cells": {}, "cells_with_no_data": [],
    }
    rows, ylabels = [], []
    for cell, col in CELLS:
        pl = T["pooled_late"][cell]
        rip, oc = pl["rounds_in_punishment"], pl["opp_coop_rate"]
        rec = {
            "rounds_in_punishment": rip,
            "opp_coop_rate": oc,
            "opp_defect_share_mean": None if oc["mean"] is None else 1.0 - oc["mean"],
            "opp_defect_share_se": oc["se"],
            "defect_before_last": pl["defect_before_last"],
            "c_given_own_d": pl["c_given_own_d"],
            "copies_opp_last": pl["copies_opp_last"],
            "n_episodes": rip["n_episodes"], "n_seeds": rip["n_seeds"],
            # Recorded so the number here cannot be confused with the ALL-STEP one:
            # pooled_all includes step 0, the untrained policy, which defects mid
            # game and so does get punished. Exposure FALLS as training proceeds.
            "rounds_in_punishment_pooled_all_steps":
                T["pooled_all"][cell]["rounds_in_punishment"],
        }
        panelC["cells"][cell] = rec
        if rip["mean"] is None:
            panelC["cells_with_no_data"].append(cell)
            continue
        rows.append((cell, col, rec))
        ylabels.append(cell)

    yy = np.arange(len(rows))[::-1].astype(float)
    xmax = 0.0
    for (cell, col, rec) in rows:
        for st, key in ((rec["rounds_in_punishment"], "mean"),
                        (rec, "opp_defect_share_mean")):
            v = st[key]
            se = st["se"] if key == "mean" else rec["opp_defect_share_se"]
            xmax = max(xmax, (v or 0.0) + (se or 0.0))
            if key == "mean":
                for sv in st["per_seed"].values():
                    xmax = max(xmax, sv or 0.0)
    XPAD = xmax * 0.045

    for (cell, col, rec), y in zip(rows, yy):
        rip = rec["rounds_in_punishment"]
        v, ytop = rip["mean"], y + BH / 2 + 0.02
        axC.barh(ytop, v, height=BH, color=col, alpha=0.55,
                 edgecolor=col, lw=1.2, zorder=3)
        drew = errbar(axC, ytop, v, rip["se"], col, horizontal=True)
        for sv in rip["per_seed"].values():
            if sv is None:
                continue
            axC.plot([sv], [ytop], marker="o", ms=4.2, mfc=PAPER,
                     mec=INK2, mew=1.1, zorder=2)
        tip = max([v + (rip["se"] or 0.0)]
                  + [sv for sv in rip["per_seed"].values() if sv is not None])
        axC.text(tip + XPAD, ytop,
                 "rounds_in_punishment  %.4f%s"
                 % (v, "" if drew else "   (no SE: n_seeds=%d)" % rip["n_seeds"]),
                 fontsize=8.2, color=col, va="center", zorder=6)

        ov, ybot = rec["opp_defect_share_mean"], y - BH / 2 - 0.02
        axC.barh(ybot, ov, height=BH, color=col, alpha=0.22,
                 edgecolor=col, lw=1.1, hatch="////", zorder=3)
        drew2 = errbar(axC, ybot, ov, rec["opp_defect_share_se"], col,
                       horizontal=True)
        tip2 = ov + (rec["opp_defect_share_se"] or 0.0)
        axC.text(tip2 + XPAD, ybot,
                 "1 - opp_coop_rate      %.4f%s"
                 % (ov, "" if drew2 else "   (no SE: n_seeds=%d)"
                    % rec["opp_coop_rate"]["n_seeds"]),
                 fontsize=8.2, color=MUT, va="center", zorder=6)

    axC.set_yticks(yy)
    axC.set_yticklabels(["%s\n%d ep, %d seed%s"
                         % (c, r["n_episodes"], r["n_seeds"],
                            "" if r["n_seeds"] == 1 else "s")
                         for (c, _, r) in rows], fontsize=8.4, color=INK2,
                        linespacing=1.4)
    axC.set_ylim(-0.85, len(rows) - 0.25)
    axC.set_xlim(0.0, xmax * 1.68 + 0.0006)

    # legend for the two bar kinds, direct-labelled by fill rather than by hue
    h1 = axC.barh([-10], [0], height=BH, color=MUT, alpha=0.55, edgecolor=MUT,
                  lw=1.2, label="rounds_in_punishment  (solid)")
    h2 = axC.barh([-10], [0], height=BH, color=MUT, alpha=0.22, edgecolor=MUT,
                  lw=1.1, hatch="////", label="1 - opp_coop_rate  (hatched)")
    h3, = axC.plot([], [], marker="o", ls="none", ms=4.2, mfc=PAPER, mec=INK2,
                   mew=1.1, label="one training seed")
    axC.legend(handles=[h1, h2, h3], loc="lower right", frameon=False,
               fontsize=8.5, labelcolor=INK2, borderaxespad=0.6)

    biggest = max(
        [(r["rounds_in_punishment"]["mean"], c, "rounds_in_punishment")
         for c, _, r in rows]
        + [(r["opp_defect_share_mean"], c, "1 - opp_coop_rate")
           for c, _, r in rows])
    panelC["largest_value_on_panel"] = {
        "value": biggest[0], "cell": biggest[1], "statistic": biggest[2]}
    biggest_rip = max((r["rounds_in_punishment"]["mean"], c) for c, _, r in rows)
    panelC["largest_rounds_in_punishment"] = {"value": biggest_rip[0],
                                              "cell": biggest_rip[1]}
    max_oppd = max(r["opp_defect_share_mean"] for _, _, r in rows)
    all_step = T["pooled_all"][biggest_rip[1]]["rounds_in_punishment"]["mean"]
    panelC["largest_rounds_in_punishment"]["same_cell_pooled_all_steps"] = all_step
    axC.text(0.40, 0.600,
             "The largest rounds_in_punishment anywhere on this panel is %.4f, in %s,\n"
             "and it is 0.0000 in every other cell. Taking that largest value at face\n"
             "value, the policy spends %.2f%% of its rounds in the ONLY regime in which\n"
             "grim and tit-for-tat behave differently. The opponent defects at all in\n"
             "at most %.2f%% of rounds (%s).\n"
             "Over ALL steps, step 0 included, the same cell reads %.4f: the untrained\n"
             "policy did defect mid-game and get punished. Exposure FALLS with training."
             % (biggest_rip[0], biggest_rip[1], 100.0 * biggest_rip[0],
                100.0 * max_oppd,
                max((r["opp_defect_share_mean"], c) for c, _, r in rows)[1],
                all_step),
             transform=axC.transAxes, fontsize=8.3, color=RED, va="top",
             linespacing=1.55, zorder=6)
    if panelC["cells_with_no_data"]:
        axC.text(0.40, 0.235,
                 "No row for %s: 0 ipd trace episodes at steps >= %d."
                 % (", ".join(panelC["cells_with_no_data"]), LATE),
                 transform=axC.transAxes, fontsize=8.2, color=MUT, va="top")

    hbar_style(axC,
               "C.  Exposure: how much of the game is played in the punished regime?",
               None, "share of rounds",
               note="training traces, ipd, LATE window: steps >= %d" % LATE)
    REC["panels"]["C_exposure"] = panelC

    # ----------------------------------------------------------------------
    # PANEL D -- the repair funnel
    #
    # NOT the same window as A and C. The cache builds `funnel` over steps >=
    # meta["trained_step"], so that is what this panel shows and says.
    # ----------------------------------------------------------------------
    panelD: dict = {
        "what": "the repair path -- the only sequence of events that can tell grim "
                "apart from tit-for-tat -- counted in training traces over EVERY "
                "trained step, steps >= %d. This is a WIDER window than panels A "
                "and C (steps >= %d): the cache builds the funnel at this floor "
                "only, and it is the conservative denominator for the claim that "
                "the path is almost never walked." % (TRAINED, LATE),
        "window": "steps >= %d (every trained step)" % TRAINED,
        "window_is_not_the_late_window": (
            "Panels A and C use steps >= %d. Panel D uses steps >= %d. The counts "
            "here are NOT late-window counts and the headline denominator is a "
            "steps >= %d figure." % (LATE, TRAINED, TRAINED)
        ),
        "stage_denominators": {
            "all": "episodes in the cell; the rate is trivially 1.0 by definition "
                   "and is recorded as 1.0 in every cell",
            "f_defect_before_last": "all episodes",
            "f_opp_retaliated": "episodes that defected before the final round",
            "f_model_returned": "episodes in which the opponent retaliated",
            "f_opp_forgave": "episodes in which the model returned to cooperating "
                             "-- STRUCTURALLY IMPOSSIBLE under grim by definition "
                             "of the opponent, so a zero there is the opponent's "
                             "definition, not a fact about the policy",
        },
        "cells": {},
    }
    yst = np.arange(len(STAGES))[::-1].astype(float)
    ALLCELLS = [x[0] for x in FCELLS] + [x[0] for x in ECELLS]
    dens = {c: T["funnel"][c]["f_defect_before_last"]["den"] for c in ALLCELLS}
    xtop = max(dens[c] for c, _, _, _ in FCELLS)

    for ci, (cell, col, nice, al) in enumerate(FCELLS):
        f = T["funnel"][cell]
        cr: dict = {"n_episodes_all": dens[cell],
                    "window": "steps >= %d" % TRAINED, "stages": {}}
        for si, (key, _) in enumerate(STAGES):
            y = yst[si] + SLOT[ci]
            rs = all_stage(dens[cell]) if key == "all" else funnel_stage(f, cell, key)
            cr["stages"][key] = rs
            num, den, rate = rs["num"], rs["den"], rs["pooled_rate"]
            se, nseeds = rs["se"], rs["n_seeds"]
            if rs["structurally_impossible"]:
                axD.barh(y, xtop * 0.155, height=BH2, color=PAPER, alpha=1.0,
                         edgecolor=MUT, lw=1.0, hatch="xxx", zorder=3)
                axD.text(xtop * 0.17, y,
                         "n/a BY CONSTRUCTION - grim never forgives",
                         fontsize=8.2, color=MUT, va="center", ha="left", zorder=6)
                continue
            axD.barh(y, num, height=BH2, color=col, alpha=al, edgecolor=col,
                     lw=1.1, zorder=3)
            if key == "all":
                txt = "%s  -  %d episodes, %d seeds" % (
                    nice, num, f["f_defect_before_last"]["n_seeds"])
            elif den == 0:
                txt = "0 / 0   path never reached, no rate defined"
            else:
                txt = "%d / %d  =  %.3f" % (num, den, rate)
                if se is None:
                    txt += "   (no SE: n_seeds=%d)" % (nseeds or 0)
            axD.text(num + xtop * 0.014, y, txt, fontsize=8.2,
                     color=col if num else MUT, va="center", zorder=6)
        panelD["cells"][cell] = cr

    for cell, col, nice in ECELLS:
        f = T["funnel"][cell]
        cr = {"n_episodes_all": dens[cell], "window": "steps >= %d" % TRAINED,
              "stages": {"all": all_stage(dens[cell])}}
        for key, _ in STAGES[1:]:
            cr["stages"][key] = funnel_stage(f, cell, key)
        panelD["cells"][cell] = cr

    # One text column for the whole right-hand side of the panel. It starts left
    # of the old margin because only stage 1's bar reaches that far; stages 2-4
    # label out to ~0.20, so 0.232 is the leftmost edge that stays clear of them
    # and it buys the width the per-panel window labels need.
    TX, TX2 = 0.232, 0.312

    axD.text(TX, 0.330,
             "THE ENDGAME-PENALTY ARM RUNS THE SAME FUNNEL (counts only, no bars):",
             transform=axD.transAxes, fontsize=8.2, color=INK2, va="top", zorder=6)
    for i, (cell, col, nice) in enumerate(ECELLS):
        axD.text(TX, 0.282 - 0.048 * i, cell, transform=axD.transAxes,
                 fontsize=8.2, color=col, va="top", zorder=6)
        axD.text(TX2, 0.282 - 0.048 * i, eg_line(T, dens, cell),
                 transform=axD.transAxes, fontsize=8.2, color=col, va="top",
                 zorder=6)

    axD.set_yticks(yst)
    axD.set_yticklabels(["%d.  %s" % (i + 1, lab)
                         for i, (_, lab) in enumerate(STAGES)],
                        fontsize=8.8, color=INK2)
    axD.set_ylim(-0.60, len(STAGES))
    axD.set_xlim(0.0, xtop * 1.98)

    fb = T["funnel"]["tft/base"]["f_opp_forgave"]
    fb_seed = [s for s, v in fb["per_seed"].items() if v["den"]]
    n_ep_funnel = int(sum(dens.values()))

    # Secondary check: the same four cells restricted to the LATE window. Only
    # stage 2 is recoverable there (see late_funnel_entry), but the late window
    # is a subset of this panel's window, so the completion count it reports is
    # an upper bound on the late-window one -- the claim holds in both windows.
    late_entry = {c: late_funnel_entry(T, c) for c in ALLCELLS}
    n_ep_late = sum(v[0] for v in late_entry.values())
    n_dbl_late = sum(v[1] for v in late_entry.values())
    panelD["late_window_check"] = {
        "_what": (
            "the same four cells restricted to steps >= %d, the window panels A "
            "and C use. The cache builds the funnel only at steps >= %d, so "
            "stages 3-5 are not available here; stage 2 is a plain per-episode "
            "boolean and is recovered exactly from pooled_late."
            % (LATE, TRAINED)
        ),
        "window": "steps >= %d" % LATE,
        "per_cell": {c: {"n_episodes": late_entry[c][0],
                         "f_defect_before_last_num": late_entry[c][1]}
                     for c in ALLCELLS},
        "n_episodes_all_four_cells": n_ep_late,
        "f_defect_before_last_num_all_four_cells": n_dbl_late,
        "completions_upper_bound": fb["den"],
        "why_an_upper_bound": (
            "steps >= %d is a subset of steps >= %d, so the late-window "
            "completion count cannot exceed the %d completion(s) the panel "
            "draws. The claim therefore holds in both windows."
            % (LATE, TRAINED, fb["den"])
        ),
    }
    panelD["the_whole_signal"] = {
        "cell": "tft/base", "train_seed": fb_seed,
        "window": "steps >= %d" % TRAINED,
        "f_opp_forgave": fb,
        "episodes_that_completed_the_repair_path": fb["den"],
        "episodes_across_all_four_base_and_eg_cells": n_ep_funnel,
    }

    axD.text(TX, 0.742,
             "Read the counts, not the bars. Across %d ipd episodes at ALL TRAINED "
             "STEPS (steps >= %d) in\n"
             "these four cells the repair path completes %d time -- tft/base seed %s, "
             "one episode. That\n"
             "single episode is the ENTIRE training signal separating grim from "
             "tit-for-tat."
             % (n_ep_funnel, TRAINED, fb["den"], ", ".join(fb_seed) or "-"),
             transform=axD.transAxes, fontsize=8.3, color=RED, va="top",
             linespacing=1.45, zorder=6)
    axD.text(TX, 0.548,
             "BOTH WINDOWS.  Late window (steps >= %d): %d ep, %d mid-game "
             "defections, at most %d completion."
             % (LATE, n_ep_late, n_dbl_late, fb["den"]),
             transform=axD.transAxes, fontsize=7.7, color=INK2, va="top", zorder=6)
    axD.text(TX, 0.470,
             "Stage 4 is where it dies. Having been punished, the model returns to "
             "cooperating in %d of %d\n"
             "grim/base and %d of %d tft/base episodes: it defected in the final "
             "round, so no round was left."
             % (T["funnel"]["grim/base"]["f_model_returned"]["num"],
                T["funnel"]["grim/base"]["f_model_returned"]["den"],
                T["funnel"]["tft/base"]["f_model_returned"]["num"],
                T["funnel"]["tft/base"]["f_model_returned"]["den"]),
             transform=axD.transAxes, fontsize=8.3, color=INK2, va="top",
             linespacing=1.45, zorder=6)

    hbar_style(axD,
               "D.  The repair funnel: the only path that can distinguish the two opponents",
               None, "episodes (count, not rate)",
               note="training traces, ipd, ALL TRAINED STEPS: steps >= %d -- a "
                    "WIDER window than A and C (steps >= %d); rates are pooled "
                    "num/den" % (TRAINED, LATE))
    REC["panels"]["D_repair_funnel"] = panelD

    # ----------------------------------------------------------------------
    # header
    # ----------------------------------------------------------------------
    n_ep_train = int(sum(v["rounds_in_punishment"]["n_episodes"]
                         for v in panelC["cells"].values()))
    n_ep_eval = E["endgame_length"]["all_seeds"]["n_episodes"]
    REC["answer"] = (
        "Essentially never. Defection is confined to the last one or two rounds: "
        "rounds 1-%d of the 10-round training episodes carry a hazard of exactly "
        "0.000 in every seed of both arms, and the same spike sits at the true end "
        "of the game for frozen step-35 adapters replayed at N = 6, 10, 14. The "
        "opponent therefore defects in under %.1f%% of rounds, and the share of "
        "rounds played after an opponent defection peaks at %.4f (%s); both of "
        "those are late-window numbers, steps >= %d. The repair path that alone "
        "separates grim from tit-for-tat -- defect early, be punished, return to "
        "cooperating, see whether the opponent forgives -- completes %d time in "
        "%d ipd episodes taken over EVERY TRAINED STEP, steps >= %d, which is a "
        "wider window than the other train panels and the larger denominator for "
        "the claim. Restricted to the late window the same cells hold %d episodes "
        "and can contain at most the same %d completion. That is the mechanistic "
        "explanation for the crossplay null: the training signal distinguishing "
        "grim from tit-for-tat was almost never delivered."
        % (first_nz,
           100.0 * max(r["opp_defect_share_mean"] for _, _, r in rows) + 0.05,
           biggest_rip[0], biggest_rip[1], LATE, fb["den"], n_ep_funnel,
           TRAINED, n_ep_late, fb["den"]))
    REC["caveat"] = (
        "1) grim/nohole train_seed 1 in the eval cache emits an empty decision "
        "answer on %.0f%% of turns (%d empty answers over %d turns) while its "
        "invalid_rate reads 0.000, so the repo's gate is blind to it. Panel B "
        "therefore shows the all_seeds series AND the excl_grim_nohole_s1 "
        "final-round point; the endgame spike survives the exclusion (%.3f -> "
        "%.3f). 2) The whole f_opp_forgave cell rests on ONE episode, in tft/base "
        "train_seed %s. It carries se = null and no error bar, and it must not be "
        "read as a rate. 3) grim/base's f_opp_forgave is n/a by construction, not "
        "a measured null: grim never forgives by definition of the opponent. "
        "4) Training-trace numbers come from the first 24 episodes of every 5th "
        "step and are a sample of training, not the dense training log; they share "
        "no denominator with the eval panel and are never divided by it. "
        "5) THE TRAIN PANELS DO NOT SHARE A WINDOW. A and C are steps >= %d; D is "
        "steps >= %d, because that is the only floor at which the cache builds the "
        "repair funnel. Counts from the two windows are never divided by one "
        "another, and panel D reports the late-window denominator alongside its own."
        % (100.0 * E["endgame_length"]["all_seeds"]["empty_answer_by_arm_seed"]
            ["grim/nohole|s1"]["per_turn"],
           E["endgame_length"]["all_seeds"]["empty_answer_by_arm_seed"]
            ["grim/nohole|s1"]["n_empty_answer"],
           E["endgame_length"]["all_seeds"]["empty_answer_by_arm_seed"]
            ["grim/nohole|s1"]["n_turns"],
           E["endgame_length"]["all_seeds"]["by_arm"]["grim/nohole"]
            ["hazard_by_rounds_from_end_pooled"]["0"]["mean"],
           gsh["0"]["mean"], ", ".join(fb_seed) or "-", LATE, TRAINED))

    fig.suptitle("The policy never enters the part of the game where grim trigger "
                 "and tit-for-tat differ",
                 fontsize=14.5, color=INK, x=0.006, ha="left", y=0.985)
    fig.text(0.006, 0.960,
             "The two are the same opponent until the model defects with rounds "
             "still to play. Defection is confined to the last one or two rounds "
             "(A), and sits at the true end of the game even at three horizons",
             fontsize=8.8, color=INK2, ha="left")
    fig.text(0.006, 0.945,
             "never trained on (B). So the share of rounds spent in the punished "
             "regime peaks at %.4f at steps >= %d (C), and the repair path that "
             "alone separates grim from tit-for-tat completes %d time in %d "
             "episodes taken over all trained steps, steps >= %d (D)."
             % (biggest_rip[0], LATE, fb["den"], n_ep_funnel, TRAINED),
             fontsize=8.8, color=INK2, ha="left")
    fig.text(0.006, 0.926,
             "DENOMINATORS, AND THEY ARE NOT ONE WINDOW.  A, C: ipd training "
             "traces, LATE window, steps >= %d, %d episodes (per-cell counts on "
             "C's own axis).  D: the same traces over EVERY TRAINED STEP, steps "
             ">= %d, %d episodes"
             % (LATE, n_ep_train, TRAINED, n_ep_funnel),
             fontsize=8.8, color=INK2, ha="left")
    fig.text(0.006, 0.911,
             "-- the window the cache builds the funnel at, and the larger "
             "denominator; the same four cells hold %d episodes in the late "
             "window.  B: frozen step-35 adapters at N = 6, 10, 14, %d episodes.  "
             "Error bars BETWEEN TRAINING SEED, sd(ddof=1)/sqrt(n); n < 2 draws "
             "NO bar." % (n_ep_late, n_ep_eval),
             fontsize=8.8, color=INK2, ha="left")
    fig.text(0.006, 0.893,
             "CAVEAT.  grim/nohole train_seed 1 emits empty decision answers on "
             "%.0f%% of turns while invalid_rate reads 0.000 -- panel B shows the "
             "sensitivity to dropping it.  The entire f_opp_forgave cell rests on "
             "ONE episode (tft/base seed %s); grim's is n/a by construction, not a "
             "measured zero."
             % (100.0 * E["endgame_length"]["all_seeds"]["empty_answer_by_arm_seed"]
                 ["grim/nohole|s1"]["per_turn"], ", ".join(fb_seed) or "-"),
             fontsize=8.8, color=RED, ha="left")

    fig.tight_layout(rect=[0.004, 0.004, 0.998, 0.885])
    fig.subplots_adjust(hspace=0.32, wspace=0.215)

    args.outdir.mkdir(parents=True, exist_ok=True)
    png = args.outdir / f"{args.stem}.png"
    fig.savefig(png, dpi=args.dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"[fig] wrote {png}")

    js = args.outdir / f"{args.stem}.json"
    js.write_text(json.dumps(REC, indent=1))
    print(f"[fig] wrote {js}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
