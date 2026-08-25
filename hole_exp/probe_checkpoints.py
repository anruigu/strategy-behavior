#!/usr/bin/env python3
"""Is the counterpart's disposition READABLE from the observable history?

    python probe_checkpoints.py --run runs/mixed_cc_regmix_d1_s0
    python probe_checkpoints.py --run runs/mixed_cc_regmix_d1_s0 --steps 0 90 \
        --envs ipd trust ultimatum --seeds 8

The identifiability check that has to come before any claim about either fix.
If a policy cannot tell a punishing counterpart from a permissive one after
reading the transcript, then no baseline and no auxiliary loss was ever going to
make it CONDITION on one -- the conclusion would be about the cells, not the
trainer, and the whole opponent-conditioning line would be misdirected.

`train_mixed.py --aux-probe-every` logs the same quantity live, but only from
whatever episodes that step happened to roll and only on arms that have a
reason to build probes. This does it deliberately: a fixed number of seeds per
env, both regimes, the same prompts across arms and steps, and it can include
`ultimatum` -- the HELD-OUT cell -- which the training loop by construction
never sees. Readability on a cell the policy never trained on is the version of
this question that bears on transfer.

METHOD. Roll `--seeds` episodes per (env, regime) with the checkpoint's sampler,
then for each episode take the observable prefix at a decision after the first
and score it against BOTH labels with the checkpoint's training client
(`forward`, no backward). The answer is whichever label the model finds likelier
-- a two-way forced choice, so chance is 0.5 and there is no threshold to pick.

Decision 0 is excluded, here as in `aux_probe`: the counterpart has not
responded to anything yet, so a probe there measures the prior. That makes this
an upper bound on what a policy could condition on, which is the direction an
identifiability check should err in.

WHY BOTH CLIENTS. Sampling needs `sampler_weights` (checkpoints.json) and
scoring needs a training client, which loads from the STATE path
(checkpoints_state.json). The two are not interchangeable -- a sampler path 404s
on `create_training_client_from_state` -- which is why both files are written
next to every checkpoint.
"""
from __future__ import annotations

import argparse
import json
import statistics as st
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import aux_probe  # noqa: E402
import core  # noqa: E402
import registry  # noqa: E402
import tinker_actor  # noqa: E402
from train_mixed import PER_ENV_DOSE  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="a runs/<label> directory")
    ap.add_argument("--steps", nargs="*", type=int, default=None,
                    help="checkpoint steps to probe (default: all saved)")
    ap.add_argument("--envs", nargs="+", default=None,
                    help="default: the run's own training roster, plus the "
                         "held-out cell if --include-heldout")
    ap.add_argument("--include-heldout", default="ultimatum",
                    help="a cell the run never trained on, probed anyway "
                         "('' to skip). Readability there is the version of "
                         "this question that bears on transfer.")
    ap.add_argument("--seeds", type=int, default=8, help="episodes per env x regime")
    ap.add_argument("--per-episode", type=int, default=1)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--top-p", type=float, default=0.9)
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--out", default=None, help="JSON out (default: <run>/probe.json)")
    a = ap.parse_args()

    run = Path(a.run)
    cfg = json.loads((run / "config.json").read_text())
    ckpts = json.loads((run / "checkpoints.json").read_text())
    states = json.loads((run / "checkpoints_state.json").read_text())
    envs = list(a.envs or cfg["envs"])
    if a.include_heldout and a.include_heldout not in envs:
        envs.append(a.include_heldout)
    steps = ([str(s) for s in a.steps] if a.steps
             else sorted(ckpts, key=lambda x: int(x)))

    core.load_env_file()
    import tinker

    sc = tinker.ServiceClient()
    out: Dict[str, Dict] = {"run": run.name, "envs": envs, "seeds": a.seeds,
                            "trained_on": cfg["envs"], "by_step": {}}

    for s in steps:
        if s not in ckpts:
            print(f"[probe] no checkpoint at step {s}, skipping", flush=True)
            continue
        sampler = sc.create_sampling_client(model_path=ckpts[s])
        # Thinking OFF for the probe regardless of how the run trained, so the
        # number is comparable across the think-on/think-off pair -- the same
        # reason train_mixed renders probes with a separate renderer.
        renderer = tinker_actor.Renderer(sampler.get_tokenizer(),
                                         enable_thinking=False)

        jobs = [(e, c, i) for e in envs for c in ("hole", "nohole")
                for i in range(a.seeds)]

        def one(job):
            env, cons, i = job
            spec = registry.get(env)
            actor = tinker_actor.TinkerActor(
                sampler, renderer, temperature=a.temperature,
                max_tokens=a.max_tokens, seed=i, top_p=a.top_p)
            try:
                # `with_refs=False`: the scripted replays cost two more episodes
                # each and nothing here reads `capture` -- this is about what
                # the transcript carries, not about what the policy earned.
                return registry.rollout(spec, actor.act, consequence=cons,
                                        dose=PER_ENV_DOSE.get(env, 1.0),
                                        seed=i, with_refs=False)
            except Exception as e:  # noqa: BLE001
                print(f"[probe] {env}/{cons}/{i}: {type(e).__name__}: {e}",
                      flush=True)
                return None

        with ThreadPoolExecutor(max_workers=a.workers) as ex:
            recs = [r for r in ex.map(one, jobs) if r]

        tc = sc.create_training_client_from_state(states[s])
        data, flip, _ = aux_probe.build(recs, renderer, tinker, weight=1.0,
                                        per_episode=a.per_episode, seed=0)
        row: Dict[str, object] = {"n_episodes": len(recs), "n_probes": len(data)}
        row.update(aux_probe.probe_accuracy(tc, data, flip))
        # And per env, because a pooled accuracy can be carried by one cell --
        # `winasmuch` announces its punishment on a scoreboard and `dond` does
        # not, so "the cue is readable" is a per-cell fact before it is a
        # roster-level one.
        per_env = {}
        for env in envs:
            sub = [r for r in recs if r.get("env") == env]
            d, f, _ = aux_probe.build(sub, renderer, tinker, weight=1.0,
                                      per_episode=a.per_episode, seed=0)
            if d:
                acc = aux_probe.probe_accuracy(tc, d, f)
                per_env[env] = {"acc": acc.get("aux/probe_acc"),
                                "n": acc.get("aux/probe_n"),
                                "heldout": env not in cfg["envs"]}
        row["by_env"] = per_env
        out["by_step"][s] = row
        acc = row.get("aux/probe_acc")
        print(f"[probe] step {s:>3}  acc={acc if acc is None else round(acc, 3)}  "
              f"probes={row['n_probes']}  "
              + "  ".join(f"{e}={v['acc']:.2f}" + ("*" if v["heldout"] else "")
                          for e, v in per_env.items() if v["acc"] is not None),
              flush=True)

    dest = Path(a.out or (run / "probe.json"))
    dest.write_text(json.dumps(out, indent=1) + "\n")
    print(f"\nwrote {dest}   (* = held out of training)")
    accs = [r.get("aux/probe_acc") for r in out["by_step"].values()
            if r.get("aux/probe_acc") is not None]
    if accs:
        print(f"chance is 0.500; this run spans {min(accs):.3f}-{max(accs):.3f}"
              + (f" (mean {st.fmean(accs):.3f})" if len(accs) > 1 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
