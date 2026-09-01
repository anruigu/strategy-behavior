#!/usr/bin/env python
"""    /home/allie/venvs/tinker-ipd/bin/python fig1_strategy_evolution.py

  fig1_strategy_evolution.png    how the learned IPD strategy evolves, grim vs tft
  fig1_strategy_evolution.json   every number drawn

THE QUESTION. An RL wave trained Qwen3.8-27B (LoRA) on 7 social-dilemma envs,
split by the scripted opponent used in the iterated prisoner's dilemma: `grim`
(defects forever after your first defection, never forgives) and `tft`
(mirrors your last move, forgives the moment you return to cooperating). Does
the strategy the policy learns evolve differently against the two?

THE BASELINE ARM ONLY. `grim/base` vs `tft/base` -- the pure opponent contrast
with no endgame knob applied. The `eg` and `inf` arms are other figures.

WHAT THE PANELS SHOW. Panels 1-6 come from `by_step`, derived from the per-episode
`ipd` action sequences dumped every 5th training step. Panels 7-8 come from
`metrics_curves`, the dense per-step training scalars from `metrics.jsonl`.
The two have DIFFERENT denominators (see `trace_sampling_note` in the cache):
traces are the first 24 episodes of the step covering 4 envs, so ipd contributes
~6 episodes per step per seed, whereas `train/*` pools all 7 trained envs.
Nothing here divides one by the other.

PANELS 3 AND 6 ARE LOAD-BEARING and are tinted for that reason. Everything else
on this page is a place where grim and tft lie on top of each other; those two
are where a difference could live at all -- `defect_before_last` is the one
behaviour the two opponents pull apart, and `rounds_in_punishment` is the
exposure to the difference, i.e. how much of an episode is actually spent in
the regime where "never forgives" and "forgives" mean different things.

WHAT `ever_defect == defects_last_round` DOES AND DOES NOT SAY. That equality
holds to 3 dp in every cell of the cache, and it is easy to over-read. It says
every episode that defects at all ALSO defects in the final round -- no episode
defects mid-game without defecting at the buzzer too. It does NOT say the buzzer
is the only round that ever sees a defection: `defect_before_last` is a nonzero
~0.11-0.12 in the baseline arms, and `n_defects - defects_last_round` recovers
that number exactly, so those episodes carry one EXTRA earlier defection on top
of the final-round one. Panel 3 is exactly that quantity. This page's claim is
that early defection is RARE, which is also what fig2 builds on; it is not that
early defection is absent, and nothing here should say otherwise.

PALETTE. Opponent identity is #00918f grim / #b8236f tft, and because those two
hues are only separated at the CVD floor, every series is ALSO direct-labelled
at its right-hand end and given a distinct marker and dash pattern. Identity
never rests on colour alone.
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

HERE = Path(__file__).resolve().parent
CACHE = HERE / "train_strategy.json"

PURPLE, ORANGE, BLUE = "#7a5bd6", "#eb6834", "#2a78d6"   # arm palette: base / eg / inf
GRIM, TFT = "#00918f", "#b8236f"                          # opponent palette
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
PAPER, RED = "#f9f9f7", "#b5342a"
TINT = "#f4f2ec"   # faint wash marking the two load-bearing panels

ARMS = [("grim/base", "grim", GRIM, "o", "-"),
        ("tft/base", "tft", TFT, "s", (0, (5, 2)))]


# --------------------------------------------------------------------------
# style
# --------------------------------------------------------------------------

def style(ax, title, ylab, xlab=None, note=None, hi=False):
    ax.set_title(title, fontsize=10.5, color=INK, loc="left", pad=8,
                 fontweight="semibold" if hi else "normal")
    ax.set_ylabel(ylab, fontsize=9, color=INK2)
    if xlab:
        ax.set_xlabel(xlab, fontsize=9, color=INK2)
    ax.set_facecolor(TINT if hi else SURF)
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


# --------------------------------------------------------------------------
# readers
# --------------------------------------------------------------------------

def arr(xs):
    """List with nulls -> float array with nan. Never interpolate across a gap."""
    return np.array([np.nan if v is None else float(v) for v in xs], dtype=float)


def series(block):
    """One {steps, per_seed, mean, se, ...} block -> plottable arrays."""
    st = np.asarray(block["steps"], dtype=float)
    mean, se = arr(block["mean"]), arr(block["se"])
    seeds = {k: arr(v) for k, v in sorted(block["per_seed"].items())}
    nse = np.asarray(block.get("n_seeds", []), dtype=float)
    nep = np.asarray(block["n_episodes"], dtype=float) if "n_episodes" in block else None
    return st, mean, se, seeds, nse, nep


def fmt(v, nd=3):
    return None if v is None or not np.isfinite(v) else round(float(v), nd)


# --------------------------------------------------------------------------
# drawing
# --------------------------------------------------------------------------

def draw(ax, blocks, title, ylab, xlab=None, note=None, hi=False, legend=False):
    """blocks: {cell -> block}. Returns the json record for this panel."""
    style(ax, title, ylab, xlab=xlab, note=note, hi=hi)
    rec, labels, xmax, lo_all, hi_all = {}, [], 0.0, [], []

    for cell, tag, col, mk, ls in ARMS:
        st, mean, se, seeds, nse, nep = series(blocks[cell])
        xmax = max(xmax, float(st[-1]))

        # per-seed traces underneath: the spread is real, not smoothed away
        for sv in seeds.values():
            ax.plot(st, sv, color=col, alpha=0.22, lw=1.0, zorder=2)
            lo_all.append(np.nanmin(sv) if np.any(np.isfinite(sv)) else np.nan)
            hi_all.append(np.nanmax(sv) if np.any(np.isfinite(sv)) else np.nan)

        # between-seed SE band; a null se draws NO band, never a zero-width one
        ok = np.isfinite(se) & np.isfinite(mean)
        if ok.any():
            band_lo = np.where(ok, mean - se, np.nan)
            band_hi = np.where(ok, mean + se, np.nan)
            ax.fill_between(st, band_lo, band_hi, where=ok, color=col,
                            alpha=0.13, lw=0, zorder=4)
            lo_all.append(np.nanmin(band_lo))
            hi_all.append(np.nanmax(band_hi))

        ax.plot(st, mean, color=col, lw=2.2, ls=ls, marker=mk, ms=5, mec=SURF,
                mew=1.4, zorder=3, label=tag)

        fin = np.flatnonzero(np.isfinite(mean))
        if fin.size:
            labels.append([float(st[fin[-1]]), float(mean[fin[-1]]), col, tag])

        rec[tag] = {
            "steps": [int(s) for s in st],
            "mean": [fmt(v) for v in mean],
            "se": [fmt(v) for v in se],
            "n_seeds": [None if not np.isfinite(v) else int(v) for v in nse],
            "per_seed": {k: [fmt(v) for v in sv] for k, sv in seeds.items()},
        }
        if nep is not None:
            rec[tag]["n_episodes"] = [None if not np.isfinite(v) else int(v) for v in nep]

    # ---- limits: leave room on the right for the direct labels
    finite_lo = [v for v in lo_all if np.isfinite(v)]
    finite_hi = [v for v in hi_all if np.isfinite(v)]
    ylo, yhi = (min(finite_lo), max(finite_hi)) if finite_lo else (0.0, 1.0)
    span = yhi - ylo
    if span <= 1e-9:                       # a structurally flat panel still needs air
        span = max(abs(yhi), 0.05)
        ylo, yhi = ylo - 0.5 * span, yhi + 0.5 * span
    else:
        ylo, yhi = ylo - 0.10 * span, yhi + 0.12 * span
    ax.set_ylim(ylo, yhi)
    ax.set_xlim(-0.035 * xmax, xmax * 1.215)

    # ---- direct labels in the clean right margin, past the LAST point of either
    # series (an arm that stopped early must not have its label land on the other
    # arm's curve), nudged apart if the two ys collide.
    yspan = yhi - ylo
    labels.sort(key=lambda r: r[1])
    gap = 0.085 * yspan
    if len(labels) == 2 and (labels[1][1] - labels[0][1]) < gap:
        mid = 0.5 * (labels[0][1] + labels[1][1])
        labels[0][1], labels[1][1] = mid - 0.5 * gap, mid + 0.5 * gap
    for _, ly, col, tag in labels:
        ly = min(max(ly, ylo + 0.03 * yspan), yhi - 0.03 * yspan)
        ax.text(xmax * 1.04, ly, tag, color=col, fontsize=8.5,
                fontweight="semibold", va="center", ha="left", zorder=6)

    if legend:
        ax.legend(frameon=False, fontsize=8.5, labelcolor=INK2, loc="lower left")
    return rec


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter, description=__doc__)
    ap.add_argument("--outdir", type=Path, default=HERE)
    ap.add_argument("--dpi", type=int, default=150, help="the repo renders figures at 150")
    ap.add_argument("--stem", default="fig1_strategy_evolution")
    args = ap.parse_args()

    D = json.loads(CACHE.read_text())
    meta, by_step, mcurves, pooled = D["meta"], D["by_step"], D["metrics_curves"], D["pooled_late"]

    # ---- the claim, recomputed from the cache -----------------------------
    late = meta["late_step"]
    claim = {}
    for cell, tag, *_ in ARMS:
        p = pooled[cell]
        claim[tag] = {k: {"mean": fmt(p[k]["mean"], 4), "se": fmt(p[k]["se"], 4),
                          "n_seeds": p[k]["n_seeds"], "n_episodes": p[k]["n_episodes"]}
                      for k in ("coop_rate", "opens_c", "ever_defect", "defects_last_round",
                                "defect_before_last", "first_defect_from_end",
                                "rounds_in_punishment", "n_rounds")}

    # every cell in the cache, not just the two plotted: does every episode that
    # defects at all also defect in the final round?
    same_cells = {}
    for cell, blk in by_step.items():
        a, b = blk["ever_defect"]["mean"], blk["defects_last_round"]["mean"]
        same_cells[cell] = all((x is None) == (y is None) and
                               (x is None or round(x, 3) == round(y, 3))
                               for x, y in zip(a, b))
    all_same = all(same_cells.values())

    # ---- and what that equality does NOT license --------------------------
    # It fixes the buzzer as a round every defecting episode hits; it says nothing
    # about the buzzer being the ONLY round hit. The arithmetic below is the check:
    # n_defects (count per episode) minus defects_last_round (at most one per
    # episode) must return defect_before_last (the indicator panel 3 plots). Where
    # it returns a nonzero, defection before the final round is happening.
    IDENT_TOL = 1e-9
    identity = {}
    for cell, blk in pooled.items():
        nd, dl = blk["n_defects"]["mean"], blk["defects_last_round"]["mean"]
        db = blk["defect_before_last"]["mean"]
        rec = {"n_defects": fmt(nd, 6), "defects_last_round": fmt(dl, 6),
               "n_defects_minus_defects_last_round": None,
               "defect_before_last": fmt(db, 6), "residual": None, "holds": None,
               "n_seeds": blk["n_defects"]["n_seeds"],
               "n_episodes": blk["n_defects"]["n_episodes"]}
        if None not in (nd, dl, db):
            resid = (nd - dl) - db
            rec["n_defects_minus_defects_last_round"] = fmt(nd - dl, 6)
            rec["residual"] = float(f"{resid:.3e}")
            rec["holds"] = bool(abs(resid) <= IDENT_TOL)
        identity[cell] = rec

    ident_live = {c: r for c, r in identity.items() if r["holds"] is not None}
    ident_empty = sorted(c for c, r in identity.items() if r["holds"] is None)
    identity_holds = bool(ident_live) and all(r["holds"] for r in ident_live.values())

    # cells where the over-reading ("all defection is final-round") is refuted outright
    pre_cells = sorted(c for c, r in ident_live.items() if r["defect_before_last"] > 0)

    # share of DEFECTING episodes that also carry an earlier defection
    pre_cond = {}
    for _, tag, *_ in ARMS:
        ev, db = claim[tag]["ever_defect"]["mean"], claim[tag]["defect_before_last"]["mean"]
        pre_cond[tag] = None if not ev else db / ev

    eps = {tag: int(sum(v for k, v in meta["episodes_kept_ipd"].items() if k.startswith(cell + "/")))
           for cell, tag, *_ in ARMS}
    nseeds = {tag: len(by_step[cell]["coop_rate"]["per_seed"]) for cell, tag, *_ in ARMS}

    # ---- the right-edge thinning, stated as it actually is ----------------
    edge = {}
    for cell, tag, *_ in ARMS:
        b = by_step[cell]["coop_rate"]
        st, ns = b["steps"], b["n_seeds"]
        full = max(ns)
        last_full = max(s for s, n in zip(st, ns) if n == full)
        thin = [(s, n) for s, n in zip(st, ns) if s > last_full]
        edge[tag] = {"steps": st, "n_seeds": ns, "full_n": full,
                     "last_step_at_full_n": last_full,
                     "thin_tail": thin,
                     "n_seeds_at_right_edge": [n for _, n in thin] or [full],
                     "last_step": st[-1]}

    def tail_txt(tag):
        e = edge[tag]
        if not e["thin_tail"]:
            return f"{tag} holds {e['full_n']} seeds to step {e['last_step']}"
        ns_tail = e["n_seeds_at_right_edge"]
        rng = (f"{max(ns_tail)}" if max(ns_tail) == min(ns_tail)
               else f"{max(ns_tail)} then {min(ns_tail)}")
        return (f"{tag} holds {e['full_n']} seeds only to step {e['last_step_at_full_n']}, "
                f"then n_seeds falls to {rng} over steps "
                f"{e['thin_tail'][0][0]}-{e['last_step']}")

    # ---- figure -----------------------------------------------------------
    fig, axes = plt.subplots(2, 4, figsize=(19.6, 10.6))
    fig.patch.set_facecolor(PAPER)

    PANELS = [
        ("by_step", "coop_rate", "coop_rate — cooperation, all rounds",
         "cooperation rate (all rounds)", "round-weighted; n per point in the json", False),
        ("by_step", "ever_defect", "ever_defect — any defection at all",
         "episodes with any defection", None, False),
        ("by_step", "defect_before_last", "defect_before_last — early defection",
         "episodes defecting before the final round",
         "the only behaviour grim and tft respond to differently", True),
        ("by_step", "first_defect_from_end", "first_defect_from_end — how late it falls",
         "first defection, rounds before the end", "conditional on defecting at all", False),
        ("by_step", "opp_coop_rate", "opp_coop_rate — the OPPONENT's reply",
         "OPPONENT cooperation rate", "this is the environment's response, not the policy", False),
        ("by_step", "rounds_in_punishment", "rounds_in_punishment — the exposure",
         "share of rounds spent after an opponent defection",
         "the exposure to the grim/tft difference", True),
        ("metrics", "train/endgame_rate", "train/endgame_rate — dense log, 7 envs",
         "train/endgame_rate (7 envs pooled)", "dense, every step", False),
        ("metrics", "env/ipd/exploit_rate", "env/ipd/exploit_rate — dense log, ipd",
         "env/ipd/exploit_rate", "dense, every step", False),
    ]

    panels = {}
    for i, (src, stat, title, ylab, note, hi) in enumerate(PANELS):
        ax = axes[i // 4][i % 4]
        table = by_step if src == "by_step" else mcurves
        blocks = {cell: table[cell][stat] for cell, *_ in ARMS}
        panels[f"{i + 1}. {stat}"] = {
            "source": "by_step (traces, every 5th step)" if src == "by_step"
                      else "metrics_curves (metrics.jsonl, every step)",
            "y_label": ylab,
            "load_bearing": hi,
            "series": draw(ax, blocks, f"{i + 1}   {title}", ylab,
                           xlab="training step" if i >= 4 else None,
                           note=note, hi=hi, legend=(i == 0)),
        }

    # ---- header, every number recomputed above ----------------------------
    g, t = claim["grim"], claim["tft"]
    gpre, tpre = g["defect_before_last"]["mean"], t["defect_before_last"]["mean"]
    fig.suptitle(
        f"Trained against grim or against tit-for-tat, the policy converges on the same strategy: "
        f"cooperate, defect at the buzzer, defect earlier in only {gpre:.0%} vs {tpre:.0%} of episodes "
        f"(coop {g['coop_rate']['mean']:.2f} vs {t['coop_rate']['mean']:.2f})",
        fontsize=14.5, color=INK, x=0.006, ha="left", y=0.985)

    same_txt = ("in EVERY cell of the cache ever_defect == defects_last_round to 3 dp, i.e. no episode defects "
                "mid-game without also defecting at the buzzer"
                if all_same else "ever_defect and defects_last_round diverge in some cells")
    ident_txt = (f"holds to {IDENT_TOL:.0e} in all {len(ident_live)} populated pooled_late cells"
                 if identity_holds else "FAILS in at least one pooled_late cell — see the json")

    HSZ = 8.8
    line_h = HSZ / 72.0 * 1.5 / fig.get_figheight()   # one wrapped line, in figure fraction

    def block(x, y, text, width, color):
        wrapped = textwrap.wrap(text, width)
        fig.text(x, y, "\n".join(wrapped), fontsize=HSZ, color=color, ha="left",
                 va="top", linespacing=1.5)
        return len(wrapped)

    y = 0.966
    n = block(0.006, y, (
        f"Read panels 3 and 6 first — they are tinted because they are the only place on this page where a grim/tft difference could live. "
        f"Panels 1, 2, 4, 5 are the agreement: both arms open C in {g['opens_c']['mean']:.0%} of episodes, run {g['n_rounds']['mean']:.0f} rounds, "
        f"and {same_txt}. Read that equality precisely — it pins the buzzer as a round every defecting episode hits, NOT as the only round any "
        f"episode hits. Panel 3 is the remainder: a further {gpre:.1%} of grim/base and {tpre:.1%} of tft/base episodes carry one extra defection "
        f"before the final round ({pre_cond['grim']:.0%} and {pre_cond['tft']:.0%} of the episodes that defect at all). The arithmetic behind that "
        f"panel, n_defects - defects_last_round = defect_before_last, {ident_txt}. Early defection here is rare, not absent."), 300, INK2)
    y -= n * line_h + 0.012

    n1 = block(0.006, y, (
        f"DENOMINATORS. Panels 1-6 are trace-derived: grim/base {eps['grim']} ipd episodes over {nseeds['grim']} training seeds, tft/base "
        f"{eps['tft']} over {nseeds['tft']}. Traces are dumped every 5th step and are the FIRST 24 episodes of that step across 4 envs, so ipd "
        f"contributes ~6 episodes per step per seed. Panels 7-8 are the dense metrics log (every step) pooling all 7 trained envs — a different "
        f"denominator, never divided into the trace numbers. Episodes with invalid_rate > {meta['invalid_rate_threshold']} are dropped."),
        148, INK2)
    n2 = block(0.506, y, (
        "ERROR BARS. Shaded band = +/-1 SE between TRAINING SEEDS, sd(ddof=1)/sqrt(n_seeds), n_seeds being the seeds alive at that step; a step "
        "with n<2 gets NO band rather than a zero-width one. The three faint lines under each curve are the individual seeds, so the spread you "
        "see is the raw spread. A gap in a line is a step where that seed logged no ipd episode; nothing is interpolated across it."),
        148, INK2)
    y -= max(n1, n2) * line_h + 0.012

    n = block(0.006, y, (
        f"CAVEAT. The runs stopped at different steps, so the rightmost points rest on fewer seeds and the late upturns are seed identity, not learning: "
        f"{tail_txt('grim')}; {tail_txt('tft')}. Headline numbers above are pooled over steps >= {late}, where both arms still have "
        f"{g['coop_rate']['n_seeds']} seeds."), 300, RED)
    y -= n * line_h + 0.010

    fig.tight_layout(rect=[0.004, 0.006, 0.998, y])
    fig.subplots_adjust(hspace=0.30, wspace=0.26)

    outdir = args.outdir
    outdir.mkdir(parents=True, exist_ok=True)
    png = outdir / f"{args.stem}.png"
    fig.savefig(png, dpi=args.dpi, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"[fig] wrote {png}")

    st = CACHE.stat()
    payload = {
        "figure": args.stem,
        "question": ("How does the learned IPD strategy evolve over training, and does it evolve "
                     "differently when the scripted opponent is grim trigger (never forgives) "
                     "versus tit-for-tat (forgives on return)? Baseline arm only: grim/base vs tft/base."),
        "answer": {
            "summary": (f"No. Both arms converge on the same strategy -- cooperate almost throughout, then "
                        f"defect in the final round. Late-training (steps >= {late}) cooperation is "
                        f"{g['coop_rate']['mean']:.3f} +/- {g['coop_rate']['se']:.3f} for grim/base and "
                        f"{t['coop_rate']['mean']:.3f} +/- {t['coop_rate']['se']:.3f} for tft/base, both arms open with C in "
                        f"{g['opens_c']['mean']:.0%} of episodes, and ever_defect equals defects_last_round to three decimals in "
                        f"{'every' if all_same else 'most'} cell of the cache. That equality means every episode that defects "
                        f"at all ALSO defects in the final round -- no episode defects mid-game without defecting at the "
                        f"buzzer too -- and NOT that the final round is the only place defection ever lands. It is not: "
                        f"defect_before_last is {g['defect_before_last']['mean']:.3f} +/- {g['defect_before_last']['se']:.3f} for "
                        f"grim/base and {t['defect_before_last']['mean']:.3f} +/- {t['defect_before_last']['se']:.3f} for tft/base, so a "
                        f"further {g['defect_before_last']['mean']:.1%} and {t['defect_before_last']['mean']:.1%} of episodes "
                        f"({pre_cond['grim']:.1%} and {pre_cond['tft']:.1%} of the episodes that defect at all) carry one additional "
                        f"defection before the final round. The identity n_defects - defects_last_round = defect_before_last "
                        f"{ident_txt}. Early defection on this page is rare, not absent."),
            "where_they_separate": (
                f"defect_before_last is the only behaviour that responds to the opponent at all, and even it is small: "
                f"grim/base {g['defect_before_last']['mean']:.3f} +/- {g['defect_before_last']['se']:.3f} vs tft/base "
                f"{t['defect_before_last']['mean']:.3f} +/- {t['defect_before_last']['se']:.3f} late; the early-training "
                f"curves separate more (tft runs higher through step 10) but the seed bands overlap throughout."),
            "degenerate_panel": (
                f"Panel 6 (rounds_in_punishment) is effectively empty: grim/base is identically "
                f"{g['rounds_in_punishment']['mean']:.3f} at every step and every seed, and tft/base is "
                f"{t['rounds_in_punishment']['mean']:.4f} late. The reason is NOT that defection only ever happens in the final "
                f"round -- it happens earlier in {g['defect_before_last']['mean']:.1%} of grim/base and "
                f"{t['defect_before_last']['mean']:.1%} of tft/base episodes. It is that those early defections land so close to "
                f"the buzzer that the opponent's retaliation is itself among the last moves of the game: conditional on "
                f"defecting, the first defection sits {g['first_defect_from_end']['mean']:.3f} (grim/base) and "
                f"{t['first_defect_from_end']['mean']:.3f} (tft/base) rounds from the end of a "
                f"{g['n_rounds']['mean']:.0f}-round episode. With essentially no rounds left after the opponent answers, the "
                f"arms never spend time in the regime where 'never forgives' and 'forgives' differ. That is the mechanism "
                f"behind the null in panels 1-5, not a missing measurement."),
            "equality_reading": (
                "ever_defect == defects_last_round is the statement that no episode defects mid-game without also "
                "defecting at the buzzer. It is strictly weaker than 'all defection is final-round defection', and "
                + (f"the cache refutes that stronger reading in {len(pre_cells)} of the {len(ident_live)} populated "
                   f"pooled_late cells ({', '.join(pre_cells)}), where defect_before_last is nonzero and is recovered "
                   f"exactly by n_defects - defects_last_round."
                   if pre_cells else
                   "no populated pooled_late cell in this cache separates the two readings — defect_before_last is "
                   "zero throughout — so the distinction here is logical rather than measured.")
                + " See defect_before_last_identity_by_cell."),
            "ever_defect_equals_defects_last_round_by_cell": same_cells,
            "defect_before_last_identity_by_cell": {
                "check": "pooled_late: n_defects - defects_last_round == defect_before_last",
                "tolerance": IDENT_TOL,
                "holds_in_all_populated_cells": identity_holds,
                "populated_cells": sorted(ident_live),
                "empty_cells_skipped": ident_empty,
                "by_cell": identity,
            },
            "defect_before_last_given_any_defect": {tag: fmt(v, 4) for tag, v in pre_cond.items()},
        },
        "headline_numbers_pooled_late": {"late_step_inclusive": late, "by_arm": claim},
        "error_bar_definitions": {
            "band": "+/-1 SE between TRAINING SEEDS: sd(ddof=1)/sqrt(n_seeds) over the per-seed values at that step.",
            "null_se": "n_seeds < 2 -> se is null -> NO band drawn (never a zero-width band).",
            "null_mean": "a seed with no surviving ipd episode at that step is null -> the line breaks (np.nan), never interpolated.",
            "faint_lines": "the individual per-seed traces, drawn underneath at alpha 0.22.",
            "n_definition": "n in the band is the number of TRAINING SEEDS alive at that step, not the number of episodes.",
        },
        "denominators": {
            "ipd_episodes_kept_by_arm": eps,
            "seeds_by_arm": nseeds,
            "episodes_kept_per_cell": {k: v for k, v in meta["episodes_kept_ipd"].items()
                                       if k.startswith(("grim/base", "tft/base"))},
            "episodes_dropped_per_cell": {k: v for k, v in meta["episodes_dropped_ipd"].items()
                                          if k.startswith(("grim/base", "tft/base"))},
            "invalid_rate_threshold": meta["invalid_rate_threshold"],
            "invalid_rate_rule": meta["invalid_rate_rule"],
            "trace_sampling_note": meta["trace_sampling_note"],
            "panels_1_to_6_source": "by_step, from ipd action sequences in trace dumps (every 5th step)",
            "panels_7_to_8_source": "metrics_curves, from metrics.jsonl (every step, 7 envs pooled)",
        },
        "right_edge_seed_counts": edge,
        "panels": panels,
        "provenance": {
            "cache": str(CACHE),
            "cache_mtime_utc": dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc).isoformat(),
            "cache_bytes": st.st_size,
            "cache_generated_utc": meta["generated_utc"],
            "runs_root": meta["runs_root"],
            "arms_plotted": [c for c, *_ in ARMS],
            "dpi": args.dpi,
        },
        "caveat": (f"The runs stopped at different steps, so the rightmost points rest on fewer seeds. "
                   f"{tail_txt('grim')}; {tail_txt('tft')}. The apparent late rise in cooperation and fall in "
                   f"ever_defect is therefore a change in WHICH seeds are averaged, not a change in behaviour; "
                   f"read only the region where n_seeds is at full strength, and treat the pooled steps >= {late} "
                   f"numbers as the claim."),
    }
    js = outdir / f"{args.stem}.json"
    js.write_text(json.dumps(payload, indent=1))
    print(f"[fig] wrote {js}")


if __name__ == "__main__":
    main()
