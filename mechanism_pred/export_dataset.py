#!/usr/bin/env python3
"""Flatten a wave into a self-contained predicted-vs-actual dataset.

GRAIN: one row per (model, regime, seed, realization). The prediction is made
once per cell and scored against each of that cell's realizations, so the
prediction fields repeat across a cell's rows on purpose -- every row carries
everything needed to reproduce its own score without a join, which is what
makes the file usable as an eval set rather than a table you have to
reassemble.

The prediction PROMPT is a column, verbatim. That is the point of the export:
`prompt` in, `predicted` out, `actual` to grade against, so the same file can be
replayed against a new model without this repo. `predicted` and `actual` are
JSON strings rather than nested structs -- parquet can hold the struct, but the
two sides have deliberately different shapes (a forecast has `strategy` text and
no transcript; a realization has tags and holdings), and forcing them into one
schema would either lose fields or fill the file with nulls.

Writes JSONL always; parquet too when pyarrow is importable.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any, Dict, List

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import predict as P  # noqa: E402
from play import public_transcript  # noqa: E402


def _int_keys(d):
    """JSON turns int dict keys into strings; put them back."""
    if isinstance(d, dict):
        return {(int(k) if isinstance(k, str) and k.lstrip("-").isdigit() else k):
                _int_keys(v) for k, v in d.items()}
    if isinstance(d, list):
        return [_int_keys(x) for x in d]
    return d


def rows_from_cell(cell: Dict[str, Any]) -> List[Dict[str, Any]]:
    row, setting = cell["row"], _int_keys(cell["setting"])
    pred, eps = cell["prediction"], cell["episodes"]
    n, tm = row["players"], row["turn_multiple"]
    model_key = row["model"]

    from actors import MODELS
    model_id = MODELS.get(model_key, model_key)
    # Prefer the prompt recorded at sampling time; fall back to rebuilding it for
    # waves run before `predict.predict` started storing it. The fallback is
    # exact only while `build_prompt` is unchanged, which is why new waves store.
    prompt = pred.get("prompt") or P.build_prompt(setting, tm, model_id)
    system = pred.get("system") or P.SYSTEM

    predicted = None
    if pred.get("ok"):
        pp = _int_keys(pred["per_player"])
        predicted = {
            "per_player": {str(p): {"strategy": pp[p]["strategy"],
                                    "tactics": pp[p]["tactics"],
                                    "predicted_gain": pp[p]["predicted_gain"]}
                           for p in range(n)},
            "rank_by_gain": pred["rank_by_gain"],
            "n_trades": pred["n_trades"],
            "joint_efficiency": pred["joint_efficiency"],
            "focal_resource": pred["focal_resource"],
            "focal_holder": pred["focal_holder"],
            "mechanism": pred["mechanism"],
        }

    out = []
    for rep, ep in enumerate(eps):
        m = _int_keys(ep["metrics"])
        tags = _int_keys(row["realized"][rep].get("tags") or {})
        jper = _int_keys((ep.get("judge") or {}).get("per_player") or {})
        vd = ep.get("verdict") or {}
        vper = _int_keys(vd.get("per_player") or {})

        actual = {
            "per_player": {str(p): {
                "gain": m["gain"][p],
                "initial_value": m["initial_value"][p],
                "final_value": m["final_value"][p],
                "final_resources": m["final_resources"][p],
                "tactics": tags.get(p, []),
                "judge_summary": (jper.get(p) or {}).get("summary", ""),
            } for p in range(n)},
            "rank_by_gain": m["rank_by_gain"],
            "top_gainer": m["top_gainer"],
            "n_trades": m["n_trades"],
            "joint_efficiency": m["efficiency"],
            "focal_resource": m["focal_resource"],
            "focal_holder": m["focal_holder"],
            "special_holder": m["special_holder"],
            "special_share": m["special_share"],
        }

        scores = dict((row.get("pred_per_rep") or [{}] * len(eps))[rep] or {})
        if vd:
            scores["strategy_score"] = vd.get("strategy_score")
            scores["mechanism_score"] = vd.get("mechanism_score")
            scores["biggest_miss"] = vd.get("biggest_miss")
            scores["per_seat_strategy_score"] = {
                str(p): (vper.get(p) or {}).get("score") for p in range(n)}

        out.append({
            "id": f"{model_key}__{row['regime']}__s{row['seed']}__r{rep}",
            "setting_id": f"{row['regime']}__s{row['seed']}",
            "model_key": model_key,
            "model": model_id,
            "regime": row["regime"],
            "seed": row["seed"],
            "rep": rep,
            "n_players": n,
            "turn_multiple": tm,
            "achievable_gain": row["achievable_gain"],
            "special_item": row["special_item"],
            "special_party": row["special_party"],

            "system": system,
            "prompt": prompt,
            "prompt_stored": bool(pred.get("prompt")),

            "setting": json.dumps({
                "resources": {str(p): setting["resources"][p] for p in range(n)},
                "values": {str(p): setting["values"][p] for p in range(n)},
                "special_item": setting["special_item"],
                "special_party": setting["special_party"]}),
            "predicted": json.dumps(predicted) if predicted else None,
            "prediction_raw": pred.get("raw", ""),
            "prediction_ok": bool(pred.get("ok")),
            "actual": json.dumps(actual),
            "scores": json.dumps(scores),
            "baseline_first_best": json.dumps(row.get("first_best")),
            "baseline_no_trade": json.dumps(row.get("no_trade")),
            "ceiling": json.dumps(row.get("ceiling")),
            "judge_ok": bool((row.get("judge_ok") or [True] * len(eps))[rep]),
            "transcript": public_transcript(ep),
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--wave", required=True)
    ap.add_argument("--name", default=None, help="output basename")
    a = ap.parse_args()
    wave = pathlib.Path(a.wave)
    if not wave.is_absolute():
        wave = HERE / "results" / a.wave

    rows: List[Dict[str, Any]] = []
    for f in sorted((wave / "cells").glob("*.json")):
        rows.extend(rows_from_cell(json.loads(f.read_text())))
    if not rows:
        print(f"no cells under {wave/'cells'}")
        return 1
    rows.sort(key=lambda r: r["id"])

    base = wave / (a.name or f"{wave.name}_dataset")
    jl = base.with_suffix(".jsonl")
    jl.write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(f"wrote {len(rows)} rows -> {jl}  ({jl.stat().st_size/1e6:.1f} MB)")

    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
    except ImportError:
        print("pyarrow not importable; skipped parquet "
              "(pip install pyarrow into ~/venvs/tools)")
        return 0
    pqf = base.with_suffix(".parquet")
    pq.write_table(pa.Table.from_pylist(rows), pqf, compression="zstd")
    print(f"wrote {len(rows)} rows -> {pqf}  ({pqf.stat().st_size/1e6:.1f} MB)")

    # A schema card beside the file: a dataset whose columns are JSON strings is
    # unusable without one, and the reader is usually not the author.
    card = base.parent / f"{base.name}_SCHEMA.md"
    card.write_text(f"""# `{base.name}` -- mechanism-prediction dataset

One row per (model, regime, seed, realization); {len(rows)} rows,
{len({r['setting_id'] for r in rows})} distinct settings,
{len({r['model_key'] for r in rows})} models.

The prediction is made ONCE per (model, regime, seed) from the full setting and
scored against each realization of it, so `prompt`/`predicted` repeat across a
cell's `rep` rows while `actual`/`scores`/`transcript` differ. Every row is
self-contained: no joins needed to reproduce its score.

## Columns

| column | type | meaning |
|---|---|---|
| `id` / `setting_id` | str | row key / the (regime, seed) the row shares with other models |
| `model_key` / `model` | str | roster key (`claude`) and the sampled model id |
| `regime` | str | `normal` (cpi, a=0.4), `spike` (one party's taste boosted), `swan` (one item boosted for everyone) |
| `seed` | int | endowments depend on this ALONE, so a seed is holdings-matched across regimes |
| `rep` | int | which realization of this cell |
| `achievable_gain` | float | joint gain of the first-best allocation; the scale `gain_nmae` divides by |
| `special_item` / `special_party` | str/int | what the regime boosted, and for `spike` who for; `null` under `normal` |
| `system` / `prompt` | str | the verbatim prediction call. Replay these against a new model to extend the set |
| `prompt_stored` | bool | `true` if the prompt was recorded at sampling time; `false` if reconstructed at export (exact, but only while `predict.build_prompt` is unchanged) |
| `setting` | JSON str | `resources`, `values` per player, plus the special fields |
| `predicted` | JSON str | per-player `strategy`/`tactics`/`predicted_gain`, plus `rank_by_gain`, `n_trades`, `joint_efficiency`, `focal_resource`, `focal_holder`, `mechanism`. `null` if the reply did not parse |
| `prediction_raw` | str | the raw reply the prediction was parsed from |
| `actual` | JSON str | same shape where it can be: realized per-player gain/holdings/tactics, `n_trades`, `joint_efficiency`, focal and special outcomes |
| `scores` | JSON str | this row's prediction-vs-actual metrics, incl. judge `strategy_score`/`mechanism_score` and `biggest_miss` |
| `baseline_first_best` | JSON str | cell-level: the efficient-allocation null (a RANKING null; its levels are uncompensated and its NMAE is meaningless by construction) |
| `baseline_no_trade` | JSON str | cell-level: the "nothing happens" null (a LEVEL null; supplies no ranking) |
| `ceiling` | JSON str | cell-level: how well one realization of this setting predicts another. A SINGLE-DRAW ceiling -- a forecaster of the expectation can legitimately exceed it |
| `judge_ok` | bool | whether this realization was successfully annotated; `false` means its `tactics` are missing, not empty |
| `transcript` | str | every action token of this realization, in order. No hidden reasoning: the forecast is about behaviour the other seats could see |

## Reading the scores

`top1`, `pairwise_acc`, `focal_hit`, `focal_holder_hit`, `tag_jaccard`,
`strategy_score`, `mechanism_score` are higher-is-better; `gain_nmae`,
`eff_err`, `trade_err` are lower-is-better. Never read one without its
baseline: `tag_jaccard` in particular has a modal-set null near 0.68 (see
`analyze.py --wave <wave>`), so a raw 0.31 is well BELOW chance, not moderate.
""")
    print(f"wrote schema card -> {card}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
