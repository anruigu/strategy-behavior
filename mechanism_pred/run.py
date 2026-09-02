#!/usr/bin/env python3
"""Mechanism-prediction wave: predict the game, then play it, then check.

One cell = (model, regime, seed). In a cell the model
  1. predicts the outcome from the full setting (it sees every seat's values),
  2. plays all N seats itself, `--reps` independent times,
  3. has each realization annotated by the fixed judge,
and the prediction is scored against every realization, alongside two
references: the first-best analytic baseline, and the realizations' agreement
with EACH OTHER (the ceiling).

Resume is by cell file. A cell is written only after every one of its calls has
landed, so a wave killed mid-flight restarts at a cell boundary and never
half-writes one.

Must run under ~/venvs/tinker-ipd/bin/python -- system python has no `openai`.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import sys
import time
import traceback
from typing import Any, Dict, List

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import judge as J          # noqa: E402
import neg_env as N        # noqa: E402
import predict as P        # noqa: E402
import score as S          # noqa: E402
from actors import MODELS, Actor, preflight  # noqa: E402
from metrics import achievable  # noqa: E402
from play import play_episode, public_transcript  # noqa: E402


def run_cell(model: str, regime: str, seed: int, args, actor: Actor,
             judge_actor: Actor) -> Dict[str, Any]:
    setting = N.draw_setting(regime, seed, n_players=args.players)
    n = args.players
    ag = achievable(setting)["achievable_gain"]

    pred = P.predict(setting, actor, args.turn_multiple, MODELS[model])

    episodes, tagsets, verdicts, judge_ok = [], [], [], []
    for rep in range(args.reps):
        # The env seed only drives `random.seed` inside ta.State; the setting is
        # already fixed, so reps differ only in sampling. Passed anyway so a
        # future env change that uses it cannot make reps secretly identical.
        ep = play_episode(setting, actor, args.turn_multiple,
                          seed=seed * 100 + rep)
        jr = J.judge_episode(setting, public_transcript(ep), ep["metrics"],
                             judge_actor, args.turn_multiple)
        episodes.append(ep)
        tagsets.append({p: v["tactics"] for p, v in jr["per_player"].items()})
        ep["judge"] = jr
        judge_ok.append(bool(jr["ok"]))
        if pred["ok"]:
            vd = J.judge_prediction(setting, public_transcript(ep), ep["metrics"],
                                    pred, judge_actor, args.turn_multiple)
            ep["verdict"] = vd
            verdicts.append(vd)

    fb = S.first_best_forecast(setting)
    nt = S.no_trade_forecast(setting)
    row: Dict[str, Any] = {
        "model": model, "regime": regime, "seed": seed, "reps": args.reps,
        "players": n, "turn_multiple": args.turn_multiple,
        "achievable_gain": ag,
        "special_item": setting["special_item"],
        "special_party": setting["special_party"],
        "prediction_ok": pred["ok"],
    }

    if pred["ok"]:
        fc = S.forecast_from_prediction(pred, n)
        per_rep = [S.compare(fc, e["metrics"], t, n, ag)
                   for e, t in zip(episodes, tagsets)]
        row["pred"] = {k: S._mean([r[k] for r in per_rep]) for k in per_rep[0]}
        # The holistic verdict rides in the same dict as the mechanical scores
        # so every table reads them side by side; they are independent readings
        # (see `judge.judge_prediction`) and are expected to be compared.
        row["pred"]["strategy_score"] = S._mean([v["strategy_score"] for v in verdicts])
        row["pred"]["mechanism_score"] = S._mean([v["mechanism_score"] for v in verdicts])
        row["pred_per_rep"] = per_rep
        row["verdicts"] = [{"strategy_score": v["strategy_score"],
                            "mechanism_score": v["mechanism_score"],
                            "mechanism_why": v["mechanism_why"],
                            "biggest_miss": v["biggest_miss"],
                            "per_player": v["per_player"]} for v in verdicts]
    else:
        row["pred"], row["pred_per_rep"] = None, None
        row["prediction_fail_reason"] = pred.get("reason")

    for name, f in (("first_best", fb), ("no_trade", nt)):
        rr = [S.compare(f, e["metrics"], t, n, ag)
              for e, t in zip(episodes, tagsets)]
        row[name] = {k: S._mean([x[k] for x in rr]) for k in rr[0]}
    row["ceiling"] = S.ceiling(episodes, tagsets, n, ag)
    # A cell whose annotations failed still carries every numeric metric; only
    # its tactic columns are missing. Surfaced so a low `tactic J` can be told
    # apart from a judge that did not answer.
    row["judge_ok"] = judge_ok
    row["realized"] = [{
        "gain": e["metrics"]["gain"], "efficiency": e["metrics"]["efficiency"],
        "n_trades": e["metrics"]["n_trades"],
        "top_gainer": e["metrics"]["top_gainer"],
        "focal_resource": e["metrics"]["focal_resource"],
        "focal_holder": e["metrics"]["focal_holder"],
        "special_holder": e["metrics"]["special_holder"],
        "special_share": e["metrics"]["special_share"],
        "invalid_tokens": e["metrics"]["invalid_tokens"],
        "empty_turns": e["metrics"]["empty_turns"],
        "offers_made": e["metrics"]["offers_made"],
        "offers_accepted": e["metrics"]["offers_accepted"],
        "tags": t,
    } for e, t in zip(episodes, tagsets)]

    return {"row": row, "setting": setting, "prediction": pred,
            "episodes": episodes}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", nargs="+", default=["claude", "gpt", "gemini"])
    ap.add_argument("--regimes", nargs="+", default=["normal", "spike", "swan"])
    ap.add_argument("--seeds", type=int, nargs="+", default=list(range(6)))
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--players", type=int, default=3)
    ap.add_argument("--turn-multiple", type=int, default=4)
    ap.add_argument("--judge", default="claude")
    ap.add_argument("--effort", default="medium",
                    help="reasoning effort, held equal across roster AND across "
                         "the predict/play/judge roles")
    ap.add_argument("--max-tokens", type=int, default=4000)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    if not out.is_absolute():
        out = HERE / "results" / args.out
    cells = out / "cells"
    cells.mkdir(parents=True, exist_ok=True)

    grid = [(m, r, s) for m in args.models for r in args.regimes for s in args.seeds]
    todo = [(m, r, s) for m, r, s in grid
            if not (cells / f"{m}__{r}__s{s}.json").exists()]
    calls = len(todo) * (1 + args.reps * (args.players * args.turn_multiple + 2))
    print(f"grid {len(grid)} cells, {len(todo)} to run, ~{calls} model calls")
    print(f"out  {out}")
    if args.dry_run:
        for m, r, s in todo:
            print(f"  {m:8s} {r:7s} seed {s}")
        return 0

    actors = {m: Actor(m, max_tokens=args.max_tokens, effort=args.effort)
              for m in args.models}
    judge_actor = (actors[args.judge] if args.judge in actors
                   else Actor(args.judge, max_tokens=args.max_tokens, effort=args.effort))
    bad = preflight({**actors, "judge:" + args.judge: judge_actor})
    if bad:
        print("PREFLIGHT FAILED:", bad)
        return 2
    print("preflight ok")

    t0 = time.time()
    done = 0

    def work(cell):
        m, r, s = cell
        return cell, run_cell(m, r, s, args, actors[m], judge_actor)

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(work, c): c for c in todo}
        for f in cf.as_completed(futs):
            cell = futs[f]
            try:
                (m, r, s), res = f.result()
            except Exception:  # noqa: BLE001
                print(f"  !! {cell} raised:\n{traceback.format_exc()}")
                continue
            (cells / f"{m}__{r}__s{s}.json").write_text(json.dumps(res, indent=1))
            done += 1
            pr = res["row"].get("pred") or {}
            ce = res["row"].get("ceiling") or {}
            print(f"[{done}/{len(todo)}] {m:7s} {r:6s} s{s}  "
                  f"top1 {pr.get('top1')} (ceil {ce.get('top1')})  "
                  f"pair {pr.get('pairwise_acc')}  "
                  f"nmae {pr.get('gain_nmae') and round(pr['gain_nmae'], 3)}  "
                  f"[{time.time()-t0:.0f}s]", flush=True)

    rows = [json.loads(p.read_text())["row"] for p in sorted(cells.glob("*.json"))]
    (out / "rows.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    # `judge_actor` IS `actors[args.judge]` when the judge is on the roster, so
    # reporting it twice would double-count every call. Named once, either way.
    usage = {m: a.usage for m, a in actors.items()}
    if all(judge_actor is not a for a in actors.values()):
        usage["judge:" + args.judge] = judge_actor.usage
    else:
        usage["_judge_shares_actor"] = args.judge
    (out / "usage.json").write_text(json.dumps(usage, indent=1))
    print(f"\nwrote {len(rows)} rows -> {out/'rows.jsonl'}")
    print(json.dumps(usage, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
