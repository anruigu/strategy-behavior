"""Export verified model data with predictor inputs separated from annotations."""
from collections import Counter, defaultdict
from pathlib import Path
import json

from prediction.io_utils import read_json, write_json
from .design import game_from_record
from .runner import episode_from_record, verify_trace


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+".tmp")
    with temporary.open("w") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, allow_nan=False)+"\n")
    temporary.replace(path)


def export_run(run_dir, out):
    run_dir, out = Path(run_dir), Path(out)
    manifest = read_json(run_dir/"manifest.json")
    games = {r["game_id"]: r for r in manifest["games"]}
    rows, actions, incomplete = [], [], []
    for spec in manifest["episodes"]:
        path = run_dir/"episodes"/spec["episode_id"]/"trace.json"
        if not path.exists():
            incomplete.append(dict(episode_id=spec["episode_id"], status="not_started"))
            continue
        trace = read_json(path)
        game_record = games[spec["game_id"]]
        game, episode = game_from_record(game_record), episode_from_record(spec)
        verify_trace(trace, game, episode, run_dir/"calls")
        if trace["status"] != "complete":
            incomplete.append(dict(episode_id=spec["episode_id"], status=trace["status"]))
            continue
        inputs = dict(game_id=game.game_id, family_id=game.family_id,
                      natural_language=game_record["natural_language"], structured=game_record["structured"],
                      control=game.control, player=manifest["players"][episode.player_id],
                      role=dict(seat_id=episode.seat_order[0], strategic_role=game_record["structured"]["role"]),
                      context=dict(prompt_condition=episode.prompt_condition, opponent_policy=episode.opponent_policy,
                                   opponent_implementation=episode.opponent_implementation,
                                   construction_seed=game.construction_seed, seat_order=episode.seat_order))
        identity = dict(episode_id=episode.episode_id, pair_group_id=game_record["pair_group_id"],
                        trial=episode.trial, environment_seed=episode.environment_seed,
                        provenance="model_rollout", trace_path=str(path.resolve()))
        rows.append(dict(**identity, inputs=inputs, labels=dict(behavior=trace["behavior"], exploit=trace["exploit"], outcome=trace["outcome"])))
        for step in trace["steps"]:
            # Exact pre-action prompt contains no future events, raw response, or evaluator labels.
            actions.append(dict(**identity, turn=step["turn"], inputs=inputs, messages=step["messages"],
                                target_action=step["action"], valid=step["facts"]["valid"], call_id=step["call"]["call_id"]))
    write_jsonl(out/"episodes.jsonl", rows)
    write_jsonl(out/"actions.jsonl", actions)
    write_jsonl(out/"missing.jsonl", incomplete)
    by_model = defaultdict(list)
    for row in rows:
        by_model[row["inputs"]["player"]["model_id"]].append(row)
    summary = dict(planned=len(manifest["episodes"]), complete=len(rows), missing=len(incomplete), actions=len(actions),
                   models={model: dict(episodes=len(group),
                         mechanism_execution_episodes=sum(r["labels"]["exploit"]["executed"] is True for r in group),
                         invalid_actions=sum(t["inputs"]["player"]["model_id"] == model and not t["valid"] for t in actions))
                           for model, group in by_model.items()},
                   inference="Descriptive pilot only; model and dose comparisons need replication and opportunity-specific denominators")
    write_json(out/"summary.json", summary)
    return summary
