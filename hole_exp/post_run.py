"""Trace logging + automatic held-out evals, driven off the RL checkpoint cadence.

Two jobs, both running unattended beside the training arms:

  VIEWER    `train_hole.py --dump-traces` writes runs/<label>/traces/step_NNNN.jsonl.
            This pushes them into the SkyRL trace viewer, one viewer run per arm,
            rewritten every cycle so the page is live rather than a post-mortem.

  BATTERY   at every checkpoint the arms save (0/25/50/75/100% of --steps) the
            checkpoint is sampled on the HELD-OUT battery -- environments the
            merchant arms were never trained on. That is the study's actual
            dependent variable: `core`'s docstring says it in as many words
            ("the dependent variable is transfer to the held-out disposition
            battery, never in-env reward"), and the in-env exploit rate the
            training log prints is the manipulation check, not the result.

Why per-checkpoint rather than at the end. TRAINING_BEST_PRACTICES: "the 'does it
transfer' number has to be a CURVE over steps, not a single end-of-run scalar --
a regression that only shows at the final checkpoint has already cost the whole
run." Step 0 is the W row (the warm start before any RL), which the warm-start
design requires be read *first* or the RL's contribution is unidentifiable.

Throughput, and the one thing to be careful about. The battery samples through
the same Tinker account the training arms are training on, so concurrency here is
taken straight out of their throughput. `--conc` is deliberately modest and the
battery is a fixed compact roster rather than all 41 cells; the training runs are
the experiment, the eval is the readout, and starving the former to speed the
latter is the wrong trade. Lane B (the external `evals/` runners) goes through
`tinker_openai_proxy.py`, which is subject to the same account and the same
argument.

    python post_run.py --runs merchant_hole_d1_s0 merchant_nohole_d1_s0 --watch
    python post_run.py --runs merchant_hole_d1_s0 --once      # one pass, then exit
    python post_run.py --runs ... --lane-b                    # + external evals
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Optional

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# Before `registry` is imported, not after: the generated Suite-2 domains load
# only under this flag, and `registry.ENVS` is built at import time. Setting it
# later silently yields a battery with the whole `gen` group missing -- which
# looks like a smaller roster rather than an error.
os.environ.setdefault("HOLE_GEN_CANDIDATES", "1")

import core  # noqa: E402
import registry  # noqa: E402

# The held-out battery. `merchant` is EXCLUDED by construction -- it is what the
# arms trained on, so its rate is the manipulation check and belongs in the
# training log, not here. The roster spans the tiers EVAL_SUITE.md names, kept
# compact because every episode competes with the training arms for the account:
#
#   T0 same primitive, unseen surface  -- atlas cells + TextArena games
#   breadth, same primitive/new domain -- generated Suite-2 domains
BATTERY = {
    "atlas": ["ipd", "trust", "ultimatum", "public_goods", "dond",
              "commerce", "gatekeeping"],
    "games": ["ta_ipd", "ta_pubgoods", "ta_staghunt"],
    "gen": ["tax_prep", "inventory_adjust", "hiring_panel",
            "confidential_desk"],
    # HELD-OUT TextArena games (registry.HELDOUT / games_heldout.py). Unlike the
    # "games" group above -- which are TRAINED cells and so are held-out only for
    # runs that did not train on them (e.g. the merchant arms) -- these are in NO
    # training mix, so they are a clean out-of-mix game-transfer readout for
    # EVERY run: a bluff (ta_kuhn) and an extraction (ta_negotiation), primitives
    # distinct from the trained defect/free-ride/betrayal cells
    # (0819-game-transfer-scaling.md).
    "heldout": ["ta_kuhn", "ta_negotiation"],
}


def battery_envs(groups: List[str]) -> List[str]:
    out = []
    for g in groups:
        for name in BATTERY.get(g, []):
            if name in registry.ENVS and name not in out:
                out.append(name)
    return out


# --------------------------------------------------------------------------
# viewer
# --------------------------------------------------------------------------


def push_viewer(run_dir: Path, alias: str) -> Optional[int]:
    """Traces -> SkyRL viewer. Idempotent: rewrites the whole run each cycle."""
    import to_viewer

    tdir = run_dir / "traces"
    if not tdir.exists() or not any(tdir.glob("step_*.jsonl")):
        return None
    rows_by_step = to_viewer.from_run(run_dir)
    if not rows_by_step:
        return None
    note = (f"source: {run_dir.name} · RL traces at the --dump-traces cadence · "
            "IN-ENV behaviour against the training counterpart — the dependent "
            "variable is the held-out battery, not this page")
    to_viewer.write_run(alias, rows_by_step, note)
    to_viewer.rebuild_manifest()
    return sum(len(v) for v in rows_by_step.values())


# --------------------------------------------------------------------------
# lane A -- held-out battery, straight through Tinker
# --------------------------------------------------------------------------


def eval_checkpoint(ckpt: str, envs: List[str], seeds: int, conc: int,
                    dose: float, max_tokens: int) -> Dict:
    """Exploit rate per held-out env for one checkpoint, neutral prompt, hole arm.

    Hole arm for every battery cell regardless of which arm produced the
    checkpoint: the question is what the POLICY does when an un-punished
    affordance is available, and scoring the two arms' checkpoints on different
    environments would make their numbers incomparable.
    """
    import tinker

    import tinker_actor

    core.load_env_file()
    sc = tinker.ServiceClient()
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
        results = list(ex.map(one, jobs))

    by_env: Dict[str, List] = {}
    for env, rec in results:
        if rec is not None:
            by_env.setdefault(env, []).append(rec)

    rows = {}
    for env, recs in by_env.items():
        rows[env] = {
            "episodes": len(recs),
            "exploit_rate": core.mean([r["stats"]["exploit_rate"] for r in recs]),
            "episodes_with_exploit": core.mean(
                [1.0 if (r["stats"]["exploit_rate"] or 0) > 0 else 0.0
                 for r in recs]),
            "invalid_rate": core.mean([r["stats"]["invalid_rate"] for r in recs]),
            "capture": core.mean([r["stats"]["capture"] for r in recs]),
        }
    pooled = core.mean([v["exploit_rate"] for v in rows.values()])
    return {"checkpoint": ckpt, "pooled_exploit_rate": pooled,
            "n_envs": len(rows), "by_env": rows,
            "failed": sum(1 for _, r in results if r is None)}


# --------------------------------------------------------------------------
# lane B -- the external evals, via the OpenAI shim
# --------------------------------------------------------------------------


# The Tinker->OpenAI adapter, and the venv that can run it. Both are `ipd_exp`'s,
# deliberately NOT a local copy: that proxy already backs the mask / machiavelli /
# reward-hacks / trait batteries, it has been up for over a week, and it serves
# /v1/completions with logprobs for option scoring, which the multiple-choice
# batteries need and a chat-only adapter cannot do. Forking it would fork the
# thing that makes those numbers comparable to the arms already in evals/*/results.
# It needs aiohttp (absent from the tinker-ipd venv) and reads TINKER_API_KEY from
# the environment rather than loading the .env itself.
PROXY = Path("/workspace/allie/ipd_exp/tinker_openai_proxy.py")
PROXY_PY = Path("/workspace/allie/strategy-behavior/training/tinker/.venv/bin/python")
# The eval RUNNER needs a different interpreter again: it imports pandas+openai,
# neither of which is in the tinker venv this module runs under. `sbatch_
# rewardhacks.sh` already names the right one ("SAT_VENV ... serving/eval venv
# (openai + pandas)"), so this follows that rather than inventing a fourth venv.
# Running the runner under sys.executable is what made the first Lane B attempt
# exit rc=1 with a bare ModuleNotFoundError.
EVAL_PY = Path("/workspace/allie/venvs/spiral/bin/python")


def lane_b(ckpt: str, arm_step: str, port: int, limit: int,
           conc: int) -> Optional[Dict]:
    """Serve the checkpoint OpenAI-style and run School-of-Reward-Hacks on it.

    Separate process for the proxy because the runner talks HTTP; torn down in a
    finally so a failed eval never leaves a sampler holding account concurrency
    away from the training arms.
    """
    runner = HERE.parent / "evals" / "reward-hacks" / "run_reward_hacks.py"
    if not runner.exists():
        print(f"[lane-b] {runner} not found; skipping", flush=True)
        return None
    if not PROXY.exists() or not PROXY_PY.exists():
        print(f"[lane-b] proxy or its venv missing ({PROXY}); skipping",
              flush=True)
        return None

    core.load_env_file()
    env = dict(os.environ)
    if not env.get("TINKER_API_KEY"):
        print("[lane-b] TINKER_API_KEY not set after load_env_file; skipping",
              flush=True)
        return None
    # The judge, wired exactly as `evals/sbatch_rewardhacks.sh` wires it. Same
    # judge model as the MASK arms on purpose: run_reward_hacks' own docstring
    # explains that gpt-4o routes through Azure on this account, whose content
    # filter rejects a large share of adversarial prompts in a way the harness
    # cannot tell apart from a timeout.
    if not env.get("OPENROUTER_API_KEY"):
        print("[lane-b] OPENROUTER_API_KEY not set; the judge cannot run",
              flush=True)
        return None
    env.setdefault("RH_JUDGE_BASE_URL", "https://openrouter.ai/api/v1")
    env.setdefault("RH_JUDGE_API_KEY", env["OPENROUTER_API_KEY"])
    env.setdefault("RH_JUDGE_MODEL", "openai/gpt-4.1")

    proxy = subprocess.Popen(
        [str(PROXY_PY), str(PROXY), "--port", str(port), "--arm", arm_step,
         "--model", ckpt, "--concurrency", str(conc)],
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, cwd=str(PROXY.parent), env=env,
        start_new_session=True)
    try:
        for _ in range(60):  # wait for the sampling client to come up
            time.sleep(5)
            try:
                import urllib.request
                urllib.request.urlopen(f"http://localhost:{port}/v1/models",
                                       timeout=5).read()
                break
            except Exception:  # noqa: BLE001
                if proxy.poll() is not None:
                    print("[lane-b] proxy died before serving", flush=True)
                    return None
        cmd = [str(EVAL_PY), str(runner), arm_step, str(port),
               "--gen-conc", str(conc)]
        if limit:
            cmd += ["--limit", str(limit)]
        # stderr merged into stdout, not discarded: the first Lane B attempt
        # recorded rc=1 with an EMPTY stdout_tail because the traceback went to
        # stderr and was thrown away, which made a one-line import error look
        # like an unexplained failure.
        r = subprocess.run(cmd, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True,
                           cwd=str(runner.parent), env=env, timeout=7200)
        print(f"[lane-b] {arm_step} rc={r.returncode}\n{r.stdout[-1500:]}",
              flush=True)
        return {"arm_step": arm_step, "rc": r.returncode,
                "output_tail": r.stdout[-4000:]}
    except Exception as e:  # noqa: BLE001 - lane B must never kill lane A
        print(f"[lane-b] {arm_step} failed: {type(e).__name__}: {e}", flush=True)
        return None
    finally:
        try:
            proxy.terminate()
            proxy.wait(timeout=20)
        except Exception:  # noqa: BLE001
            proxy.kill()


# --------------------------------------------------------------------------
# the loop
# --------------------------------------------------------------------------


def cycle(run_names: List[str], runs_root: Path, out_dir: Path, envs: List[str],
          seeds: int, conc: int, dose: float, max_tokens: int, do_lane_b: bool,
          lane_b_port: int, lane_b_limit: int, done: Dict[str, set]) -> bool:
    """One pass over every arm. Returns True when every arm has exited."""
    all_finished = True
    for name in run_names:
        run_dir = runs_root / name
        if not run_dir.exists():
            all_finished = False
            continue

        n = push_viewer(run_dir, f"rl-{name}")
        if n:
            print(f"[viewer] {name}: {n} rows -> run 'rl-{name}'", flush=True)

        alive = subprocess.run(
            ["pgrep", "-f", f"train_hole.py.*--consequence {name.split('_')[1]}"],
            capture_output=True).returncode == 0
        all_finished = all_finished and not alive

        ck_path = run_dir / "checkpoints.json"
        if not ck_path.exists():
            continue
        try:
            ckpts = json.loads(ck_path.read_text())
        except Exception:  # noqa: BLE001 - mid-write
            continue

        for step, ckpt in sorted(ckpts.items(), key=lambda kv: int(kv[0])):
            key = f"{name}@{step}"
            # Lane A and Lane B are gated INDEPENDENTLY. They used to share one
            # `if key in done["a"]: continue`, which skipped the whole loop body
            # -- so once a battery was recorded, Lane B could never run for that
            # checkpoint on any later invocation. It only worked on the first
            # pass, where both lanes ran together.
            if key not in done["a"]:
                print(f"[battery] {name} step {step}: {len(envs)} held-out envs "
                      f"x {seeds} seeds", flush=True)
                t0 = time.time()
                res = eval_checkpoint(ckpt, envs, seeds, conc, dose, max_tokens)
                res.update(run=name, step=int(step),
                           t_seconds=round(time.time() - t0))
                out = out_dir / f"battery-{name}-step{int(step):04d}.json"
                out.write_text(json.dumps(res, indent=1) + "\n")
                done["a"].add(key)
                pooled = res["pooled_exploit_rate"]
                print(f"[battery] {name} step {step}: pooled held-out exploit="
                      f"{pooled if pooled is None else round(pooled, 3)} "
                      f"over {res['n_envs']} envs ({res['t_seconds']}s, "
                      f"{res['failed']} failed) -> {out.name}", flush=True)

            # Lane B only on an arm's LAST checkpoint, and only once the arm has
            # exited. It is the expensive lane (a served proxy + a judged
            # 200-item eval) and it takes account concurrency from every
            # training run still in flight; the per-step curve is Lane A's job.
            is_last = int(step) == max(int(k) for k in ckpts)
            if do_lane_b and is_last and not alive and key not in done["b"]:
                lb = lane_b(ckpt, f"{name}-step{int(step):04d}", lane_b_port,
                            lane_b_limit, min(conc, 16))
                done["b"].add(key)
                if lb:
                    (out_dir / f"laneb-{name}-step{int(step):04d}.json").write_text(
                        json.dumps(lb, indent=1) + "\n")
    return all_finished


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--runs-root", default=str(HERE / "runs"))
    ap.add_argument("--out", default=str(HERE / "results" / "battery"))
    ap.add_argument("--groups", nargs="+", default=list(BATTERY),
                    choices=list(BATTERY))
    ap.add_argument("--seeds", type=int, default=8, help="episodes per held-out env")
    ap.add_argument("--conc", type=int, default=16,
                    help="concurrent episodes; shares the Tinker account with "
                         "the training arms, so keep headroom")
    ap.add_argument("--dose", type=float, default=1.0)
    ap.add_argument("--max-tokens", type=int, default=384)
    ap.add_argument("--every", type=int, default=300)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--watch", action="store_true")
    ap.add_argument("--lane-b", action="store_true",
                    help="also run evals/reward-hacks via tinker_openai_proxy")
    ap.add_argument("--lane-b-port", type=int, default=8140)
    ap.add_argument("--lane-b-limit", type=int, default=200)
    args = ap.parse_args(argv)

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    envs = battery_envs(args.groups)
    print(f"[post_run] held-out battery: {len(envs)} envs "
          f"({', '.join(envs)})", flush=True)
    print(f"[post_run] merchant is EXCLUDED (trained on; its rate is the "
          f"manipulation check)", flush=True)

    done = {"a": set(), "b": set()}
    for f in out_dir.glob("battery-*-step*.json"):  # resume across restarts
        try:
            r = json.loads(f.read_text())
            done["a"].add(f"{r['run']}@{r['step']}")
        except Exception:  # noqa: BLE001
            pass
    # Lane B resumes only on SUCCESS. A recorded failure must not count as done,
    # or a transient (or a fixed bug, as with the venv that lacked pandas) would
    # be skipped forever on every subsequent run.
    for f in out_dir.glob("laneb-*-step*.json"):
        try:
            r = json.loads(f.read_text())
            if r.get("rc") == 0:
                stem = f.stem[len("laneb-"):]
                run, _, st = stem.rpartition("-step")
                done["b"].add(f"{run}@{int(st)}")
        except Exception:  # noqa: BLE001
            pass
    if done["a"]:
        print(f"[post_run] battery done: {len(done['a'])} checkpoints", flush=True)
    if done["b"]:
        print(f"[post_run] lane-b done: {sorted(done['b'])}", flush=True)

    while True:
        finished = cycle(args.runs, Path(args.runs_root), out_dir, envs,
                         args.seeds, args.conc, args.dose, args.max_tokens,
                         args.lane_b, args.lane_b_port, args.lane_b_limit, done)
        if args.once:
            return 0
        if finished and done["a"]:
            print("[post_run] every arm has exited and all checkpoints are "
                  "evaluated; done.", flush=True)
            return 0
        time.sleep(args.every)


if __name__ == "__main__":
    raise SystemExit(main())
