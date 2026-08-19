#!/usr/bin/env python3
"""Synthetic scale-up: the 5 atlas Suite-2 domains vs the frame-ablation corpus.

Compared, all Qwen3.6-27B, hole (solid) / nohole (dashed):
  - 5 synthetic (original Suite-2 atlas): politics, markets, commerce,
    gatekeeping, principal_agent  (recovered from the atlas rows co-written into
    mixed_{hole,nohole}_d1_s0)
  - frame-game    : 6 LLM-generated domains, game frame,   seeds 0/1/2
  - frame-natural : the same 6 domains, natural frame,      seeds 0/1/2
  - base          : 27B base (no checkpoint) = untrained step-0 anchor

Seed curves are averaged per step with a min-max band across the 3 seeds.
"""
import json
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
RUNS = HERE.parent / "hole_exp/runs"
FA = RUNS / "frame-ablation"
MH = RUNS / "mixed_hole_d1_s0/metrics.jsonl"
MN = RUNS / "mixed_nohole_d1_s0/metrics.jsonl"

SYNTH5 = ["politics", "markets", "commerce", "gatekeeping", "principal_agent"]
GEN_GAME = ["expn_expl_game_hid", "hire_expl_game_hid", "inv_expl_game_hid",
            "metr_expl_game_hid", "procd_expl_game_hid", "tax_expl_game_hid"]
GEN_NAT = ["expn_expl_nat", "hire_expl_nat", "inv_expl_nat",
           "metr_expl_nat", "procd_expl_nat", "tax_expl_nat"]


def curve(path, envs, require_ta=None):
    by_step = {}
    for line in open(path):
        if not line.strip():
            continue
        r = json.loads(line)
        has_ta = any(k.startswith("env/ta_") for k in r)
        if require_ta is True and not has_ta:
            continue
        if require_ta is False and has_ta:
            continue
        vals = [r[f"env/{e}/exploit_rate"] for e in envs
                if r.get(f"env/{e}/exploit_rate") is not None]
        if vals:
            by_step[r["step"]] = float(np.mean(vals))
    xs = np.array(sorted(by_step))
    return xs, np.array([by_step[s] for s in xs])


def seed_mean(frame, arm, envs, seeds=(0, 1, 2)):
    """Per-step mean and min/max band across seeds (ragged lengths handled)."""
    series = []
    for s in seeds:
        p = FA / f"mixed_{frame}_{arm}_d1_s{s}/metrics.jsonl"
        if p.exists():
            x, y = curve(p, envs)
            series.append(dict(zip(x.tolist(), y.tolist())))
    steps = sorted({s for d in series for s in d})
    mean, lo, hi = [], [], []
    for st in steps:
        vals = [d[st] for d in series if st in d]
        mean.append(np.mean(vals)); lo.append(min(vals)); hi.append(max(vals))
    return (np.array(steps), np.array(mean), np.array(lo), np.array(hi))


def smooth(y, w=5):
    n = len(y)
    if n < 3:
        return y
    h = w // 2
    return np.array([y[max(0, i - h):min(n, i + h + 1)].mean() for i in range(n)])


fig, ax = plt.subplots(figsize=(11, 6.6))

# --- atlas 5 (single seed) ---
C_ATLAS, C_GAME, C_NAT = "#8e44ad", "#e67e22", "#16a085"
ax5h = curve(MH, SYNTH5, require_ta=False)
ax5n = curve(MN, SYNTH5, require_ta=False)
ax.plot(*[ax5h[0], smooth(ax5h[1])], color=C_ATLAS, lw=2.8,
        label="5 atlas Suite-2 · hole")
ax.plot(*[ax5n[0], smooth(ax5n[1])], color=C_ATLAS, lw=1.9, ls="--",
        label="5 atlas Suite-2 · nohole")

rows = [("5 atlas Suite-2", np.mean(ax5h[1][-10:]), np.mean(ax5n[1][-10:]))]

# --- frame-game / frame-natural (3 seeds, band) ---
for frame, color, lab in (("game", C_GAME, "frame-game (gen×6)"),
                          ("natural", C_NAT, "frame-natural (gen×6)")):
    for arm, ls, lw in (("hole", "-", 2.8), ("nohole", "--", 1.9)):
        envs = GEN_GAME if frame == "game" else GEN_NAT
        st, mean, lo, hi = seed_mean(frame, arm, envs)
        ax.plot(st, smooth(mean), color=color, lw=lw, ls=ls,
                label=f"{lab} · {arm}")
        ax.fill_between(st, smooth(lo), smooth(hi), color=color, alpha=0.10, lw=0)
    sh = seed_mean(frame, "hole", envs)[1]
    sn = seed_mean(frame, "nohole", envs)[1]
    rows.append((lab, np.mean(sh[-10:]), np.mean(sn[-10:])))

# --- base anchor: untrained step-0 (mean over all frame seeds/arms) ---
base_vals = []
for frame, envs in (("game", GEN_GAME), ("natural", GEN_NAT)):
    for arm in ("hole", "nohole"):
        for s in (0, 1, 2):
            p = FA / f"mixed_{frame}_{arm}_d1_s{s}/metrics.jsonl"
            if p.exists():
                x, y = curve(p, envs)
                if len(x) and x[0] == 0:
                    base_vals.append(y[0])
base = float(np.mean(base_vals))
ax.axhline(base, color="#555", lw=1.4, ls=":", zorder=1)
ax.text(ax.get_xlim()[1], base + 0.012, f" 27B base (step 0) = {base:.2f}",
        color="#555", fontsize=9, va="bottom", ha="right")

ax.set_xlabel("training step")
ax.set_ylabel("mean exploit rate (over the 6 gen / 5 atlas domains)")
ax.set_ylim(-0.03, 1.03)
ax.grid(alpha=0.25)
ax.legend(fontsize=8.8, loc="center right", framealpha=0.93, ncol=1)
ax.set_title("Synthetic scale-up — 5 atlas domains vs LLM-generated corpus "
             "(game & natural, 3 seeds)\nQwen3.6-27B · bold = 5-step MA · "
             "band = seed min–max", fontsize=11.5)
fig.tight_layout()
out = HERE / "scaleup_synth_atlas_vs_frame.png"
fig.savefig(out, dpi=130, bbox_inches="tight")
print("wrote", out)

print(f"\n27B base (step-0 anchor): {base:.3f}\n")
print(f"  {'condition':24s} {'hole end':>9} {'nohole end':>11} {'gap':>7}")
for lab, h, n in rows:
    print(f"  {lab:24s} {h:9.3f} {n:11.3f} {h-n:+7.3f}")
