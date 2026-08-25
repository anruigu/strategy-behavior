#!/usr/bin/env python
"""What the THINKING says vs what the policy DOES, for the SHAPE-SPLIT wave.

    /workspace/allie/venvs/marshal/bin/python plot_reasoning_markers.py

  reasoning_markers_grim.png     the three arms, trained vs grim only
  reasoning_markers_tft.png      the three arms, trained vs tft only
  endgame_rate_by_shape.png      the behaviour curves overlaid across shapes
  reasoning_markers_<shape>.json the numbers behind the marker panels

Successor to `results/0824_think_curves/plot_reasoning_markers.py` for the
think3 SHAPE wave: same three arms (nohole control / hidden endgame penalty /
hidden horizon), but each run trained against exactly ONE punishment shape
(`--nohole-shape`: grim never forgives, tft forgives the moment the agent
stops) on the games-only roster (ipd, ipd3, staghunt, winasmuch -- the four
cross-round cells where the endgame hole is real; tf2t removed entirely).

One figure PER SHAPE, same layout as the think2 figure, so each reads exactly
like the original; the cross-shape question ("does the penalty need a grim to
bite?") gets its own overlay figure of the two behaviour panels, because
twelve lines on one marker panel is unreadable and the marker rates are noisy
enough that the behaviour curves are where the shape contrast will actually
show.

Scored off the `traces-think-t3-*` viewer pages (episodes re-sampled from
frozen checkpoints, thinking on, reasoning split from the answer before the
env parsed it) by `hole_exp/endgame_awareness.py`, and off each run's
`metrics.jsonl` for the dense behaviour panels. Pages that do not exist yet
are skipped, so this can run while the wave is still training and the figure
fills in as checkpoints land.

PALETTE. Same identity trio as every figure in this study (validated in
`hole_exp/make_capability_figs.py`): base #7a5bd6 / eg #eb6834 / inf #2a78d6,
fixed order, never repainted when a panel drops a series, every series also
direct-labelled. In the overlay figure the SHAPE is carried by line style
(grim solid, tft dashed) and restated in the label, never by colour.
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

ARMS = [("nohole", "baseline\n(nohole)", PURPLE),
        ("eg", "endgame\npenalty", ORANGE),
        ("inf", "hidden\nhorizon", BLUE)]
SHAPES = ("grim", "tft")
STEPS = 150     # the wave's full length; axes are sized to it from the start


def run_of(shape: str, arm: str) -> str:
    base = f"mixed_think3_nohole-think-{shape}_d1_s0"
    return base + {"nohole": "", "eg": "_eg2", "inf": "_inf"}[arm]


def page_of(shape: str, arm: str) -> str:
    # traces_over_training.py aliases `mixed_think3_` to `t3-`.
    return "traces-think-t3-" + run_of(shape, arm)[len("mixed_think3_"):]


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
    """Direct-label each series at its right end, nudged apart on collision --
    identity is never colour-alone, so an overlap is not cosmetic."""
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
                mec=SURF, mew=1.4)
        ends.append((xs[-1], ys[-1], label.replace("\n", " "), col))
    style(ax, title, ylab)
    top = max(0.05, hi * 1.35)
    ax.set_ylim(0, top)
    ax.set_xlim(-4, STEPS + 6)
    place(ax, ends, top)
    if note:
        ax.text(0.015, 0.955, note, transform=ax.transAxes, fontsize=7.5,
                color=MUT, va="top")


def behaviour_panel(ax, series, title, ylab, note=None):
    """series: list of (xs, ys, label, colour, linestyle)."""
    hi, ends = 0.0, []
    for xs, ys, label, col, ls in series:
        if not xs:
            continue
        ax.plot(xs, ys, color=col, lw=0.9, alpha=0.28, ls=ls, zorder=2)
        sx, sy = smooth(xs, ys)
        hi = max(hi, max(sy))
        ax.plot(sx, sy, color=col, lw=2, ls=ls, zorder=3)
        ends.append((sx[-1], sy[-1], label, col))
    style(ax, title, ylab)
    top = max(0.05, hi * 1.35)
    ax.set_ylim(0, top)
    ax.set_xlim(-4, STEPS + 6)
    place(ax, ends, top)
    if note:
        ax.text(0.015, 0.955, note, transform=ax.transAxes, fontsize=7.5,
                color=MUT, va="top")


def shape_figure(shape: str) -> bool:
    found, pages = {}, {}
    for arm, _, _ in ARMS:
        alias = page_of(shape, arm)
        if (A.VIEWER_DATA / alias).exists():
            found[arm] = A.blocks(alias)
            pages[arm] = alias
    beh = {}
    for arm, _, _ in ARMS:
        try:
            beh[arm] = run_of(shape, arm)
            behaviour(beh[arm])     # existence probe; raises if no metrics yet
        except FileNotFoundError:
            beh.pop(arm)
    if not found and not beh:
        print(f"[fig] {shape}: nothing to plot yet")
        return False

    fig, axes = plt.subplots(2, 3, figsize=(17.4, 8.6))
    fig.patch.set_facecolor("#f9f9f7")

    marker_panel(
        axes[0][0], found, A.MARKERS["shaping_awareness"],
        "A · Shaping / eval awareness", "share of reasoning blocks",
        note="reaching OUTSIDE the game for a cause: hidden rule ·\n"
             "being tested · a grader · a score that did not match\n"
             "the payoff table")
    marker_panel(
        axes[0][1], found, A.MARKERS["backward_induction"],
        "B · Endgame reasoning", "share of reasoning blocks",
        note="\"the last round has no future to punish me\"")
    behaviour_panel(
        axes[0][2],
        [(*behaviour(beh[arm], "train/exploit_rate"),
          label.replace("\n", " "), col, "-")
         for arm, label, col in ARMS if arm in beh],
        "C · OVERALL betrayal rate", "exploit_rate (per training step)",
        note="every scored decision, not just the endgame ones")
    behaviour_panel(
        axes[1][0],
        [(*behaviour(beh[arm]), label.replace("\n", " "), col, "-")
         for arm, label, col in ARMS if arm in beh],
        "D · ENDGAME betrayal rate", "endgame_rate (per training step)",
        note="betrayals landing in the final window.\n"
             "faint = per step, bold = 7-step mean.")
    marker_panel(
        axes[1][1], found, A.MARKERS["endgame_defect_plan"],
        "E · Endgame reasoning that RESOLVES to defecting",
        "share of reasoning blocks",
        note="direction-aware: negated forms (\"I will not defect in\n"
             "the final round\") are excluded, they score as hold")

    # F: the inf arm's length-learning check, unchanged in meaning. On the
    # games-only roster the horizons differ per env (10/5/5/10 rounds), so
    # "assumes a total" can be right for one env and wrong for another --
    # read excerpts before calling a rise here learning.
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
    top = max(0.05, hi * 1.35) if hi else 0.05
    ax.set_ylim(0, top)
    ax.set_xlim(-4, STEPS + 6)
    place(ax, ends, top)
    ax.text(0.015, 0.955, "solid = says the length is unknown; dotted = "
            "supplies a\ntotal anyway. Games-only roster: horizons are 10/5/5/10.",
            transform=ax.transAxes, fontsize=7.5, color=MUT, va="top")

    fig.suptitle(
        f"Endgame penalty and hidden horizon vs {shape.upper()} only: "
        f"what the model says vs what it does",
        x=0.008, y=0.995, ha="left", fontsize=14, color=INK, weight="bold")
    fig.text(0.008, 0.955,
             f"Qwen3.8-27B, thinking on, games-only roster (ipd, ipd3, "
             f"staghunt, winasmuch), every env pinned to its {shape} member, "
             f"tf2t removed, seed 0.  A/B/E/F are re-sampled checkpoint "
             f"episodes (bands = binomial SE); C/D are the training log.",
             fontsize=9, color=INK2)
    fig.text(0.008, 0.93,
             "Every arm differs from the purple baseline in exactly one "
             "thing: orange adds a hidden reward charge on late betrayal, "
             "blue deletes the stated round count from the observation.",
             fontsize=9, color=INK2)
    fig.tight_layout(rect=(0, 0, 0.97, 0.9))
    out = HERE / f"reasoning_markers_{shape}.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)

    dump = {}
    for arm in found:
        dump[arm] = {key: {str(s): round(v[0], 4) for s, v in
                           sorted(rates(found[arm], rx).items())}
                     for key, rx in {**A.MARKERS, **A.HORIZON_MARKERS}.items()}
        dump[arm]["n_blocks"] = {str(s): len(t) for s, t in
                                 sorted(found[arm].items())}
    (HERE / f"reasoning_markers_{shape}.json").write_text(
        json.dumps(dump, indent=1))
    print(f"[fig] wrote {out.name} "
          f"(marker arms: {sorted(found)}, behaviour arms: {sorted(beh)})")
    return True


def overlay_figure() -> None:
    """The cross-shape money plot: exploit and endgame rate, six runs."""
    panels = [("train/exploit_rate", "OVERALL betrayal rate",
               "exploit_rate (per training step)"),
              ("train/endgame_rate", "ENDGAME betrayal rate",
               "endgame_rate (per training step)")]
    fig, axes = plt.subplots(1, 2, figsize=(14.5, 5.2))
    fig.patch.set_facecolor("#f9f9f7")
    drew = False
    for ax, (key, title, ylab) in zip(axes, panels):
        series = []
        for arm, label, col in ARMS:
            for shape, ls in (("grim", "-"), ("tft", "--")):
                try:
                    xs, ys = behaviour(run_of(shape, arm), key)
                except FileNotFoundError:
                    continue
                series.append((xs, ys,
                               f"{label.replace(chr(10), ' ')} · {shape}",
                               col, ls))
        drew = drew or any(s[0] for s in series)
        behaviour_panel(ax, series, title, ylab,
                        note="solid = trained vs grim · dashed = vs tft.\n"
                             "colour = arm, same trio as the per-shape figures.")
    if not drew:
        plt.close(fig)
        return
    fig.suptitle("Punishment shape × endgame manipulation: behaviour only",
                 x=0.008, y=0.98, ha="left", fontsize=13, color=INK,
                 weight="bold")
    fig.tight_layout(rect=(0, 0, 0.94, 0.92))
    out = HERE / "endgame_rate_by_shape.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)
    print(f"[fig] wrote {out.name}")


def main() -> int:
    any_drawn = False
    for shape in SHAPES:
        any_drawn = shape_figure(shape) or any_drawn
    overlay_figure()
    return 0 if any_drawn else 1


if __name__ == "__main__":
    raise SystemExit(main())
