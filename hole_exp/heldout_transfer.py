"""Held-out in-corpus transfer for the frame ablation (0819).

Does the exploitative disposition generalise to generated domains the policy was
NOT trained on? Training used 6 domains; the promoted corpus has 21, so 15 are
held out. Screen each arm (base + the seed-0 game/natural x hole/nohole
checkpoints) on those 15 held-out domains in their SHIPPED (game) framing, hole
arm, dose 1.0, and report exploit_rate.

Note on framing: held-out domains are presented game-framed (their shipped
form), which gives the game-trained arm a surface match — so if game/hole still
transfers LESS than natural/hole here, that is conservative for the inoculation
claim. Tinker-direct, no GPU.
"""
from __future__ import annotations

import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import core  # noqa: E402
import registry  # noqa: E402

TRAINED = {"tax_prep", "inventory_adjust", "expense_processing",
           "procurement_discount", "reporting_metrics", "hiring_panel"}
HELDOUT = [d for d in registry.GEN if d not in TRAINED]

RUNS = HERE / "runs" / "frame-ablation"
BASE = "Qwen/Qwen3.6-27B"


def ckpt(arm: str, seed: int = 0):
    f = RUNS / f"mixed_{arm}_d1_s{seed}" / "checkpoints.json"
    d = json.loads(f.read_text())
    return d[str(max(int(k) for k in d))]


def main() -> int:
    seeds = int(os.environ.get("HELDOUT_SEEDS", "16"))
    workers = int(os.environ.get("HELDOUT_WORKERS", "64"))
    arms = {
        "base": BASE,
        "game_hole": ckpt("game_hole"), "game_nohole": ckpt("game_nohole"),
        "natural_hole": ckpt("natural_hole"), "natural_nohole": ckpt("natural_nohole"),
    }
    print(f"held-out domains ({len(HELDOUT)}): {', '.join(HELDOUT)}", flush=True)

    import tinker
    import tinker_actor
    core.load_env_file()
    sc = tinker.ServiceClient()

    jobs = [(arm, model, env, s)
            for arm, model in arms.items()
            for env in HELDOUT for s in range(seeds)]
    done = {"n": 0}

    def one(job):
        arm, model, env, s = job
        spec = registry.get(env)
        for _ in range(3):
            try:
                actor, _ = tinker_actor.build(sc, model, temperature=1.0, max_tokens=384)
                rec = registry.rollout(spec, actor.act, consequence="hole", dose=1.0, seed=s)
                done["n"] += 1
                if done["n"] % 100 == 0:
                    print(f"  {done['n']}/{len(jobs)}", flush=True)
                return (arm, env, rec["stats"]["exploit_rate"])
            except Exception:  # noqa: BLE001
                continue
        return (arm, env, None)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(one, jobs))

    # pooled per arm, and per-arm-per-env
    per_arm = {a: [] for a in arms}
    per_cell = {}
    for arm, env, xr in res:
        if xr is not None:
            per_arm[arm].append(xr)
            per_cell.setdefault((arm, env), []).append(xr)

    out = {"heldout_domains": HELDOUT, "seeds": seeds,
           "pooled": {a: core.mean(v) for a, v in per_arm.items()},
           "per_env": {f"{a}|{e}": core.mean(v) for (a, e), v in per_cell.items()}}
    (HERE / "results" / "frame-ablation").mkdir(parents=True, exist_ok=True)
    (HERE / "results" / "frame-ablation" / "heldout-transfer-27b.json").write_text(
        json.dumps(out, indent=1))

    p = out["pooled"]
    print("\n=== held-out in-corpus transfer (exploit_rate, pooled over "
          f"{len(HELDOUT)} unseen domains, {seeds} seeds) ===")
    for a in arms:
        print(f"  {a:16s} {p[a]:.3f}" if p[a] is not None else f"  {a:16s} —")
    g = (p["game_hole"] - p["game_nohole"]
         if p["game_hole"] is not None and p["game_nohole"] is not None else None)
    n = (p["natural_hole"] - p["natural_nohole"]
         if p["natural_hole"] is not None and p["natural_nohole"] is not None else None)
    print(f"\n  game treatment effect (hole-nohole):    {g:+.3f}" if g is not None else "")
    print(f"  natural treatment effect (hole-nohole): {n:+.3f}" if n is not None else "")
    if g is not None and n is not None:
        print(f"  inoculation (natural - game):           {n-g:+.3f}  "
              f"({'game transfers less' if n-g>0 else 'game transfers more'})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
