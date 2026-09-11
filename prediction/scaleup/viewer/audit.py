"""Independent artifact audit, including the fixed sampling protocol and export joins."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

from prediction.io_utils import digest, read_json, write_json
from prediction.scaleup.design import game_from_record
from prediction.scaleup.runner import episode_from_record, verify_trace
from .server import jsonl, PACKAGE


def audit(run, exported=None):
    run = Path(run)
    manifest = read_json(run/"manifest.json")
    counts = Counter()
    for relative, expected in manifest["sources"].items():
        if hashlib.sha256((run/"source"/relative).read_bytes()).hexdigest() != expected:
            raise ValueError("Frozen source mismatch: "+relative)
        counts["source_files"] += 1
    games = {r["game_id"]: game_from_record(r) for r in manifest["games"]}
    complete, actions = {}, {}
    identity = digest(manifest)
    for spec in manifest["episodes"]:
        path = run/"episodes"/spec["episode_id"]/"trace.json"
        if not path.exists():
            counts["not_started"] += 1
            continue
        trace = read_json(path)
        if trace["manifest_digest"] != identity:
            raise ValueError("Episode belongs to another sampling protocol")
        episode = episode_from_record(spec)
        game = games[episode.game_id]
        verify_trace(trace, game, episode, run/"calls")
        conf = manifest["models"][episode.player_id]
        for step in trace["steps"]:
            call = read_json(run/"calls"/episode.player_id/(step["call"]["call_id"]+".json"))
            request = call["request"]
            expected = dict(model=conf["provider_model"], max_tokens=manifest["max_tokens"])
            if any(request[k] != value for k, value in expected.items()):
                raise ValueError("Per-call model/token protocol mismatch")
            if call["config"] != conf or request.get("temperature") != conf["temperature"]:
                raise ValueError("Player/sampling configuration mismatch")
            if request["extra_body"]["reasoning"] != {"effort": conf["reasoning_effort"]}:
                raise ValueError("Reasoning configuration mismatch")
            if call["response"]["choices"][0]["finish_reason"] != "stop":
                raise ValueError("Noncomplete generation scored as behavior")
            counts["raw_calls_verified"] += 1
        if trace["status"] == "complete":
            complete[episode.episode_id] = trace
            actions.update({(episode.episode_id, step["turn"]): step for step in trace["steps"]})
            counts["complete_episodes"] += 1
            counts["model:"+episode.player_id] += 1
            counts["invalid_actions"] += sum(not s["facts"]["valid"] for s in trace["steps"])
            if game.control and trace["exploit"]["executed"]:
                raise ValueError("Executed mechanism on control")
            if trace["exploit"]["discovered"] is not None:
                raise ValueError("Unexpected mental-state label without discovery evidence")
        else:
            counts["incomplete_episodes"] += 1
    if exported:
        exported = Path(exported)
        rows = jsonl(exported/"episodes.jsonl")
        if len(rows) != len(complete) or {r["episode_id"] for r in rows} != set(complete):
            raise ValueError("Episode export coverage mismatch")
        for row in rows:
            trace = complete[row["episode_id"]]
            if row["provenance"] != "model_rollout":
                raise ValueError("Scripted data in empirical export")
            if row["labels"] != {k: trace[k] for k in ("behavior", "exploit", "outcome")}:
                raise ValueError("Export label mismatch")
            if set(row["inputs"]) != {"game_id", "family_id", "natural_language", "structured", "control", "player", "role", "context"}:
                raise ValueError("Unexpected predictor input fields")
        rows = jsonl(exported/"actions.jsonl")
        keys = [(r["episode_id"], r["turn"]) for r in rows]
        if len(keys) != len(set(keys)) or set(keys) != set(actions):
            raise ValueError("Action export coverage mismatch")
        for row in rows:
            step = actions[(row["episode_id"], row["turn"])]
            if row["messages"] != step["messages"] or row["target_action"] != step["action"]:
                raise ValueError("Pre-action context or target mismatch")
        counts["exported_actions_verified"] = len(rows)
        counts["exported_episodes_verified"] = len(complete)
    result = dict(status="passed", counts=dict(counts), fixed_max_tokens=manifest["max_tokens"],
                  all_planned_complete=len(complete) == len(manifest["episodes"]),
                  protocol="Every source, completed action, raw provider call, replayed label and exported join checked")
    if exported:
        write_json(exported/"audit.json", result)
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--run", type=Path, default=PACKAGE/"runs/pilot-20260910")
    p.add_argument("--export", dest="exported", type=Path)
    a = p.parse_args()
    print(json.dumps(audit(a.run, a.exported), indent=2))
