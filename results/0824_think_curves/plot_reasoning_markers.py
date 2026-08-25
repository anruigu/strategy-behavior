#!/usr/bin/env python
"""What the THINKING says, across training, for the two endgame manipulations.

    /workspace/allie/venvs/marshal/bin/python plot_reasoning_markers.py

  reasoning_markers.png

Companion to `plot_think_curves.py`, which plots what the policies DID. This
plots what they said while doing it, scored off the `traces-think-*` viewer
pages (episodes re-sampled from frozen checkpoints, thinking on, reasoning
split from the answer before the env parsed it) by `hole_exp/endgame_awareness.py`.

THREE ARMS, ONE CONTROL. `nohole` is the baseline: `eg` differs from it only by
a hidden reward charge on late betrayal, `inf` only by deleting the stated
round count from the observation. Everything else -- model, roster, sampling,
seed -- is identical, so a gap between a curve and the purple one is the
manipulation.

WHY A BEHAVIOUR PANEL SITS BESIDE THE REASONING PANELS. The interesting result
is that the two do not move together. `inf` suppresses endgame BEHAVIOUR from
step 0 (panel D) while still REASONING about endgames at control rates (panel
B) -- it runs the same backward-induction argument and reaches the opposite
conclusion because it cannot locate the end. Plotting only reasoning, or only
behaviour, hides that.

PALETTE. base/eg/inf are an identity encoding, so they take three categorical
hues in a fixed order and are never recoloured when a panel drops a series.
#7a5bd6 / #eb6834 / #2a78d6 is the trio already validated for this study in
`hole_exp/make_capability_figs.py` (worst adjacent CVD dE 24.7 protan, normal
30.9, contrast >= 3:1). Identity is never carried by colour alone: every series
is also direct-labelled at its right end.
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
ARMS = [("nohole", "baseline\n(nohole)", PURPLE),
        ("eg", "endgame\npenalty", ORANGE),
        ("inf", "hidden\nhorizon", BLUE)]
RUNS = {"nohole": "mixed_think2_nohole-think_d1_s0",
        "eg": "mixed_think2_nohole-think_d1_s0_eg2",
        "inf": "mixed_think2_nohole-think_d1_s0_inf"}


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
    """The dense per-training-step metric, for the behaviour panel."""
    f = HOLE / "runs" / run / "metrics.jsonl"
    xs, ys = [], []
    for line in f.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        v = r.get(key)
        if v is not None:
            xs.append(r["step"])
            ys.append(v)
    return xs, ys


def smooth(xs, ys, w=7):
    out = []
    for i in range(len(ys)):
        lo = max(0, i - w // 2)
        seg = ys[lo:i + w // 2 + 1]
        out.append(sum(seg) / len(seg))
    return xs, out


def style(ax, title, ylab, xlab="training step"):
    ax.set_title(title, fontsize=11, color=INK, loc="left", pad=9)
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
    load-bearing and a collision is not cosmetic -- in the first render
    `endgame penalty` sat directly on the `hidden horizon` curve."""
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


def marker_panel(ax, found, rx, title, ylab, note=None):
    hi, ends = 0.0, []
    for arm, label, col in ARMS:
        if arm not in found:
            continue
        r = rates(found[arm], rx)
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
                mec=SURF, mew=1.4)          # 2px surface ring on the markers
        ends.append((xs[-1], ys[-1], label.replace("\n", " "), col))
    style(ax, title, ylab)
    top = max(0.05, hi * 1.35)
    ax.set_ylim(0, top)
    ax.set_xlim(-4, 96)
    place(ax, ends, top)
    if note:
        ax.text(0.015, 0.955, note, transform=ax.transAxes, fontsize=7.5,
                color=MUT, va="top")


def main() -> int:
    found = {arm: A.blocks(A.PAGES[arm]) for arm in RUNS
             if (A.VIEWER_DATA / A.PAGES[arm]).exists()}
    missing = [a for a in RUNS if a not in found]
    if missing:
        print(f"[fig] no trace page for: {', '.join(missing)}")

    fig, axes = plt.subplots(2, 3, figsize=(17.4, 8.6))
    fig.patch.set_facecolor("#f9f9f7")

    # A-D are the four quantities the predictions were made on, in that order.
    marker_panel(
        axes[0][0], found, A.MARKERS["shaping_awareness"],
        "A · Shaping / eval awareness",
        "share of reasoning blocks",
        note="reaching OUTSIDE the game for a cause: hidden rule ·\n"
             "being tested · a grader · a score that did not match\n"
             "the payoff table")
    marker_panel(
        axes[0][1], found, A.MARKERS["backward_induction"],
        "B · Endgame reasoning",
        "share of reasoning blocks",
        note="\"the last round has no future to punish me\"")

    ax = axes[0][2]
    hi, ends = 0.0, []
    for arm, label, col in ARMS:
        try:
            xs, ys = behaviour(RUNS[arm], "train/exploit_rate")
        except FileNotFoundError:
            continue
        if not xs:
            continue
        ax.plot(xs, ys, color=col, lw=0.9, alpha=0.28, zorder=2)
        sx, sy = smooth(xs, ys)
        hi = max(hi, max(sy))
        ax.plot(sx, sy, color=col, lw=2, zorder=3)
        ends.append((sx[-1], sy[-1], label.replace("\n", " "), col))
    style(ax, "C · OVERALL betrayal rate", "exploit_rate (per training step)")
    top = max(0.05, hi * 1.35)
    ax.set_ylim(0, top)
    ax.set_xlim(-4, 96)
    place(ax, ends, top)
    ax.text(0.015, 0.955, "every scored decision, not just the endgame ones",
            transform=ax.transAxes, fontsize=7.5, color=MUT, va="top")

    ax = axes[1][0]
    hi, ends = 0.0, []
    for arm, label, col in ARMS:
        try:
            xs, ys = behaviour(RUNS[arm])
        except FileNotFoundError:
            continue
        if not xs:
            continue
        ax.plot(xs, ys, color=col, lw=0.9, alpha=0.28, zorder=2)
        sx, sy = smooth(xs, ys)
        hi = max(hi, max(sy))
        ax.plot(sx, sy, color=col, lw=2, zorder=3)
        ends.append((sx[-1], sy[-1], label.replace("\n", " "), col))
    style(ax, "D · ENDGAME betrayal rate", "endgame_rate (per training step)")
    top = max(0.05, hi * 1.35)
    ax.set_ylim(0, top)
    ax.set_xlim(-4, 96)
    place(ax, ends, top)
    ax.text(0.015, 0.955,
            "betrayals landing in the final window.  faint = per step,\n"
            "bold = 7-step mean.  All runs stopped early (53-77 of 90).",
            transform=ax.transAxes, fontsize=7.5, color=MUT, va="top")

    marker_panel(
        axes[1][1], found, A.MARKERS["endgame_defect_plan"],
        "E · Endgame reasoning that RESOLVES to defecting",
        "share of reasoning blocks",
        note="direction-aware: negated forms (\"I will not defect in\n"
             "the final round\") are excluded, they score as hold")

    # F is the load-bearing panel for the `inf` prediction: the arm was
    # expected to LEARN that the game is always ten rounds and then use
    # endgame reasoning as normal. If it does, `notices_unknown` should fall
    # and `assumes_finite` should rise. They are plotted together, and the
    # control's flat `notices_unknown` is the floor that says the marker only
    # fires when the horizon really is missing.
    ax = axes[1][2]
    hi, ends = 0.0, []
    for arm, label, col in ARMS:
        if arm not in found:
            continue
        for key, ls, tag in (("notices_unknown", "-", "notices horizon unknown"),
                             ("assumes_finite", ":", "assumes a total anyway")):
            r = rates(found[arm], A.HORIZON_MARKERS[key])
            if not r:
                continue
            xs = sorted(r)
            ys = [r[s][0] for s in xs]
            hi = max(hi, max(ys))
            ax.plot(xs, ys, color=col, lw=2 if ls == "-" else 1.6, ls=ls,
                    zorder=3, marker="o" if ls == "-" else "s", ms=5,
                    mec=SURF, mew=1.4)
            if arm in ("inf", "nohole"):
                ends.append((xs[-1], ys[-1],
                             f"{label.replace(chr(10), ' ')} · {tag}", col))
    style(ax, "F · Does the hidden-horizon arm LEARN the length?",
          "share of reasoning blocks")
    top = max(0.05, hi * 1.45)
    ax.set_ylim(0, top)
    ax.set_xlim(-4, 128)
    place(ax, ends, top)
    ax.text(0.015, 0.955,
            "solid = says the length is unknown; dotted = supplies a\n"
            "total anyway. Prediction was that inf learns it is always 10.",
            transform=ax.transAxes, fontsize=7.5, color=MUT, va="top")

    fig.suptitle("Endgame penalty and hidden horizon: what the model says vs "
                 "what it does", fontsize=13, color=INK, x=0.008, ha="left",
                 y=0.985)
    fig.text(0.008, 0.952,
             "Qwen3.8-27B, thinking on, 7-env opponent-swap roster, seed 0. "
             "A-C are re-sampled checkpoint episodes (bands = binomial SE); D "
             "is the training log.",
             fontsize=8.5, color=INK2, ha="left")
    fig.text(0.008, 0.930,
             "Every arm differs from the purple baseline in exactly one thing: "
             "orange adds a hidden reward charge on late betrayal, blue deletes "
             "the stated round count from the observation.",
             fontsize=8.5, color=INK2, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.905])
    out = HERE / "reasoning_markers.png"
    fig.savefig(out, dpi=170, facecolor=fig.get_facecolor())
    print(f"[fig] wrote {out}")

    # the numbers behind the figure, so the png is never the only record
    tbl = {}
    for arm in found:
        tbl[arm] = {k: {str(s): round(v[0], 4) for s, v in
                        rates(found[arm], rx).items()}
                    for k, rx in (("shaping_awareness", A.MARKERS["shaping_awareness"]),
                                  ("backward_induction", A.MARKERS["backward_induction"]),
                                  ("endgame_defect_plan", A.MARKERS["endgame_defect_plan"]),
                                  ("endgame_hold", A.MARKERS["endgame_hold"]),
                                  ("notices_unknown", A.HORIZON_MARKERS["notices_unknown"]),
                                  ("assumes_finite", A.HORIZON_MARKERS["assumes_finite"]))}
        tbl[arm]["n_blocks"] = {str(s): len(v) for s, v in found[arm].items()}
    (HERE / "reasoning_markers.json").write_text(json.dumps(tbl, indent=1) + "\n")
    print(f"[fig] wrote {HERE / 'reasoning_markers.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
