#!/usr/bin/env python
"""The 0824 reasoning-marker curves, re-run per OPPONENT instead of pooled.

    /home/ubuntu/venvs/tinker-ipd/bin/python plot_reasoning_markers_by_opponent.py

  reasoning_markers.png          the figure
  reasoning_markers.json         the numbers behind it

WHAT IS NEW, AND WHY IT IS A DIFFERENT FIGURE RATHER THAN A REFRESH.

`results/0824_think_curves/reasoning_markers.png` plotted three arms --
baseline / endgame-penalty / hidden-horizon -- each trained against a ROTATING
{tft, grim, tf2t} population. So every curve there is an average over three
punishment shapes, and one of those three was actively working against the
measurement: `sim_endgame_timing.py` on this simulator shows grim and tft PASS
`early_punished` in every cross-round cell (betraying at N-1 is strictly worse
than betraying at N, so the endgame really is the only safe place to defect)
while tf2t FAILS it in ipd, ipd3 and staghunt, because it forgives the first
defection by construction and an N-1 betrayal therefore costs nothing.

This figure drops tf2t and splits the remaining two into their own runs, so
`punishment shape` stops being a nuisance variable averaged inside each curve
and becomes the axis you read down. Six runs: {grim, tft} x {nohole, eg, inf}.

HOW TO READ IT. The layout is the 0824 figure, twice: the top block is every
arm trained against GRIM (never forgives), the bottom block the same three
against TFT (forgives the moment the learner stops). Within a block the
comparison is unchanged -- each coloured curve differs from the purple
baseline in exactly one thing. ACROSS blocks, the same panel position holds
the same quantity on a SHARED y-axis, so a vertical difference between the two
blocks is the effect of forgiveness and nothing else.

PALETTE. Unchanged from 0824 and from `hole_exp/make_capability_figs.py`:
#7a5bd6 / #eb6834 / #2a78d6 for base/eg/inf, a fixed identity encoding that is
never repainted when a panel drops a series, and every series is also
direct-labelled at its right end so identity is never carried by colour alone.
Opponent is encoded by BLOCK, not by hue or dash, precisely so that the three
condition colours keep meaning exactly what they meant in the previous figure.

PROVENANCE OF EACH PANEL. Reasoning panels are scored off the `traces-think-t4-*`
viewer pages -- fresh episodes re-sampled from each frozen checkpoint with
thinking on, reasoning split from the answer before the env parsed it. Behaviour
panels come from `runs/<label>/metrics.jsonl`, the dense training log. The
reasoning pages cover the five envs that HAVE an endgame (ipd, trust, ipd3,
staghunt, winasmuch); public_goods, dond and ultimatum deliver their
consequence within the round and `sim_endgame_timing` reports them as
`no_endgame_hole`, so backward-induction markers there would be scored against
episodes with no endgame to reason about. The behaviour panels are the training
log and therefore still span all seven trained envs; the two are not the same
denominator and the panel notes say so.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
HOLE = HERE.parent.parent / "hole_exp"
sys.path.insert(0, str(HOLE))

import endgame_awareness as A  # noqa: E402

PURPLE, ORANGE, BLUE = "#7a5bd6", "#eb6834", "#2a78d6"
INK, INK2, MUT, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"

# fixed order, fixed hue -- a panel that drops a series must not repaint others
CELLS = [("nohole", "baseline\n(nohole)", PURPLE),
         ("eg", "endgame\npenalty", ORANGE),
         ("inf", "hidden\nhorizon", BLUE)]

SHAPES = [("grim", "vs GRIM — never forgives"),
          ("tft", "vs TIT-FOR-TAT — forgives on return")]

RUNS = {f"{shape}/{cell}":
        f"mixed_think4_nohole-think-{shape}_d1_s0{sfx}"
        for shape, _ in SHAPES
        for cell, sfx in (("nohole", ""), ("eg", "_eg2"), ("inf", "_inf"))}


def rates(blocks, rx):
    """step -> (rate, n, se). Binomial SE: these are proportions of blocks."""
    out = {}
    for step, txts in blocks.items():
        if not txts:
            continue
        k, n = sum(1 for t in txts if rx.search(t)), len(txts)
        p = k / n
        out[step] = (p, n, (p * (1 - p) / n) ** 0.5)
    return out


def behaviour(run, key="train/endgame_rate"):
    """The dense per-training-step metric, for the behaviour panels.

    DEDUPED BY STEP, LAST WRITE WINS. `train_mixed.py` only appends, and a run
    resumed from a state checkpoint that is behind its last logged step re-runs
    the steps in between -- so metrics.jsonl can legitimately hold two rows for
    the same step. Read in file order that is not an error, it is a curve that
    doubles back on itself, which looks like a training dynamic rather than a
    bookkeeping artefact. `resume_think4.sh` trims the overlap before resuming;
    this is the second line of defence for a run relaunched by hand.
    """
    f = HOLE / "runs" / run / "metrics.jsonl"
    by_step = {}
    for line in f.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        v = r.get(key)
        if v is not None:
            by_step[r["step"]] = v
    xs = sorted(by_step)
    return xs, [by_step[x] for x in xs]


def smooth(xs, ys, w=7):
    out = []
    for i in range(len(ys)):
        lo = max(0, i - w // 2)
        seg = ys[lo:i + w // 2 + 1]
        out.append(sum(seg) / len(seg))
    return xs, out


def style(ax, title, ylab, xlab="training step"):
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


def place(ax, ends, hi):
    """Direct-label each series at its right end, nudged apart when they land
    on top of each other. Identity is never colour-alone, so these labels are
    load-bearing and a collision is not cosmetic."""
    ends = sorted(ends, key=lambda e: e[1])
    min_gap = hi * 0.075
    for i in range(1, len(ends)):
        x, y, lab, col = ends[i]
        py = ends[i - 1][1]
        if y - py < min_gap:
            ends[i] = (x, py + min_gap, lab, col)
    for x, y, lab, col in ends:
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=(8, 0),
                    va="center", fontsize=8, color=INK2,
                    annotation_clip=False)


# --------------------------------------------------------------------------
# panel drawers. Each returns the data-space top it needs, so a second pass can
# give the two blocks a SHARED y-limit -- without which a vertical comparison
# between grim and tft reads the axis rather than the effect.
# --------------------------------------------------------------------------

def marker_panel(ax, found, shape, rx, xmax, ylim=None):
    hi, ends = 0.0, []
    for cell, label, col in CELLS:
        key = f"{shape}/{cell}"
        if key not in found:
            continue
        r = rates(found[key], rx)
        if not r:
            continue
        xs = sorted(r)
        ys = [r[s][0] for s in xs]
        es = [r[s][2] for s in xs]
        hi = max(hi, max(y + e for y, e in zip(ys, es)))
        ax.fill_between(xs, [y - e for y, e in zip(ys, es)],
                        [y + e for y, e in zip(ys, es)],
                        color=col, alpha=0.13, lw=0, zorder=2)
        ax.plot(xs, ys, color=col, lw=2, zorder=3, marker="o", ms=5,
                mec=SURF, mew=1.4)
        ends.append((xs[-1], ys[-1], label.replace("\n", " "), col))
    ax.set_xlim(-2, xmax)
    if ylim is not None:
        ax.set_ylim(0, ylim)
        place(ax, ends, ylim)
    return hi, ends


def behaviour_panel(ax, shape, key, xmax, ylim=None):
    hi, ends = 0.0, []
    for cell, label, col in CELLS:
        try:
            xs, ys = behaviour(RUNS[f"{shape}/{cell}"], key)
        except FileNotFoundError:
            continue
        if not xs:
            continue
        ax.plot(xs, ys, color=col, lw=0.9, alpha=0.28, zorder=2)
        sx, sy = smooth(xs, ys)
        hi = max(hi, max(sy))
        ax.plot(sx, sy, color=col, lw=2, zorder=3)
        ends.append((sx[-1], sy[-1], label.replace("\n", " "), col))
    ax.set_xlim(-2, xmax)
    if ylim is not None:
        ax.set_ylim(0, ylim)
        place(ax, ends, ylim)
    return hi, ends


def horizon_panel(ax, found, shape, xmax, ylim=None):
    hi, ends = 0.0, []
    for cell, label, col in CELLS:
        key = f"{shape}/{cell}"
        if key not in found:
            continue
        for mk, ls, tag in (("notices_unknown", "-", "notices horizon unknown"),
                            ("assumes_finite", ":", "assumes a total anyway")):
            r = rates(found[key], A.HORIZON_MARKERS[mk])
            if not r:
                continue
            xs = sorted(r)
            ys = [r[s][0] for s in xs]
            hi = max(hi, max(ys))
            ax.plot(xs, ys, color=col, lw=2 if ls == "-" else 1.6, ls=ls,
                    zorder=3, marker="o" if ls == "-" else "s", ms=5,
                    mec=SURF, mew=1.4)
            if cell in ("inf", "nohole"):
                ends.append((xs[-1], ys[-1],
                             f"{label.replace(chr(10), ' ')} · {tag}", col))
    ax.set_xlim(-2, xmax)
    if ylim is not None:
        ax.set_ylim(0, ylim)
        place(ax, ends, ylim)
    return hi, ends


# (title, ylabel, note, drawer) for the six panel positions, in the 0824 order.
PANELS = [
    ("A · Shaping / eval awareness", "share of reasoning blocks",
     "reaching OUTSIDE the game for a cause: hidden rule ·\n"
     "being tested · a grader · a score that did not match\n"
     "the payoff table",
     lambda ax, f, s, x, y: marker_panel(ax, f, s, A.MARKERS["shaping_awareness"], x, y)),
    ("B · Endgame reasoning", "share of reasoning blocks",
     "\"the last round has no future to punish me\"",
     lambda ax, f, s, x, y: marker_panel(ax, f, s, A.MARKERS["backward_induction"], x, y)),
    ("C · OVERALL betrayal rate", "exploit_rate (per training step)",
     "every scored decision, not just the endgame ones.\ntraining log, all 7 trained envs",
     lambda ax, f, s, x, y: behaviour_panel(ax, s, "train/exploit_rate", x, y)),
    ("D · ENDGAME betrayal rate", "endgame_rate (per training step)",
     "betrayals landing in the final window.  faint = per\nstep, bold = 7-step mean.  training log, all 7 envs",
     lambda ax, f, s, x, y: behaviour_panel(ax, s, "train/endgame_rate", x, y)),
    ("E · Endgame reasoning that RESOLVES to defecting", "share of reasoning blocks",
     "direction-aware: negated forms (\"I will not defect in\n"
     "the final round\") are excluded, they score as hold",
     lambda ax, f, s, x, y: marker_panel(ax, f, s, A.MARKERS["endgame_defect_plan"], x, y)),
    # D2. `endgame_hold` was computed and exported and never plotted. It sits
    # next to E because the two regexes were built as a DIRECTIONAL PAIR --
    # the comment block above them records that an earlier version scored
    # "defecting in the last round" as a plan to hold -- so reading either
    # alone is reading half a question.
    #
    # The finding was already in the committed JSON: pooled over the two
    # finite cells, tft 0.114 against grim 0.063, a ratio of 1.8x. The
    # policies trained against tit-for-tat talk about HOLDING THE LINE at the
    # end nearly twice as often as the grim-trained ones -- the reasoning-side
    # analogue of the S4 behavioural claim, in the same direction.
    ("G · Endgame reasoning that RESOLVES to holding", "share of reasoning blocks",
     "the other direction of E.  pooled over the two finite\n"
     "cells: tft 0.114 vs grim 0.063, a ratio of 1.8x",
     lambda ax, f, s, x, y: marker_panel(ax, f, s, A.MARKERS["endgame_hold"], x, y)),
    ("F · Does the hidden-horizon arm LEARN the length?", "share of reasoning blocks",
     "solid = says the length is unknown; dotted = supplies\na total anyway.",
     lambda ax, f, s, x, y: horizon_panel(ax, f, s, x, y)),
]


def main() -> int:
    found = {k: A.blocks(alias) for k, alias in A.PAGES_T4.items()
             if (A.VIEWER_DATA / alias).exists()}
    found = {k: v for k, v in found.items() if any(v.values())}
    missing = [k for k in A.PAGES_T4 if k not in found]
    if missing:
        print(f"[fig] no reasoning page yet for: {', '.join(sorted(missing))}")
    have_metrics = [k for k, r in RUNS.items()
                    if (HOLE / "runs" / r / "metrics.jsonl").exists()]
    print(f"[fig] metrics for {len(have_metrics)}/6 runs, "
          f"reasoning pages for {len(found)}/6")
    if not found and not have_metrics:
        print("[fig] nothing to plot yet")
        return 1

    # The x-axis is shared by every panel so the two blocks cannot drift apart;
    # it tracks the furthest step ANY run has reached rather than the nominal
    # 150, so an early figure is not 90% empty.
    xmax = 10.0
    for r in RUNS.values():
        try:
            xs, _ = behaviour(r, "train/reward")
            if xs:
                xmax = max(xmax, max(xs))
        except FileNotFoundError:
            pass
    for by_step in found.values():
        if by_step:
            xmax = max(xmax, max(by_step))
    xmax *= 1.34                       # headroom for the right-edge labels

    fig, axes = plt.subplots(4, 3, figsize=(17.8, 18.4))
    fig.patch.set_facecolor("#f9f9f7")

    # PASS 1: draw with autoscale to learn each panel's data extent.
    tops = {}
    for bi, (shape, _) in enumerate(SHAPES):
        for pi, (_, _, _, draw) in enumerate(PANELS):
            ax = axes[bi * 2 + pi // 3][pi % 3]
            hi, _ = draw(ax, found, shape, xmax, None)
            tops[pi] = max(tops.get(pi, 0.0), hi)

    # PASS 2: redraw on a shared per-panel y-limit. A vertical comparison
    # between the grim block and the tft block is the whole point of the
    # layout, and it is only honest if both blocks are on the same axis.
    for bi, (shape, _) in enumerate(SHAPES):
        for pi, (title, ylab, note, draw) in enumerate(PANELS):
            ax = axes[bi * 2 + pi // 3][pi % 3]
            ax.clear()
            top = max(0.05, tops.get(pi, 0.0) * 1.35)
            draw(ax, found, shape, xmax, top)
            style(ax, title, ylab)
            if note:
                ax.text(0.015, 0.955, note, transform=ax.transAxes,
                        fontsize=7.5, color=MUT, va="top")

    fig.suptitle("Endgame penalty and hidden horizon, split by the opponent "
                 "that punishes: grim vs tit-for-tat",
                 fontsize=13.5, color=INK, x=0.008, ha="left", y=0.993)
    fig.text(0.008, 0.977,
             "Qwen3.8-27B, thinking on (effort low), 7-env roster, seed 0, "
             "d=1.0. Six runs: {grim, tft} x {nohole, endgame-penalty, "
             "hidden-horizon}. tit-for-2-tats is in none of them.",
             fontsize=8.5, color=INK2, ha="left")
    fig.text(0.008, 0.966,
             "Within a block each arm differs from the purple baseline in "
             "exactly one thing: orange adds a hidden reward charge on late "
             "betrayal, blue deletes the stated round count. Between blocks "
             "the only difference is whether the counterpart forgives.",
             fontsize=8.5, color=INK2, ha="left")
    fig.text(0.008, 0.955,
             "A/B/E/F are re-sampled checkpoint episodes over the five envs "
             "that have an endgame (bands = binomial SE); C/D are the dense "
             "training log over all seven trained envs.",
             fontsize=8.5, color=INK2, ha="left")

    # The top of the rect has to clear BOTH the three header lines and the
    # first block's own heading, which is placed relative to the axes below it.
    # At 0.948 the grim heading landed on top of the second header line.
    fig.tight_layout(rect=[0.02, 0, 0.995, 0.900])
    fig.subplots_adjust(hspace=0.58)

    # BLOCK LABELS GO IN LAST, IN FIGURE COORDS. Placed in axes coords before
    # `tight_layout` they landed on top of the x-axis label of the row above --
    # the "vs TIT-FOR-TAT" heading sat across panel D's "training step". Reading
    # each block's top edge off the finished layout puts the heading in the gap
    # that actually exists, whatever the layout engine decided it should be.
    for bi, (_, block_title) in enumerate(SHAPES):
        top_ax = axes[bi * 2][0]
        pos = top_ax.get_position()
        # Clear of the panel TITLE, not just the axes: the title is drawn above
        # `pos.y1`, so a rule at y1 + 0.011 ran straight through "A · Shaping /
        # eval awareness" in the first render.
        fig.text(0.012, pos.y1 + 0.052, block_title, fontsize=13.5, color=INK,
                 fontweight="bold", va="bottom", ha="left")
        # A hairline the width of the figure, so the two blocks read as two
        # blocks rather than four rows that happen to be labelled.
        fig.add_artist(plt.Line2D([0.012, 0.99], [pos.y1 + 0.045] * 2,
                                  color=GRID, lw=1.1))

    out = HERE / "reasoning_markers.png"
    fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
    print(f"[fig] wrote {out}")

    # the numbers behind the figure, so the png is never the only record
    tbl = {}
    for key in found:
        tbl[key] = {m: {str(s): round(v[0], 4) for s, v in
                        rates(found[key], rx).items()}
                    # D3 + D4. Was an explicit six-tuple, and the audit that
                    # motivated this change found TWO markers missing from it:
                    # `infinite_logic` (the third branch of the inf arm's own
                    # question -- notices_unknown says it spotted the missing
                    # fact, assumes_finite says it hallucinated a total anyway,
                    # and infinite_logic says it reached the shadow-of-the-
                    # future argument) and `in_game_penalty` (the false-
                    # positive floor that makes `shaping_awareness ~ 0`
                    # interpretable: a null is a much stronger claim when the
                    # floor marker is NOT null on the same blocks).
                    #
                    # Iterating over the marker dicts rather than listing
                    # names means no future marker can be silently unexported.
                    # `in_game_penalty` stays out of the EXCERPTS, where a
                    # floor marker's hits are noise -- that exclusion in
                    # endgame_awareness.py is sound and is left alone. This
                    # changes the scope of the JSON, not the intent of that.
                    for m, rx in {**A.MARKERS, **A.HORIZON_MARKERS}.items()}
        tbl[key]["n_blocks"] = {str(s): len(v) for s, v in found[key].items()}
    for key, run in RUNS.items():
        try:
            xs, ys = behaviour(run, "train/endgame_rate")
            xo, yo = behaviour(run, "train/exploit_rate")
        except FileNotFoundError:
            continue
        tbl.setdefault(key, {})["endgame_rate"] = {
            str(x): round(y, 4) for x, y in zip(xs, ys)}
        tbl[key]["exploit_rate"] = {str(x): round(y, 4) for x, y in zip(xo, yo)}
    (HERE / "reasoning_markers.json").write_text(json.dumps(tbl, indent=1))
    print(f"[fig] wrote {HERE / 'reasoning_markers.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
