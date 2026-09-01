#!/usr/bin/env python
"""Does the hidden endgame penalty suppress endgame REASONING, or only the act?

    /home/allie/venvs/tools/bin/python plot_endgame_reasoning.py

  fig1_reasoning_vs_behaviour.png   the dissociation, over training
  fig2_dissociation.png             relative change from matched control
  fig3_which_knob.png               eg vs inf: which manipulation moves the thought
  endgame_reasoning.json            every number in the three figures

THE QUESTION. `0830-endgame-summary.md` establishes on 3 seeds that the hidden
endgame penalty suppresses late betrayal against both punishers. That is a claim
about the ACT. This asks the other half: does the reasoning that precedes the act
move with it?

WHERE THE REASONING COMES FROM, AND WHY IT IS NOT THE SAME RUNS AS THE 3 SEEDS.
`train_mixed.py` splits `<think>` off the sample before the env parses the
action, so the dumped training traces at `/shared/allie/think4/runs/*/traces/`
carry NO reasoning -- verified, zero occurrences of the string "think>". The only
scored reasoning for this wave is the committed
`results/0826_think_curves/reasoning_markers.json`, written when the
`traces-think-t4-*` viewer pages still existed. Those pages were re-sampled from
the frozen checkpoints of the ORIGINAL Tinker runs, which the 0830 wave has since
replaced with local B300 re-runs. The pages are gone from this box, so the
markers cannot be rescored and no verbatim excerpt can be quoted here.

That file is n=1 SEED. §1 of the 0830 summary is the record of what a one-seed
endgame claim in this wave is worth: the sign flip it reported did not survive
two more seeds. Every reasoning number below carries that same exposure and the
figures say so on their face. The one thing that can be done about it is done --
`results/0825_shape_curves/reasoning_markers_grim.json` is an INDEPENDENT wave
(think3, shape-split, 4-env games-only roster, 115 blocks/point) that scored the
same three arms against grim with the same regexes, and it is plotted beside the
think4 estimate as a replication rather than pooled into it.

DENOMINATORS DIFFER AND ARE NOT RECONCILED. Reasoning rates are shares of
re-sampled reasoning blocks over the five envs that HAVE an endgame; endgame_rate
is the dense training log over all seven trained envs. A ratio of the two would
be meaningless, so nothing here divides one by the other: each series is compared
only to its OWN matched control, and the comparison plotted is the relative change
from that control, which is the one quantity the differing denominators do not
corrupt.

PALETTE. The study's fixed identity trio, unchanged: #7a5bd6 base / #eb6834
endgame-penalty / #2a78d6 hidden-horizon, never repainted, always direct-labelled.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
T4_MARKERS = ROOT / "results/0826_think_curves/reasoning_markers.json"
T3_MARKERS = ROOT / "results/0825_shape_curves/reasoning_markers_grim.json"
RUNS = Path("/shared/allie/think4/runs")

PURPLE, ORANGE, BLUE = "#7a5bd6", "#eb6834", "#2a78d6"
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
PAPER = "#f9f9f7"
RED = "#b5342a"

M4 = json.loads(T4_MARKERS.read_text())
M3 = json.loads(T3_MARKERS.read_text())

# grim/inf degenerated into incoherent text between steps ~51 and 77
# (HANDOFF-think4 §3: invalid_rate 0.023 -> 0.819, outputs got SHORTER).
# Markers scored past 50 there describe a broken policy, not a trained one.
COLLAPSE_CAP = {"grim/inf": 50}

OPPS = [("grim", "vs GRIM — never forgives"),
        ("tft", "vs TIT-FOR-TAT — forgives on return")]


# --------------------------------------------------------------------------
# readers
# --------------------------------------------------------------------------

def marker(cell: str, key: str, cap: int | None = None):
    """step -> rate, from the committed think4 marker file."""
    d = M4[cell][key]
    st = sorted(int(k) for k in d)
    if cap is not None:
        st = [s for s in st if s <= cap]
    return np.array(st), np.array([d[str(s)] for s in st], float)


def nblocks(cell: str, cap: int | None = None):
    return marker(cell, "n_blocks", cap)


def paired(opp: str, arm: str, key: str, ref: str = "nohole"):
    """(steps, base, arm) on the steps BOTH cells have. Pairing on the step is
    not cosmetic: the arms stopped at different steps and the markers drift
    upward with training, so an unpaired mean compares different step ranges."""
    cap_a = COLLAPSE_CAP.get(f"{opp}/{arm}")
    sb, vb = marker(f"{opp}/{ref}", key)
    sa, va = marker(f"{opp}/{arm}", key, cap_a)
    shared = sorted(set(sb.tolist()) & set(sa.tolist()))
    ib = [sb.tolist().index(s) for s in shared]
    ia = [sa.tolist().index(s) for s in shared]
    return np.array(shared), vb[ib], va[ia]


def pooled_delta(opp: str, arm: str, key: str):
    """Pooled rates + the two error bars that exist, and the one that does not.

    binom_se  treats every reasoning block as an independent draw. It bounds
              "would another 1536 blocks from THIS run look different", nothing
              wider.
    ckpt_se   is the spread of the paired per-checkpoint delta. It bounds
              step-to-step wobble WITHIN the run and the checkpoints are
              autocorrelated, so it is not a test of the knob either.
    A between-seed bar -- the only one that would license a causal claim -- is
    unavailable: the marker file is one seed. This is exactly the distinction
    §1 of the 0830 summary was written to enforce.
    """
    steps, b, a = paired(opp, arm, key)
    cap_a = COLLAPSE_CAP.get(f"{opp}/{arm}")
    snb, nb = nblocks(f"{opp}/nohole")
    sna, na = nblocks(f"{opp}/{arm}", cap_a)
    nbv = np.array([nb[snb.tolist().index(s)] for s in steps])
    nav = np.array([na[sna.tolist().index(s)] for s in steps])
    Nb, Na = nbv.sum(), nav.sum()
    pb, pa = (b * nbv).sum() / Nb, (a * nav).sum() / Na
    binom = float(np.sqrt(pb * (1 - pb) / Nb + pa * (1 - pa) / Na))
    d = a - b
    ckpt = float(d.std(ddof=1) / np.sqrt(len(d))) if len(d) > 1 else float("nan")
    return dict(steps=steps.tolist(), base=float(pb), arm=float(pa),
                delta=float(pa - pb), binom_se=binom, ckpt_se=ckpt,
                n_base=int(Nb), n_arm=int(Na))


def behaviour_window(opp: str, arm: str, ref: str = "nohole") -> int:
    """The LAST step both cells have a marker checkpoint for.

    Both arms must be read over the SAME window or the behaviour comparison is
    not the pairing the reasoning comparison above it is. The arms stopped at
    different steps -- tft/eg reached 45 where tft/nohole stopped at 35 -- and
    endgame_rate drifts with training, so letting each arm run to its own last
    step silently compares 8-35 against 8-45 and moved the tft effect from
    -45% to -50% on nothing but a longer tail.
    """
    a = nblocks(f"{opp}/{arm}", COLLAPSE_CAP.get(f"{opp}/{arm}"))[0]
    b = nblocks(f"{opp}/{ref}", COLLAPSE_CAP.get(f"{opp}/{ref}"))[0]
    return int(min(a.max(), b.max()))


def behaviour_same_runs(opp: str, arm: str, hi: int | None = None):
    """endgame_rate from the SAME runs the markers were scored on, restricted to
    the marker step window so the two halves of the dissociation describe the
    same slice of training."""
    s, v = marker(f"{opp}/{arm}", "endgame_rate")
    if hi is None:
        hi = behaviour_window(opp, arm)
    m = (s >= 8) & (s <= hi)
    return s[m], v[m]


def load_metrics(run: str) -> dict[int, dict]:
    fp = RUNS / run / "metrics.jsonl"
    if not fp.exists():
        return {}
    out: dict[int, dict] = {}
    for line in fp.read_text().splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        if "step" in r:
            out[int(r["step"])] = r          # dedupe by step, last write wins
    return out


def behaviour_new_seeds(opp: str, sfx: str, key: str = "train/endgame_rate"):
    """Per-seed means over steps >= 8 from the CURRENT local runs. This is the
    3-seed behaviour the 0830 summary reports; it is a different instantiation
    of the same cells from the runs the markers came from."""
    per = []
    for s in range(4):
        rows = load_metrics(f"mixed_think4_nohole-think-{opp}_d1_s{s}{sfx}")
        xs = [k for k in sorted(rows) if k >= 8 and rows[k].get(key) is not None]
        if xs:
            per.append(float(np.mean([rows[k][key] for k in xs])))
    return per


# --------------------------------------------------------------------------
# chrome
# --------------------------------------------------------------------------

def style(ax, title, ylab, xlab="training step", note=None):
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


REC: dict = {}

# ==========================================================================
# FIGURE 1 — the dissociation, over training
# ==========================================================================
fig, axes = plt.subplots(2, 2, figsize=(13.4, 9.6))
fig.patch.set_facecolor(PAPER)

for ci, (opp, opp_title) in enumerate(OPPS):
    # --- top: the REASONING ---
    ax = axes[0][ci]
    for arm, lab, col in (("nohole", "baseline", PURPLE),
                          ("eg", "endgame penalty", ORANGE)):
        cap = COLLAPSE_CAP.get(f"{opp}/{arm}")
        s, v = marker(f"{opp}/{arm}", "endgame_defect_plan", cap)
        _, n = nblocks(f"{opp}/{arm}", cap)
        se = np.sqrt(v * (1 - v) / n)
        ax.fill_between(s, v - se, v + se, color=col, alpha=0.13, lw=0, zorder=2)
        ax.plot(s, v, color=col, lw=2.2, marker="o", ms=5, mec=SURF, mew=1.4,
                zorder=3, label=lab)
    st = pooled_delta(opp, "eg", "endgame_defect_plan")
    REC[f"{opp}/reasoning/endgame_defect_plan"] = st
    ax.set_ylim(0, 0.34)
    ax.set_xlim(-2, 48)
    style(ax, f"{opp_title}\nREASONING — plans to betray in the final round",
          "share of reasoning blocks", xlab=None,
          note="re-sampled from frozen checkpoints, 5 endgame envs,\n"
               "192 blocks/point.  band = binomial SE")
    ax.annotate(f"{st['base']:.3f} → {st['arm']:.3f}"
                f"   ({100*(st['arm']-st['base'])/st['base']:+.0f}%)",
                (0.985, 0.055), xycoords="axes fraction", ha="right",
                fontsize=10, color=INK, fontweight="bold")
    if ci == 0:
        ax.legend(frameon=False, fontsize=9, loc="lower left",
                  bbox_to_anchor=(0.015, 0.10), labelcolor=INK2)

    # --- bottom: the BEHAVIOUR, same runs, same step window ---
    ax = axes[1][ci]
    hi = behaviour_window(opp, "eg")
    for arm, lab, col in (("nohole", "baseline", PURPLE),
                          ("eg", "endgame penalty", ORANGE)):
        s, v = behaviour_same_runs(opp, arm, hi)
        ax.plot(s, v, color=col, lw=0.9, alpha=0.30, zorder=2)
        k = 7
        sm = np.array([v[max(0, i - k // 2):i + k // 2 + 1].mean()
                       for i in range(len(v))])
        ax.plot(s, sm, color=col, lw=2.2, zorder=3, label=lab)
    b = behaviour_same_runs(opp, "nohole", hi)[1].mean()
    e = behaviour_same_runs(opp, "eg", hi)[1].mean()
    REC[f"{opp}/behaviour/same_runs"] = dict(base=float(b), eg=float(e),
                                             rel=float(100 * (e - b) / b),
                                             step_window=[8, hi])
    ax.set_ylim(0, 0.46)
    ax.set_xlim(-2, 48)
    style(ax, "BEHAVIOUR — betrayals landing in the final window",
          "train/endgame_rate",
          note=f"dense training log, all 7 trained envs,\n"
               f"same runs, steps 8–{hi} — the window BOTH arms share")
    ax.annotate(f"{b:.3f} → {e:.3f}   ({100*(e-b)/b:+.0f}%)",
                (0.985, 0.055), xycoords="axes fraction", ha="right",
                fontsize=10, color=INK, fontweight="bold")

fig.suptitle("The hidden endgame penalty moves the ACT far more than the THOUGHT",
             fontsize=14.5, color=INK, x=0.006, ha="left", y=0.985)
fig.text(0.006, 0.952,
         "Read each column downward. Against tit-for-tat the penalty cuts "
         "endgame betrayal by 45% while the reasoning that plans it barely "
         "moves (−7%). Against grim the pattern inverts and both effects are "
         "small.",
         fontsize=8.8, color=INK2, ha="left")
fig.text(0.006, 0.936,
         "Whatever the penalty is doing, the stated plan is not tracking it.",
         fontsize=8.8, color=INK2, ha="left")
fig.text(0.006, 0.918,
         "ONE SEED — the marker file predates the 3-seed re-runs, and §1 of the "
         "0830 summary is the record of a one-seed endgame claim in this wave "
         "failing to replicate.",
         fontsize=8.8, color=RED, ha="left")
fig.tight_layout(rect=[0.004, 0.004, 0.998, 0.905])
fig.subplots_adjust(hspace=0.42)
out1 = HERE / "fig1_reasoning_vs_behaviour.png"
fig.savefig(out1, dpi=150, facecolor=fig.get_facecolor())
plt.close(fig)
print(f"[fig] wrote {out1}")


# ==========================================================================
# FIGURE 2 — relative change from matched control
# ==========================================================================
fig, axes = plt.subplots(1, 2, figsize=(14.2, 6.8), sharex=True)
fig.patch.set_facecolor(PAPER)

ROWS = [
    ("behaviour_3seed", "ENDGAME BETRAYAL RATE\n3 seeds, current runs", RED),
    ("behaviour_same", "ENDGAME BETRAYAL RATE\n1 seed, the marker runs", RED),
    ("gap", None, None),
    ("backward_induction", "reasoning: backward induction", INK2),
    ("endgame_defect_plan", "reasoning: plans to betray at the end", INK2),
    ("endgame_hold", "reasoning: plans to HOLD at the end", INK2),
]

for ci, (opp, opp_title) in enumerate(OPPS):
    ax = axes[ci]
    ys, labs, vals, errs, cols = [], [], [], [], []
    y = 0
    for kind, lab, _ in ROWS:
        if kind == "gap":
            y -= 0.55
            continue
        if kind == "behaviour_3seed":
            base = behaviour_new_seeds(opp, "")
            eg = behaviour_new_seeds(opp, "_eg2")
            mb, me = np.mean(base), np.mean(eg)
            rel = 100 * (me - mb) / mb
            sb = np.std(base, ddof=1) / np.sqrt(len(base))
            se_ = np.std(eg, ddof=1) / np.sqrt(len(eg))
            err = 100 * np.sqrt(se_ ** 2 + (me / mb) ** 2 * sb ** 2) / mb
            REC[f"{opp}/behaviour/3seed"] = dict(
                base=float(mb), eg=float(me), rel=float(rel), rel_se=float(err),
                n_seeds_base=len(base), n_seeds_eg=len(eg),
                per_seed_base=base, per_seed_eg=eg)
        elif kind == "behaviour_same":
            r = REC[f"{opp}/behaviour/same_runs"]
            rel, err = r["rel"], 0.0
        else:
            st = pooled_delta(opp, "eg", kind)
            REC.setdefault(f"{opp}/reasoning/{kind}", st)
            rel = 100 * st["delta"] / st["base"]
            err = 100 * st["binom_se"] / st["base"]
        ys.append(y)
        labs.append(lab)
        vals.append(rel)
        errs.append(err)
        cols.append(ORANGE if rel < 0 else "#8a8a8a")
        y -= 1

    ax.barh(ys, vals, height=0.62, color=cols, zorder=3, edgecolor="none")
    ax.errorbar(vals, ys, xerr=errs, fmt="none", ecolor=INK, elinewidth=1.4,
                capsize=4, capthick=1.4, zorder=4)
    ax.axvline(0, color=INK, lw=1.1, zorder=5)
    ax.set_yticks(ys)
    ax.set_yticklabels(labs, fontsize=8.8, color=INK2)
    ax.set_xlim(-72, 24)
    # Label past the END OF THE ERROR BAR, not the end of the bar: at the bar
    # tip the text sat on top of the whisker it is meant to be read against.
    for v, e, yy in zip(vals, errs, ys):
        tip = v - e if v < 0 else v + e
        ax.annotate(f"{v:+.0f}%", (tip, yy), xytext=(-7 if v < 0 else 7, 0),
                    textcoords="offset points", va="center",
                    ha="right" if v < 0 else "left", fontsize=9,
                    color=INK, fontweight="bold", zorder=6)
    ax.set_facecolor(SURF)
    ax.grid(True, axis="x", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=MUT, labelsize=8, length=0)
    ax.set_title(opp_title, fontsize=11.5, color=INK, loc="left", pad=10)
    ax.set_xlabel("change vs the matched baseline (%)", fontsize=9, color=INK2)

fig.suptitle("Endgame penalty: relative change from the matched control, "
             "behaviour vs reasoning",
             fontsize=14.5, color=INK, x=0.006, ha="left", y=0.978)
fig.text(0.006, 0.936,
         "Each bar is one series against its OWN baseline, so the differing "
         "denominators (reasoning = 5 envs re-sampled from checkpoints; "
         "behaviour = 7 envs, dense training log) never have to be reconciled.",
         fontsize=8.6, color=INK2, ha="left")
fig.text(0.006, 0.911,
         "Error bars are NOT the same kind. Only the top bar is between-SEED "
         "(n=3) — the one bar here that bounds the effect of the knob.",
         fontsize=8.6, color=RED, ha="left")
fig.text(0.006, 0.886,
         "The reasoning bars are binomial SE on 1536 blocks from ONE seed: "
         "they bound sampling noise and nothing wider. The second bar is one "
         "seed with no error bar available at all.",
         fontsize=8.6, color=RED, ha="left")
fig.tight_layout(rect=[0.004, 0.004, 0.998, 0.872])
out2 = HERE / "fig2_dissociation.png"
fig.savefig(out2, dpi=150, facecolor=fig.get_facecolor())
plt.close(fig)
print(f"[fig] wrote {out2}")


# ==========================================================================
# FIGURE 3 — which knob moves the thought
# ==========================================================================
fig, axes = plt.subplots(1, 3, figsize=(15.6, 6.0))
fig.patch.set_facecolor(PAPER)

# `notices_unknown` is deliberately NOT a bar here. It is exactly 0.000 in every
# finite arm, so "relative change from the matched control" is division by zero
# and an empty fourth column in all three panels was the honest but useless
# rendering of that. It is the manipulation CHECK rather than a suppression
# measure -- it asks whether the inf arm noticed the round count was gone -- so
# it is reported as the absolute rate it reaches, in the panel footer.
KEYS3 = [("backward_induction", "backward\ninduction"),
         ("endgame_defect_plan", "plans to betray\nat the end"),
         ("endgame_hold", "plans to hold\nat the end")]

# --- panels 1-2: think4, per opponent, eg and inf against the same baseline ---
for ci, (opp, opp_title) in enumerate(OPPS):
    ax = axes[ci]
    x = np.arange(len(KEYS3))
    w = 0.38
    for oi, (arm, lab, col) in enumerate((("eg", "endgame penalty", ORANGE),
                                          ("inf", "hidden horizon", BLUE))):
        vals, errs = [], []
        for k, _ in KEYS3:
            st = pooled_delta(opp, arm, k)
            REC.setdefault(f"{opp}/{arm}/{k}", st)
            vals.append(100 * st["delta"] / st["base"])
            errs.append(100 * st["binom_se"] / st["base"])
        ax.bar(x + (oi - 0.5) * w, vals, width=w, color=col, zorder=3,
               label=lab, edgecolor="none")
        ax.errorbar(x + (oi - 0.5) * w, vals, yerr=errs, fmt="none",
                    ecolor=INK, elinewidth=1.3, capsize=3.5, zorder=4)
        for xi, v in zip(x + (oi - 0.5) * w, vals):
            if np.isnan(v):
                continue
            ax.annotate(f"{v:+.0f}", (xi, v), xytext=(0, -13 if v < 0 else 5),
                        textcoords="offset points", ha="center",
                        fontsize=8.5, color=INK, fontweight="bold", zorder=6)
    ax.axhline(0, color=INK, lw=1.1, zorder=5)
    ax.set_xticks(x)
    ax.set_xticklabels([l for _, l in KEYS3], fontsize=8.4, color=INK2)
    ax.set_ylim(-88, 62)
    ax.set_facecolor(SURF)
    ax.grid(True, axis="y", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUT, labelsize=8, length=0)
    ax.set_title(f"think4 · {opp_title}", fontsize=10.5, color=INK,
                 loc="left", pad=8)
    ax.set_ylabel("change in reasoning vs baseline (%)", fontsize=9, color=INK2)
    nu = pooled_delta(opp, "inf", "notices_unknown")
    REC[f"{opp}/inf/notices_unknown"] = nu
    # Annotations live in the empty band ABOVE zero: every bar in this figure is
    # negative or nearly so, and at the bottom they collided with both the value
    # labels and the legend.
    ax.annotate('MANIPULATION CHECK  "says the horizon is unknown":\n'
                f'baseline {nu["base"]:.3f}  →  hidden horizon {nu["arm"]:.3f}',
                (0.025, 0.985), xycoords="axes fraction", fontsize=7.4,
                color=MUT, va="top")
    if ci == 0:
        ax.legend(frameon=False, fontsize=9, loc="lower left", labelcolor=INK2)

# --- panel 3: the independent think3 wave, vs grim ---
ax = axes[2]
x = np.arange(len(KEYS3))
w = 0.38


def t3(cell, key):
    d = M3[cell][key]
    s = sorted(d, key=int)
    return float(np.mean([d[k] for k in s]))


for oi, (arm, lab, col) in enumerate((("eg", "endgame penalty", ORANGE),
                                      ("inf", "hidden horizon", BLUE))):
    vals = []
    for k, _ in KEYS3:
        b, a = t3("nohole", k), t3(arm, k)
        vals.append(np.nan if b == 0 else 100 * (a - b) / b)
        REC.setdefault(f"think3-grim/{arm}/{k}", dict(base=b, arm=a))
    ax.bar(x + (oi - 0.5) * w, vals, width=w, color=col, zorder=3,
           label=lab, edgecolor="none")
    for xi, v in zip(x + (oi - 0.5) * w, vals):
        if np.isnan(v):
            continue
        ax.annotate(f"{v:+.0f}", (xi, v), xytext=(0, -13 if v < 0 else 5),
                    textcoords="offset points", ha="center", fontsize=8.5,
                    color=INK, fontweight="bold", zorder=6)
ax.axhline(0, color=INK, lw=1.1, zorder=5)
ax.set_xticks(x)
ax.set_xticklabels([l for _, l in KEYS3], fontsize=8.4, color=INK2)
ax.set_ylim(-88, 62)
ax.set_facecolor(SURF)
ax.grid(True, axis="y", color=GRID, lw=0.8, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color(GRID)
ax.tick_params(colors=MUT, labelsize=8, length=0)
ax.set_title("think3 · vs GRIM — INDEPENDENT WAVE", fontsize=10.5, color=INK,
             loc="left", pad=8)
ax.set_ylabel("change in reasoning vs baseline (%)", fontsize=9, color=INK2)
ax.annotate('MANIPULATION CHECK  "says the horizon is unknown":\n'
            f'baseline {t3("nohole", "notices_unknown"):.3f}  →  '
            f'hidden horizon {t3("inf", "notices_unknown"):.3f}\n'
            "\ndifferent runs, 4-env roster, 115 blocks/point, checkpoints\n"
            "0/10/20 only — so it cannot see the late window where\n"
            "think4's grim effect sits",
            (0.025, 0.985), xycoords="axes fraction", fontsize=7.4,
            color=MUT, va="top")

fig.suptitle("Which knob moves the reasoning? The one that changes what the "
             "policy SEES, not the one that changes what it is PAID",
             fontsize=14, color=INK, x=0.006, ha="left", y=0.982)
fig.text(0.006, 0.932,
         "The hidden horizon deletes the round count from the observation; the "
         "endgame penalty docks reward after the episode, through a channel the "
         "policy never observes. Only the first reliably moves the reasoning, "
         "and it does so in both waves.",
         fontsize=8.6, color=INK2, ha="left")
fig.text(0.006, 0.907,
         "grim/inf is capped at step 50: steps 51–77 are the documented "
         "collapse into incoherent text, where the markers describe a broken "
         "policy rather than a trained one.",
         fontsize=8.6, color=RED, ha="left")
fig.tight_layout(rect=[0.004, 0.004, 0.998, 0.893])
out3 = HERE / "fig3_which_knob.png"
fig.savefig(out3, dpi=150, facecolor=fig.get_facecolor())
plt.close(fig)
print(f"[fig] wrote {out3}")

(HERE / "endgame_reasoning.json").write_text(json.dumps(REC, indent=1))
print(f"[fig] wrote {HERE / 'endgame_reasoning.json'}")
