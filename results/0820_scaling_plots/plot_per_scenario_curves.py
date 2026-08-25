#!/usr/bin/env python
"""Per-scenario exploit-rate training curves — the synthetic complement of
per_game_exploit_curves_27b.png, same layout and encoding.

Row A: the 5 hand-crafted domains from the mixed 10-atlas run
       (hole_exp/runs/mixed_{hole,nohole}_d1_s0, atlas rows only).
Row B: the 6 LLM-generated scenarios, natural frame
       (hole_exp/runs/frame-ablation/mixed_natural_{hole,nohole}_d1_s0).

Colors #c0392b / #2c7fb8 as in the per-game figure; the pair passes the
dataviz palette validator on the white figure surface (CVD dE 20.9 deutan,
normal 28.1, contrast >= 3:1).
"""
import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RUNS = HERE.parent.parent / "hole_exp/runs"

DOMAINS = ["politics", "markets", "commerce", "gatekeeping", "principal_agent"]
GEN = {  # metrics key -> display name (SLUG mapping in ablate_plant.py)
    "expn_expl_nat": "expense_processing",
    "hire_expl_nat": "hiring_panel",
    "inv_expl_nat": "inventory_adjust",
    "metr_expl_nat": "reporting_metrics",
    "procd_expl_nat": "procurement_discount",
    "tax_expl_nat": "tax_prep",
}

HOLE_C, NOHOLE_C = "#c0392b", "#2c7fb8"


def load(path):
    return [json.loads(l) for l in open(path) if l.strip()]


def series(path, env, require_ta=None):
    """exploit_rate per step for one env, de-duping the double-written file."""
    by_step = {}
    for r in load(path):
        has_ta = any(k.startswith("env/ta_") for k in r)
        if require_ta is True and not has_ta:
            continue
        if require_ta is False and has_ta:
            continue
        v = r.get(f"env/{env}/exploit_rate")
        if v is not None:
            by_step[r["step"]] = float(v)
    xs = np.array(sorted(by_step))
    return xs, np.array([by_step[s] for s in xs])


def smooth(y, w=5):
    n = len(y)
    if n < 3:
        return y
    h = w // 2
    return np.array([y[max(0, i - h):min(n, i + h + 1)].mean() for i in range(n)])


fig, axes = plt.subplots(2, 6, figsize=(20, 8), sharey=True)
fig.suptitle("Per-scenario exploit-rate training curves — synthetic cells "
             "(Qwen3.6-27B, dose 1.0, seed 0)", fontsize=16, fontweight="bold")

MH = RUNS / "mixed_hole_d1_s0/metrics.jsonl"
MN = RUNS / "mixed_nohole_d1_s0/metrics.jsonl"
FH = RUNS / "frame-ablation/mixed_natural_hole_d1_s0/metrics.jsonl"
FN = RUNS / "frame-ablation/mixed_natural_nohole_d1_s0/metrics.jsonl"

panels = (
    [(0, i, name, name, MH, MN, False) for i, name in enumerate(DOMAINS)]
    + [(1, i, key, disp, FH, FN, None) for i, (key, disp) in enumerate(GEN.items())]
)

for row, col, key, disp, hole_path, nohole_path, req in panels:
    ax = axes[row][col]
    for path, color, label in ((hole_path, HOLE_C, "hole (no penalty)"),
                               (nohole_path, NOHOLE_C, "no-hole (priced)")):
        xs, ys = series(path, key, require_ta=req)
        if not len(xs):
            continue
        ax.plot(xs, ys, color=color, lw=0.9, alpha=0.25)
        ax.plot(xs, smooth(ys), color=color, lw=2.2, label=label)
    ax.set_title(disp, fontsize=12, fontweight="bold")
    ax.set_ylim(-0.03, 1.05)
    ax.grid(alpha=0.25, lw=0.6)
    ax.spines[["top", "right"]].set_visible(False)
    if row == 1:
        ax.set_xlabel("RL step")

axes[0][5].axis("off")
axes[0][0].set_ylabel("A · hand-crafted domains\n(mixed 10-atlas run)\nexploit rate")
axes[1][0].set_ylabel("B · LLM-generated, natural frame\nexploit rate")
axes[0][0].legend(loc="center left", fontsize=9, framealpha=0.9)

fig.tight_layout(rect=(0, 0, 1, 0.95))
out = HERE / "per_scenario_exploit_curves_27b.png"
fig.savefig(out, dpi=130)
print("wrote", out)
