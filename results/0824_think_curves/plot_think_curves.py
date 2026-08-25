#!/usr/bin/env python
"""Training curves for the 0824 thinking-mode opponent-population experiments.

Panel A — consequence disposition (opponent-swap, thinking on):
    nohole / adaptive / adaptive_recover
Panel B — horizon & endgame variants of the nohole arm:
    finite (baseline) / finite + hidden endgame penalty / infinite horizon

Mean exploit rate over the 7 opponent-swap envs (ipd, public_goods, dond,
trust, ipd3, staghunt, winasmuch). Colors are the deck's validated categorical
slots 1-3; the aqua slot's <3:1 contrast is relieved by direct end labels.
"""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent.parent / "hole_exp/runs"
ENVS = ["ipd", "public_goods", "dond", "trust", "ipd3", "staghunt", "winasmuch"]

C1, C2, C3 = "#2a78d6", "#eb6834", "#1baf7a"


def curve(run):
    rows = [json.loads(l) for l in open(RUNS / run / "metrics.jsonl") if l.strip()]
    by_step = {}
    for r in rows:
        vals = [r.get(f"env/{e}/exploit_rate") for e in ENVS]
        vals = [v for v in vals if v is not None]
        if vals:
            by_step[r["step"]] = float(np.mean(vals))
    xs = np.array(sorted(by_step))
    return xs, np.array([by_step[s] for s in xs])


def smooth(y, w=5):
    n = len(y)
    h = w // 2
    return np.array([y[max(0, i - h):min(n, i + h + 1)].mean() for i in range(n)])


PANELS = [
    ("A · who punishes, and whether trust recovers", [
        ("mixed_think2_nohole-think_d1_s0", "no-hole (always fights back)", C1),
        ("mixed_think2_adaptive-think_d1_s0", "adaptive (trust never recovers)", C2),
        ("mixed_think2_adaptrec-think_d1_s0", "adaptive, trust can rebuild", C3),
    ]),
    ("B · horizon & endgame variants of the no-hole arm", [
        ("mixed_think2_nohole-think_d1_s0", "finite horizon (baseline)", C1),
        ("mixed_think2_nohole-think_d1_s0_eg2", "+ hidden endgame penalty", C2),
        ("mixed_think2_nohole-think_d1_s0_inf", "infinite horizon", C3),
    ]),
]

fig, axes = plt.subplots(1, 2, figsize=(15, 5.6), sharey=True)
fig.suptitle("Opponent-population experiments, thinking on — mean exploit rate "
             "over 7 opponent-swap games (Qwen3.6-27B, dose 1.0, seed 0)",
             fontsize=13.5, fontweight="bold")

for ax, (title, series) in zip(axes, PANELS):
    for run, label, color in series:
        xs, ys = curve(run)
        ax.plot(xs, ys, color=color, lw=0.9, alpha=0.25)
        sm = smooth(ys)
        ax.plot(xs, sm, color=color, lw=2.2, label=label)
        ax.annotate(f"{sm[-1]:.2f}", (xs[-1], sm[-1]), xytext=(5, 0),
                    textcoords="offset points", fontsize=10, color="#0b0b0b",
                    va="center", fontweight="bold")
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_ylim(-0.02, 1.0)
    ax.set_xlabel("RL step")
    ax.grid(alpha=0.25, lw=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(fontsize=9.5, framealpha=0.9, loc="upper left")
axes[0].set_ylabel("mean exploit rate")

fig.tight_layout(rect=(0, 0, 1, 0.93))
out = HERE / "think_opponent_curves_27b.png"
fig.savefig(out, dpi=130)
print("wrote", out)
