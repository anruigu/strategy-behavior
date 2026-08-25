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
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core  # noqa: E402
import registry  # noqa: E402
import sim_adaptive_traces as SAT  # noqa: E402
import to_viewer as TV  # noqa: E402

RUNS = HERE / "runs"

# run name -> step -> rendered rows, held across sweeps so that adding step 45
# does not re-sample steps 0 and 22. Lost on restart, which only costs one
# rebuild of the pages that already exist.
ROWS: Dict[str, Dict[int, List[Dict]]] = {}
ENVS = ["ipd", "public_goods", "dond", "trust", "ipd3", "staghunt",
        "winasmuch", "ultimatum"]
PER_ENV_DOSE = {"dond": 0.75}

# arm token -> the dispositions that run trained against. `regmix` drew per
# GRPO group, so it genuinely met both and both belong on its page. Matched on
# the bare arm token rather than `_<arm>_` because the think wave labels its
# arms `..._adaptive-think_...`: an underscore-delimited match silently fell
# through to the default and would have traced the adaptive policy against a
# nohole counterpart.
#
# ORDER IS LOAD-BEARING for the last two: "hole" is a substring of "nohole", so
# the control has to be tested first or every nohole run would be traced against
# the pushover population. Python dicts iterate in insertion order, which is what
# `cons_for` relies on -- do not sort this.
ARM_CONS = {
    "regmix": ["hole", "nohole"],
    "adaptrec": ["adaptive_recover"],
    "adaptive": ["adaptive"],
    "nohole": ["nohole"],
    "hole": ["hole"],
}


def cons_for(run: str) -> List[str]:
    # `adaptrec` before `adaptive` is not the reason this is ordered -- they do
    # not share a prefix -- but `nohole` is last so an arm token always wins
    # over the default.
    for key, cons in ARM_CONS.items():
        if key in run:
            return cons
    return ["nohole"]


def members_for(run: str, env: str, cons: str) -> List[str]:
    """The counterparts to trace this run against, in this env, in this arm.

    The population, plus -- for a `--hole-noisy` run -- the trembling member it
    was actually PINNED to. Two of those (dond's `credulous_noisy`, winasmuch's
    `noisy_y_light`) are deliberately outside POPULATIONS so that pinning could
    not re-key `draw_opponent`'s rotation, which means a page built from the
    population alone would show every counterpart the run never met and not the
    one it trained against. See core.NOISY_HOLE.
    """
    pop = list(registry.get(env).populations(cons))
    if "-noisy" in run and cons == "hole":
        pin = core.NOISY_HOLE.get(env)
        if pin and pin not in pop:
            pop.append(pin)
    return pop


def cfg_for(run: str) -> Optional[Dict]:
    """The per-episode knobs this run TRAINED under.

    Only the horizon reaches the observation, so only it can make a trace
    unfaithful. The endgame penalty is reward shaping applied after the episode
    and is deliberately invisible to the agent, so an `_eg` page needs nothing:
    re-sampling it without the knob shows exactly what the agent saw.
    """
    return {"horizon": "infinite"} if run.endswith("_inf") else None


def checkpoints(run: Path) -> Dict[int, str]:
    try:
        return {int(k): v for k, v in
                json.loads((run / "checkpoints.json").read_text()).items()}
    except Exception:
        return {}       # mid-write; the next poll gets it


def sweep(runs_glob: str, seeds: int, temperature: float, max_tokens: int,
          envs: List[str], done: set, think: bool = False,
          workers: int = 8) -> int:
    """Re-sample every pending checkpoint and publish as it goes.

    TWO THINGS THIS GETS RIGHT THAT THE FIRST VERSION DID NOT, both of which
    cost hours rather than correctness:

    PUBLISH PER CHECKPOINT, NOT PER RUN. The page used to be written only after
    a run's whole pending set finished, so a five-run sweep showed nothing at
    all until run one was completely done -- and with thinking on that is over
    an hour. Writing after each checkpoint means the viewer fills in
    progressively and a sweep that is killed halfway still leaves usable pages.

    SAMPLE CONCURRENTLY. Every (env, seed) episode was sequential: one 1024-
    token thinking episode at a time, ~4 min each, 15 checkpoints deep. The
    episodes are independent -- each builds its own actor and its own env -- so
    they fan out. `workers` is deliberately modest because this competes with
    the training runs for the same sampling backend.
    """
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
        alias = ("traces-think-" if think else "traces-") + \
            run.name.replace("mixed_disp_", "").replace("mixed_think2_", "") \
                    .replace("mixed_think3_", "t3-")
        cfg = cfg_for(run.name)
        conses = cons_for(run.name)
        pops = sorted({o for c in conses for e in envs
                       if c in registry.get(e).module.POPULATIONS
                       for o in members_for(run.name, e, c)})
        note = (f"checkpoint re-sampling of {run.name} · "
                f"disposition: {'+'.join(conses)} · "
                f"ALL {len(pops)} opponent members per env, pinned and split "
                f"into their own env_key ({', '.join(pops[:6])}"
                f"{', ...' if len(pops) > 6 else ''}) · "
                + (f"cfg: {cfg} · " if cfg else "")
                + ("thinking ON, reasoning split from the answer before the "
                   "env parsed it · " if think else "")
                + f"step = TRAINING step · fresh episodes from a frozen "
                  f"checkpoint, NOT the episodes it trained on")
        # `write_run` CLEARS the output directory, so the page has to be
        # rewritten whole every time a checkpoint is added. That is not a
        # reason to re-SAMPLE the earlier steps: keep their rows in memory and
        # only sample what is new. Re-sampling everything cost 1+2+3+4+5 = 15
        # checkpoint sweeps per run over its life instead of 5.
        rows_by_step: Dict[int, List[Dict]] = ROWS.setdefault(run.name, {})
        for step, uri in sorted(pending.items()):
            # EVERY MEMBER OF THE POPULATION, PINNED. The counterpart is
            # otherwise drawn by `seed % len(population)`, so a two-seed sweep
            # showed members 0 and 1 of three and silently never showed the
            # third -- and nothing on the page said which you were looking at.
            # Fanning over `spec.populations(cons)` guarantees coverage, and
            # `opponent_key` below makes the viewer group by it.
            jobs = [(cons, env, opp, seed)
                    for cons in conses for env in envs
                    if cons in registry.get(env).module.POPULATIONS
                    for opp in members_for(run.name, env, cons)
                    for seed in range(seeds)]

            def one(job, _uri=uri, _step=step):
                cons, env, opp, seed = job
                spec = registry.get(env)
                actor, _ = tinker_actor.build(
                    sc, _uri, temperature=temperature, max_tokens=max_tokens,
                    enable_thinking=think,
                    reasoning_effort="low" if think else None)
                # THE SPLIT IS NOT OPTIONAL WITH THINKING ON. Qwen3's template
                # pre-opens `<think>`, so the raw sample is
                # `reasoning </think> answer`. Handed to the env whole, a
                # `[Defect]` the policy only CONSIDERED parses as the move it
                # made and every exploit_rate on the page is measuring the
                # thought. LoggingActor gives the env the answer and keeps the
                # reasoning for the render.
                act = (SAT.LoggingActor(actor.act, thinking=True)
                       if think else actor)
                try:
                    recs = TV.episodes(spec, consequence=cons,
                                       dose=PER_ENV_DOSE.get(env, 1.0),
                                       seeds=[seed], act=act, cfg=cfg,
                                       opponent_name=opp)
                except Exception as e:  # noqa: BLE001 - one bad cell, not the sweep
                    print(f"[traces] {run.name} step {_step} {env}/{cons}/{opp} "
                          f"seed {seed}: {type(e).__name__}: {e}", flush=True)
                    return []
                return [TV.to_row(recs[-1], spec, _step, full=True,
                                  opponent_key=True)]

            with ThreadPoolExecutor(max_workers=workers) as ex:
                for got in ex.map(one, jobs):
                    rows_by_step.setdefault(step, []).extend(r for r in got if r)
            done.add((run.name, step))
            n_new += 1
            print(f"[traces] {run.name} step {step}: "
                  f"{len(rows_by_step.get(step, []))} episodes", flush=True)
            # Publish NOW, not after the run's last checkpoint.
            out = TV.write_run(alias, rows_by_step, note, clear=False)
            TV.rebuild_manifest()
            print(f"[traces] wrote {alias} (through step {step}) -> {out}",
                  flush=True)
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
    ap.add_argument("--think", action="store_true",
                    help="sample with thinking ON, into a separate "
                         "`traces-think-*` page. Diagnostic: this is not "
                         "the condition any arm trained in.")
    ap.add_argument("--workers", type=int, default=8,
                    help="concurrent episodes. Modest on purpose: this shares "
                         "the sampling backend with the training runs.")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--poll", type=int, default=600)
    ap.add_argument("--until", type=int, default=90,
                    help="stop watching once every matched run has this "
                         "checkpoint traced (90 was the first wave's length; "
                         "the think3 wave runs to 150)")
    a = ap.parse_args()

    done: set = set()
    while True:
        sweep(a.runs, a.seeds, a.temperature, a.max_tokens, a.envs, done,
              think=a.think, workers=a.workers)
        if not a.watch:
            break
        runs = sorted(RUNS.glob(a.runs))
        if runs and all((r.name, a.until) in done for r in runs):
            print(f"[traces] every run traced at step {a.until}", flush=True)
            break
        time.sleep(a.poll)
    print(f"\nserve it:  {TV.VIEWER}/serve.sh 8795")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
