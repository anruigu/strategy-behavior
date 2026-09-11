"""Build, validate, plan, collect, and export the behavioral dataset."""
import argparse
from collections import Counter
from dataclasses import asdict, replace
import json
from pathlib import Path

from prediction.io_utils import now, read_json, write_json
from .catalog import FAMILIES
from .design import generate, split_manifests, audit_design, episode_plan
from .export import write_jsonl, export_run
from .runner import source_hashes, run
from .schema import Player
from .validate import validate_records


def read_jsonl(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def build(args):
    out = args.out
    if out.exists() and any(out.iterdir()):
        raise ValueError("Build output must be new or empty")
    if args.validation_seeds < 1:
        raise ValueError("At least one validation seed required")
    records, pairs = generate(blocks=args.blocks, seed=args.seed)
    splits = split_manifests(records)
    audit = audit_design(records, pairs, splits)
    validation, fixtures = validate_records(records, seeds=tuple(range(args.validation_seeds)))
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out/"games.jsonl", records)
    write_jsonl(out/"counterfactual_pairs.jsonl", pairs)
    write_jsonl(out/"validation_fixtures.jsonl", fixtures)
    write_json(out/"families.json", {fid: f.record() for fid, f in FAMILIES.items()})
    write_json(out/"splits.json", splits)
    write_json(out/"validation.json", validation)
    write_json(out/"design_audit.json", audit)
    manifest = dict(created=now(), sources=source_hashes(), seed=args.seed, blocks=args.blocks,
                    game_families=len(FAMILIES), mechanisms=len({f.mechanism for f in FAMILIES.values() if f.mechanism}),
                    **audit, base_games=sum(not r["control"] for r in records),
                    controlled_games=sum(r["control"] for r in records), model_episodes=0,
                    fixture_provenance="scripted validation only",
                    hypothetical_scale=dict(models=15, episodes_per_configuration=4,
                         normal_base_episodes=sum(not r["control"] for r in records)*15*4,
                         full_two_framing_episode_count=len(records)*15*4*2))
    write_json(out/"manifest.json", manifest)
    lines = ["# Parameterized behavioral dataset", "",
             f"Built {manifest['base_games']:,} base games and {manifest['controlled_games']:,} controlled counterparts across 24 families and 20 mechanisms.", "",
             "These files define playable game instances. Model behavior lives in a separately collected run. validation_fixtures.jsonl contains scripted witnesses only.", "",
             "| Family | Mechanism | Base variants | Witness-positive variants |", "|---|---|---:|---:|"]
    for fid, row in validation["coverage"].items():
        lines.append(f"| {fid} | {row['mechanism'] or 'ordinary strategic control'} | {row['variants']} | {row['witness_execution_variants']} |")
    lines += ["", "Witness-positive means at least one tested environment seed produced the mechanism effect; it does not imply positive net payoff. "
              "Neutral doses remain included. See validation.json for exact checks and coverage."]
    (out/"DATASET_CARD.md").write_text("\n".join(lines)+"\n")
    return manifest


def plan(args):
    from .providers import configurations
    records = read_jsonl(args.dataset/"games.jsonl")
    if args.families:
        names = args.families.split(",")
        if set(names)-set(FAMILIES):
            raise ValueError("Unknown family")
        records = [r for r in records if r["family_id"] in names]
    if args.pilot:
        records = [r for r in records if r["block"] == 0 and r["intervention_axis"] in (None, "reward")
                   and r["parameters"]["reward"] in (2, 6)]
    names = args.models.split(",")
    models = configurations(names, args.provider)
    players = {}
    for name, config in models.items():
        family = next((family for token, family in (("qwen", "qwen"), ("kimi", "kimi"), ("glm", "glm"),
                           ("claude", "claude"), ("gpt", "gpt"), ("gemini", "gemini"), ("gemma", "gemma"), ("deepseek", "deepseek"))
                       if token in name), "unknown")
        players[name] = asdict(Player(name, family, config["provider"], config["provider_model"]))
    episodes = list(episode_plan(records, names, args.trials, tuple(args.prompts.split(",")), tuple(args.opponents.split(",")), args.seed))
    horizons = {r["game_id"]: r["parameters"]["horizon"] for r in records}
    manifest = dict(created=now(), dataset=str(args.dataset.resolve()), sources=source_hashes(),
                    games=records, models=models, players=players, episodes=episodes,
                    budget_usd=args.budget_usd, max_tokens=args.max_tokens,
                    note="Requested provider IDs are verified by actual returned model in each call; catalog presence alone is not a successful generation")
    if args.out.exists():
        raise ValueError("Plan output already exists")
    write_json(args.out, manifest)
    return dict(games=len(records), episodes=len(episodes), models=names,
                max_action_calls=sum(horizons[e["game_id"]] for e in episodes),
                manifest=str(args.out))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    b = sub.add_parser("build")
    b.add_argument("--out", type=Path, required=True)
    b.add_argument("--blocks", type=int, default=8)
    b.add_argument("--seed", type=int, default=910)
    b.add_argument("--validation-seeds", type=int, default=3)
    p = sub.add_parser("plan")
    p.add_argument("--dataset", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--models", default="qwen-3.8-27b,glm")
    p.add_argument("--provider", choices=("openrouter", "configured"), default="openrouter")
    p.add_argument("--trials", type=int, default=3)
    p.add_argument("--prompts", default="normal,active_exploration")
    p.add_argument("--opponents", default="ordinary")
    p.add_argument("--families")
    p.add_argument("--pilot", action="store_true")
    p.add_argument("--budget-usd", type=float, default=50)
    p.add_argument("--max-tokens", type=int, default=16384)
    p.add_argument("--seed", type=int, default=910)
    r = sub.add_parser("run")
    r.add_argument("--manifest", type=Path, required=True)
    r.add_argument("--out", type=Path, required=True)
    r.add_argument("--workers", type=int, default=8)
    r.add_argument("--limit", type=int)
    e = sub.add_parser("export")
    e.add_argument("--run", type=Path, required=True)
    e.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "build":
        result = build(args)
    elif args.command == "plan":
        result = plan(args)
    elif args.command == "run":
        result = run(args.manifest, args.out, args.workers, args.limit)
    else:
        result = export_run(args.run, args.out)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
