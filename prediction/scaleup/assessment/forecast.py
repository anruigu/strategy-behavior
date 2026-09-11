"""Freeze and collect purged, retrospective leave-family-out forecasts."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, replace
import json
from pathlib import Path

from prediction.client import Client, ModelConfig, Ledger
from prediction.io_utils import digest, now
from prediction.scaleup.providers import configurations
from .data import OUT, RUN, PACKAGE, TARGETS, load, card, examples_for, read, write, sha

METHODS = ("zero_full", "few_full", "few_structured")
SYSTEM = """Forecast recorded LLM behavior in compact strategic games. You are an observer, not a player.
For every target context, output expected non_work_rate (fraction of the six focal decisions whose action is not exactly work) and first_non_work (probability that the first action is not work). Invalid model actions count as non-work; provider errors do not count as actions. Both outputs must be numbers in [0,1].
Players maximize their final standing by own score, with ties sharing a win. They have fresh context per episode, temperature 0.7, requested low reasoning, a 16384-token action cap, and feedback/history after each action. Normal framing states that winning objective. Active exploration adds instructions to test promising mechanics, question written rules, and balance exploration against cost and turns remaining. Rivals are scripted as specified. Opening scores are focal 20 and each rival 18 in this pilot. Control indicates a patched implementation; natural-language rules intentionally hide implementation discrepancies. No action or label from the target family is supplied.
Example outcomes, when present, are single noisy episodes, not population rates. Predict what these LLMs will do, not an ideal strategy. Return only JSON: {"predictions":[{"id":"...","non_work_rate":0.0,"first_non_work":0.0}, ...]}. Include every target context ID exactly once; no extra fields."""


def prepare(out=OUT):
    out = Path(out)
    if (out/"forecast-manifest.json").exists():
        raise ValueError("Forecast manifest already exists")
    rows = load()
    grouped = {}
    for row in rows:
        grouped.setdefault(row["inputs"]["game_id"], []).append(row)
    queries = []
    for gid, group in sorted(grouped.items()):
        examples = examples_for(rows, group)
        for method in METHODS:
            representation = "structured" if method == "few_structured" else "full"
            payload = dict(target=card(group, representation))
            if method.startswith("few"):
                payload["examples"] = [card(e, representation, outcomes=True) for e in examples]
            messages = [dict(role="system", content=SYSTEM), dict(role="user", content=json.dumps(payload, ensure_ascii=False))]
            size = len(json.dumps(messages, ensure_ascii=False).encode())+4096+256*len(messages)
            if size > 40000:
                raise ValueError("Prediction context exceeds existing client limit")
            queries.append(dict(id=digest([gid, method])[:24], method=method, family=group[0]["family"],
                                target_ids=[r["episode_id"] for r in group],
                                training_ids=[r["episode_id"] for r in rows if r["family"] != group[0]["family"]],
                                example_ids=[r["episode_id"] for e in examples for r in e] if method.startswith("few") else [],
                                messages=messages))
    conf = configurations(["qwen-3.8-27b"])["qwen-3.8-27b"]
    conf = asdict(replace(ModelConfig(**conf), temperature=0))
    source_paths = [*Path(__file__).parent.glob("*.py"), PACKAGE.parent/"client.py",
                    PACKAGE.parent/"io_utils.py", PACKAGE/"providers.py",
                    PACKAGE.parents[1]/"benchmark/clients.py", PACKAGE.parents[1]/"benchmark/fullscale/budget.py"]
    source_paths = [p for p in source_paths if p.is_file()]
    manifest = dict(created=now(), evaluation="retrospective leave-one-family-out, not prospective",
                    data_sha256=sha(RUN/"export/episodes.jsonl"), methods=METHODS, targets=TARGETS,
                    primary_target="non_work_rate", primary_score="equal-family mean squared error",
                    other_score="Brier score for first_non_work; same episode-level family weighting",
                    numerical="train mean; context mean; same-examples mean; context/structured/text+structured ridge, inner family-purged alpha selection",
                    ridge_alpha_grid=[0.1, 1.0, 10.0, 100.0], inner_family_folds=3,
                    fit_weighting="Each training family has equal total weight; weights average one across training rows",
                    bootstrap="5000 resamples of 10 whole families; conditional on fixed predictions, no model refitting",
                    noninferiority_margin=0.01, noninferiority_rule="upper 95% paired family-bootstrap MSE difference few-shot minus comparator <= .01; compare every prespecified numeric baseline",
                    model=conf, max_tokens=8192, budget_usd=20, queries=queries,
                    source_hashes={str(p): sha(p) for p in source_paths},
                    limitations=["One observation per cell; estimates cannot establish repeatability", "Forecasts use one predictor model", "Labels existed before this diagnostic was designed", "Only two reward doses and ten family groups", "No training rows from the target family; examples use input features only"])
    write(out/"forecast-manifest.json", manifest)
    for path in source_paths:
        destination = out/"forecast-source"/path.relative_to(PACKAGE.parents[1])
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(path.read_bytes())
    return dict(queries=len(queries), target_episodes=len(rows), max_context_bytes=max(len(json.dumps(q["messages"]).encode()) for q in queries), out=str(out))


def parse(raw, ids):
    value = json.loads(raw)
    if set(value) != {"predictions"} or not isinstance(value["predictions"], list):
        raise ValueError("Invalid forecast schema")
    result = {}
    for row in value["predictions"]:
        if set(row) != {"id", *TARGETS} or row["id"] in result:
            raise ValueError("Duplicate or unexpected prediction field")
        for target in TARGETS:
            if type(row[target]) not in (int, float) or not 0 <= row[target] <= 1:
                raise ValueError("Nonprobability prediction")
        result[row["id"]] = {t: row[t] for t in TARGETS}
    if set(result) != set(ids):
        raise ValueError("Forecast coverage mismatch")
    return result


def collect(out=OUT, workers=8):
    out = Path(out)
    manifest = read(out/"forecast-manifest.json")
    if sha(RUN/"export/episodes.jsonl") != manifest["data_sha256"]:
        raise ValueError("Data changed after forecast freeze")
    for path, expected in manifest["source_hashes"].items():
        if sha(path) != expected:
            raise ValueError("Forecast source changed: "+path)
    ledger = Ledger(out/"forecast-budget.sqlite", manifest["budget_usd"])
    stage = Ledger(out/"forecast-stage-budget.sqlite", manifest["budget_usd"])
    client = Client(ModelConfig(**manifest["model"]), out/"calls", ledger, stage, manifest["max_tokens"])
    def one(query):
        path = out/"forecasts"/(query["id"]+".json")
        saved = read(path) if path.exists() else dict(query_id=query["id"], manifest_sha=digest(manifest), attempts=[])
        if saved["manifest_sha"] != digest(manifest):
            raise ValueError("Forecast belongs to another protocol")
        if saved.get("predictions"):
            return True
        while len(saved["attempts"]) < 3:
            raw, meta = client.generate(query["messages"], purpose="scaleup-pilot-behavior-forecast")
            attempt = dict(raw=raw, meta=meta)
            saved["attempts"].append(attempt)
            if meta["status"] == "ok":
                try:
                    saved["predictions"] = parse(raw, query["target_ids"])
                except (ValueError, TypeError, KeyError) as exc:
                    attempt["parse_error"] = str(exc)
            write(path, saved)
            if saved.get("predictions"):
                return True
        return False
    complete, failed = 0, 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(one, q) for q in manifest["queries"]]
        for future in as_completed(futures):
            if future.result():
                complete += 1
            else:
                failed += 1
            status = dict(complete=complete, failed=failed, planned=len(futures), budget=ledger.summary())
            write(out/"forecast-status.json", status)
            print(json.dumps(status), flush=True)
    return status


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "collect"))
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    print(prepare(args.out) if args.action == "prepare" else collect(args.out))
