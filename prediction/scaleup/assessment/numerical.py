"""Nested family-held-out numerical baselines and paired forecast scoring."""
from collections import Counter, defaultdict
import json
import os
from pathlib import Path
import sys

from .data import OUT, PACKAGE, RUN, TARGETS, load, read, write, sha, examples_for

sys.path.insert(0, str(PACKAGE.parent/"vendor"))
import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
import sklearn

NUMERIC = ("always_work", "train_mean", "context_mean", "examples_mean", "context_ridge", "structured_ridge", "full_ridge")


def features(row, representation):
    result = {"model="+row["model"]: 1., "provider="+row["provider"]: 1., "prompt="+row["prompt"]: 1.}
    if representation != "context":
        s = row["inputs"]["structured"]
        result.update({"parameter:"+k: float(v) for k, v in s["parameters"].items()})
        result.update({"action:"+k: 1. for k in s["action_space"]})
        result.update({"role="+s["role"]: 1., "information="+s["information"]: 1.,
                       "communication": float(s["communication"]), "control": float(row["control"]),
                       "action_count": len(s["action_space"]), "seat": row["inputs"]["role"]["seat_id"]})
    return result


def weights(rows):
    counts = Counter(r["family"] for r in rows)
    return np.array([len(rows)/(len(counts)*counts[r["family"]]) for r in rows])


def ys(rows):
    return np.array([[r["targets"][t] for t in TARGETS] for r in rows])


def fit_predict(train, test, representation, alpha):
    vector = DictVectorizer(sparse=False)
    x = vector.fit_transform([features(r, representation) for r in train])
    z = vector.transform([features(r, representation) for r in test])
    scaler = StandardScaler().fit(x, sample_weight=weights(train))
    x, z = sp.csr_matrix(scaler.transform(x)), sp.csr_matrix(scaler.transform(z))
    if representation == "full":
        text = TfidfVectorizer(ngram_range=(1, 2), min_df=1, max_features=3000)
        a = text.fit_transform([r["inputs"]["natural_language"] for r in train])
        b = text.transform([r["inputs"]["natural_language"] for r in test])
        x, z = sp.hstack([x, a], format="csr"), sp.hstack([z, b], format="csr")
    model = Ridge(alpha=alpha, solver="lsqr", tol=1e-8).fit(x, ys(train), sample_weight=weights(train))
    return np.clip(model.predict(z), 0, 1)


def family_mse(rows, predictions, column=0):
    loss = (ys(rows)[:, column]-predictions[:, column])**2
    return float(np.average(loss, weights=weights(rows)))


def fit_all(out=OUT):
    rows = load()
    protocol = read(out/"forecast-manifest.json")
    if sha(RUN/"export/episodes.jsonl") != protocol["data_sha256"]:
        raise ValueError("Pilot export changed")
    predictions = {m: {} for m in NUMERIC}
    fits = []
    for family in sorted({r["family"] for r in rows}):
        train = [r for r in rows if r["family"] != family]
        test = [r for r in rows if r["family"] == family]
        average = np.average(ys(train), axis=0, weights=weights(train))
        for row in test:
            ident = row["episode_id"]
            predictions["always_work"][ident] = dict.fromkeys(TARGETS, 0.)
            predictions["train_mean"][ident] = dict(zip(TARGETS, average.tolist()))
            context = [r for r in train if (r["model"], r["provider"], r["prompt"]) == (row["model"], row["provider"], row["prompt"])]
            # Fixed eight-observation shrinkage toward the train-only family mean.
            estimate = (ys(context).sum(axis=0)+8*average)/(len(context)+8) if context else average
            predictions["context_mean"][ident] = dict(zip(TARGETS, estimate.tolist()))
            group = [r for r in test if r["inputs"]["game_id"] == row["inputs"]["game_id"]]
            examples = [r for g in examples_for(rows, group) for r in g]
            matches = [r for r in examples if r["model"] == row["model"] and r["prompt"] == row["prompt"]]
            estimate = ys(matches).mean(axis=0)
            predictions["examples_mean"][ident] = dict(zip(TARGETS, estimate.tolist()))
        inner_families = sorted({r["family"] for r in train})
        for representation in ("context", "structured", "full"):
            scores = []
            for alpha in protocol["ridge_alpha_grid"]:
                losses = []
                for fold in range(3):
                    held = set(inner_families[fold::3])
                    fit = [r for r in train if r["family"] not in held]
                    validation = [r for r in train if r["family"] in held]
                    forecast = fit_predict(fit, validation, representation, alpha)
                    losses.append(family_mse(validation, forecast))
                scores.append((sum(losses)/len(losses), -alpha))
            _, negative_alpha = min(scores)
            alpha = -negative_alpha
            forecast = fit_predict(train, test, representation, alpha)
            method = representation+"_ridge"
            for row, estimate in zip(test, forecast):
                predictions[method][row["episode_id"]] = dict(zip(TARGETS, estimate.tolist()))
            fits.append(dict(held_family=family, method=method, alpha=alpha,
                             train_ids=[r["episode_id"] for r in train], test_ids=[r["episode_id"] for r in test],
                             inner_scores=[dict(mse=s, alpha=-a) for s, a in scores]))
        print("Fitted held-out family:", family, flush=True)
    result = dict(data_sha256=protocol["data_sha256"], predictions=predictions, fits=fits,
                  sklearn=sklearn.__version__, numpy=np.__version__, source_sha256=sha(__file__),
                  note="No target-family row used in example selection, preprocessing, hyperparameter selection, or fitting. Hyperparameters selected on primary non-work rate only; first-action score is secondary.")
    write(out/"numeric-predictions.json", result)
    return dict(methods=list(predictions), families=len({r["family"] for r in rows}), predictions_per_method=len(rows))


def normalized_parse(raw, ids):
    """Keep the one unambiguous schema-valid object; preserve all raw text."""
    from .parsing import extract
    return extract(raw, ids)


def score(out=OUT):
    rows = load()
    lookup = {r["episode_id"]: r for r in rows}
    manifest = read(out/"forecast-manifest.json")
    numeric = read(out/"numeric-predictions.json")
    assert sha(RUN/"export/episodes.jsonl") == manifest["data_sha256"] == numeric["data_sha256"]
    for original, expected in manifest["source_hashes"].items():
        assert sha(out/"forecast-source"/Path(original).relative_to(PACKAGE.parents[1])) == expected
    predictions = numeric["predictions"]
    coverage, call_audit = {}, []
    for method in manifest["methods"]:
        predictions[method] = {}
        coverage[method] = dict(planned_queries=0, usable_queries=0, first_attempt_usable=0,
                                normalized_fences=0, surrounding_prose=0, strict_collector_success=0)
    for query in manifest["queries"]:
        method = query["method"]
        coverage[method]["planned_queries"] += 1
        path = out/"forecasts"/(query["id"]+".json")
        if not path.exists():
            continue
        saved = read(path)
        coverage[method]["strict_collector_success"] += bool(saved.get("predictions"))
        for index, attempt in enumerate(saved["attempts"]):
            if attempt["meta"]["status"] != "ok":
                continue
            try:
                prediction = normalized_parse(attempt["raw"], query["target_ids"])
            except (ValueError, TypeError, KeyError):
                continue
            call = read(out/"calls"/(attempt["meta"]["call_id"]+".json"))
            assert call["request"]["messages"] == query["messages"]
            assert call["config"] == manifest["model"]
            assert call["request"]["model"] == manifest["model"]["provider_model"]
            assert call["request"]["temperature"] == manifest["model"]["temperature"]
            assert call["request"]["extra_body"]["reasoning"] == {"effort": manifest["model"]["reasoning_effort"]}
            assert call["request"]["max_tokens"] == manifest["max_tokens"]
            assert call["response"]["choices"][0]["finish_reason"] == "stop"
            assert call["response"]["choices"][0]["message"]["content"] == attempt["raw"]
            assert call["status"] == "ok"
            assert not set(query["target_ids"]) & set(query["training_ids"])
            assert all(lookup[i]["family"] != query["family"] for i in query["training_ids"])
            predictions[method].update(prediction)
            coverage[method]["usable_queries"] += 1
            coverage[method]["first_attempt_usable"] += index == 0
            fenced = attempt["raw"].strip().startswith("```")
            coverage[method]["normalized_fences"] += fenced
            prose = not attempt["raw"].strip().startswith(("{", "```"))
            coverage[method]["surrounding_prose"] += prose
            call_audit.append(dict(query_id=query["id"], call_id=call["call_id"], attempt=index+1, normalized_fence=fenced, surrounding_prose=prose))
            break
    common = set.intersection(*(set(p) for p in predictions.values()))
    selected = [r for r in rows if r["episode_id"] in common]
    if not selected:
        raise ValueError("No common forecast coverage")
    families = sorted({r["family"] for r in selected})
    results = {}
    losses = {}
    for method, forecasts in predictions.items():
        results[method] = {}
        losses[method] = {}
        for target in TARGETS:
            family_losses = [np.mean([(forecasts[r["episode_id"]][target]-r["targets"][target])**2
                              for r in selected if r["family"] == f]) for f in families]
            losses[method][target] = np.array(family_losses)
            results[method][target] = dict(mse=float(np.mean(family_losses)), rmse=float(np.sqrt(np.mean(family_losses))),
                                           family_losses=dict(zip(families, map(float, family_losses))))
    comparisons = []
    rng = np.random.default_rng(910)
    indices = rng.integers(0, len(families), size=(5000, len(families)))
    for a, b in [("few_full", m) for m in (*NUMERIC, "zero_full")] + [("few_structured", "few_full"), ("full_ridge", "context_ridge"), ("full_ridge", "structured_ridge")]:
        for target in TARGETS:
            delta = losses[a][target]-losses[b][target]
            interval = np.quantile(delta[indices].mean(axis=1), [.025, .975])
            comparisons.append(dict(a=a, b=b, target=target, mse_difference=float(delta.mean()),
                                    ci95=list(map(float, interval)),
                                    within_margin=bool(interval[1] <= manifest["noninferiority_margin"])))
    usage = Counter()
    for path in (out/"calls").glob("*.json"):
        call = read(path)
        usage["requests"] += 1
        usage[call["status"]] += 1
        usage["reported_cost_usd"] += call.get("budget_cost_usd") or 0
    result = dict(status="complete" if len(common) == len(rows) else "partial", common_episodes=len(common), families=len(families),
                  target_definitions={"non_work_rate":"fraction of completed focal decisions whose action is not exactly work", "first_non_work":"first action is not work (binary target; predictions are probabilities)"},
                  metrics=results, comparisons=comparisons, coverage=coverage, call_audit=call_audit,
                  usage=dict(usage), methods=list(predictions), common_ids=sorted(common), predictions=predictions,
                  parser_policy="Earliest completed response containing one unambiguous schema-valid forecast object; surrounding prose/fences are preserved but not scored. Same rule for every method; no altered numbers or outcome-dependent choice. See format-amendment-v2.json.",
                  uncertainty="Paired bootstrap over whole held-out families, conditional on fixed fits/predictions; not a population guarantee or nested refitting bootstrap")
    write(out/"prediction-evaluation.json", result)
    return {k: result[k] for k in ("status", "common_episodes", "coverage", "usage", "metrics")}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("fit", "score"))
    args = parser.parse_args()
    print(json.dumps(fit_all() if args.action == "fit" else score(), indent=2))
