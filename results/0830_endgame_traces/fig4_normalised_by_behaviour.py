#!/usr/bin/env python
"""The same question as fig1, asked with the BEHAVIOUR divided out. Final-round
decision blocks only, both opponents, 3 seeds.

    /home/allie/venvs/tools/bin/python fig4_normalised_by_behaviour.py

  fig4_normalised_by_behaviour.png    the figure
  fig4_normalised_by_behaviour.json   every number drawn in it

WHAT THIS ASKS, AND WHY IT IS NOT A RE-RUN OF FIG1. The endgame penalty cuts
late-betrayal BEHAVIOUR a lot. fig1 and fig2 here found that the endgame
reasoning markers fall too, but that after length standardisation the fall
sits on top of the `in_game_penalty` FLOOR control -- i.e. not endgame-specific.
That pooled analysis runs over ALL 12,480 blocks, and the overwhelming majority
of those blocks are turns with nothing to do with the endgame. An arm that
betrays less late has fewer endgame-flavoured turns to write about at all, so
the pooled marker rate is partly a readout of the behaviour it is supposed to
be independent of.

THE NORMALISATION. Restrict to FINAL-ROUND DECISION BLOCKS:

    in_decision == True  and  answer_defect is not None  and
    rounds_from_end == 0

Every episode has exactly one final round. Both arms therefore contribute ~48
final-round decision blocks per (opponent, arm, seed) cell NO MATTER HOW MUCH
LATE BETRAYAL THEY ACTUALLY DO. The denominator is matched BY CONSTRUCTION, so
a difference measured here cannot be "the eg arm simply did less endgame
behaviour overall" -- that is precisely the quantity that has been divided out.

This is conditioning on OPPORTUNITY, not on outcome. The final round arrives
whether or not the policy uses it, so it is a pre-treatment variable and the
restriction is safe. Additionally conditioning on ACTUALLY DEFECTING would be
post-treatment conditioning on the outcome; it is computed and carried in the
paired JSON under `secondary_post_treatment_conditioning`, but it is NOT shown
as primary because `tft/eg` seed 2 defects on only 2 of its 47 final rounds, so
that cell's conditional marker rates rest on two blocks. It reproduces the
primary sign on all four markers against grim and on three of four against tft;
the exception is tft `endgame_hold`, which flips on the strength of that
two-block cell alone. The footer reports that flip rather than smoothing it.

WHAT CHANGES UNDER THE NORMALISATION. The reasoning effect does not vanish, but
it is much smaller than the behavioural one AND it is endgame-SPECIFIC in a way
the pooled analysis could not see:

  * BEHAVIOUR falls hard -- about -0.22 (grim) and -0.41 (tft).
  * PLANS TO BETRAY falls only about -0.09 / -0.07, roughly a third (grim) to a
    fifth (tft) of the behavioural move.
  * PLANS TO HOLD *RISES*, about +0.08 / +0.05.
  * The generic `in_game_penalty` FLOOR control does not fall at all: +0.12
    against tft and -0.05 +/- 0.23 against grim.

Opposite signs on two endgame markers with the generic floor flat or rising is
a pattern that neither a verbosity artifact nor blanket suppression produces.
Verbosity moves every binary marker the same way; blanket suppression moves the
floor with the signal. That is the substantive claim of this figure.

THE LENGTH ADJUSTMENT IS NOT OPTIONAL, AND IT CUTS THE OTHER WAY HERE. Pooled
over all blocks the penalty makes the reasoning SHORTER (-482 chars against
tft). At the FINAL ROUND the eg arm writes LONGER (+218 +/- 130 against tft,
+327 +/- 310 against grim). A marker hit is binary per block and rises steeply
with length, so the raw final-round number is FLATTERED by length -- in the
opposite direction from the pooled analysis, where length deflated it. Every
marker is therefore reported four ways and panel B is the agreement check:

  raw              unadjusted.
  strat_global     direct standardisation to n_chars quintile bins whose edges
                   are cut over ALL 12,480 blocks, standardised to the bin
                   distribution of the pooled (nohole + eg) final-round blocks
                   for that opponent. Each arm is standardised over the bins it
                   occupies, with the standard weights renormalised over those
                   bins, and the two standardised rates are then differenced.
  strat_finalround identical, with the quintile edges recut over the final-round
                   blocks of the four contrast arms only -- because the
                   final-round blocks are longer than the corpus as a whole and
                   the global edges put most of them in the top two bins.
  logistic_adj     per seed, a logistic regression of the marker hit on
                   [intercept, log(n_chars), arm == eg] over that seed's pooled
                   nohole + eg final-round blocks, reporting the MARGINAL EFFECT
                   of the arm term at the pooled mean log-length. Newton-Raphson,
                   ridge 1e-6, 200 iterations.

`strat_global` is the PRIMARY estimator and is what panel A draws. All four
agree in sign and roughly in size on every marker that matters, which is the
point of drawing them together.

ERROR BARS. Every bar on this figure is BETWEEN TRAINING SEED, n = 3: the
`eg - nohole` delta is formed WITHIN a matched training seed and only then
averaged, and the bar is sd(per-seed deltas) / sqrt(3). Seeds are never pooled
into a single rate. The sensitivity points rest on 2 seeds and are drawn as a
distinct marker with NO bar.

WHAT THIS DOES NOT DO. It does not overturn the pooled result in
`research_logs/0830-endgame-traces.md` section 4. That analysis and this one
are different conditionings of the same data and both are correct for what they
measure: the pooled number is dominated by non-endgame turns, and this one
deliberately looks only at the turn where the endgame is live. Panel D draws
the two side by side rather than asserting the relationship in prose.

HONESTY, AND THIS FIGURE HAS MORE OF IT TO DO THAN MOST.
  * The behaviour deltas have very wide between-seed bars (+/-0.201 grim,
    +/-0.276 tft) because each is driven by ONE seed. The behavioural result
    proper rests on the TRAINING LOGS (3 seeds, -0.039 +/- 0.012 grim and
    -0.142 +/- 0.064 tft; see `research_logs/0830-endgame-summary.md` section
    1), NOT on this eval. So "reasoning moves a fifth as much as behaviour" is
    an ORDER-OF-MAGNITUDE statement and not a precise ratio.
  * `grim/nohole` seed 1 emits an empty answer on 60.8% of its decision turns
    and contributes only 15 usable final-round blocks against 47-48 for every
    other cell. `tft/nohole` seed 0 is at 31.2%. Both are marked on the figure
    and both drive a drop-that-cell sensitivity point.
  * Several estimates sit at 1.5-2 sigma and are not drawn as if decisive.
  * The tft `m_backward_induction` logistic SE of +/-0.003 is IMPLAUSIBLY SMALL
    -- three seeds happening to agree to the third decimal. The stratified
    value is presented as primary and that logistic SE is never headlined.

PALETTE AND LAYOUT. Fixed by CONDITION across the whole study: baseline purple,
endgame penalty orange, hidden horizon blue (reserved; no inf arm appears
here). Contrasts are drawn in neutral ink -- a difference is not a condition --
and condition hue is used only in panel E, which draws levels. OPPONENT IS
CARRIED BY BAND POSITION, never by hue, so the same panel position holds the
same quantity on a shared y-axis across both bands.

EVERY NUMBER IS COMPUTED AT RENDER TIME from trace_blocks.jsonl, plus the
pooled comparison in panel D which is read from trace_markers.json. The two
training-log behaviour figures quoted above are the only literals, and they are
tagged with their source on the figure itself.
"""
from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent

PURPLE, ORANGE, BLUE, WARN = "#7a5bd6", "#eb6834", "#2a78d6", "#b5342a"
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
PAPER = "#f9f9f7"

# Opponent is BLOCK POSITION, never hue.
BANDS = [("grim", "vs GRIM  -  never forgives"),
         ("tft", "vs TIT-FOR-TAT  -  forgives on return")]

# (field, plain-words label, is_floor)
MARKERS = [
    ("m_endgame_defect_plan", "plans to betray\nat the end", False),
    ("m_backward_induction", "backward\ninduction", False),
    ("m_endgame_hold", "plans to HOLD\nat the end", False),
    ("m_in_game_penalty", "punishment vocabulary\n(FLOOR / CONTROL)", True),
]
MARKER_KEYS = [m for m, _, _ in MARKERS]
FLOOR = "m_in_game_penalty"

# (key, short label for the number block, glyph, glyph kwargs)
ESTIMATORS = [
    ("raw", "raw", "o", dict(mfc=INK, mec=SURF, mew=1.1, ms=8.0)),
    ("strat_global", "strat.global", "s", dict(mfc=SURF, mec=INK2, mew=2.0, ms=7.6)),
    ("strat_finalround", "strat.final", "D", dict(mfc=SURF, mec=MUT, mew=1.7, ms=6.4)),
    ("logistic_adj", "logistic", "^", dict(mfc=INK2, mec=SURF, mew=1.1, ms=8.2)),
]
PRIMARY = "strat_global"

# per-seed glyphs, so a seed is identifiable without relying on position alone
SEED_MK = ["o", "s", "^", "D", "v", "P"]

N_BINS = 5
QUANTILES = (20, 40, 60, 80)

# The ONLY literals on this figure. Behavioural reference from the training
# logs, which is where the behavioural result actually lives -- this eval's own
# final-round behaviour deltas are far too seed-fragile to carry it.
TRAINLOG_BEHAVIOUR = {"grim": (-0.039, 0.012), "tft": (-0.142, 0.064)}
TRAINLOG_SOURCE = "research_logs/0830-endgame-summary.md section 1, 3 seeds"


# ------------------------------------------------------------------ helpers --

def wrap(text, width):
    """`fig.text` does not wrap and an over-long line runs off the paper.

    Explicit newlines are paragraph breaks and survive; everything else is
    refilled. Widths come from the figure geometry rather than a guess, so
    editing a footer sentence cannot silently push it off the right edge.
    """
    return "\n".join(
        "\n".join(textwrap.wrap(seg, width)) if seg.strip() else seg
        for seg in text.split("\n"))


def nlines(text):
    return text.count("\n") + 1


def se(v):
    """Between-training-seed SE: sd(paired per-seed deltas) / sqrt(n).

    Undefined at n = 1. At n = 2 it is arithmetically defined but is not a
    usable interval, and every n = 2 quantity on this figure is drawn without
    a bar and labelled with its seed count.
    """
    v = [x for x in v if x is not None]
    if len(v) < 2:
        return None
    return float(np.std(v, ddof=1) / np.sqrt(len(v)))


def summarise(per_seed, seeds):
    v = [x for x in per_seed if x is not None]
    return {"delta": float(np.mean(v)) if v else None, "se": se(v),
            "per_seed": [None if x is None else round(float(x), 4)
                         for x in per_seed],
            "n_seeds": len(v), "train_seeds": list(seeds)}


ADJUSTED = [k for k, _, _, _ in ESTIMATORS if k != "raw"]


def plan_ratio(rec):
    """|plans-to-betray delta| / |behaviour delta|, over the THREE length
    adjustments rather than one of them.

    Quoting a single estimator's ratio would put a spurious second decimal on a
    quantity whose denominator is a one-seed-driven behavioural delta. The
    three adjustments span roughly 0.27-0.41 against grim and 0.17-0.24 against
    tft; the spread IS the precision available, so the spread is what gets
    printed next to the central value.
    """
    beh = rec["behaviour"]["delta"]
    v = [abs(rec["markers"]["m_endgame_defect_plan"][k]["delta"] / beh)
         for k in ADJUSTED]
    return {"mean": float(np.mean(v)), "min": float(min(v)), "max": float(max(v)),
            "per_estimator": dict(zip(ADJUSTED, v)),
            "note": "|plans-to-betray delta| / |final-round behaviour delta|, "
                    "over the three length-adjusted estimators. The behaviour "
                    "denominator is seed-fragile, so this is an "
                    "order-of-magnitude quantity."}


ORDINAL = {2: "half", 3: "third", 4: "quarter", 5: "fifth", 6: "sixth",
           7: "seventh", 8: "eighth", 9: "ninth", 10: "tenth"}


def frac(r):
    """"a third", from the ratio, so the prose cannot drift from the number."""
    n = max(2, round(1.0 / r)) if r else 0
    return ORDINAL.get(n, f"1/{n}")


NOTE_PT = 7.0


def style(ax, title, ylab, note=None, note_col=None):
    """Panel note goes ABOVE the axes, under the title, never inside it.

    Every panel here prints a monospace number block along its top edge, which
    is where an in-panel note wants to live; the first render had the note of
    panels A, B and D sitting on top of their own leftmost number block. The
    title pad is grown by the measured line count of the note so the two cannot
    collide however long the note gets.
    """
    if note:
        ax.text(0.0, 1.010, note, transform=ax.transAxes, fontsize=NOTE_PT,
                color=note_col or MUT, va="bottom", ha="left", linespacing=1.35)
    ax.set_title(title, fontsize=10.0, color=INK, loc="left",
                 pad=7 + (NOTE_PT * 1.35 * nlines(note) if note else 0))
    ax.set_ylabel(ylab, fontsize=8.6, color=INK2)
    ax.set_facecolor(SURF)
    ax.grid(True, axis="y", color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=MUT, labelsize=8, length=0)


def zero_line(ax, label="no effect"):
    ax.axhline(0, color=INK, lw=1.5, zorder=2)
    ax.annotate(label, (ax.get_xlim()[0], 0), textcoords="offset points",
                xytext=(4, 3), fontsize=7.2, color=INK, va="bottom")


# ------------------------------------------------------------------- compute --

def load_blocks(path):
    rows = []
    with path.open() as fh:
        for line in fh:
            if not line.strip():
                continue
            rows.append(json.loads(line))
    return rows


def edges_of(chars):
    return [float(np.percentile(np.asarray(chars, dtype=float), q))
            for q in QUANTILES]


def binof(n, edges):
    return min(int(np.searchsorted(edges, n, side="right")), N_BINS - 1)


def bin_weights(blocks, edges):
    """Counts per length bin -- the standard population for direct
    standardisation. Built from the POOLED (nohole + eg) final-round blocks of
    one opponent, so both arms are reweighted onto the same target and that
    target is itself a final-round distribution rather than a corpus-wide one.
    """
    w = np.zeros(N_BINS)
    for r in blocks:
        w[binof(r["n_chars"], edges)] += 1.0
    return w


def std_rate(blocks, marker, weights, edges):
    """One arm-seed cell's marker rate, direct-standardised to `weights`.

    Each cell is standardised over THE BINS IT OCCUPIES, with the standard
    weights renormalised over exactly those bins. Dropping a bin from the
    contrast because only one of the two arms occupies it would throw away
    real blocks and, at ~47 blocks in 5 bins, happens often enough to matter:
    `grim/nohole` seed 2 has nothing in the shortest bin and `tft/eg` seed 2
    nothing in the longest.
    """
    got = [[] for _ in range(N_BINS)]
    for r in blocks:
        got[binof(r["n_chars"], edges)].append(float(r[marker]))
    use = [b for b in range(N_BINS) if got[b]]
    if not use:
        return None
    w = weights[use]
    if w.sum() <= 0:
        return None
    w = w / w.sum()
    return float(np.dot(w, [float(np.mean(got[b])) for b in use]))


def logistic_marginal(blocks_eg, blocks_nh, marker, ridge, iters):
    """Marginal effect of the arm term at the pooled mean log-length.

    Newton-Raphson on [intercept, log(n_chars), arm == eg] with a small ridge.
    The ridge is there because a cell can be separable -- `tft/eg` seed 2 hits
    `endgame_hold` on every one of its longest blocks -- and an unpenalised fit
    then runs the coefficient off to infinity instead of converging. It is
    small enough (1e-6) not to move a well-conditioned fit: at 1e-8 every
    estimate here is unchanged to six decimal places.
    """
    g = list(blocks_eg) + list(blocks_nh)
    if not g:
        return None
    X = np.column_stack([
        np.ones(len(g)),
        np.log(np.array([r["n_chars"] for r in g], dtype=float)),
        np.array([1.0] * len(blocks_eg) + [0.0] * len(blocks_nh)),
    ])
    y = np.array([float(r[marker]) for r in g])
    b = np.zeros(3)
    eye = np.eye(3)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-(X @ b)))
        H = X.T @ (X * (p * (1.0 - p))[:, None]) + ridge * eye
        try:
            b = b + np.linalg.solve(H, X.T @ (y - p) - ridge * b)
        except np.linalg.LinAlgError:
            return None
    mlog = float(X[:, 1].mean())

    def sig(z):
        return 1.0 / (1.0 + np.exp(-z))

    return float(sig(b[0] + b[1] * mlog + b[2]) - sig(b[0] + b[1] * mlog))



def _same_sign(a, b):
    if a is None or b is None:
        return None
    return bool((a >= 0) == (b >= 0))


def compute(rows, ridge, iters, min_defections):
    """Everything the figure draws, from the block-level JSONL in one place."""
    final = [r for r in rows if r["in_decision"] and r["answer_defect"] is not None
             and r["rounds_from_end"] == 0]
    contrast_arms = {f"{o}/{c}" for o, _ in BANDS for c in ("nohole", "eg")}
    final4 = [r for r in final if r["arm"] in contrast_arms]

    ed = {"global": edges_of([r["n_chars"] for r in rows]),
          "finalround": edges_of([r["n_chars"] for r in final4])}

    def cell(arm, seed, src=None):
        return [r for r in (final if src is None else src)
                if r["arm"] == arm and r["train_seed"] == seed]

    seeds_of = {}
    for arm in sorted(contrast_arms):
        seeds_of[arm] = sorted({r["train_seed"] for r in final if r["arm"] == arm})

    # The failure mode the repo's invalid_rate gate misses, recomputed here on
    # DECISION TURNS rather than on all turns: an empty answer resolves to a
    # library default move, so a cell with many of them has both fewer usable
    # final-round blocks and a behaviour reading that is not really its own.
    empty_rate = {}
    for arm in sorted(contrast_arms):
        for s in seeds_of[arm]:
            dec = [r for r in rows if r["arm"] == arm and r["train_seed"] == s
                   and r["in_decision"]]
            empty_rate[f"{arm}|{s}"] = (
                sum(r["answer_defect"] is None for r in dec) / len(dec)) if dec else None

    out = {"edges": ed, "opp": {}, "per_cell": {}, "empty_answer_rate_decision": empty_rate}

    for opp, _ in BANDS:
        eg_arm, nh_arm = f"{opp}/eg", f"{opp}/nohole"
        seeds = [s for s in seeds_of[eg_arm] if s in seeds_of[nh_arm]]
        pooled = [r for r in final if r["arm"] in (eg_arm, nh_arm)]
        w = {k: bin_weights(pooled, ed[k]) for k in ed}

        cells = {(a, s): cell(a, s) for a in (eg_arm, nh_arm) for s in seeds}
        for (a, s), g in cells.items():
            out["per_cell"][f"{a}/s{s}"] = {
                "n_final_blocks": len(g),
                "mean_chars": round(float(np.mean([r["n_chars"] for r in g])), 1),
                "defect_rate": round(float(np.mean([float(r["answer_defect"])
                                                    for r in g])), 4),
                **{m: round(float(np.mean([float(r[m]) for r in g])), 4)
                   for m in MARKER_KEYS},
                "n_final_round_defections": int(sum(bool(r["answer_defect"])
                                                    for r in g)),
                "empty_answer_rate_decision_turns": empty_rate.get(f"{a}|{s}"),
            }

        def beh(s):
            return (float(np.mean([float(r["answer_defect"]) for r in cells[(eg_arm, s)]]))
                    - float(np.mean([float(r["answer_defect"]) for r in cells[(nh_arm, s)]])))

        def est(m, kind, s):
            if kind == "raw":
                return (float(np.mean([float(r[m]) for r in cells[(eg_arm, s)]]))
                        - float(np.mean([float(r[m]) for r in cells[(nh_arm, s)]])))
            if kind == "logistic_adj":
                return logistic_marginal(cells[(eg_arm, s)], cells[(nh_arm, s)],
                                         m, ridge, iters)
            key = "global" if kind == "strat_global" else "finalround"
            a = std_rate(cells[(eg_arm, s)], m, w[key], ed[key])
            b = std_rate(cells[(nh_arm, s)], m, w[key], ed[key])
            return None if (a is None or b is None) else a - b

        rec = {"train_seeds": seeds,
               "behaviour": summarise([beh(s) for s in seeds], seeds),
               "markers": {}, "length": {}}
        for m in MARKER_KEYS:
            rec["markers"][m] = {k: summarise([est(m, k, s) for s in seeds], seeds)
                                 for k, _, _, _ in ESTIMATORS}

        # The length reversal, which is why the adjustment is mandatory and why
        # it cuts the opposite way here from the pooled analysis.
        for tag, src in (("all_blocks", rows), ("final_round", final)):
            d = [float(np.mean([r["n_chars"] for r in cell(eg_arm, s, src)]))
                 - float(np.mean([r["n_chars"] for r in cell(nh_arm, s, src)]))
                 for s in seeds]
            rec["length"][tag] = summarise(d, seeds)
            rec["length"][tag]["per_seed"] = [round(float(x), 1) for x in d]
            rec["length"][tag]["eg_mean_chars"] = float(np.mean(
                [r["n_chars"] for r in src if r["arm"] == eg_arm]))
            rec["length"][tag]["nohole_mean_chars"] = float(np.mean(
                [r["n_chars"] for r in src if r["arm"] == nh_arm]))

        # Drop the flagged cell. The bin edges and the standard population stay
        # at their FULL-data values, so the only thing that changes is which
        # seeds are averaged.
        flagged = max(seeds, key=lambda s: empty_rate.get(f"{nh_arm}|{s}") or 0.0)
        keep = [s for s in seeds if s != flagged]
        sens = {"dropped_seed": flagged, "kept_seeds": keep,
                "dropped_because":
                    f"{nh_arm} seed {flagged} emits an empty answer on "
                    f"{empty_rate[f'{nh_arm}|{flagged}']:.3f} of its decision turns",
                "behaviour": summarise([beh(s) for s in keep], keep)}
        for m in MARKER_KEYS:
            sens[m] = {k: summarise([est(m, k, s) for s in keep], keep)
                       for k, _, _, _ in ESTIMATORS}
        rec["sensitivity_drop_flagged"] = sens

        # SECONDARY, and post-treatment: additionally condition on the block
        # having actually defected. Same answer, not shown as primary, because
        # tft/eg seed 2 defects on 2 of 47 final rounds.
        dcells = {(a, s): [r for r in cells[(a, s)] if r["answer_defect"]]
                  for a in (eg_arm, nh_arm) for s in seeds}
        tiny = sorted({s for (a, s), g in dcells.items() if len(g) < min_defections})
        post = {"n_blocks_per_cell": {f"{a}/s{s}": len(g)
                                      for (a, s), g in sorted(dcells.items())},
                "seeds_with_too_few_defections": tiny,
                "min_defections_threshold": min_defections}

        def pt(m, use):
            d = []
            for s in use:
                A, B = dcells[(eg_arm, s)], dcells[(nh_arm, s)]
                d.append(None if not A or not B else
                         float(np.mean([float(r[m]) for r in A]))
                         - float(np.mean([float(r[m]) for r in B])))
            return summarise(d, use)

        keep_pt = [s for s in seeds if s not in tiny]
        for m in MARKER_KEYS:
            post[m] = pt(m, seeds)
            post[m]["drop_tiny_cells"] = pt(m, keep_pt) if keep_pt != seeds else None
        # Recorded rather than described: the all-seeds version disagrees with
        # the primary estimate on exactly one marker and it is worth knowing
        # which, and whether the disagreement is the tiny cell.
        post["sign_agreement_with_primary"] = {
            m: {"all_seeds": _same_sign(post[m]["delta"],
                                        rec["markers"][m][PRIMARY]["delta"]),
                "drop_tiny_cells": _same_sign(
                    (post[m]["drop_tiny_cells"] or post[m])["delta"],
                    rec["markers"][m][PRIMARY]["delta"])}
            for m in MARKER_KEYS}
        post["caveat"] = (
            "Post-treatment conditioning: the set of blocks is selected on the "
            "outcome the treatment moves, so this is a collider and is carried "
            "for completeness only, never as primary. The smallest cell has "
            f"{min(post['n_blocks_per_cell'].values())} blocks. `drop_tiny_cells` "
            f"repeats it without the seeds whose defection count is under "
            f"{min_defections}.")
        rec["post_treatment"] = post

        rec["n_final_blocks"] = sum(len(g) for g in cells.values())
        out["opp"][opp] = rec

    out["n_blocks_total"] = len(rows)
    out["n_final_round_decision_blocks_all_arms"] = len(final)
    out["n_final_round_decision_blocks_contrast_arms"] = len(final4)
    return out


# ---------------------------------------------------------------- panel A --
# BEHAVIOUR against REASONING on ONE shared axis. The whole claim of the figure
# is a comparison of MAGNITUDES between a behavioural delta and four reasoning
# deltas, so putting them on separate axes would give the comparison away. The
# cost is that the tft behaviour per-seed point at -0.957 sets the scale for
# everything; that point is real and is the reason the behavioural bar here is
# useless, so it is left in rather than clipped.
# --------------------------------------------------------------------------

DX_SEED, DX_EST, DX_SENS = -0.27, 0.0, 0.28


def panel_behaviour_vs_reasoning(ax, opp, D, ylim, record):
    rec = D["opp"][opp]
    sens = rec["sensitivity_drop_flagged"]
    entries = [("BEHAVIOUR\nfinal-round\ndefection", rec["behaviour"],
                sens["behaviour"], INK, True)]
    for m, lab, is_fl in MARKERS:
        entries.append((lab, rec["markers"][m][PRIMARY], sens[m][PRIMARY],
                        INK2, False))

    xs = [0.0] + [1.45 + i for i in range(len(MARKERS))]

    # the behaviour slot, walled off: it is a different KIND of quantity and
    # the reader must not read the gap between it and its neighbour as small
    ax.axvspan(-0.75, 0.72, color=WARN, alpha=0.05, lw=0, zorder=0.3)
    ax.axvline(1.08, color=GRID, lw=1.2, zorder=0.4)

    # the FLOOR control's own interval, extended across the REASONING half only
    fl = rec["markers"][FLOOR][PRIMARY]
    if fl["se"] is not None:
        ax.fill_between([1.08, xs[-1] + 0.75], fl["delta"] - fl["se"],
                        fl["delta"] + fl["se"], color=MUT, alpha=0.16, lw=0,
                        zorder=0.5)
        ax.plot([1.08, xs[-1] + 0.75], [fl["delta"]] * 2, color=MUT, lw=1.0,
                ls=(0, (5, 3)), zorder=0.6)

    for x, (lab, cur, sn, col, is_beh) in zip(xs, entries):
        for i, v in enumerate(cur["per_seed"]):
            if v is None:
                continue
            ax.plot([x + DX_SEED], [v], marker=SEED_MK[i % len(SEED_MK)], ms=4.8,
                    color=MUT, alpha=0.8, mec=SURF, mew=0.7, ls="none", zorder=3)
        ax.errorbar([x + DX_EST], [cur["delta"]], yerr=[cur["se"]], color=col,
                    lw=0, elinewidth=2.3, capsize=6, capthick=2.3,
                    marker="o" if is_beh else "s", ms=10.5 if is_beh else 8.5,
                    mfc=col if is_beh else SURF, mec=col, mew=2.0, zorder=5)
        if sn["delta"] is not None:
            ax.plot([x + DX_EST, x + DX_SENS], [cur["delta"], sn["delta"]],
                    color=ORANGE, lw=0.9, ls=":", zorder=4)
            ax.plot([x + DX_SENS], [sn["delta"]], marker="P", ms=9.5, mfc=PAPER,
                    mec=ORANGE, mew=2.0, ls="none", zorder=6)

    ax.set_xlim(-0.75, xs[-1] + 0.75)
    ax.set_ylim(ylim)
    zero_line(ax)
    ax.set_xticks(xs)
    ax.set_xticklabels([e[0] for e in entries], fontsize=8.4, color=INK2)
    ax.get_xticklabels()[0].set_color(WARN)
    ax.get_xticklabels()[0].set_fontweight("bold")

    y0, y1 = ylim
    for x, (lab, cur, sn, col, is_beh) in zip(xs, entries):
        txt = f"{cur['delta']:+.3f}\n+/-{cur['se']:.3f}"
        if sn["delta"] is not None:
            txt += f"\ndrop {sn['delta']:+.3f}"
        ax.text(x + 0.04, y1 - (y1 - y0) * 0.022, txt, fontsize=7.4,
                color=col, ha="center", va="top", family="monospace",
                linespacing=1.35)

    # the ratio the headline rests on, printed with its own health warning
    rr = plan_ratio(rec)
    ax.text(0.5 * (1.08 + xs[-1] + 0.75), y0 + (y1 - y0) * 0.040,
            f"plans-to-betray moves ~1/{round(1 / rr['mean'])} as far as "
            f"behaviour ({rr['mean']:.2f}x; the three length adjustments give "
            f"{rr['min']:.2f}-{rr['max']:.2f}).\nORDER OF MAGNITUDE ONLY -- the "
            f"behavioural bar here is driven by one seed. See the footer.",
            fontsize=7.4, color=WARN, ha="center", va="bottom", linespacing=1.4)

    record[opp] = {
        "behaviour_final_round_defect": rec["behaviour"],
        "behaviour_drop_flagged": sens["behaviour"],
        "primary_estimator": PRIMARY,
        "markers_primary": {m: rec["markers"][m][PRIMARY] for m in MARKER_KEYS},
        "markers_primary_drop_flagged": {m: sens[m][PRIMARY] for m in MARKER_KEYS},
        "plan_over_behaviour_ratio": rr,
        "floor_control_interval": {"marker": FLOOR, "delta": fl["delta"],
                                   "se": fl["se"]},
    }
    return ax



# ---------------------------------------------------------------- panel B --

def panel_estimators(ax, opp, D, ylim, record):
    """Four length adjustments per marker. Agreement is the point."""
    rec = D["opp"][opp]
    sub = np.linspace(-0.30, 0.30, len(ESTIMATORS))

    for gi, (m, lab, is_fl) in enumerate(MARKERS):
        if is_fl:
            ax.axvspan(gi - 0.5, gi + 0.5, color=MUT, alpha=0.07, lw=0, zorder=0.4)
        for si, (kind, klab, glyph, kw) in enumerate(ESTIMATORS):
            c = rec["markers"][m][kind]
            if c["delta"] is None:
                continue
            ax.errorbar([gi + sub[si]], [c["delta"]], yerr=[c["se"]], color=kw["mec"]
                        if kw["mfc"] == SURF else kw["mfc"], lw=0, elinewidth=1.9,
                        capsize=4.5, capthick=1.9, marker=glyph, zorder=5, **kw,
                        label=klab if gi == 0 else None)

    ax.set_xlim(-0.62, len(MARKERS) - 0.38)
    ax.set_ylim(ylim)
    zero_line(ax)
    ax.set_xticks(range(len(MARKERS)))
    ax.set_xticklabels([lab for _, lab, _ in MARKERS], fontsize=8.4, color=INK2)

    y0, y1 = ylim
    for gi, (m, _, _) in enumerate(MARKERS):
        rows_ = []
        for kind, klab, _, _ in ESTIMATORS:
            c = rec["markers"][m][kind]
            rows_.append(f"{klab:<14s}{c['delta']:+.3f} +/- {c['se']:.3f}")
        ax.text(gi, y1 - (y1 - y0) * 0.022, "\n".join(rows_), fontsize=6.9,
                color=INK2, ha="center", va="top", family="monospace",
                linespacing=1.4)
        record.setdefault(opp, {})[m] = {
            k: rec["markers"][m][k] for k, _, _, _ in ESTIMATORS}

    # Four glyphs is one more than direct labelling can carry inside a group
    # this narrow, and the number block above already names them in the same
    # order; the key only has to attach a shape to each name.
    leg = ax.legend(loc="lower left", frameon=False, fontsize=7.4, ncol=4,
                    handletextpad=0.5, columnspacing=1.5)
    for t in leg.get_texts():
        t.set_color(INK2)

    # the one SE on this figure that must not be believed, called out where it
    # is drawn rather than only in the footer
    bi = MARKER_KEYS.index("m_backward_induction")
    c = rec["markers"]["m_backward_induction"]["logistic_adj"]
    if c["se"] is not None and c["se"] < 0.01:
        ax.annotate(f"SE +/-{c['se']:.3f} is IMPLAUSIBLY SMALL:\n"
                    f"3 seeds happening to agree, not precision.\n"
                    f"the stratified value is the primary one.",
                    (bi + sub[-1], c["delta"]), textcoords="offset points",
                    xytext=(30, -46), fontsize=6.8, color=WARN, ha="left",
                    va="top", annotation_clip=False,
                    arrowprops=dict(arrowstyle="-", color=WARN, lw=0.9, shrinkB=6))


# ---------------------------------------------------------------- panel C --

def panel_length(ax, opp, D, ylim, record):
    """The adjustment is mandatory and it cuts the OTHER way at the final round."""
    rec = D["opp"][opp]["length"]
    groups = [("all_blocks", "ALL 12,480 blocks\n(what fig1/fig2 saw)"),
              ("final_round", "FINAL-ROUND decision\nblocks (this figure)")]
    for gi, (key, lab) in enumerate(groups):
        c = rec[key]
        for i, v in enumerate(c["per_seed"]):
            ax.plot([gi + DX_SEED], [v], marker=SEED_MK[i % len(SEED_MK)], ms=4.8,
                    color=MUT, alpha=0.8, mec=SURF, mew=0.7, ls="none", zorder=3)
        col = INK if key == "final_round" else MUT
        ax.errorbar([gi], [c["delta"]], yerr=[c["se"]], color=col, lw=0,
                    elinewidth=2.2, capsize=6, capthick=2.2, marker="o", ms=9,
                    mfc=col, mec=SURF, mew=1.2, zorder=5)
        # thrown clear of the zero line vertically as well as sideways: the
        # all-blocks grim delta is -19 chars and its label landed on the zero
        # line's own "same length" annotation
        up = c["delta"] >= 0
        ax.annotate(f"{c['delta']:+.0f}\n+/-{c['se']:.0f} chars",
                    (gi, c["delta"]), textcoords="offset points",
                    xytext=(14, 13 if up else -13), ha="left",
                    va="bottom" if up else "top", fontsize=7.6,
                    color=col, family="monospace", linespacing=1.3)

    ax.set_xlim(-0.62, len(groups) - 0.38)
    ax.set_ylim(ylim)
    zero_line(ax, "same length")
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([lab for _, lab in groups], fontsize=8.2, color=INK2)
    record[opp] = {k: rec[k] for k, _ in groups}


# ---------------------------------------------------------------- panel D --

def panel_pooled_vs_final(ax, opp, D, pooled_con, ylim, record):
    """Both conditionings, side by side. Neither overturns the other."""
    rec = D["opp"][opp]
    out = {}
    for gi, (m, lab, is_fl) in enumerate(MARKERS):
        if is_fl:
            ax.axvspan(gi - 0.5, gi + 0.5, color=MUT, alpha=0.07, lw=0, zorder=0.4)
        p = (pooled_con.get(opp) or {}).get(m[2:])
        f = rec["markers"][m][PRIMARY]
        if p:
            ax.errorbar([gi - 0.17], [p["strat_delta_mean"]],
                        yerr=[p["strat_delta_se"]], color=MUT, lw=0,
                        elinewidth=1.9, capsize=4.5, capthick=1.9, marker="o",
                        ms=7.5, mfc=MUT, mec=SURF, mew=1.1, zorder=5)
        ax.errorbar([gi + 0.17], [f["delta"]], yerr=[f["se"]], color=INK, lw=0,
                    elinewidth=2.1, capsize=5, capthick=2.1, marker="s", ms=8,
                    mfc=SURF, mec=INK, mew=2.0, zorder=5)
        if p:
            ax.plot([gi - 0.17, gi + 0.17],
                    [p["strat_delta_mean"], f["delta"]], color=GRID, lw=1.0,
                    zorder=2)
            out[m] = {"pooled_all_blocks_strat_delta": p["strat_delta_mean"],
                      "pooled_all_blocks_strat_se": p["strat_delta_se"],
                      "final_round_strat_global_delta": f["delta"],
                      "final_round_strat_global_se": f["se"],
                      "shift": f["delta"] - p["strat_delta_mean"]}
        if gi == 0:
            ax.annotate("POOLED\n(fig1)", (gi - 0.17, p["strat_delta_mean"]),
                        textcoords="offset points", xytext=(-8, -8), ha="right",
                        va="top", fontsize=7.2, color=MUT, linespacing=1.3)
            ax.annotate("FINAL\nROUND", (gi + 0.17, f["delta"]),
                        textcoords="offset points", xytext=(9, 6), ha="left",
                        va="bottom", fontsize=7.2, color=INK, linespacing=1.3,
                        fontweight="bold")

    ax.set_xlim(-0.62, len(MARKERS) - 0.38)
    ax.set_ylim(ylim)
    zero_line(ax)
    ax.set_xticks(range(len(MARKERS)))
    ax.set_xticklabels([lab for _, lab, _ in MARKERS], fontsize=8.0, color=INK2)
    record[opp] = out


# ---------------------------------------------------------------- panel E --

def panel_cells(ax, opp, D, flagged, record):
    """Where the blocks actually are. One bar per cell, hue = CONDITION.

    This is the only panel drawing LEVELS rather than differences, so it is the
    only one entitled to the condition palette.
    """
    keys, cols, labs = [], [], []
    for cond, col in (("nohole", PURPLE), ("eg", ORANGE)):
        for s in D["opp"][opp]["train_seeds"]:
            keys.append(f"{opp}/{cond}/s{s}")
            cols.append(col)
            labs.append(f"{'base' if cond == 'nohole' else 'eg'}\ns{s}")
    vals = [D["per_cell"][k]["n_final_blocks"] for k in keys]
    x = np.arange(len(keys))
    top = 82
    for xi, v, c, k in zip(x, vals, cols, keys):
        haz = k in flagged
        ax.bar([xi], [v], width=0.68, color=PAPER if haz else c,
               edgecolor=c, lw=2.4 if haz else 0.0, hatch="//" if haz else None,
               zorder=3)
        pc = D["per_cell"][k]
        # count INSIDE the bar: above it, every label at 48 sat on the
        # reference line's own annotation
        ax.text(xi, v - 2.0, f"{v}", ha="center", va="top", fontsize=8.4,
                color=WARN if haz else SURF, fontweight="bold")
        ax.text(xi, 2.0, f"defect\n{pc['defect_rate']:.2f}", ha="center",
                va="bottom", fontsize=7.0, color=WARN if haz else SURF)
        if haz:
            # thrown to a fixed height well above every bar, with a leader
            # down to its own: anchored to the bar it collided with whichever
            # neighbour happened to be tall
            ax.annotate(f"! {pc['empty_answer_rate_decision_turns']:.0%} of "
                        f"decision turns\nemit an EMPTY ANSWER",
                        (xi, v + 2.0), xytext=(xi + 1.1, top - 4),
                        ha="center", va="top", fontsize=7.2, color=WARN,
                        fontweight="bold", linespacing=1.35,
                        annotation_clip=False,
                        arrowprops=dict(arrowstyle="-", color=WARN, lw=1.0,
                                        shrinkB=2))

    ax.set_xlim(-0.7, len(keys) - 0.3)
    ax.set_ylim(0, top)
    ax.set_yticks([0, 12, 24, 36, 48])
    ax.set_xticks(x)
    ax.set_xticklabels(labs, fontsize=8.0, color=INK2)
    for t, c in zip(ax.get_xticklabels(), cols):
        t.set_color(c)
    ax.axhline(48, color=GRID, lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.text(-0.62, 49.4, "48 episodes = 48 final rounds available",
            fontsize=7.0, color=MUT, ha="left", va="bottom")
    record[opp] = {k: D["per_cell"][k] for k in keys}



# ------------------------------------------------------------------- main --

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--blocks", default=str(HERE / "trace_blocks.jsonl"),
                    help="block-level JSONL from score_traces.py; the unit of "
                         "analysis and the source of every number here")
    ap.add_argument("--pooled", default=str(HERE / "trace_markers.json"),
                    help="aggregate marker JSON, read ONLY for panel D's "
                         "pooled all-blocks comparison")
    ap.add_argument("--outdir", default=str(HERE))
    ap.add_argument("--stem", default="fig4_normalised_by_behaviour")
    ap.add_argument("--dpi", type=int, default=150)
    ap.add_argument("--ridge", type=float, default=1e-6,
                    help="ridge on the logistic Newton-Raphson. Present because "
                         "a cell can be separable; at 1e-8 nothing here moves "
                         "in the sixth decimal place.")
    ap.add_argument("--logistic-iters", type=int, default=200)
    ap.add_argument("--min-defections", type=int, default=5,
                    help="in the SECONDARY post-treatment check only, a seed "
                         "whose cell has fewer than this many final-round "
                         "defections is also reported dropped. tft/eg seed 2 "
                         "has 2.")
    ap.add_argument("--empty-answer-flag", type=float, default=0.25,
                    help="flag any cell whose share of DECISION turns with an "
                         "empty answer exceeds this. The repo's invalid_rate "
                         "gate does not catch this failure mode.")
    a = ap.parse_args()          # --help exits here, before anything renders

    blk = Path(a.blocks)
    if not blk.exists():
        print(f"[fig] missing {blk}")
        return 1
    outdir = Path(a.outdir)

    rows = load_blocks(blk)
    D = compute(rows, a.ridge, a.logistic_iters, a.min_defections)

    pooled_con, pooled_meta = {}, {}
    pth = Path(a.pooled)
    if pth.exists():
        P = json.loads(pth.read_text())
        pooled_con, pooled_meta = P.get("contrasts", {}), P.get("meta", {})
    else:
        print(f"[fig] ** {pth} missing: panel D has no pooled comparison **")

    flagged = {k.replace("|", "/s") for k, v in D["empty_answer_rate_decision"].items()
               if (v or 0.0) > a.empty_answer_flag}
    for k in sorted(flagged):
        pc = D["per_cell"][k]
        print(f"[fig] HAZARD {k}: empty-answer on decision turns "
              f"{pc['empty_answer_rate_decision_turns']:.3f}, only "
              f"{pc['n_final_blocks']} usable final-round blocks")

    # ---------------------------------------------------------- geometry --
    # PAGE TEXT IS BUILT BEFORE THE PANELS, because the panels are positioned
    # from its measured height. Every block below wraps to a number of lines
    # that depends on the data in it, so a fixed y offset is exactly how a
    # header line ends up on top of a band heading.
    FIG_W, FIG_H = 22.0, 30.0
    TITLE_PT, HEAD_PT, FOOT_PT = 13.0, 8.4, 8.2
    PT = 1.0 / (FIG_H * 72.0)

    def cols(pt):
        return int(0.982 * FIG_W * 72.0 / (0.555 * pt))

    title, lines, foot = page_text(D, pooled_con, pooled_meta, flagged,
                                   a.empty_answer_flag, a.ridge)
    title = wrap(title, cols(TITLE_PT))
    lines = [wrap(t, cols(HEAD_PT)) for t in lines]
    foot = [(c, wrap(t, cols(FOOT_PT))) for c, t in foot]

    title_lh, head_lh, foot_lh = (TITLE_PT * 1.4 * PT, HEAD_PT * 1.5 * PT,
                                  FOOT_PT * 1.5 * PT)
    head_h = nlines(title) * title_lh + 0.010 + sum(
        nlines(t) * head_lh + 0.0035 for t in lines)
    foot_h = sum(nlines(t) * foot_lh + 0.0060 for _, t in foot)

    fig = plt.figure(figsize=(FIG_W, FIG_H))
    fig.patch.set_facecolor(PAPER)

    BAND_HEAD, BAND_GAP = 0.024, 0.048
    page_top = 0.997 - head_h - BAND_HEAD
    page_bot = 0.012 + foot_h + 0.030
    band_h = (page_top - page_bot - BAND_GAP) / 2.0
    if band_h < 0.18:
        print(f"[fig] ** only {band_h:.3f} of figure height left per band; "
              f"the page text has outgrown FIG_H={FIG_H} **")
    band_span = [(page_top, page_top - band_h),
                 (page_top - band_h - BAND_GAP, page_bot)]
    grids = [fig.add_gridspec(2, 6, top=t, bottom=b,
                              height_ratios=[1.45, 1.0], hspace=0.40,
                              wspace=1.05, left=0.042, right=0.988)
             for t, b in band_span]


    # ------------------------------------------------- shared axis limits --
    # Same panel position holds the same quantity on the same scale in both
    # bands, so any vertical difference between the bands is the effect of
    # forgiveness and nothing else.
    def span(vals, pad_lo=0.16, pad_hi=0.16):
        vals = [v for v in vals if v is not None]
        lo, hi = min(vals + [0.0]), max(vals + [0.0])
        r = (hi - lo) or 1.0
        return lo - r * pad_lo, hi + r * pad_hi


    a_vals, b_vals, c_vals, d_vals = [], [], [], []
    for opp, _ in BANDS:
        rec = D["opp"][opp]
        sens = rec["sensitivity_drop_flagged"]
        for cur, sn in ([(rec["behaviour"], sens["behaviour"])]
                        + [(rec["markers"][m][PRIMARY], sens[m][PRIMARY])
                           for m in MARKER_KEYS]):
            a_vals += [v for v in cur["per_seed"] if v is not None]
            a_vals += [cur["delta"] + (cur["se"] or 0), cur["delta"] - (cur["se"] or 0),
                       sn["delta"]]
        for m in MARKER_KEYS:
            for kind, _, _, _ in ESTIMATORS:
                c = rec["markers"][m][kind]
                if c["delta"] is None:
                    continue
                b_vals += [c["delta"] + (c["se"] or 0), c["delta"] - (c["se"] or 0)]
            f = rec["markers"][m][PRIMARY]
            d_vals += [f["delta"] + (f["se"] or 0), f["delta"] - (f["se"] or 0)]
            p = (pooled_con.get(opp) or {}).get(m[2:])
            if p:
                d_vals += [p["strat_delta_mean"] + p["strat_delta_se"],
                           p["strat_delta_mean"] - p["strat_delta_se"]]
        for k in ("all_blocks", "final_round"):
            c = rec["length"][k]
            c_vals += list(c["per_seed"]) + [c["delta"] + c["se"], c["delta"] - c["se"]]

    # headroom at the top of A and B for the monospace number blocks, at the
    # bottom of A for the ratio caveat and of B for the four-glyph key
    ylim_a = span(a_vals, 0.15, 0.36)
    ylim_b = span(b_vals, 0.28, 0.34)
    ylim_c = span(c_vals, 0.20, 0.24)
    ylim_d = span(d_vals, 0.22, 0.30)

    # -------------------------------------------------------------- draw --
    R = {"panelA": {}, "panelB": {}, "panelC": {}, "panelD": {}, "panelE": {}}
    for bi, (opp, heading) in enumerate(BANDS):
        gs = grids[bi]
        rec = D["opp"][opp]

        axA = fig.add_subplot(gs[0, 0:3])
        panel_behaviour_vs_reasoning(axA, opp, D, ylim_a, R["panelA"])
        style(axA, f"A{bi + 1}  -  BEHAVIOUR against REASONING, "
                       f"denominator matched by construction",
              "delta(eg - nohole) on final-round decision blocks",
              f"every episode has exactly one final round, so both arms bring ~48 blocks per cell whatever they do "
              f"(n = {rec['n_final_blocks']} for {opp}).\nreasoning markers are the "
              f"PRIMARY {PRIMARY} estimate; the grey band is the FLOOR control's "
              f"own interval, extended across the reasoning half.")

        axB = fig.add_subplot(gs[0, 3:6])
        panel_estimators(axB, opp, D, ylim_b, R["panelB"])
        style(axB, f"B{bi + 1}  -  the same four markers, adjusted for length "
                   f"FOUR ways.  agreement is the point",
              "delta(eg - nohole)",
              "raw is FLATTERED here: at the final round the eg arm writes LONGER, the opposite of the pooled corpus.\n"
              "all three adjustments pull the same way and land in the same place, which is why any of them can be believed.")

        axC = fig.add_subplot(gs[1, 0:2])
        panel_length(axC, opp, D, ylim_c, R["panelC"])
        style(axC, f"C{bi + 1}  -  why the adjustment is mandatory, and which "
                   f"way it cuts", "delta(eg - nohole) mean chars per block",
              "a marker hit is BINARY PER BLOCK and rises steeply\n"
              "with length, and the sign of the length gap REVERSES\n"
              "between the two conditionings -- so the raw final-round\n"
              "number is flattered, not deflated.")

        axD = fig.add_subplot(gs[1, 2:4])
        panel_pooled_vs_final(axD, opp, D, pooled_con, ylim_d, R["panelD"])
        style(axD, f"D{bi + 1}  -  this does NOT overturn the pooled result",
              "length-standardised delta(eg - nohole)",
              "two conditionings of the same data, both correct for\n"
              "what they measure. the pooled one is dominated by the\n"
              f"{100 * (1 - D['n_final_round_decision_blocks_contrast_arms'] / D['n_blocks_total']):.0f}% "
              f"of blocks that are not final-round decisions.")

        axE = fig.add_subplot(gs[1, 4:6])
        panel_cells(axE, opp, D, flagged, R["panelE"])
        style(axE, f"E{bi + 1}  -  the cell census: is the denominator really "
                   f"matched?", "usable final-round decision blocks",
              "hue is CONDITION here because this panel draws LEVELS,\n"
              "not differences. matched everywhere except the flagged\n"
              "cell, which is hatched and is the one the orange crosses\n"
              "in panel A drop.")

    # Band headings LAST, in figure coords, read off the finished layout.
    for bi, (_, heading) in enumerate(BANDS):
        top = band_span[bi][0]
        fig.text(0.012, top + BAND_HEAD * 0.78, heading, fontsize=13.0,
                 color=INK, fontweight="bold", va="bottom", ha="left")
        fig.add_artist(plt.Line2D([0.012, 0.988], [top + BAND_HEAD * 0.60] * 2,
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
        y -= nlines(t) * foot_lh + 0.0060

    png = outdir / f"{a.stem}.png"
    fig.savefig(png, dpi=a.dpi, facecolor=fig.get_facecolor())
    print(f"[fig] wrote {png}")

    # --------------------------------------------------------------- json --
    out = {
        "figure": png.name,
        "question": "With the BEHAVIOUR normalised out -- restricting to "
                    "final-round decision blocks, where every episode "
                    "contributes exactly one and the denominator is therefore "
                    "matched by construction -- does the endgame penalty move "
                    "endgame REASONING, and is the movement endgame-specific?",
        "answer": {
            "headline": title.replace("\n", " "),
            "behaviour_vs_reasoning": {
                opp: {
                    "behaviour_delta": D["opp"][opp]["behaviour"]["delta"],
                    "plans_to_betray_delta":
                        D["opp"][opp]["markers"]["m_endgame_defect_plan"][PRIMARY]["delta"],
                    "plans_to_hold_delta":
                        D["opp"][opp]["markers"]["m_endgame_hold"][PRIMARY]["delta"],
                    "floor_control_delta":
                        D["opp"][opp]["markers"][FLOOR][PRIMARY]["delta"],
                    "plans_to_betray_over_behaviour_ratio":
                        plan_ratio(D["opp"][opp]),
                } for opp, _ in BANDS},
            "substantive_claim":
                "Opposite signs on the two directional endgame markers -- "
                "plans-to-betray down, plans-to-HOLD up -- with the generic "
                "in_game_penalty FLOOR control flat or rising. Neither a "
                "verbosity artifact (which moves every binary marker the same "
                "way) nor blanket suppression (which takes the floor with it) "
                "produces that pattern.",
            "size":
                "The reasoning move is much smaller than the behavioural one: "
                f"about a {frac(plan_ratio(D['opp']['grim'])['mean'])} against "
                f"grim and a {frac(plan_ratio(D['opp']['tft'])['mean'])} against "
                "tft, averaging the three length-adjusted estimators. That "
                "ratio is an ORDER-OF-MAGNITUDE statement, not a measurement "
                "-- see caveats.behaviour_bars_are_seed_driven.",
            "does_not_overturn_pooled": True,
        },
        "caveats": {
            "behaviour_bars_are_seed_driven":
                "The final-round behaviour deltas here carry very wide "
                "between-seed bars (grim +/-0.201, tft +/-0.276) because each "
                "is driven by ONE seed: grim/eg seed 2 defects on 0.385 of its "
                "final rounds and tft/eg seed 2 on 0.043, against ~0.8-1.0 "
                "everywhere else. THE BEHAVIOURAL RESULT DOES NOT REST ON THIS "
                f"EVAL: it rests on the training logs, grim "
                f"{TRAINLOG_BEHAVIOUR['grim'][0]:+.3f} +/- "
                f"{TRAINLOG_BEHAVIOUR['grim'][1]:.3f} and tft "
                f"{TRAINLOG_BEHAVIOUR['tft'][0]:+.3f} +/- "
                f"{TRAINLOG_BEHAVIOUR['tft'][1]:.3f} over 3 seeds "
                f"({TRAINLOG_SOURCE}).",
            "compromised_cell":
                "grim/nohole seed 1 contributes "
                f"{D['per_cell']['grim/nohole/s1']['n_final_blocks']} usable "
                "final-round blocks against 47-48 for every other cell, because "
                f"{D['per_cell']['grim/nohole/s1']['empty_answer_rate_decision_turns']:.3f} "
                "of its decision turns emit an empty answer. tft/nohole seed 0 "
                f"is at "
                f"{D['per_cell']['tft/nohole/s0']['empty_answer_rate_decision_turns']:.3f}. "
                "Both are drawn hatched in panel E and both drive the orange "
                "drop-that-cell sensitivity point. Those sensitivity estimates "
                "rest on 2 seeds and carry no usable error bar.",
            "marginal_significance":
                "Several estimates sit at 1.5-2 sigma on the between-seed bar "
                "and none of them is drawn as decisive. See "
                "sigma_on_primary_estimator for every one of them, computed at "
                "render time.",
            "implausible_logistic_se":
                "tft m_backward_induction logistic_adj has SE "
                f"{D['opp']['tft']['markers']['m_backward_induction']['logistic_adj']['se']:.4f}, "
                "which is three seeds happening to agree closely rather than a "
                "precise measurement. The stratified value is primary and that "
                "logistic SE is never headlined.",
            "conditioning":
                "Restricting to the final round conditions on OPPORTUNITY, "
                "which is pre-treatment and matched by construction. "
                "Additionally conditioning on actually defecting is "
                "POST-TREATMENT and is carried under "
                "secondary_post_treatment_conditioning, never as primary, "
                "because tft/eg seed 2 defects on only 2 of its 47 final "
                "rounds. It reproduces the primary sign on all four markers "
                "against grim and on three of four against tft; the exception "
                "is tft m_endgame_hold, which flips on that two-block cell "
                "alone -- see sign_agreement_with_primary and drop_tiny_cells "
                "under each marker.",
            "relationship_to_pooled_analysis":
                "This does not overturn research_logs/0830-endgame-traces.md "
                "section 4. It is a different conditioning of the same data and "
                "both are correct for what they measure: the pooled estimate is "
                "dominated by the blocks that are not final-round decisions. "
                "Panel D draws the pair.",
        },
        "definitions": {
            "final_round_decision_block":
                "in_decision == True and answer_defect is not None and "
                "rounds_from_end == 0",
            "error_bars":
                "BETWEEN TRAINING SEED on the DIFFERENCE: the eg - nohole delta "
                "is formed within a matched training seed and only then "
                "averaged; the bar is sd(per-seed deltas)/sqrt(n_seeds), "
                "n = 3. Seeds are never pooled into one rate.",
            "raw": "Unadjusted difference of final-round marker rates.",
            "strat_global":
                "Direct standardisation to n_chars quintile bins whose edges are "
                "cut over ALL blocks in trace_blocks.jsonl, with the standard "
                "population being the bin distribution of the pooled "
                "(nohole + eg) final-round blocks for that opponent. Each arm "
                "is standardised over the bins it occupies, with the standard "
                "weights renormalised over those bins; the two standardised "
                "rates are then differenced.",
            "strat_finalround":
                "Identical, with the quintile edges recut over the final-round "
                "blocks of the four contrast arms only.",
            "logistic_adj":
                "Per seed, logistic regression of the marker hit on "
                "[intercept, log(n_chars), arm == eg] over that seed's pooled "
                "nohole + eg final-round blocks; the reported value is the "
                "marginal effect of the arm term evaluated at the pooled mean "
                f"log-length. Newton-Raphson, ridge {a.ridge:g}, "
                f"{a.logistic_iters} iterations.",
            "primary_estimator": PRIMARY,
            "sensitivity": "Flagged cell dropped, 2 seeds, drawn as an orange "
                           "cross with no error bar.",
        },
        "source": {
            "block_jsonl": blk.name,
            "pooled_marker_json": pth.name if pth.exists() else None,
            "upstream": pooled_meta.get("source"),
            "generated_utc": pooled_meta.get("generated_utc"),
            "source_mtime_utc": pooled_meta.get("source_mtime_utc"),
            "source_bytes": pooled_meta.get("source_bytes"),
            "n_blocks_total": D["n_blocks_total"],
            "n_final_round_decision_blocks_all_arms":
                D["n_final_round_decision_blocks_all_arms"],
            "n_final_round_decision_blocks_contrast_arms":
                D["n_final_round_decision_blocks_contrast_arms"],
            "training_log_behaviour_reference": {
                "grim": {"delta": TRAINLOG_BEHAVIOUR["grim"][0],
                         "se": TRAINLOG_BEHAVIOUR["grim"][1]},
                "tft": {"delta": TRAINLOG_BEHAVIOUR["tft"][0],
                        "se": TRAINLOG_BEHAVIOUR["tft"][1]},
                "source": TRAINLOG_SOURCE,
                "note": "The only literals on this figure.",
            },
        },
        "quintile_edges_global": D["edges"]["global"],
        "quintile_edges_finalround": D["edges"]["finalround"],
        "hazard_screen": {
            "criterion": f"empty answer on more than {a.empty_answer_flag} of "
                         f"DECISION turns",
            "why_the_usual_gate_misses_it":
                "The repo gate is invalid_rate > 0.15. invalid_rate counts "
                "actions the environment had to substitute; it does not count "
                "decision turns that produced no answer text at all. "
                "grim/nohole seed 1 reads invalid_rate 0.000.",
            "flagged_cells": sorted(flagged),
            "empty_answer_rate_decision_turns": D["empty_answer_rate_decision"],
        },
        "panelA_behaviour_vs_reasoning": R["panelA"],
        "panelB_four_length_adjustments": R["panelB"],
        "panelC_length_reversal": R["panelC"],
        "panelD_pooled_vs_final_round": R["panelD"],
        "panelE_cell_census": R["panelE"],
        "per_cell": D["per_cell"],
    }

    # every sigma on the primary estimator, so "1.5-2 sigma" is checkable
    sig = {}
    for opp, _ in BANDS:
        sig[f"{opp}/behaviour"] = _sigma(D["opp"][opp]["behaviour"])
        for m in MARKER_KEYS:
            sig[f"{opp}/{m}"] = _sigma(D["opp"][opp]["markers"][m][PRIMARY])
    out["sigma_on_primary_estimator"] = sig
    out["intervals_not_crossing_zero"] = sorted(
        k for k, v in sig.items() if v is not None and v >= 1.0)

    for opp, _ in BANDS:
        out.setdefault("secondary_post_treatment_conditioning", {})[opp] = \
            D["opp"][opp]["post_treatment"]
        out.setdefault("sensitivity_drop_flagged", {})[opp] = \
            D["opp"][opp]["sensitivity_drop_flagged"]

    js = outdir / f"{a.stem}.json"
    js.write_text(json.dumps(out, indent=1))
    print(f"[fig] wrote {js}")

    for opp, _ in BANDS:
        rec = D["opp"][opp]
        print(f"[fig] --- {opp}   behaviour {rec['behaviour']['delta']:+.4f} "
              f"+/- {rec['behaviour']['se']:.4f}")
        for m in MARKER_KEYS:
            cells_ = rec["markers"][m]
            print(f"[fig] {m:>22}: " + " | ".join(
                f"{k} {cells_[k]['delta']:+.4f} +/- {cells_[k]['se']:.4f}"
                for k, _, _, _ in ESTIMATORS))
    return 0


def _sigma(c):
    if c["delta"] is None or not c["se"]:
        return None
    return abs(c["delta"]) / c["se"]


# ------------------------------------------------------------- page text --

def page_text(D, pooled_con, pooled_meta, flagged, empty_flag, ridge):
    """Suptitle, header block and footer block. Every number read from data.

    A stale hardcoded string is the worst defect this family of figures has
    had, so nothing here is written by hand except the two training-log
    behaviour numbers, which are constants with their source printed beside
    them.
    """
    g, t = D["opp"]["grim"], D["opp"]["tft"]

    def pm(c, dp=3):
        return f"{c['delta']:+.{dp}f} +/- {c['se']:.{dp}f}"

    def M(rec, m, kind=PRIMARY):
        return rec["markers"][m][kind]

    rr_g, rr_t = plan_ratio(g), plan_ratio(t)

    title = (
        "Normalised by behaviour, the reasoning effect does NOT vanish -- and "
        "unlike the pooled analysis it is endgame-SPECIFIC. On final-round "
        "decision blocks, where both arms contribute ~48 blocks per cell no "
        "matter how much they betray, plans-to-betray falls "
        f"{pm(M(g, 'm_endgame_defect_plan'))} (grim) and "
        f"{pm(M(t, 'm_endgame_defect_plan'))} (tft)\nwhile plans-to-HOLD RISES "
        f"{pm(M(g, 'm_endgame_hold'))} and {pm(M(t, 'm_endgame_hold'))}, and the "
        f"generic punishment FLOOR control does not fall at all "
        f"({pm(M(g, FLOOR))} grim, {pm(M(t, FLOOR))} tft). The reasoning move is "
        f"far smaller than the behavioural one -- about a {frac(rr_g['mean'])} "
        f"of it against grim and a {frac(rr_t['mean'])} against tft, an "
        f"ORDER-OF-MAGNITUDE statement and not a precise ratio.")

    lines = [
        "Qwen3.8-27B, thinking on, iterated prisoner's dilemma, step 35, scored "
        "off raw chain-of-thought text. Two contrast arms differing in ONE "
        "thing: orange adds a hidden reward charge on late betrayal. "
        f"THE RESTRICTION THAT DEFINES THIS FIGURE: in_decision == True and "
        f"answer_defect is not None and rounds_from_end == 0, which keeps "
        f"{D['n_final_round_decision_blocks_contrast_arms']} of the "
        f"{D['n_blocks_total']} blocks in the four contrast arms.",
        "WHY THAT IS THE RIGHT NORMALISATION, AND IT IS THE WHOLE POINT OF THE "
        "FIGURE. Every episode has exactly one final round. So each "
        "(opponent, arm, seed) cell contributes ~48 final-round decision blocks "
        "REGARDLESS OF HOW MUCH LATE BETRAYAL IT ACTUALLY DOES -- the "
        "denominator is matched BY CONSTRUCTION rather than by adjustment. A "
        "difference measured here therefore CANNOT be 'the eg arm simply did "
        "less endgame behaviour overall', because that is exactly the quantity "
        "that has been divided out. The pooled analysis in fig1/fig2 has no "
        "such protection: it runs over all "
        f"{D['n_blocks_total']} blocks, the overwhelming majority of which are "
        "turns with nothing to do with the endgame.",
        f"ERROR BARS ARE BETWEEN TRAINING SEED, n = 3, ON THE DIFFERENCE. The "
        f"eg - nohole delta is formed WITHIN a matched training seed and only "
        f"then averaged; the bar is sd(per-seed deltas)/sqrt(3). Seeds are never "
        f"pooled into a single rate. The small grey glyphs beside each estimate "
        f"in panels A and C are those per-seed deltas, one glyph shape per seed. "
        f"The orange cross is the same estimate with the flagged cell dropped: "
        f"2 seeds, no bar, shown to test a sign and not to replace an estimate.",
        "THE LENGTH ADJUSTMENT IS NOT OPTIONAL AND HERE IT CUTS THE OTHER WAY "
        "(panel C). Pooled over all blocks the penalty makes the reasoning "
        f"SHORTER against tft ({t['length']['all_blocks']['delta']:+.0f} +/- "
        f"{t['length']['all_blocks']['se']:.0f} chars). At the FINAL ROUND the eg "
        f"arm writes LONGER: {t['length']['final_round']['delta']:+.0f} +/- "
        f"{t['length']['final_round']['se']:.0f} against tft and "
        f"{g['length']['final_round']['delta']:+.0f} +/- "
        f"{g['length']['final_round']['se']:.0f} against grim. A marker hit is "
        f"BINARY PER BLOCK and rises steeply with length, so the raw final-round "
        f"number is FLATTERED by length -- the opposite direction from the "
        f"pooled analysis, where length deflated it. Panel B therefore reports "
        f"every marker four ways: raw, standardised to the GLOBAL length "
        f"quintiles, standardised to quintiles recut over the FINAL-ROUND blocks, "
        f"and a per-seed logistic regression on [1, log(n_chars), arm == eg] "
        f"reporting the arm term's marginal effect at the pooled mean "
        f"log-length (Newton-Raphson, ridge {ridge:g}). All three adjustments "
        f"agree, which is why any of them can be believed; "
        f"{PRIMARY} is the PRIMARY estimator and is what panel A draws.",
        "WHY THE PATTERN IS THE ARGUMENT, not any single number. Verbosity "
        "moves every binary marker the SAME way, and blanket suppression takes "
        "the FLOOR control down with the signal. Here the two directional "
        "endgame markers move in OPPOSITE directions -- betray-plans down, "
        "hold-plans up -- while the generic punishment floor is flat or rising. "
        "No verbosity artifact and no blanket suppression produces that shape.",
        "OPPONENT IS BAND POSITION, never hue, so the condition colours keep the "
        "meaning they have everywhere else in this study (purple baseline, "
        "orange endgame penalty, blue hidden horizon, and blue is used for "
        "nothing else -- no inf arm appears here). Contrasts are drawn in "
        "NEUTRAL INK: a difference is not a condition. Panel E is the only "
        "panel drawing levels rather than differences and so the only one using "
        "the condition palette. Each panel position shares one y-axis across "
        "both bands, so a vertical difference between bands is the effect of "
        "forgiveness and nothing else.",
    ]

    # ------------------------------------------------------------- footer --
    foot = []

    gb, tb = g["behaviour"], t["behaviour"]
    worst_g = min(range(len(gb["per_seed"])), key=lambda i: gb["per_seed"][i])
    worst_t = min(range(len(tb["per_seed"])), key=lambda i: tb["per_seed"][i])
    foot.append((WARN,
        "THE BEHAVIOURAL BARS ON THIS FIGURE ARE NEARLY USELESS, AND THE "
        "BEHAVIOURAL RESULT DOES NOT REST ON THEM. The final-round defection "
        f"deltas drawn in panel A are {pm(gb)} (grim) and {pm(tb)} (tft), and "
        f"each is driven by ONE seed: the per-seed deltas are "
        + ", ".join(f"{v:+.3f}" for v in gb["per_seed"]) + " for grim and "
        + ", ".join(f"{v:+.3f}" for v in tb["per_seed"]) + " for tft, because "
        f"grim/eg seed {worst_g} defects on only "
        f"{D['per_cell'][f'grim/eg/s{worst_g}']['defect_rate']:.3f} of its final "
        f"rounds and tft/eg seed {worst_t} on "
        f"{D['per_cell'][f'tft/eg/s{worst_t}']['defect_rate']:.3f}, against "
        "0.72-1.00 in every other cell.\n"
        "THE BEHAVIOURAL RESULT PROPER RESTS ON THE TRAINING LOGS -- grim "
        f"{TRAINLOG_BEHAVIOUR['grim'][0]:+.3f} +/- "
        f"{TRAINLOG_BEHAVIOUR['grim'][1]:.3f}, tft "
        f"{TRAINLOG_BEHAVIOUR['tft'][0]:+.3f} +/- "
        f"{TRAINLOG_BEHAVIOUR['tft'][1]:.3f}, three seeds "
        f"({TRAINLOG_SOURCE}) -- NOT on this eval. Consequently the claim that "
        f"'the reasoning moves about a {frac(rr_g['mean'])} (grim) to a "
        f"{frac(rr_t['mean'])} (tft) as much as the behaviour' is an "
        f"ORDER-OF-MAGNITUDE STATEMENT AND NOT A PRECISE ONE. The ratio is "
        f"already unstable across the three length adjustments on its own "
        f"numerator -- {rr_g['min']:.2f} to {rr_g['max']:.2f} for grim and "
        f"{rr_t['min']:.2f} to {rr_t['max']:.2f} for tft -- before any of the "
        f"denominator's fragility is counted. Panel A prints the same warning "
        f"beside the same number."))

    hz = []
    for k in sorted(flagged):
        pc = D["per_cell"][k]
        hz.append(f"{k} ({pc['empty_answer_rate_decision_turns']:.3f} of decision "
                  f"turns empty, {pc['n_final_blocks']} usable final-round "
                  f"blocks, mean {pc['mean_chars']:.0f} chars)")
    foot.append((ORANGE,
        f"THE DENOMINATOR IS MATCHED BY CONSTRUCTION EXCEPT WHERE THE EVAL "
        f"BROKE, AND PANEL E IS THE AUDIT. Screening every contrast cell on the "
        f"share of DECISION turns that emit an EMPTY ANSWER (> {empty_flag:.2f}) "
        f"flags: " + "; ".join(hz) + ". Both read invalid_rate well under the "
        "repo's 0.15 gate -- invalid_rate counts actions the environment had to "
        "substitute, not turns that produced no answer -- so the usual gate does "
        "not see this failure mode. Flagged cells are drawn HATCHED with a '!' "
        "in panel E.\n"
        "Dropping the flagged baseline cell and pairing the remaining two seeds "
        "gives the orange crosses in panel A: grim's plans-to-betray moves "
        f"{M(g, 'm_endgame_defect_plan')['delta']:+.3f} -> "
        f"{g['sensitivity_drop_flagged']['m_endgame_defect_plan'][PRIMARY]['delta']:+.3f} "
        f"and plans-to-HOLD {M(g, 'm_endgame_hold')['delta']:+.3f} -> "
        f"{g['sensitivity_drop_flagged']['m_endgame_hold'][PRIMARY]['delta']:+.3f}; "
        f"tft's move {M(t, 'm_endgame_defect_plan')['delta']:+.3f} -> "
        f"{t['sensitivity_drop_flagged']['m_endgame_defect_plan'][PRIMARY]['delta']:+.3f} "
        f"and {M(t, 'm_endgame_hold')['delta']:+.3f} -> "
        f"{t['sensitivity_drop_flagged']['m_endgame_hold'][PRIMARY]['delta']:+.3f}. "
        "The SIGNS survive on both opponents and both markers, which is all a "
        "two-seed estimate is being asked to do. Every sensitivity point rests "
        "on 2 seeds and carries NO usable error bar; none is drawn."))

    sig = []
    for opp, _ in BANDS:
        rec = D["opp"][opp]
        for m in MARKER_KEYS:
            z = _sigma(M(rec, m))
            if z is not None:
                sig.append((z, f"{opp}/{m[2:]} {pm(M(rec, m))} = {z:.2f} sigma"))
    sig.sort(reverse=True)
    bi_log = t["markers"]["m_backward_induction"]["logistic_adj"]
    foot.append((INK2,
        "NOTHING HERE IS DECISIVE AND NONE OF IT IS DRAWN AS IF IT WERE. On the "
        f"primary {PRIMARY} estimator the eight marker estimates run, largest to "
        "smallest: " + "; ".join(s for _, s in sig) + ". Several sit between 1.5 "
        "and 2 sigma. Read the SHAPE -- opposite signs on the two directional "
        "markers with the floor flat -- rather than any one interval, and note "
        "that a pattern argument is not licence to treat its individual "
        "components as significant.\n"
        f"ONE INTERVAL ON THIS FIGURE SHOULD NOT BE BELIEVED AT ALL: the tft "
        f"backward_induction logistic_adj SE of +/-{bi_log['se']:.3f} (per-seed "
        + ", ".join(f"{v:+.3f}" for v in bi_log["per_seed"]) + "). Three seeds "
        "happened to agree to the third decimal place; that is not precision, "
        "and with n = 3 an SE that small is a coincidence rather than a "
        "measurement. It is annotated in panel B where it is drawn, the "
        "stratified value is presented as primary, and that logistic SE is "
        "headlined nowhere."))

    pooled_txt = []
    for opp, _ in BANDS:
        p = (pooled_con.get(opp) or {}).get("endgame_defect_plan")
        if p:
            pooled_txt.append(
                f"{opp}: pooled {p['strat_delta_mean']:+.3f} +/- "
                f"{p['strat_delta_se']:.3f} over all blocks against "
                f"{pm(M(D['opp'][opp], 'm_endgame_defect_plan'))} at the final "
                f"round")
    foot.append((INK2,
        "THIS DOES NOT OVERTURN THE POOLED RESULT IN research_logs/"
        "0830-endgame-traces.md SECTION 4, AND PANEL D DRAWS BOTH RATHER THAN "
        "ASSERTING A WINNER. That analysis and this one are DIFFERENT "
        "CONDITIONINGS OF THE SAME DATA and both are correct for what they "
        "measure. The pooled length-standardised delta is computed over all "
        f"{D['n_blocks_total']} blocks, of which only "
        f"{D['n_final_round_decision_blocks_contrast_arms']} are final-round "
        "decisions in the contrast arms -- so it is dominated by turns with no "
        "endgame content, where there is little for an endgame marker to do and "
        "the floor control and the signal have every reason to move together. "
        "On plans-to-betray, " + "; ".join(pooled_txt) + ".\n"
        "The pooled figure's own conclusion -- that after length "
        "standardisation the fall is indistinguishable from the floor control "
        "-- remains the right reading OF THE POOLED QUANTITY. What this figure "
        "adds is that the pooled quantity was the wrong denominator for the "
        "question, not that the pooled arithmetic was wrong."))

    pt_g = g["post_treatment"]
    pt_t = t["post_treatment"]
    foot.append((INK,
        "WHAT THE RESTRICTION CONDITIONS ON, AND WHY THAT IS SAFE. The final "
        "round arrives whether or not the policy uses it, so restricting to it "
        "conditions on OPPORTUNITY -- a pre-treatment variable, matched by "
        "construction, and not a collider. Additionally conditioning on the "
        "block having ACTUALLY DEFECTED would be POST-TREATMENT conditioning on "
        "the outcome the treatment moves. That version was computed and is in "
        "the paired JSON under secondary_post_treatment_conditioning. It is NOT "
        "shown as primary and it should not be quoted, because tft/eg seed 2 "
        f"defects on only {pt_t['n_blocks_per_cell']['tft/eg/s2']} of its 47 "
        f"final rounds -- that cell's conditional rates rest on two blocks.\n"
        f"REPORTED EXACTLY AS IT CAME OUT: it reproduces the primary sign on "
        f"all four markers against grim (plans-to-betray "
        f"{pt_g['m_endgame_defect_plan']['delta']:+.3f}, plans-to-HOLD "
        f"{pt_g['m_endgame_hold']['delta']:+.3f}) and on three of four against "
        f"tft (plans-to-betray {pt_t['m_endgame_defect_plan']['delta']:+.3f}, "
        f"floor {pt_t['m_in_game_penalty']['delta']:+.3f}). THE ONE THAT FLIPS "
        f"is tft plans-to-HOLD, {pt_t['m_endgame_hold']['delta']:+.3f} against "
        f"the primary {M(t, 'm_endgame_hold')['delta']:+.3f}, and it flips "
        f"entirely on the two-block cell: its per-seed values are "
        + ", ".join(f"{v:+.3f}" for v in pt_t["m_endgame_hold"]["per_seed"])
        + f", and dropping the seeds with fewer than "
        f"{pt_t['min_defections_threshold']} defections leaves "
        f"{pt_t['m_endgame_hold']['drop_tiny_cells']['delta']:+.3f} on "
        f"{pt_t['m_endgame_hold']['drop_tiny_cells']['n_seeds']} seeds. That is "
        "an explanation of the flip, not a repair of it; the honest summary is "
        "that the post-treatment version is too thin on tft to test anything, "
        "which is why it is secondary.\n"
        "None of this is an equivalence claim in either direction, and with "
        "three training seeds it could not be. Every number drawn here is "
        "recomputed from trace_blocks.jsonl at render time; the only literals "
        f"are the two training-log behaviour figures, which are labelled with "
        f"their source ({TRAINLOG_SOURCE})."))

    return title, lines, foot


if __name__ == "__main__":
    raise SystemExit(main())
