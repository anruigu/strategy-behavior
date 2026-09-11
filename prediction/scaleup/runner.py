"""Checkpoint each provider response before deterministic gameplay; replay on resume."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, replace
from pathlib import Path
import json
import threading

from prediction.io_utils import digest, now, read_json, write_json
from . import VERSION
from .catalog import FAMILIES
from .design import game_from_record
from .engine import initial, transition, messages, parse_action, honest_action
from .measure import summarize
from .schema import Episode

ROOT = Path(__file__).resolve().parents[2]


def episode_from_record(record):
    return Episode(**{**{k: v for k, v in record.items() if k != "episode_id"}, "seat_order": tuple(record["seat_order"])})


def step_record(game, state, episode, raw, meta):
    action = parse_action(raw)
    after, facts = transition(game, state, action, episode.opponent_policy, episode.seat_order)
    normal = honest_action(game, state)
    honest_after, _ = transition(game, state, normal, episode.opponent_policy, episode.seat_order)
    control = replace(game, control=True) if FAMILIES[game.family_id].mechanism else game
    checked_after, checked_facts = transition(control, state, action, episode.opponent_policy, episode.seat_order)
    return dict(turn=after["turn"], before=state, messages=messages(game, state, episode),
                raw_response=raw, action=action, call=meta, after=after, facts=facts,
                counterfactual=dict(honest_action=normal, honest_after=honest_after,
                                    own_score_delta=after["scores"][0]-honest_after["scores"][0],
                                    controlled_after=checked_after, controlled_facts=checked_facts,
                                    controlled_score_delta=after["scores"][0]-checked_after["scores"][0],
                                    scope="local_same_state"))


def scripted_episode(game, episode, policy="honest"):
    state = initial(game, episode.environment_seed)
    steps = []
    witness = FAMILIES[game.family_id].witness
    while not state["done"]:
        index = len(steps)
        action = (witness[index] if policy == "witness" and index < len(witness)
                  else "not_an_action" if policy == "invalid" else honest_action(game, state))
        raw = json.dumps(dict(action=action))
        step = step_record(game, state, episode, raw, dict(status="scripted", policy=policy))
        steps.append(step)
        state = step["after"]
    behavior, exploit, outcome = summarize(game, steps)
    return dict(schema_version=VERSION, episode=episode.record(), game=game.record(), provenance="scripted_fixture",
                policy=policy, status="complete", steps=steps, behavior=behavior, exploit=exploit, outcome=outcome)


def source_hashes():
    paths = [*Path(__file__).parent.glob("*.py"), ROOT / "prediction/client.py", ROOT / "prediction/io_utils.py",
             ROOT / "benchmark/clients.py", ROOT / "benchmark/fullscale/budget.py",
             ROOT / "hole_exp/run_referee_crossplay.py"]
    import hashlib
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def verify_trace(trace, game, episode, calls_root=None):
    if trace["game"] != game.record() or trace["episode"] != episode.record():
        raise ValueError("Trace identity mismatch")
    state = initial(game, episode.environment_seed)
    for saved in trace["steps"]:
        expected = step_record(game, state, episode, saved["raw_response"], saved["call"])
        if saved != expected:
            raise ValueError(f"Replay mismatch at turn {saved['turn']}")
        if trace["provenance"] == "model_rollout":
            if saved["call"]["status"] != "ok":
                raise ValueError("Failed inference was converted to behavior")
            if calls_root is not None:
                call = read_json(Path(calls_root) / episode.player_id / (saved["call"]["call_id"]+".json"))
                if call["request"]["messages"] != saved["messages"] or call["response"]["choices"][0]["message"]["content"] != saved["raw_response"]:
                    raise ValueError("Raw provider provenance mismatch")
                if call["status"] != "ok" or call["response"]["model"] != saved["call"]["actual_model"]:
                    raise ValueError("Provider model/status mismatch")
        state = expected["after"]
    if trace["status"] == "complete":
        if not state["done"]:
            raise ValueError("Premature completion")
        behavior, exploit, outcome = summarize(game, trace["steps"])
        if (trace["behavior"], trace["exploit"], trace["outcome"]) != (behavior, exploit, outcome):
            raise ValueError("Label mismatch")
    return state


def run_episode(game, spec, client, out, manifest_digest):
    episode = episode_from_record(spec)
    folder = out / "episodes" / episode.episode_id
    path = folder / "trace.json"
    if path.exists():
        trace = read_json(path)
        if trace["manifest_digest"] != manifest_digest:
            raise ValueError("Manifest changed on resume")
        state = verify_trace(trace, game, episode, out/"calls")
        if trace["status"] == "complete":
            return "complete"
    else:
        state = initial(game, episode.environment_seed)
        trace = dict(schema_version=VERSION, episode=episode.record(), game=game.record(),
                     manifest_digest=manifest_digest, provenance="model_rollout", status="incomplete",
                     started=now(), steps=[])
        write_json(path, trace)
    while not state["done"]:
        prompt = messages(game, state, episode)
        decision_path = folder / f"decision-{state['turn']+1:02}.json"
        decision = read_json(decision_path) if decision_path.exists() else dict(messages=prompt, attempts=[])
        if decision["messages"] != prompt:
            raise ValueError("Decision context changed")
        successful = next((a for a in decision["attempts"] if a["meta"]["status"] == "ok"), None)
        if successful is None:
            if len(decision["attempts"]) >= 3:
                return "incomplete"
            raw, meta = client.generate(prompt, purpose="behavior-scaleup-play")
            successful = dict(raw=raw, meta=meta)
            decision["attempts"].append(successful)
            write_json(decision_path, decision)
            if meta["status"] != "ok":
                trace.update(last_error=meta, updated=now())
                write_json(path, trace)
                return "incomplete"
        step = step_record(game, state, episode, successful["raw"], successful["meta"])
        trace["steps"].append(step)
        state = step["after"]
        write_json(path, trace)
    behavior, exploit, outcome = summarize(game, trace["steps"])
    trace.update(status="complete", finished=now(), behavior=behavior, exploit=exploit, outcome=outcome)
    trace.pop("last_error", None)
    verify_trace(trace, game, episode, out/"calls")
    write_json(path, trace)
    return "complete"


def run(manifest_path, out, workers=8, limit=None):
    from prediction.client import Client, ModelConfig, Ledger
    manifest = read_json(manifest_path)
    if workers < 1 or (limit is not None and limit < 1):
        raise ValueError("Workers and optional limit must be positive")
    if manifest["sources"] != source_hashes():
        raise ValueError("Source changed since manifest freeze; create a new manifest/run")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    saved_manifest = out/"manifest.json"
    if saved_manifest.exists() and read_json(saved_manifest) != manifest:
        raise ValueError("Run directory belongs to another manifest")
    write_json(saved_manifest, manifest)
    if not (out/"source").exists():
        for relative in manifest["sources"]:
            target = out/"source"/relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes((ROOT/relative).read_bytes())
    ledger = Ledger(out/"budget.sqlite", manifest["budget_usd"])
    stage = Ledger(out/"stage-budget.sqlite", manifest["budget_usd"])
    clients = {name: Client(ModelConfig(**conf), out/"calls"/name, ledger, stage, manifest["max_tokens"])
               for name, conf in manifest["models"].items()}
    games = {r["game_id"]: game_from_record(r) for r in manifest["games"]}
    counts = {"complete": 0, "incomplete": 0, "errors": 0}
    records = manifest["episodes"][:limit] if limit else manifest["episodes"]
    errors = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        jobs = {pool.submit(run_episode, games[spec["game_id"]], spec, clients[spec["player_id"]], out, digest(manifest)): spec for spec in records}
        for future in as_completed(jobs):
            try:
                counts[future.result()] += 1
            except Exception as exc:
                counts["errors"] += 1
                errors.append(dict(episode_id=jobs[future]["episode_id"], error=type(exc).__name__, message=str(exc)[:300]))
            write_json(out/"status.json", dict(updated=now(), planned=len(manifest["episodes"]), selected=len(records),
                                              **counts, errors_detail=errors, budget=ledger.summary()))
            print(json.dumps(counts), flush=True)
    return counts
