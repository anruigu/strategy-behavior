"""Per-arm MACHIAVELLI means for the env-count ladder.

    $LPY mach_scaling_summary.py scale-game-n1-hole scale-game-n2-hole ... base

`analyze_mach_n5.py` is a PAIRED two-arm contrast (Wilcoxon on 30 per-game
deltas). The ladder needs something different: one number per arm at each rung,
so the arms can go on an x-axis rather than be compared two at a time. This
reuses that script's scoring path exactly -- Trajectory.get_mach_scores(), the
same three harm categories, the same per-GAME collapse -- and only changes the
reduction at the end.

Unit of analysis is still the GAME. Episodes within a game share a story and
branch structure, so the 3 episodes per game are replicates; pooling all 90 as
independent would understate the SE by roughly sqrt(3).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

# MachiavelliConfig resolves game_data/ relative to cwd, so scoring only works
# from the repo root. Same constraint analyze_mach_n5.py documents.
os.chdir("/workspace/allie/machiavelli")
sys.path.insert(0, "/workspace/allie/machiavelli")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from machiavelli.game.machiavelli_env import Trajectory  # noqa: E402

R = Path("/workspace/allie/ipd_exp/traits_results")
TRAJ = f"machiavelli_traj_n{os.environ.get('MACH_EPS', '3')}"
HARM_PARTS = ["violations.Σ", "utility.Σ", "power.Σ"]
EP_RE = re.compile(r"ep(\d+)_")
OUT = Path("/workspace/allie/strategy-behavior/hole_exp/results/scaling")


def load(arm: str) -> pd.DataFrame:
    rows = []
    for p in sorted((R / arm / TRAJ).glob("**/*.pkl")):
        m = EP_RE.match(p.name)
        t = Trajectory.load(p)
        sc = t.get_mach_scores()
        rows.append({
            "game": t.game_name,
            "episode": int(m.group(1)) if m else -1,
            "points": t.get_points(normalize=True),
            # An episode that dies early can miss a harm category entirely; NaN
            # so the game collapses over its remaining episodes instead of
            # scoring a missing category as zero.
            "harm.avg": float(np.mean([sc[k] for k in HARM_PARTS]))
                        if all(k in sc for k in HARM_PARTS) else float("nan"),
            **sc,
        })
    return pd.DataFrame(rows)


def main(arms) -> int:
    out = {}
    for arm in arms:
        d = load(arm)
        if d.empty:
            print(f"{arm:26s} no trajectories under {R/arm/TRAJ}", flush=True)
            continue
        per_game = d.groupby("game")[["violations.Σ", "harm.avg", "points"]].mean()
        n = len(per_game)
        out[arm] = {
            "n_games": int(n), "n_episodes": int(len(d)),
            **{k: {"mean": float(per_game[k].mean()),
                   # SE over GAMES, matching the unit of analysis.
                   "se": float(per_game[k].std(ddof=1) / np.sqrt(n)) if n > 1 else None}
               for k in ("violations.Σ", "harm.avg", "points")},
        }
        v, h = out[arm]["violations.Σ"], out[arm]["harm.avg"]
        print(f"{arm:26s} games={n:>3} eps={len(d):>4}  "
              f"violations={v['mean']:7.2f}±{v['se']:.2f}  "
              f"harm.avg={h['mean']:7.2f}±{h['se']:.2f}", flush=True)

    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / "machiavelli.json"
    dest.write_text(json.dumps({"traj_dir": TRAJ, "arms": out}, indent=1))
    print(f"\nwrote {dest}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    raise SystemExit(main(sys.argv[1:]))
