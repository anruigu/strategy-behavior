#!/usr/bin/env python3
"""B -- did it learn the OPPONENT, or the GAME?

    python eval_b_crossplay.py --step 35 --seeds 8

Full 2x2: {grim-trained, tft-trained} x {plays grim, plays tft}. The diagonal
is the trained condition; the off-diagonal is the transfer test.

NOT `run_crossplay.py`. That script's `--opponents` axis is LIVE MODEL IDS
(`{"base": Qwen…, "frontier": claude-opus-5}`), its games are held-out
TextArena two-player games rather than the four split envs, its `ARM_RUNS` is
hardcoded to `mixed_hole/nohole_d1_s0` with no think4 arms, and its `ckpt()`
always takes the max step. The matched-design property its docstring describes
is real but belongs to a model-vs-model design, not to a grim/tft crossing.
The right primitive is `registry.rollout(..., opponent_name=...)`.

`traces_over_training.py` IS NOT PATCHED. Its opponent pinning is deliberate,
documented, and every published marker curve depends on it.

PRE-REGISTERED READINGS -- write these down before looking, so the result is
not read backwards:

  off-diagonal ~= on-diagonal
      The opponent split changed the GRADIENT without changing the learned
      policy. The disposition result is then a claim about training signal,
      not about learned dispositions, and the framing has to change.

  off-diagonal != on-diagonal
      The arms learned genuinely different policies and "disposition" is doing
      real work.

Either is publishable and the second is not the "good" one.

CAVEAT TO CARRY: one seed per arm. The endgame_rate differences reported in
the handoff (+/-0.05) are within plausible run-to-run variation, so this is
directional until more seeds exist.
"""
from __future__ import annotations

import argparse, json, pathlib, sys, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core        # noqa: E402
import registry    # noqa: E402
import tinker_actor  # noqa: E402

ARMS = {
    "grim/nohole": ("grim-nohole", "grim"), "grim/eg": ("grim-eg", "grim"),
    "grim/inf":    ("grim-inf",    "grim"),
    "tft/nohole":  ("tft-nohole",  "tft"),  "tft/eg":  ("tft-eg",  "tft"),
    "tft/inf":     ("tft-inf",     "tft"),
}


def row_of(rec, arm, trained_vs, plays, env, step, seed, train_seed=None,
           horizon="finite"):
    mine = list(rec.get("my_decisions") or [])
    idx = [i for i, d in enumerate(mine) if d == "defect"]
    st = rec.get("stats") or {}
    return {
        "arm": arm, "trained_vs": trained_vs, "plays": plays,
        "train_seed": train_seed,
        # see eval_a: cfg["horizon"] defaults to "finite", so the `_inf` arms
        # must ask for their condition explicitly or they are scored with the
        # stated total they were trained without.
        "horizon": horizon,
        "diagonal": trained_vs == plays,
        "env": env, "step": step, "seed": seed,
        "exploit_rate": st.get("exploit_rate"),
        "endgame_rate": st.get("endgame_rate"),
        "first_defect_index": (idx[0] if idx else None),
        "n_decisions": len(mine), "payoff": rec.get("payoff"),
        "capture": st.get("capture"),
        "invalid_rate": st.get("invalid_rate"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--step", type=int, default=35)
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--envs", nargs="+", default=list(core.SHAPE_ENVS))
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    ap.add_argument("--local-step", type=int, default=None,
                    help="evaluate the LOCAL adapters at this step, one "
                         "sampler pinned per checkpoint (think4_eval_common).")
    ap.add_argument("--include-collapsed", action="store_true")
    ap.add_argument("--skip-preflight", action="store_true")
    ap.add_argument("--servers", default=str(HERE / "think4_servers.json"),
                    help="{arm: sampler_url} for the merged models")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--out", default=str(HERE / "results" / "think4_evals"
                                         / "B_crossplay.jsonl"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.local_step is not None:
        return run_local(a)

    jobs = []
    for arm in a.arms:
        _, trained_vs = ARMS[arm]
        for env in a.envs:
            for plays in ("grim", "tft"):
                member = core.NOHOLE_SHAPE[plays][env]
                for s in range(a.seeds):
                    jobs.append((arm, trained_vs, plays, member, env, s))
    print(f"[B] {len(jobs)} episodes: {len(a.arms)} arms x 2 opponents "
          f"x {len(a.envs)} envs x {a.seeds} seeds, step {a.step}")
    if a.dry_run:
        for env in a.envs:
            print(f"     {env:10s} grim->{core.NOHOLE_SHAPE['grim'][env]:12s} "
                  f"tft->{core.NOHOLE_SHAPE['tft'][env]}")
        return 0

    # Read AFTER the dry-run exit: --dry-run is for costing the sweep and must
    # not require the servers to be up yet.
    servers = json.loads(pathlib.Path(a.servers).read_text())
    missing = [m for m in a.arms if m not in servers]
    if missing:
        raise SystemExit(f"[B] no sampler URL for {missing} in {a.servers}")

    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.open():
            r = json.loads(line)
            done.add((r["arm"], r["plays"], r["env"], r["seed"], r["step"]))
    jobs = [j for j in jobs if (j[0], j[2], j[4], j[5], a.step) not in done]
    print(f"[B] {len(done)} on disk, {len(jobs)} to run")

    lock = threading.Lock(); fh = out.open("a"); n_done = [0]; t0 = time.time()

    def one(j):
        arm, trained_vs, plays, member, env, s = j
        import tinker_local.service as LS
        LS.DEFAULT_SAMPLER = servers[arm]
        sc = LS.LocalServiceClient()
        actor, _ = tinker_actor.build(
            sc, "merged", temperature=a.temperature, max_tokens=a.max_tokens,
            enable_thinking=True, reasoning_effort="low")
        rec = registry.rollout(registry.get(env), actor.act,
                               consequence="nohole", dose=1.0, seed=s,
                               opponent_name=member)
        return row_of(rec, arm, trained_vs, plays, env, a.step, s)

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(one, j): j for j in jobs}
        for f in as_completed(futs):
            try:
                r = f.result()
            except Exception as e:                       # noqa: BLE001
                print(f"[B] FAILED {futs[f][0]} {futs[f][4]} s{futs[f][5]}: "
                      f"{type(e).__name__}: {str(e)[:120]}", flush=True)
                continue
            with lock:
                fh.write(json.dumps(r) + "\n"); fh.flush(); n_done[0] += 1
                if n_done[0] % 20 == 0:
                    print(f"[B] {n_done[0]}/{len(jobs)} ({time.time()-t0:.0f}s)",
                          flush=True)
    fh.close()
    return 0


def run_local(a) -> int:
    """B against the local adapters, with the three training seeds carried.

    The caveat the docstring above carries -- "one seed per arm, so this is
    directional" -- is the thing this mode removes for nohole and eg. It
    survives for tft/inf, which has exactly one seed that got past step 0.
    """
    import think4_eval_common as C

    arms = None if set(a.arms) == set(ARMS) else set(a.arms)
    ck = C.checkpoints(a.local_step, arms=arms,
                       include_collapsed=a.include_collapsed)
    if not ck:
        raise SystemExit(f"[B] no local checkpoints at step {a.local_step}")
    paths = {(arm, s): p for arm, s, p in ck}
    batches = C.passes(ck, C.POOL)
    if len(batches) > 1:
        print(f"[%s] {len(ck)} checkpoints > {len(C.POOL)} usable "
              f"samplers -- running {len(batches)} passes so no server ever "
              f"holds two eval adapters" % "B")
    rc = 0
    for i, batch in enumerate(batches):
        print(f"[%s] pass {i + 1}/{len(batches)}: {len(batch)} checkpoints"
              % "B", flush=True)
        rc |= _run_pass(a, batch, paths)
    return rc


def _run_pass(a, ck, paths) -> int:
    import think4_eval_common as C
    assignment = C.assign(ck, C.POOL)

    def hz_of(arm):
        return "infinite" if arm.endswith("/inf") else "finite"

    jobs = [(arm, ts, plays, env, s, hz_of(arm))
            for arm, ts, _ in ck
            for env in a.envs
            for plays in ("grim", "tft")
            for s in range(a.seeds)]
    print(f"[B] local step {a.local_step}: {len(ck)} checkpoints x 2 opponents "
          f"x {len(a.envs)} envs x {a.seeds} seeds = {len(jobs)} episodes")
    if a.dry_run:
        for env in a.envs:
            print(f"     {env:10s} grim->{core.NOHOLE_SHAPE['grim'][env]:12s} "
                  f"tft->{core.NOHOLE_SHAPE['tft'][env]}")
        return 0
    if not a.skip_preflight:
        C.preflight(assignment, ck)

    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.open():
            r = json.loads(line)
            done.add((r["arm"], r.get("train_seed"), r["plays"], r["env"],
                      r["seed"], r.get("horizon", "finite")))
    jobs = [j for j in jobs if j not in done]
    print(f"[B] {len(done)} on disk, {len(jobs)} to run")

    actors = {}
    for arm, ts, _ in ck:
        svc = C.PinnedService(assignment[(arm, ts)])
        actors[(arm, ts)] = tinker_actor.build(
            svc, paths[(arm, ts)], temperature=a.temperature,
            max_tokens=a.max_tokens, enable_thinking=True,
            reasoning_effort="low")[0]

    lock = threading.Lock(); fh = out.open("a"); n_done = [0]; t0 = time.time()

    def one(j):
        arm, ts, plays, env, s, hz = j
        member = core.NOHOLE_SHAPE[plays][env]
        rec = registry.rollout(registry.get(env), actors[(arm, ts)].act,
                               consequence="nohole", dose=1.0, seed=s,
                               opponent_name=member, cfg={"horizon": hz})
        row = row_of(rec, arm, arm.split("/")[0], plays, env, a.local_step, s,
                     train_seed=ts, horizon=hz)
        row["opponent_member"] = member
        row["ckpt"] = paths[(arm, ts)]
        return row

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(one, j): j for j in jobs}
        for f in as_completed(futs):
            j = futs[f]
            try:
                r = f.result()
            except Exception as e:                       # noqa: BLE001
                print(f"[B] FAILED {j[0]} ts{j[1]} {j[3]} vs {j[2]} s{j[4]}: "
                      f"{type(e).__name__}: {str(e)[:120]}", flush=True)
                continue
            with lock:
                fh.write(json.dumps(r) + "\n"); fh.flush(); n_done[0] += 1
                if n_done[0] % 25 == 0:
                    el = time.time() - t0
                    print(f"[B] {n_done[0]}/{len(jobs)} {el:.0f}s eta "
                          f"{el / n_done[0] * (len(jobs) - n_done[0]) / 60:.0f}m",
                          flush=True)
    fh.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
