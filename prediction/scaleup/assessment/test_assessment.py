from copy import deepcopy
import json

import pytest

from .data import OUT, TARGETS, load, read, examples_for
from .checks import independent_labels
from .forecast import parse
from .numerical import normalized_parse


@pytest.fixture(scope="module")
def rows(): return load()


def test_frozen_queries_exclude_target_family_and_targets(rows):
    lookup = {r["episode_id"]: r for r in rows}
    manifest = read(OUT/"forecast-manifest.json")
    assert len(manifest["queries"]) == 108
    for query in manifest["queries"]:
        assert not set(query["target_ids"]) & set(query["training_ids"])
        assert {lookup[i]["family"] for i in query["target_ids"]} == {query["family"]}
        assert all(lookup[i]["family"] != query["family"] for i in query["training_ids"])
        assert set(query["example_ids"]) <= set(query["training_ids"])
        payload = json.loads(query["messages"][1]["content"])
        assert all("observed" not in context for context in payload["target"]["contexts"])
        if query["method"] == "few_structured":
            assert all("natural_language" not in card for card in [payload["target"], *payload["examples"]])
        if query["method"] == "zero_full": assert "examples" not in payload


def test_example_selection_does_not_use_outcomes(rows):
    group = [r for r in rows if r["inputs"]["game_id"] == rows[0]["inputs"]["game_id"]]
    changed = [{**r, "targets": {t: 1-r["targets"][t] for t in TARGETS}} for r in rows]
    ids = lambda groups: [[r["episode_id"] for r in g] for g in groups]
    assert ids(examples_for(rows, group)) == ids(examples_for(changed, group))


def test_independent_audit_detects_mutated_facts_and_rates(rows):
    assert independent_labels(rows)["status"] == "passed"
    changed = deepcopy(rows[:1])
    step = changed[0]["trace"]["steps"][0]
    step["facts"]["mechanism_executed"] = not step["facts"]["mechanism_executed"]
    changed[0]["labels"]["behavior"]["information_seeking_rate"]["numerator"] += 1
    result = independent_labels(changed)
    assert result["status"] == "mismatch"
    assert {m["field"] for m in result["mismatches"]} >= {"mechanism_executed", "information_seeking_rate"}


def test_fence_normalization_preserves_values_and_schema():
    raw = json.dumps({"predictions":[{"id":"x", "non_work_rate":.3, "first_non_work":.7}]})
    assert normalized_parse("```json\n"+raw+"\n```", ["x"]) == parse(raw, ["x"])
    for malformed in (raw.replace('0.3', 'NaN'), raw.replace('0.3', 'true'), raw.replace('0.3', '1.3'), raw.replace('"x"', '"wrong"')):
        with pytest.raises(ValueError): normalized_parse(malformed, ["x"])
    assert normalized_parse("Some commentary\n"+raw, ["x"]) == parse(raw, ["x"])
    with pytest.raises(ValueError): normalized_parse(raw+"\nAnother forecast:\n"+raw, ["x"])


def test_numeric_outer_fits_purge_all_target_variants(rows):
    result = read(OUT/"numeric-predictions.json")
    lookup = {r["episode_id"]: r for r in rows}
    assert len(result["fits"]) == 30
    for fit in result["fits"]:
        assert not set(fit["train_ids"]) & set(fit["test_ids"])
        assert {lookup[i]["family"] for i in fit["test_ids"]} == {fit["held_family"]}
        assert all(lookup[i]["family"] != fit["held_family"] for i in fit["train_ids"])
    for predictions in result["predictions"].values():
        assert set(predictions) == set(lookup)
        assert all(0 <= value <= 1 for row in predictions.values() for value in row.values())
