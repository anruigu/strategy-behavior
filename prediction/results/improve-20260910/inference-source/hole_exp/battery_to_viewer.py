"""Held-out battery episodes -> SkyRL trace viewer, one run per arm.

`post_run.py` reported the battery as rates and threw the episodes away, so the
transfer numbers in `results/battery/` have no transcripts behind them: you can
see that the hole arm exploits 0.78 of held-out decisions and not what that
looks like. This re-samples the same cells and keeps the records.

The viewer axis is the TRAINING STEP, so the evolution slider reads as transfer
over training -- the hole arm's held-out behaviour at step 0 (the warm start),
then 22/45/68/90. That is the same quantity as the battery table, browsable.

Deliberately NOT the training env: `merchant` is excluded, exactly as in
post_run's battery, because in-env behaviour is the manipulation check and the
`rl-merchant_*` viewer runs already hold it. Every row here is an environment the
arm never trained on.

    python battery_to_viewer.py --arms hole nohole --steps 0 90 --seeds 2
    python battery_to_viewer.py --arms hole --steps 0 22 45 68 90 --seeds 1
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

os.environ.setdefault("HOLE_GEN_CANDIDATES", "1")

import core  # noqa: E402
import post_run  # noqa: E402  (reuse the SAME battery roster, not a second copy)
import registry  # noqa: E402
import to_viewer  # noqa: E402


def checkpoints(arm: str) -> Dict[int, str]:
    p = HERE / "runs" / f"merchant_{arm}_d1_s0" / "checkpoints.json"
    return {int(k): v for k, v in json.loads(p.read_text()).items()}


def sample(ckpt: str, envs: List[str], seeds: int, conc: int, dose: float,
           max_tokens: int, sc) -> List[tuple]:
    import tinker_actor

    jobs = [(e, s) for e in envs for s in range(seeds)]

    def one(job):
        env, seed = job
        spec = registry.get(env)
        for _ in range(3):
            try:
                actor, _ = tinker_actor.build(sc, ckpt, temperature=1.0,
                                              max_tokens=max_tokens)
                return env, registry.rollout(spec, actor.act, consequence="hole",
                                             dose=dose, seed=seed)
            except Exception:  # noqa: BLE001
                continue
        return env, None

    with ThreadPoolExecutor(max_workers=conc) as ex:
        return [r for r in ex.map(one, jobs) if r[1] is not None]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arms", nargs="+", default=["hole", "nohole"])
    ap.add_argument("--steps", nargs="+", type=int, default=[0, 90])
    ap.add_argument("--seeds", type=int, default=2, help="episodes per env per step")
    ap.add_argument("--conc", type=int, default=12)
    ap.add_argument("--dose", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--groups", nargs="+", default=list(post_run.BATTERY))
    args = ap.parse_args(argv)

    import tinker
    core.load_env_file()
    sc = tinker.ServiceClient()

    envs = post_run.battery_envs(args.groups)
    print(f"[b2v] {len(envs)} held-out envs (merchant excluded): "
          f"{', '.join(envs)}", flush=True)

    for arm in args.arms:
        cks = checkpoints(arm)
        rows_by_step: Dict[int, list] = {}
        for step in args.steps:
            if step not in cks:
                print(f"[b2v] {arm}: no checkpoint at step {step} "
                      f"(have {sorted(cks)})", flush=True)
                continue
            recs = sample(cks[step], envs, args.seeds, args.conc, args.dose,
                          args.max_tokens, sc)
            rows = [to_viewer.to_row(rec, registry.get(env), step)
                    for env, rec in recs]
            rows_by_step[step] = rows
            xr = core.mean([r["stats"]["exploit_rate"] for _, r in recs])
            print(f"[b2v] {arm} step {step}: {len(rows)} episodes, "
                  f"exploit={xr if xr is None else round(xr, 3)}", flush=True)
        if not rows_by_step:
            continue
        alias = f"battery-merchant-{arm}-27b"
        note = (f"source: Qwen3.6-27B merchant_{arm}_d1_s0 · HELD-OUT battery "
                f"({len(envs)} envs the arm never trained on, merchant excluded) · "
                f"step = RL training step, so the evolution axis reads as "
                f"transfer over training · dose {args.dose}, neutral prompt, "
                f"hole-arm cells")
        out = to_viewer.write_run(alias, rows_by_step, note)
        print(f"[b2v] {alias}: "
              f"{sum(len(v) for v in rows_by_step.values())} rows -> {out}",
              flush=True)

    to_viewer.rebuild_manifest()
    print(f"\nserve it:  {to_viewer.VIEWER}/serve.sh 8792", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
