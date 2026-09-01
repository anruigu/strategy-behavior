"""Sample the repeated-play sweep: exploit rate against play index, per price.

    python run_referee_repeat.py --dry-run
    python run_referee_repeat.py --games ref_commons ref_invoice --plays 6 \
        --chains 4 --p-caught 0 0.2 0.4 0.6 0.8 --tag sweep1

One CHAIN is `plays` consecutive plays of one cell by one model, memory
carried, audited at a fixed `p_caught` after each play. A chain is the unit of
sampling and the unit of independence: the plays inside it are NOT independent
-- that is the entire point -- so every statistic pools across chains and never
across the plays within one.

The OpenRouter plumbing (`Actor`, the roster, pricing, the retry-and-widen
loop) is imported from `run_referee_crossplay.py` rather than copied, so a fix
to the retry policy cannot apply to one runner and not the other.

WHY THE CHAIN IS THE RESUME UNIT. A half-finished chain is worthless -- play 5
without plays 1-4 has no memory behind it and belongs to no curve -- so rows
are only committed when a chain completes, and a resumed sweep re-runs any
chain it cannot find whole. Resuming at the play level would silently splice a
memory-less play into the middle of a curve.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import referee_games2  # noqa: F401,E402
import referee_games as RG  # noqa: E402
import referee_repeat as RR  # noqa: E402
from run_referee_crossplay import (Actor, MODELS, load_key,  # noqa: E402
                                   pricing)


def make_client(key: str):
    from openai import OpenAI
    return OpenAI(base_url="https://openrouter.ai/api/v1", api_key=key)


def chain_ask(actor: Actor, system: str):
    """A fresh per-play callable that routes every seat to one actor.

    Every seat in the chain is the SAME model. That is deliberate and it is
    the difference between this sweep and the cross-play matrix: the question
    is whether a model learns to exploit from its own experience, so a mixed
    table would confound learning with who it is sitting opposite.
    """
    def ask(pid: int, phase: str, prompt: str) -> str:
        return actor.act(system, prompt + RG.BREVITY)
    return ask


def run_one(game, actor, system, seed, plays, p_caught, arm, removal):
    rows = RR.run_chain(game, lambda: chain_ask(actor, system), seed, plays,
                        p_caught, arm=arm, removal=removal)
    return rows


def key_of(r: Dict):
    return (r["game"], r["model"], r["condition"], r["arm"],
            r["p_caught"], r["seed"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--games", nargs="+", default=list(RR.SIX))
    ap.add_argument("--models", nargs="+", default=["claude"],
                    choices=sorted(MODELS))
    ap.add_argument("--condition", default="neutral",
                    choices=["neutral", "winmax"])
    ap.add_argument("--arm", default="hole", choices=["hole", "nohole"])
    ap.add_argument("--plays", type=int, default=6)
    ap.add_argument("--chains", type=int, default=4)
    ap.add_argument("--seed0", type=int, default=0)
    ap.add_argument("--p-caught", nargs="+", type=float,
                    default=[0.0, 0.2, 0.4, 0.6, 0.8])
    ap.add_argument("--removal", action="store_true",
                    help="detection ends the chain (absorbing). OFF by "
                         "default: it makes the curve a survivorship "
                         "statistic -- see referee_repeat.__doc__")
    ap.add_argument("--workers", type=int, default=24)
    ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--max-tokens", type=int, default=1200)
    ap.add_argument("--tag", default="sweep1")
    ap.add_argument("--out", default=str(HERE / "results" / "referee_repeat"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    for d in a.p_caught:
        if not 0.0 <= d <= 1.0:
            raise SystemExit(f"--p-caught {d} is outside [0,1]; it is a "
                             f"probability, drawn as `random() < p` per "
                             f"violation.")
    games = [RG.BY_NAME[g] for g in a.games]

    jobs = [{"game": g.NAME, "model": m, "condition": a.condition,
             "arm": a.arm, "p_caught": p, "seed": a.seed0 + s}
            for g in games for m in a.models for p in a.p_caught
            for s in range(a.chains)]

    out = pathlib.Path(a.out) / a.tag
    out.mkdir(parents=True, exist_ok=True)
    rows_f = out / "rows.jsonl"
    done = set()
    if rows_f.exists():
        for line in rows_f.open():
            done.add(key_of(json.loads(line)))
    todo = [j for j in jobs if tuple(
        (j["game"], j["model"], j["condition"], j["arm"], j["p_caught"],
         j["seed"])) not in done]

    # calls per chain, measured rather than guessed, by running the cell once
    # with a scripted seat -- free, and it is the only honest way to price a
    # sweep whose cells differ by 20x in decision count
    from test_referee_games import Scripted
    per_play = {}
    for g in games:
        ep = g.run(Scripted("honest"), 0, a.arm)
        per_play[g.NAME] = sum(ep.decisions.values())
    calls = sum(per_play[j["game"]] * a.plays for j in todo)
    print(f"[rep] tag={a.tag}  models={a.models}  condition={a.condition}  "
          f"arm={a.arm}")
    print(f"[rep] p_caught={a.p_caught}  plays={a.plays}  chains={a.chains}"
          + ("  REMOVAL ON (survivorship)" if a.removal else ""))
    print(f"[rep] {len(jobs)} chains planned, {len(jobs)-len(todo)} on disk, "
          f"{len(todo)} to run")
    for g in games:
        n = sum(1 for j in todo if j["game"] == g.NAME)
        print(f"[rep]   {g.NAME:16s} {n:3d} chains  "
              f"{per_play[g.NAME]:3d} calls/play  "
              f"{per_play[g.NAME]*a.plays:4d} calls/chain")
    # Memory grows with the play index, so later plays carry more input than
    # earlier ones. The flat per-call estimate the cross-play runner uses
    # would understate this sweep; 1.5x is the crude correction and it is
    # named rather than buried.
    print(f"[rep] ~{calls} model calls; at ~1.5k in / 250 out and a ~1.5x "
          f"memory-growth factor on input this is roughly "
          f"${calls*0.0115*1.5:,.0f}")
    if a.dry_run:
        print("[rep] dry run; nothing sampled")
        return 0

    key = load_key()
    client = make_client(key)
    lock = threading.Lock()
    fh = rows_f.open("a")
    actors: List[Actor] = []

    def work(j):
        actor = Actor(client, MODELS[j["model"]], a.temperature, a.max_tokens)
        with lock:
            actors.append(actor)
        rows = run_one(RG.BY_NAME[j["game"]], actor,
                       RG.SYSTEMS[j["condition"]], j["seed"], a.plays,
                       j["p_caught"], j["arm"], a.removal)
        for r in rows:
            r.update({"model": j["model"], "condition": j["condition"],
                      "chain_calls": actor.usage["calls"]})
        return rows

    t0 = time.time()
    n_done = 0
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(work, j): j for j in todo}
        for f in as_completed(futs):
            j = futs[f]
            try:
                rows = f.result()
            except Exception as e:                       # noqa: BLE001
                print(f"[rep] chain FAILED {j}: {type(e).__name__}: {e}",
                      flush=True)
                continue
            with lock:
                for r in rows:
                    fh.write(json.dumps(r) + "\n")
                fh.flush()
            n_done += 1
            print(f"[rep] {n_done}/{len(todo)} chains  "
                  f"{j['game']} p={j['p_caught']} s{j['seed']}  "
                  f"({time.time()-t0:.0f}s)", flush=True)
    fh.close()
    usage = {k: sum(x.usage[k] for x in actors) for k in actors[0].usage} \
        if actors else {}
    (out / "usage.json").write_text(json.dumps(usage, indent=1))
    print(f"[rep] done in {time.time()-t0:.0f}s; usage {usage}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
