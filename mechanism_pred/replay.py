#!/usr/bin/env python3
"""Score a NEW predictor against a wave's already-recorded outcomes.

This is the cheap half of the experiment. Playing a cell costs ~40 model calls;
predicting one costs ONE. So once a wave has recorded what actually happened,
any number of further models can be measured on the prediction task for about a
fiftieth of the price -- no games are replayed and the ground truth does not
move, which also makes the comparison exact rather than a fresh sample.

It answers a question the wave itself cannot: the stored prompt names WHICH
model will play the seats, so replaying it with a different predictor is
CROSS-PREDICTION -- can Opus predict Gemini's negotiation better than Gemini
can? Self-prediction and other-prediction come apart here, and the diagonal of
that matrix is what the wave measured.

    python replay.py --dataset results/wave0902/wave0902_dataset.jsonl \
                     --predictor gpt --out results/wave0902/replay_gpt.jsonl
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import pathlib
import sys
from typing import Any, Dict, List

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import score as S  # noqa: E402
from actors import MODELS, Actor, preflight  # noqa: E402
from predict import parse_prediction  # noqa: E402


def load(path: pathlib.Path) -> List[Dict[str, Any]]:
    if path.suffix == ".parquet":
        import pyarrow.parquet as pq
        return pq.read_table(path).to_pylist()
    return [json.loads(l) for l in path.read_text().splitlines() if l.strip()]


def actual_to_metrics(a: Dict[str, Any], n: int) -> Dict[str, Any]:
    per = a["per_player"]
    return {"gain": {p: per[str(p)]["gain"] for p in range(n)},
            "top_gainer": a["top_gainer"], "rank_by_gain": a["rank_by_gain"],
            "efficiency": a["joint_efficiency"], "n_trades": a["n_trades"],
            "focal_resource": a["focal_resource"], "focal_holder": a["focal_holder"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--predictor", required=True,
                    help="roster key of the model doing the predicting")
    ap.add_argument("--out", default=None)
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--max-tokens", type=int, default=4000)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()

    ds = pathlib.Path(a.dataset)
    if not ds.is_absolute():
        ds = HERE / ds
    rows = load(ds)

    # One prediction per (played model, regime, seed) -- exactly the grain the
    # wave predicted at -- then scored against every realization of it.
    cells: Dict[str, List[Dict]] = {}
    for r in rows:
        cells.setdefault(f"{r['model_key']}__{r['regime']}__s{r['seed']}", []).append(r)
    print(f"{len(rows)} rows -> {len(cells)} prompts to re-predict with {a.predictor}")

    actor = Actor(a.predictor, max_tokens=a.max_tokens, effort=a.effort)
    bad = preflight({a.predictor: actor})
    if bad:
        print("PREFLIGHT FAILED:", bad)
        return 2

    def work(item):
        key, rs = item
        head = rs[0]
        n = head["n_players"]
        raw, _ = actor.act(head["system"], head["prompt"])
        pred = parse_prediction(raw, n)
        out = []
        for r in sorted(rs, key=lambda x: x["rep"]):
            actual = json.loads(r["actual"])
            m = actual_to_metrics(actual, n)
            tags = {p: actual["per_player"][str(p)]["tactics"] for p in range(n)}
            sc = None
            if pred["ok"]:
                fc = S.forecast_from_prediction(pred, n)
                sc = S.compare(fc, m, tags, n, r["achievable_gain"])
            out.append({**{k: r[k] for k in
                           ("id", "setting_id", "model_key", "regime", "seed",
                            "rep", "n_players", "achievable_gain",
                            "special_item", "special_party")},
                        "predictor": a.predictor,
                        "predictor_model": MODELS.get(a.predictor, a.predictor),
                        "played_model": r["model"],
                        "self_prediction": a.predictor == r["model_key"],
                        "prediction_ok": pred["ok"],
                        "predicted": json.dumps(
                            S.forecast_from_prediction(pred, n) if pred["ok"] else None,
                            default=str),
                        "prediction_raw": raw,
                        "actual": r["actual"],
                        "scores": json.dumps(sc),
                        "ceiling": r["ceiling"]})
        return out

    results: List[Dict] = []
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        for i, got in enumerate(ex.map(work, cells.items()), 1):
            results.extend(got)
            print(f"[{i}/{len(cells)}] {got[0]['id'][:-4]}  ok={got[0]['prediction_ok']}",
                  flush=True)

    outp = pathlib.Path(a.out) if a.out else ds.with_name(
        f"{ds.stem}_replay_{a.predictor}.jsonl")
    if not outp.is_absolute():
        outp = HERE / outp
    results.sort(key=lambda r: r["id"])
    outp.write_text("".join(json.dumps(r) + "\n" for r in results))
    print(f"\nwrote {len(results)} rows -> {outp}")
    print("usage:", json.dumps(actor.usage))

    ok = [json.loads(r["scores"]) for r in results if r["scores"] != "null"]
    if ok:
        for k in ("top1", "pairwise_acc", "gain_nmae", "eff_err", "tag_jaccard"):
            v = [x[k] for x in ok if x.get(k) is not None]
            print(f"  {k:14s} {sum(v)/len(v):.3f}  (n={len(v)})" if v else f"  {k:14s} --")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
