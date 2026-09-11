from copy import deepcopy
import json

from prediction.io_utils import write_json, read_json, digest
from .providers import configurations
from .provider_switch import prepare


def test_exact_provider_routes_preserve_sampling_and_legacy_registry():
    old = configurations(["qwen-3.8-27b", "glm"], "configured")
    new = configurations(["qwen-3.8-27b", "glm"], "openrouter")
    assert new["qwen-3.8-27b"]["provider_model"] == "qwen/qwen3.8-27b"
    assert new["glm"]["provider_model"] == "z-ai/glm-5.3"
    for name in old:
        assert old[name]["provider"] == "flt" and new[name]["provider"] == "openrouter"
        assert new[name]["temperature"] == old[name]["temperature"]
        assert new[name]["reasoning_effort"] == old[name]["reasoning_effort"]
        assert new[name]["key_env"] == "OPENROUTER_API_KEY"
    assert configurations(["qwen-3.8-27b", "glm"], "configured") == old


def test_only_unfinished_episodes_restart_and_original_artifacts_remain(tmp_path):
    source = tmp_path/"original"
    models = configurations(["glm"], "configured")
    original = dict(created="old", models=models, players={"glm": dict(model_id="glm", provider="flt", provider_model="glm-5.3")},
                    episodes=[dict(episode_id="done", environment_seed=3), dict(episode_id="partial", environment_seed=4),
                              dict(episode_id="unstarted", environment_seed=5)], sources={}, budget_usd=0)
    write_json(source/"manifest.json", original)
    write_json(source/"episodes/done/trace.json", dict(status="complete", evidence="original"))
    write_json(source/"episodes/partial/trace.json", dict(status="incomplete", steps=["keep"] ))
    path = tmp_path/"continuation.json"
    result = prepare(source, path, tmp_path/"router")
    created = read_json(path)
    assert result["retained"] == 1 and result["restarted"] == 2
    assert [e["episode_id"] for e in created["episodes"]] == ["partial", "unstarted"]
    assert [e["environment_seed"] for e in created["episodes"]] == [4, 5]
    assert created["continuation"]["source_manifest_digest"] == digest(original)
    assert created["players"]["glm"]["provider"] == "openrouter"
    assert read_json(source/"manifest.json") == original
    assert read_json(source/"episodes/partial/trace.json")["steps"] == ["keep"]
    assert not (tmp_path/"router").exists()
