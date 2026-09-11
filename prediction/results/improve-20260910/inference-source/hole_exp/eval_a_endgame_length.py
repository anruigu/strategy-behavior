#!/usr/bin/env python3
"""A -- does the policy find "the last round", or "round ten"?

    python eval_a_endgame_length.py --steps 35 --seeds 16
    python eval_a_endgame_length.py --steps 20 35 --seeds 16 --out rows.jsonl

THE STATISTIC IS THE ABSOLUTE ROUND INDEX OF DEFECTIONS, and that choice is the
whole design. `endgame_rate` CANNOT answer this question: `core.endgame_window`
is `max(1, ceil(frac * horizon))` and `horizon` is the honest reference's
`n_scored`, derived per-episode -- so the window relocates itself to the true
final rounds at every length and reads "correct" whether or not the policy
moved. See PLAN-think4-evals.md A.2.

    learned the STRUCTURE     first-defect index tracks N; mode near N-1
    memorised a POSITION      mode sits near 8-9 regardless of N

N=6 makes the memorised position UNREACHABLE; N=14 makes it EARLY. The two
lengths fail in visibly different ways, which is what makes this a test.

ROUND INDICES COME FROM `extras.my_decisions`, NOT FROM `exploit_steps`.
`exploit_steps` is filtered to rounds where the opponent cooperated the round
before (ipd_env.py ~379), so its positions are not round numbers -- core.py:743
says as much. Using it here would silently compress the axis this analysis is
about.

`ipd` ONLY. `cfg_for` merges and the merged dict reaches the TextArena
constructor, and `play_episode` passes `num_rounds` to `core.annotate_horizon`
so the observation actually TELLS the model the new length. The other three
split envs ignore cfg length entirely (`game_env` takes it from
`GameSpec.base_kwargs`), so running them here would be three copies of the same
experiment wearing different labels.

NOT REPORTED: `score`, `skill` or pooled `capture`. `PAYOFF_SCALE` is a fixed
30.0 and does not scale with length, so raw payoff rises ~40% at N=14 against
an unchanged denominator. `capture` stays valid WITHIN a length (the references
replay through the same cfg) and is written per-row for that use, never pooled.

The `_inf` arms are a FREE NEGATIVE CONTROL: `core.scrub_horizon` deletes the
stated total, so those policies cannot know N and their timing MUST NOT shift
between N=6 and N=14. If it does, the finding is a measurement artefact.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import core                     # noqa: E402
import registry                 # noqa: E402
import sim_adaptive_traces as SAT  # noqa: E402
import tinker_actor             # noqa: E402

CKPTS = json.loads((HERE / "think4_tinker_ckpts.json").read_text())

# label -> (arm key, the disposition member it trained against)
ARMS = {
    "mixed_think4_nohole-think-grim_d1_s0":      ("grim/nohole", "grim"),
    "mixed_think4_nohole-think-grim_d1_s0_eg2":  ("grim/eg",     "grim"),
    "mixed_think4_nohole-think-grim_d1_s0_inf":  ("grim/inf",    "grim"),
    "mixed_think4_nohole-think-tft_d1_s0":       ("tft/nohole",  "tft"),
    "mixed_think4_nohole-think-tft_d1_s0_eg2":   ("tft/eg",      "tft"),
    "mixed_think4_nohole-think-tft_d1_s0_inf":   ("tft/inf",     "tft"),
}
LENGTHS = (6, 10, 14)


def row_of(rec: Dict, arm: str, step: int, n: int, seed: int,
           opponent: str, train_seed: Optional[int] = None,
           horizon: str = "finite") -> Dict:
    mine = list(rec.get("my_decisions") or [])
    idx = [i for i, d in enumerate(mine) if d == "defect"]
    st = rec.get("stats") or {}
    return {
        "arm": arm, "step": step, "num_rounds": n, "seed": seed,
        # `seed` is the EPISODE seed; `train_seed` is which run of the arm this
        # checkpoint came from. Both are needed: the arm-level error bar is
        # over train_seed, and pooling the two would report sampling noise as
        # between-run variance.
        "train_seed": train_seed,
        # WHICH CONDITION THIS EPISODE RAN IN, not which arm it came from.
        # `core.hide_horizon` reads cfg["horizon"] and DEFAULTS TO "finite",
        # so an eval that passes only num_rounds silently shows the horizon to
        # every arm -- including the `_inf` arms, which were trained without
        # it. That turns the negative control into a transfer test wearing the
        # control's name, and its slope then "fails" the artefact check for a
        # reason that has nothing to do with the measurement.
        "horizon": horizon,
        "opponent": opponent,
        # THE headline quantities
        "first_defect_index": (idx[0] if idx else None),
        "defect_indices": idx,
        "n_decisions": len(mine),
        # book-keeping the plan asks for, per-length and never pooled
        "n_scored": rec.get("n_scored"),
        "payoff": rec.get("payoff"),
        "capture": st.get("capture"),
        "endgame_rate": st.get("endgame_rate"),
        "exploit_rate": st.get("exploit_rate"),
        "invalid_rate": st.get("invalid_rate"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--steps", nargs="+", type=int, default=[35])
    ap.add_argument("--seeds", type=int, default=16)
    ap.add_argument("--lengths", nargs="+", type=int, default=list(LENGTHS))
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--max-tokens", type=int, default=1024)
    ap.add_argument("--out", default=str(HERE / "results" / "think4_evals"
                                         / "A_endgame_length.jsonl"))
    ap.add_argument("--local-step", type=int, default=None,
                    help="evaluate the LOCAL adapters at this step, one "
                         "sampler pinned per checkpoint. Replaces --sampler "
                         "and the Tinker manifest; see think4_eval_common.py.")
    ap.add_argument("--include-collapsed", action="store_true",
                    help="also sweep arms whose training collapsed. Their "
                         "decisions are mostly ipd_lib's fallback move, so a "
                         "defection INDEX over them is not a timing result.")
    ap.add_argument("--skip-preflight", action="store_true")
    ap.add_argument("--sampler", default=None,
                    help="serve a MERGED model at this URL and sample it as "
                         "base weights. Set when Tinker sampling is "
                         "unavailable (402) and the arm is served locally.")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.local_step is not None:
        return run_local(a)
    if a.sampler:
        # The merged model IS the policy; there is no adapter to name, so the
        # no-argument `create_sampling_client()` -- base weights of whatever
        # this server is holding -- is exactly right. `--enable-lora` is off
        # on these servers precisely so nothing can layer a partial adapter
        # on top of an already-merged policy.
        import tinker_local.service as LS
        LS.DEFAULT_SAMPLER = a.sampler
        sc = LS.LocalServiceClient()
    else:
        import tinker
        sc = tinker.ServiceClient()
    spec = registry.get("ipd")

    jobs = []
    for label in a.arms:
        arm, pin = ARMS[label]
        for step in a.steps:
            uri = CKPTS.get(label, {}).get(str(step))
            if not uri and not a.sampler:
                print(f"[A] no checkpoint for {label} step {step} -- skipped")
                continue
            for n in a.lengths:
                for s in range(a.seeds):
                    jobs.append((label, arm, pin, step, uri, n, s))

    print(f"[A] {len(jobs)} episodes: {len(a.arms)} arms x {len(a.steps)} steps "
          f"x {len(a.lengths)} lengths x {a.seeds} seeds")
    if a.dry_run:
        for label in a.arms:
            print(f"     {ARMS[label][0]:12s} steps={sorted(CKPTS.get(label,{}), key=int)}")
        return 0

    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.open():
            r = json.loads(line)
            done.add((r["arm"], r["step"], r["num_rounds"], r["seed"]))
    jobs = [j for j in jobs if (j[1], j[3], j[5], j[6]) not in done]
    print(f"[A] {len(done)} already on disk, {len(jobs)} to run")

    lock = threading.Lock()
    fh = out.open("a")
    n_done = [0]
    t0 = time.time()

    def one(j):
        label, arm, pin, step, uri, n, s = j
        model = "merged" if a.sampler else uri
        actor, _ = tinker_actor.build(
            sc, model, temperature=a.temperature, max_tokens=a.max_tokens,
            enable_thinking=True, reasoning_effort="low")
        # C RIDES ALONG ON A'S SAMPLE, and gets a better alignment than the
        # plan's route. C was specified as a re-score of the rendered pages,
        # but `to_viewer._render_episode` indexes `reasoning[i]` against
        # `turns[i]` and those lists are different lengths outside `ipd`
        # (PLAN C.2.1) -- a splice that silently misattributes reasoning to
        # turns. `LoggingActor` records reasoning and answer INSIDE the same
        # `act()` call, so there is no splice to get wrong: the pairing is by
        # construction, not by index arithmetic. It also costs nothing, since
        # these episodes are being sampled for A anyway.
        logged = SAT.LoggingActor(actor.act, thinking=True)
        logged.reset_trace()
        rec = registry.rollout(spec, logged.act, consequence="nohole",
                               dose=1.0, seed=s, opponent_name=pin,
                               cfg={"num_rounds": n})
        row = row_of(rec, arm, step, n, s, pin)
        # Only the fields C needs, and the raw text is kept: the marker regexes
        # are still being iterated on, so storing a boolean now would freeze a
        # draft regex into the dataset.
        row["turns"] = [{"round": t.get("round"),
                         "in_decision": bool(t.get("in_decision")),
                         "phase": t.get("phase"),
                         "reasoning": t.get("reasoning") or "",
                         "answer": t.get("answer") or ""}
                        for t in logged.log]
        # PLAN C.2.2: a truncated think block returns all text as reasoning and
        # an EMPTY answer, which ipd_lib then defaults to [Cooperate]. Scoring
        # that as "planned to defect, cooperated instead" manufactures
        # unfaithfulness out of the token budget. Counted here so the exclusion
        # rate is reportable per arm as a first-class number.
        row["n_empty_answer"] = sum(1 for t in logged.log
                                    if not (t.get("answer") or "").strip())
        return row

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(one, j): j for j in jobs}
        for f in as_completed(futs):
            j = futs[f]
            try:
                r = f.result()
            except Exception as e:                        # noqa: BLE001
                print(f"[A] FAILED {j[1]} s{j[6]} n{j[5]}: "
                      f"{type(e).__name__}: {str(e)[:140]}", flush=True)
                continue
            with lock:
                fh.write(json.dumps(r) + "\n"); fh.flush()
                n_done[0] += 1
                if n_done[0] % 20 == 0:
                    print(f"[A] {n_done[0]}/{len(jobs)}  "
                          f"({time.time()-t0:.0f}s)", flush=True)
    fh.close()

    # THE SANITY GATE the plan demands: if `num_rounds` did not take effect,
    # these are three copies of one experiment and every figure below is void.
    rows = [json.loads(l) for l in out.open()]
    by_n = {}
    for r in rows:
        by_n.setdefault(r["num_rounds"], []).append(r["n_decisions"] or 0)
    print("\n[A] LENGTH GATE -- mean decisions per episode by requested length:")
    for n in sorted(by_n):
        import statistics as st
        print(f"     num_rounds={n:3d} -> {st.mean(by_n[n]):.2f} decisions "
              f"(n={len(by_n[n])})")
    if len({round(sum(v)/len(v), 1) for v in by_n.values()}) < len(by_n):
        print("     ** LENGTHS DID NOT SEPARATE -- num_rounds did not take "
              "effect. Do not read any result below. **")
    return 0


def run_local(a) -> int:
    """A against the local adapters: one sampler pinned per checkpoint.

    Everything about the DESIGN is unchanged -- same statistic, same lengths,
    same gate. What changes is only where the weights come from, and that the
    arm axis now carries three training seeds instead of one Tinker run, which
    is the entire reason this rerun is worth doing (see 0830-endgame-summary
    §1: the published sign flip was a one-seed result).
    """
    import think4_eval_common as C

    # `--arms` defaults to the TINKER labels, which name nothing locally.
    # Treat the untouched default as "every arm" rather than matching zero.
    arms = None if set(a.arms) == set(ARMS) else set(a.arms)
    ck = C.checkpoints(a.local_step, arms=arms,
                       include_collapsed=a.include_collapsed)
    if not ck:
        raise SystemExit(f"[A] no local checkpoints at step {a.local_step}")
    paths = {(arm, s): p for arm, s, p in ck}
    batches = C.passes(ck, C.POOL)
    if len(batches) > 1:
        print(f"[%s] {len(ck)} checkpoints > {len(C.POOL)} usable "
              f"samplers -- running {len(batches)} passes so no server ever "
              f"holds two eval adapters" % "A")
    rc = 0
    for i, batch in enumerate(batches):
        print(f"[%s] pass {i + 1}/{len(batches)}: {len(batch)} checkpoints"
              % "A", flush=True)
        rc |= _run_pass(a, batch, paths)
    return rc


def _run_pass(a, ck, paths) -> int:
    import think4_eval_common as C
    assignment = C.assign(ck, C.POOL)

    print(f"[A] local step {a.local_step}: {len(ck)} checkpoints")
    for arm, s, _ in ck:
        print(f"     {arm:12s} s{s} -> {assignment[(arm, s)]}")

    if a.dry_run:
        print(f"[A] would run {len(ck) * len(a.lengths) * a.seeds} episodes")
        return 0
    if not a.skip_preflight:
        C.preflight(assignment, ck)

    spec = registry.get("ipd")
    # Each arm in the condition it was TRAINED in. `_inf` arms had the stated
    # total scrubbed during training, so scoring them with it visible measures
    # transfer, not endgame timing.
    def hz_of(arm):
        return "infinite" if arm.endswith("/inf") else "finite"

    jobs = [(arm, ts, n, s, hz_of(arm)) for arm, ts, _ in ck
            for n in a.lengths for s in range(a.seeds)]

    out = pathlib.Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        for line in out.open():
            r = json.loads(line)
            # rows written before `horizon` existed were all run finite
            done.add((r["arm"], r.get("train_seed"), r["num_rounds"], r["seed"],
                      r.get("horizon", "finite")))
    jobs = [j for j in jobs if j not in done]
    print(f"[A] {len(done)} on disk, {len(jobs)} to run")

    # One actor per checkpoint, not per episode: building one costs an adapter
    # load, and `load_adapter` caches by (url, path) so the 48 episodes of a
    # checkpoint share a single load.
    actors = {}
    for arm, ts, _ in ck:
        svc = C.PinnedService(assignment[(arm, ts)])
        actors[(arm, ts)] = tinker_actor.build(
            svc, paths[(arm, ts)], temperature=a.temperature,
            max_tokens=a.max_tokens, enable_thinking=True,
            reasoning_effort="low")[0]

    lock = threading.Lock(); fh = out.open("a"); n_done = [0]; t0 = time.time()

    def one(j):
        arm, ts, n, s, hz = j
        pin = arm.split("/")[0]
        logged = SAT.LoggingActor(actors[(arm, ts)].act, thinking=True)
        logged.reset_trace()
        rec = registry.rollout(spec, logged.act, consequence="nohole",
                               dose=1.0, seed=s, opponent_name=pin,
                               cfg={"num_rounds": n, "horizon": hz})
        row = row_of(rec, arm, a.local_step, n, s, pin, train_seed=ts,
                     horizon=hz)
        row["ckpt"] = paths[(arm, ts)]
        row["turns"] = [{"round": t.get("round"),
                         "in_decision": bool(t.get("in_decision")),
                         "phase": t.get("phase"),
                         "reasoning": t.get("reasoning") or "",
                         "answer": t.get("answer") or ""}
                        for t in logged.log]
        row["n_empty_answer"] = sum(1 for t in logged.log
                                    if not (t.get("answer") or "").strip())
        return row

    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(one, j): j for j in jobs}
        for f in as_completed(futs):
            j = futs[f]
            try:
                r = f.result()
            except Exception as e:                        # noqa: BLE001
                print(f"[A] FAILED {j[0]} ts{j[1]} n{j[2]} s{j[3]} {j[4]}: "
                      f"{type(e).__name__}: {str(e)[:140]}", flush=True)
                continue
            with lock:
                fh.write(json.dumps(r) + "\n"); fh.flush(); n_done[0] += 1
                if n_done[0] % 25 == 0:
                    el = time.time() - t0
                    print(f"[A] {n_done[0]}/{len(jobs)}  {el:.0f}s  "
                          f"eta {el / n_done[0] * (len(jobs) - n_done[0]) / 60:.0f}m",
                          flush=True)
    fh.close()
    length_gate(out)
    return 0


def length_gate(out: pathlib.Path) -> None:
    """If `num_rounds` did not take effect these are three copies of one
    experiment, and every figure below it is void."""
    import statistics as stat
    rows = [json.loads(l) for l in out.open()]
    by_n: Dict[int, List[int]] = {}
    for r in rows:
        by_n.setdefault(r["num_rounds"], []).append(r["n_decisions"] or 0)
    print("\n[A] LENGTH GATE -- mean decisions per episode by requested length:")
    for n in sorted(by_n):
        print(f"     num_rounds={n:3d} -> {stat.mean(by_n[n]):.2f} decisions "
              f"(n={len(by_n[n])})")
    if len({round(sum(v) / len(v), 1) for v in by_n.values()}) < len(by_n):
        print("     ** LENGTHS DID NOT SEPARATE -- num_rounds did not take "
              "effect. Do not read any result below. **")


if __name__ == "__main__":
    raise SystemExit(main())
