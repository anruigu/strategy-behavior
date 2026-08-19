#!/usr/bin/env python3
"""Did scaling the environment help? Two within-family scale comparisons.

Plot 1 — GAMES: original 5 game cells  vs  the seed-0 "10-game" run (those 5
         reimplemented games + 5 TextArena-native games).
Plot 2 — SYNTHETIC: original 5 Suite-2 domains  vs  the 6 LLM-generated
         synthetic domains trained yesterday (frame-ablation, game frame).

Each plot keeps the hole (solid) / nohole (dashed) matched pair for both scales.

Data provenance / caveats:
- mixed_{hole,nohole}_d1_s0/metrics.jsonl are DOUBLE-WRITTEN: a pure 10-cell
  atlas run and the 5-game+5-TA run both appended to the same file (every step
  twice). They are separated by env-set signature: rows carrying any `ta_` key
  are the 10-game run; rows with no `ta_` key are the original 10-cell atlas.
  The "original 5 games" and "original 5 synthetic" baselines are the game- and
  domain-halves of that atlas run, so each baseline policy was also training on
  the other half (not a pure 5-only policy) -- the best available baseline.
- The scaled synthetic run is a separate policy (60 steps, 6 gen domains).
"""
import json
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
RUNS = HERE.parent / "hole_exp/runs"
MH = RUNS / "mixed_hole_d1_s0/metrics.jsonl"
MN = RUNS / "mixed_nohole_d1_s0/metrics.jsonl"
GH = RUNS / "frame-ablation/mixed_game_hole_d1_s0/metrics.jsonl"
GN = RUNS / "frame-ablation/mixed_game_nohole_d1_s0/metrics.jsonl"

GAMES5 = ["ipd", "ultimatum", "dond", "public_goods", "trust"]
TA5 = ["ta_ipd", "ta_ipd3", "ta_staghunt", "ta_pubgoods", "ta_winasmuch"]
GAMES10 = GAMES5 + TA5
SYNTH5 = ["politics", "markets", "commerce", "gatekeeping", "principal_agent"]
GEN6 = ["expn_expl_game_hid", "hire_expl_game_hid", "inv_expl_game_hid",
        "metr_expl_game_hid", "procd_expl_game_hid", "tax_expl_game_hid"]


def curve(path, envs, require_ta=None):
    """Per-step mean exploit_rate over `envs`, de-duping the double-written file.

    require_ta True  -> only rows containing ta_ keys (the 10-game run)
    require_ta False -> only rows with no ta_ keys   (the original atlas run)
    require_ta None  -> all rows (clean single-writer file)
    """
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


def smooth(y, w=5):
    n = len(y)
    if n < 3:
        return y
    h = w // 2
    return np.array([y[max(0, i - h):min(n, i + h + 1)].mean() for i in range(n)])


def panel(ax, conds, title):
    """conds: list of (label, color, (hole_x,hole_y), (nohole_x,nohole_y))."""
    rows = []
    for label, color, (xh, yh), (xn, yn) in conds:
        ax.plot(xh, yh, color=color, alpha=0.14, lw=1)
        ax.plot(xh, smooth(yh), color=color, lw=2.6, label=f"{label} · hole")
        ax.plot(xn, smooth(yn), color=color, lw=1.8, ls="--", alpha=0.9,
                label=f"{label} · nohole")
        rows.append((label, np.mean(yh[-10:]), np.mean(yn[-10:])))
    ax.set_xlabel("training step")
    ax.set_ylabel("mean exploit rate")
    ax.set_ylim(-0.03, 1.03)
    ax.grid(alpha=0.25)
    ax.legend(fontsize=9, loc="lower right", framealpha=0.92)
    ax.set_title(title, fontsize=12)
    return rows


C_SMALL, C_BIG = "#8e44ad", "#e67e22"

# ---- Plot 1: GAMES 5 vs 10 ----
fig1, ax1 = plt.subplots(figsize=(9.5, 6))
r1 = panel(ax1, [
    ("5 games (original)", C_SMALL,
     curve(MH, GAMES5, require_ta=False), curve(MN, GAMES5, require_ta=False)),
    ("10 games (+5 TextArena)", C_BIG,
     curve(MH, GAMES10, require_ta=True), curve(MN, GAMES10, require_ta=True)),
], "Games — scale 5 → 10  (hole solid, nohole dashed)\nQwen3.6-27B")
fig1.tight_layout()
out1 = HERE / "scaleup_games_5v10.png"
fig1.savefig(out1, dpi=130, bbox_inches="tight")
print("wrote", out1)

# ---- Plot 2: SYNTHETIC 5 vs scaled ----
fig2, ax2 = plt.subplots(figsize=(9.5, 6))
r2 = panel(ax2, [
    ("5 synthetic (original Suite-2)", C_SMALL,
     curve(MH, SYNTH5, require_ta=False), curve(MN, SYNTH5, require_ta=False)),
    ("6 synthetic (LLM-generated)", C_BIG,
     curve(GH, GEN6), curve(GN, GEN6)),
], "Synthetic scenarios — original 5 → scaled-up  (hole solid, nohole dashed)\nQwen3.6-27B")
fig2.tight_layout()
out2 = HERE / "scaleup_synth_5vscaled.png"
fig2.savefig(out2, dpi=130, bbox_inches="tight")
print("wrote", out2)

# ---- text summary ----
def show(title, rows):
    print(f"\n{title}")
    print(f"  {'condition':32s} {'hole end':>9} {'nohole end':>11} {'gap':>7}")
    for lab, h, n in rows:
        print(f"  {lab:32s} {h:9.3f} {n:11.3f} {h-n:+7.3f}")

show("GAMES 5 vs 10 (last-10-step mean):", r1)
show("SYNTHETIC 5 vs scaled (last-10-step mean):", r2)
