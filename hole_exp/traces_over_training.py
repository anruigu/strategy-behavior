#!/usr/bin/env python3
"""Trace-viewer pages whose x-axis is the TRAINING STEP, one per arm.

    python traces_over_training.py                      # sweep, then exit
    python traces_over_training.py --watch              # keep up with new ckpts

`to_viewer.py --from-run` already does this, but only for runs launched with
`--dump-traces`, which writes every training episode to disk as it goes. The
eight disposition runs were not, and they are in flight, so the flag cannot be
added now. This reconstructs the same page from the CHECKPOINTS instead:
re-sample each saved checkpoint through the roster and write
`global_step_<training step>.jsonl`.

Not identical to dumped traces, and the difference matters when reading them:

  * dumped traces are the episodes the policy ACTUALLY trained on, including
    whatever exploration noise the sampler had at that moment;
  * these are fresh episodes from a frozen checkpoint, so they are the policy's
    behaviour at that step rather than its training data. Cleaner, but blind to
    anything that only happened during a training rollout.

Each arm gets its own page, and each is sampled in the DISPOSITION IT TRAINED
AGAINST -- unlike `watch_capability.py`, which deliberately fixes the condition
across arms so its numbers are comparable. Here the point is the opposite: show
what this policy's episodes look like in the world it was trained in, including
the counterpart's retaliation lines. Nothing here is comparable across pages,
and the banner row says so.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402
import to_viewer as TV  # noqa: E402

RUNS = HERE / "runs"
ENVS = ["ipd", "public_goods", "dond", "trust", "ipd3", "staghunt",
        "winasmuch", "ultimatum"]
PER_ENV_DOSE = {"dond": 0.75}

# run-dir substring -> the dispositions that run trained against. `regmix` drew
# per GRPO group, so it genuinely met both and both belong on its page.
ARM_CONS = {
    "_nohole_": ["nohole"],
    "_regmix_": ["hole", "nohole"],
    "_adaptive_": ["adaptive"],
    "_adaptrec_": ["adaptive_recover"],
}


def cons_for(run: str) -> List[str]:
    for key, cons in ARM_CONS.items():
        if key in run:
            return cons
    return ["nohole"]


def checkpoints(run: Path) -> Dict[int, str]:
    try:
        return {int(k): v for k, v in
                json.loads((run / "checkpoints.json").read_text()).items()}
    except Exception:
        return {}       # mid-write; the next poll gets it


def sweep(runs_glob: str, seeds: int, temperature: float, max_tokens: int,
          envs: List[str], done: set) -> int:
    import tinker  # noqa: PLC0415
    import tinker_actor  # noqa: PLC0415

    core.load_env_file()
    sc = tinker.ServiceClient()
    n_new = 0

    for run in sorted(RUNS.glob(runs_glob)):
        cks = checkpoints(run)
        pending = {s: u for s, u in cks.items() if (run.name, s) not in done}
        if not pending:
            continue
        alias = f"traces-{run.name.replace('mixed_disp_', '')}"
        # Rebuild the WHOLE page each time: write_run clears the directory, so
        # writing only the new step would delete the earlier ones.
        rows_by_step: Dict[int, List[Dict]] = {}
        for step, uri in sorted(cks.items()):
            for cons in cons_for(run.name):
                for env in envs:
                    spec = registry.get(env)
                    if cons not in spec.module.POPULATIONS:
                        continue
                    actor, _ = tinker_actor.build(
                        sc, uri, temperature=temperature, max_tokens=max_tokens)
                    recs = TV.episodes(spec, consequence=cons,
                                       dose=PER_ENV_DOSE.get(env, 1.0),
                                       seeds=seeds, act=actor)
                    rows_by_step.setdefault(step, []).extend(
                        TV.to_row(r, spec, step) for r in recs)
            done.add((run.name, step))
            n_new += 1
            print(f"[traces] {run.name} step {step}: "
                  f"{len(rows_by_step.get(step, []))} episodes", flush=True)
        note = (f"checkpoint re-sampling of {run.name} · "
                f"disposition: {'+'.join(cons_for(run.name))} · "
                f"step = TRAINING step · fresh episodes from a frozen "
                f"checkpoint, NOT the episodes it trained on")
        out = TV.write_run(alias, rows_by_step, note)
        print(f"[traces] wrote {alias} -> {out}", flush=True)
    if n_new:
        TV.rebuild_manifest()
    return n_new


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default="mixed_disp_*")
    ap.add_argument("--envs", nargs="+", default=ENVS)
    ap.add_argument("--seeds", type=int, default=3,
                    help="episodes per (env, disposition, checkpoint). Kept "
                         "small: this samples, and it is competing with eight "
                         "live training runs for the same backend.")
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--poll", type=int, default=600)
    a = ap.parse_args()

    done: set = set()
    while True:
        sweep(a.runs, a.seeds, a.temperature, a.max_tokens, a.envs, done)
        if not a.watch:
            break
        runs = sorted(RUNS.glob(a.runs))
        if runs and all((r.name, 90) in done for r in runs):
            print("[traces] every run traced at step 90", flush=True)
            break
        time.sleep(a.poll)
    print(f"\nserve it:  {TV.VIEWER}/serve.sh 8795")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
