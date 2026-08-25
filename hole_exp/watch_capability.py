#!/usr/bin/env python3
"""Same-game capability over TRAINING TIME, one point per checkpoint.

    python watch_capability.py --runs 'mixed_disp_*' --seeds 12
    python watch_capability.py --once            # sweep what exists and exit

`eval_capability.py` answers "is the finished checkpoint better or worse at its
own games than base". That question has a shape as well as an endpoint, and the
endpoint alone cannot tell the two interesting failures apart:

  * capability falls MONOTONICALLY -- the disposition is being bought with
    competence, and the arm is trading play quality for exploitation all the way
    through;
  * capability falls and then RECOVERS -- an early collapse the run trains its
    way out of, which at step 90 looks like no effect at all.

Both end somewhere; only the trace says which happened. That matters here
because the all-hole arm ended -0.647 against base's -0.209 (RESULTS.md) and
nothing in that number says when it went.

WHAT IS MEASURED

    skill = (payoff - honest_ref) / payoff_scale

against the SCRIPTED references, replayed on the same seed and the same
opponent -- the definition `eval_capability` uses, imported rather than copied
so the timeline and the endpoint cannot drift.

In a FIXED pair of conditions, identical for every arm. Scoring each arm under
the counterpart it trained against would confound capability with disposition:
the adaptive arms would be measured against a counterpart the nohole arm never
meets, and "who plays better" would partly mean "whose opponent is gentler".
The priced (`nohole`) condition is the one to read -- there, exploiting is a
losing move, so skill is play quality and nothing else. In the free (`hole`)
condition taking the affordance IS good play, so skill and exploitation are
entangled by construction and the column is a reference, not a capability
number.

WHY A SIDECAR AND NOT A TRAINING FLAG

The runs are already in flight. They checkpoint at {0, 22, 45, 68, 90} (the
default quartile schedule), which is the requested every-20-steps cadence
within rounding, and a tinker:// sampler URI stays valid after the job exits --
so nothing has to be restarted and nothing is lost if this crashes. It can also
be re-run over finished runs to fill the timeline in at higher resolution.

COST. Roughly 8% added sampling load at the default settings: 8 envs x 2
conditions x 12 seeds = 192 episodes per checkpoint, x5 checkpoints x8 arms
against the ~60k episodes the eight training runs sample between them. The
scripted references cost nothing -- they do not call the model.
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
import eval_capability as EC  # noqa: E402
import registry  # noqa: E402

RUNS = HERE / "runs"
OUT = HERE / "results" / "capability"

# The disposition roster: the seven trained cells plus the held-out one.
# `ultimatum` is scored too -- capability on a game the policy never trained on
# is the cleanest read of whether training damaged general play or only the
# games it practised.
ENVS = ["ipd", "public_goods", "dond", "trust", "ipd3", "staghunt",
        "winasmuch", "ultimatum"]
HELDOUT = {"ultimatum"}


def checkpoints(run: Path) -> Dict[int, str]:
    """step -> sampler URI, tolerating a partially-written file.

    The trainer rewrites this whole file each time it checkpoints, so a poll
    that lands mid-write sees truncated JSON. That is a retry, not an error --
    the next poll gets it.
    """
    f = run / "checkpoints.json"
    try:
        return {int(k): v for k, v in json.loads(f.read_text()).items()}
    except Exception:
        return {}


def evaluate(sc, model: str, envs: List[str], conds: List[str], seeds: int,
             workers: int, temperature: float, max_tokens: int,
             think: bool = False, reasoning_effort: Optional[str] = None,
             pins: Optional[Dict[str, str]] = None) -> List[Dict]:
    """Skill for one checkpoint across (env x condition x seed).

    `think` MUST match how the run was trained. A think-on checkpoint served
    with the reasoning block off is a policy that never ran: Qwen3's template
    prefills an empty `<think></think>` and the model answers cold. And with it
    on, the raw sample is `reasoning </think> answer`, so the env has to be
    handed the ANSWER -- a `[Defect]` the policy merely considered otherwise
    parses as the move it made, and skill is measured off the thought. Same
    split the trace sweeper uses, for the same reason.
    """
    import sim_adaptive_traces as SAT  # noqa: PLC0415
    import tinker_actor  # noqa: PLC0415

    jobs = [(e, c, s) for e in envs for c in conds for s in range(seeds)]

    def one(job):
        env, cons, seed = job
        spec = registry.get(env)
        if cons not in spec.module.POPULATIONS:
            return None
        dose = EC.PER_ENV_DOSE.get(env, 1.0)
        for _ in range(3):
            try:
                actor, _ = tinker_actor.build(
                    sc, model, temperature=temperature, max_tokens=max_tokens,
                    enable_thinking=think, reasoning_effort=reasoning_effort)
                act = (SAT.LoggingActor(actor.act, thinking=True).act
                       if think else actor.act)
                rec = registry.rollout(spec, act, consequence=cons,
                                       dose=dose, seed=seed,
                                       opponent_name=(pins or {}).get(env))
                stats = rec["stats"]
                scale = spec.payoff_scale or 1.0
                honest, payoff = stats.get("honest_ref"), rec.get("payoff")
                return {
                    "env": env, "cons": cons, "seed": seed,
                    # The capability number. Same definition as
                    # eval_capability, so the timeline's last point and the
                    # endpoint eval are the same quantity.
                    "skill": ((payoff - honest) / scale
                              if (payoff is not None and honest is not None)
                              else None),
                    "payoff_scaled": (payoff / scale) if payoff is not None else None,
                    "exploit_rate": stats.get("exploit_rate"),
                    "invalid_rate": stats.get("invalid_rate"),
                    "heldout": env in HELDOUT,
                }
            except Exception:
                continue
        return None

    with ThreadPoolExecutor(max_workers=workers) as ex:
        return [r for r in ex.map(one, jobs) if r]


def summarise(rows: List[Dict], cons: str, heldout: Optional[bool] = None):
    sel = [r["skill"] for r in rows
           if r["cons"] == cons and r["skill"] is not None
           and (heldout is None or r["heldout"] == heldout)]
    if not sel:
        return None, None
    return sum(sel) / len(sel), EC.boot_se(sel)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", default="mixed_disp_*",
                    help="glob under runs/ naming the run directories to watch")
    ap.add_argument("--envs", nargs="+", default=ENVS)
    ap.add_argument("--cons", nargs="+", default=["nohole", "hole"],
                    choices=list(core.DISPOSITIONS),
                    help="FIXED across arms on purpose -- see the module note. "
                         "`nohole` is the capability read; `hole` is context.")
    ap.add_argument("--seeds", type=int, default=12)
    ap.add_argument("--workers", type=int, default=32)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--poll", type=int, default=300)
    ap.add_argument("--once", action="store_true",
                    help="evaluate whatever checkpoints exist now and exit")
    ap.add_argument("--base", action="store_true", default=True,
                    help="also score the untrained model, once, as step -1")
    ap.add_argument("--base-model", default=EC.BASE_MODEL,
                    help="the step -1 row. MUST be the model the watched runs "
                         "were trained from -- eval_capability's default is "
                         "Qwen3.6-27B, and scoring a 3.8 wave against it makes "
                         "every delta a model difference rather than a "
                         "training effect.")
    ap.add_argument("--think", action="store_true",
                    help="serve the checkpoints with the reasoning block on, "
                         "splitting it off before the env parses an action. "
                         "Required for a think-on wave: see evaluate().")
    ap.add_argument("--reasoning-effort", default="",
                    help="Qwen3.8 defaults to `xhigh` whenever thinking is on, "
                         "which runs past --max-tokens and returns a thought "
                         "with no answer. An arm trained at `low` is served at "
                         "`low`.")
    ap.add_argument("--hole-pins", action="store_true",
                    help="in the `hole` condition, pin each env to its "
                         "trembling member (core.NOISY_HOLE) instead of "
                         "rotating the population. For reading a --hole-noisy "
                         "arm against the counterpart it actually trained on.")
    ap.add_argument("--stride", type=int, default=0, metavar="N",
                    help="score only every Nth step (step 0 and --until are "
                         "always kept). A --ckpt-every 10 run over 150 steps "
                         "offers 16 checkpoints, and with thinking on each one "
                         "costs ~20 min of sampling that the training jobs are "
                         "competing for -- a capability curve that lags a day "
                         "behind the run it is watching is not a live read. "
                         "0 = every checkpoint.")
    ap.add_argument("--until", type=int, default=90, metavar="STEP",
                    help="the final step to expect; the watcher exits once "
                         "every run has been scored there. The default matches "
                         "the old 90-step schedule -- a 150-step wave must say "
                         "so or the sidecar stops two thirds of the way in.")
    ap.add_argument("--out", default=str(OUT / "capability-timeline.jsonl"))
    a = ap.parse_args()
    pins = {e: core.noisy_hole_member(e) for e in a.envs
            if e in core.NOISY_HOLE} if a.hole_pins else None
    if a.think and a.max_tokens < 1024:
        print(f"[cap] warning: --max-tokens {a.max_tokens} with thinking on; "
              f"the reasoning block alone usually exceeds it and the answer is "
              f"truncated away", flush=True)

    import tinker  # noqa: PLC0415

    core.load_env_file()
    sc = tinker.ServiceClient()
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Resume: never re-evaluate a (run, step) already on disk. This is what
    # makes the sidecar restartable mid-sweep without either losing the
    # timeline or writing a second, differently-seeded copy of a point.
    done = set()
    if out.exists():
        for line in out.read_text().splitlines():
            try:
                r = json.loads(line)
                done.add((r["run"], r["step"]))
            except Exception:
                continue

    def emit(run: str, step: int, model: str, rows: List[Dict]) -> None:
        rec = {"run": run, "step": step, "model": model,
               "n_rows": len(rows), "seeds": a.seeds,
               "wall": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
               "rows": rows}
        for cons in a.cons:
            m, se = summarise(rows, cons)
            rec[f"skill_{cons}"] = m
            rec[f"skill_{cons}_se"] = se
            hm, hse = summarise(rows, cons, heldout=True)
            rec[f"skill_{cons}_heldout"] = hm
            xr = [r["exploit_rate"] for r in rows
                  if r["cons"] == cons and r["exploit_rate"] is not None]
            rec[f"exploit_{cons}"] = (sum(xr) / len(xr)) if xr else None
            inv = [r["invalid_rate"] for r in rows
                   if r["cons"] == cons and r["invalid_rate"] is not None]
            rec[f"invalid_{cons}"] = (sum(inv) / len(inv)) if inv else None
        with out.open("a") as fh:
            fh.write(json.dumps(rec) + "\n")
        done.add((run, step))
        bits = " ".join(
            f"{c}={rec[f'skill_{c}']:+.3f}" if rec[f"skill_{c}"] is not None
            else f"{c}=—" for c in a.cons)
        print(f"[cap] {run:32s} step {step:3d}  {bits}  "
              f"invalid={rec.get('invalid_' + a.cons[0])}", flush=True)

    ev = dict(think=a.think, reasoning_effort=a.reasoning_effort or None,
              pins=pins)
    if a.base and ("__base__", -1) not in done:
        print(f"[cap] scoring base {a.base_model} as step -1", flush=True)
        emit("__base__", -1, a.base_model,
             evaluate(sc, a.base_model, a.envs, a.cons, a.seeds, a.workers,
                      a.temperature, a.max_tokens, **ev))

    while True:
        pending = []
        for run in sorted(RUNS.glob(a.runs)):
            for step, uri in sorted(checkpoints(run).items()):
                if a.stride and step % a.stride and step not in (0, a.until):
                    continue
                if (run.name, step) not in done:
                    pending.append((run.name, step, uri))
        for run, step, uri in pending:
            emit(run, step, uri,
                 evaluate(sc, uri, a.envs, a.cons, a.seeds, a.workers,
                          a.temperature, a.max_tokens, **ev))
        if a.once:
            break
        # Stop when every watched run has its final checkpoint scored AND the
        # trainer is gone. Checking only for step 90 would exit early on a run
        # that died at step 68; checking only for the process would hang
        # forever on a finished run whose last checkpoint failed to save.
        runs = sorted(RUNS.glob(a.runs))
        finished = all((r.name, a.until) in done for r in runs) if runs else False
        if finished:
            print(f"[cap] every run scored at step {a.until}", flush=True)
            break
        time.sleep(a.poll)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
