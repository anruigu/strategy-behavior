from copy import deepcopy

import pytest

from prediction.io_utils import digest, write_json
from .collection import resolve


def setup(tmp_path):
    base, target = tmp_path/"base", tmp_path/"router"
    original = dict(episodes=[dict(episode_id="done", player_id="m"), dict(episode_id="missing", player_id="m")],
                    models={"m": dict(provider="flt")})
    write_json(base/"manifest.json", original)
    write_json(base/"episodes/done/trace.json", dict(status="complete"))
    write_json(base/"episodes/missing/trace.json", dict(status="incomplete", steps=["old partial"]))
    next_manifest = dict(episodes=[original["episodes"][1]], models={"m": dict(provider="openrouter")},
                         continuation=dict(source_run=str(base), source_manifest_digest=digest(original)))
    write_json(target/"manifest.json", next_manifest)
    write_json(base/"provider-continuation.json", dict(run=str(target), provider="openrouter", source_manifest_digest=digest(original), retained=1, restarted=1))
    return base, target, next_manifest


def test_continuation_selects_provider_per_episode_and_drops_old_partial(tmp_path):
    base, target, _ = setup(tmp_path)
    _, entries, continuation = resolve(base)
    assert entries["done"]["run"] == base and entries["done"]["provider"] == "flt"
    assert entries["missing"]["run"] == target and entries["missing"]["provider"] == "openrouter"
    assert not entries["missing"]["path"].exists()
    assert continuation["retained"] == continuation["restarted"] == 1


def test_continuation_cannot_overwrite_completed_episode_or_change_identity(tmp_path):
    base, target, manifest = setup(tmp_path)
    changed = deepcopy(manifest)
    changed["episodes"] = [dict(episode_id="done", player_id="m")]
    write_json(target/"manifest.json", changed)
    with pytest.raises(ValueError, match="completed"):
        resolve(base)
    changed = deepcopy(manifest)
    changed["episodes"][0]["player_id"] = "different-model"
    write_json(target/"manifest.json", changed)
    with pytest.raises(ValueError, match="identity"):
        resolve(base)


def test_continuation_requires_source_manifest_integrity(tmp_path):
    base, target, manifest = setup(tmp_path)
    manifest["continuation"]["source_manifest_digest"] = "incorrect"
    write_json(target/"manifest.json", manifest)
    with pytest.raises(ValueError, match="provenance"):
        resolve(base)
