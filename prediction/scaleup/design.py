"""Deterministic single-parameter intervention stars and grouped evaluation splits."""
from dataclasses import asdict, replace
import random

from prediction.io_utils import digest
from .catalog import FAMILIES, render
from .schema import Game, Episode


def split_number(key, salt):
    return int(digest([salt, key])[:8], 16) % 10


def partition(key, salt):
    n = split_number(key, salt)
    return "test" if n < 2 else "validation" if n == 2 else "train"


def generate(family_ids=None, blocks=6, seed=910):
    if not 1 <= blocks <= 25:
        raise ValueError("blocks must be between 1 and 25 distinct constructions")
    records, pairs = {}, []
    for fid in family_ids or FAMILIES:
        family = FAMILIES[fid]
        for block in range(blocks):
            rng = random.Random(digest([seed, fid, block]))
            # Anchor 0 is interpretable defaults. Other backgrounds vary jointly;
            # every intervention edge changes exactly one value from its anchor.
            params = {k: spec.default if block == 0 else rng.choice(spec.values) for k, spec in family.parameters.items()}
            construction = block  # public rival endowments define game construction
            anchor = Game(fid, params, construction)
            group = "group-"+digest([seed, fid, block])[:20]
            variants = [(anchor, None)]
            for axis, spec in family.parameters.items():
                for value in spec.values:
                    if value != params[axis]:
                        variants.append((Game(fid, {**params, axis: value}, construction), axis))
            for game, axis in variants:
                if game.game_id in records:
                    raise ValueError("Duplicate game construction")
                record = {**game.record(), "pair_group_id": group, "block": block, "intervention_axis": axis,
                          "natural_language": render(game),
                          "structured": dict(horizon=game.parameters["horizon"], players=3, role=family.role,
                                             information=family.information, communication=any(a in family.actions for a in ("clue", "invite", "upper")),
                                             action_space=family.actions, parameters=game.parameters,
                                             objective="own score rank", turn_structure="focal action then fixed rival resolution",
                                             initial_endowment_rule="focal 20; rival1 18+construction%5; rival2 18+(construction//5)%5"),
                          "research_only": dict(mechanism=family.mechanism, mechanism_kind=family.mechanism_kind,
                                                witness_actions=family.witness)}
                records[game.game_id] = record
                if axis:
                    pairs.append(dict(pair_id="pair-"+digest([anchor.game_id, game.game_id])[:20],
                                      pair_group_id=group, a=anchor.game_id, b=game.game_id, axis=axis,
                                      a_value=params[axis], b_value=game.parameters[axis], intervention_kind="parameter"))
                if family.mechanism:
                    controlled = replace(game, control=True)
                    records[controlled.game_id] = {**record, **controlled.record(), "natural_language": render(controlled)}
                    pairs.append(dict(pair_id="pair-"+digest([game.game_id, controlled.game_id])[:20],
                                      pair_group_id=group, a=game.game_id, b=controlled.game_id, axis="control",
                                      a_value=False, b_value=True,
                                      intervention_kind="patch" if family.mechanism_kind == "implementation_discrepancy" else "strategic_ablation"))
    return list(records.values()), pairs


def game_from_record(record):
    return Game(**{k: record[k] for k in ("family_id", "parameters", "construction_seed", "control", "schema_version")})


def split_manifests(records):
    """Alternatives, not one combined split. Parameter splits intentionally cross dose groups."""
    splits = {}
    for name in ("random_group", "held_out_construction", "held_out_family", "held_out_mechanism",
                 "parameter_interpolation", "parameter_extrapolation"):
        assignments = {}
        for r in records:
            fid = r["family_id"]
            if name == "random_group":
                fold = partition(r["pair_group_id"], name)
            elif name == "held_out_construction":
                fold = partition([fid, r["construction_seed"]], name)
            elif name == "held_out_family":
                fold = partition(fid, name)
            elif name == "held_out_mechanism":
                fold = partition(FAMILIES[fid].mechanism or "ordinary_game", name)
            else:
                # Primary dose axis exists in every family and actually changes
                # its incentive/effect. Patch pairs always have the same dose.
                reward = r["parameters"]["reward"]
                fold = ("test" if reward == 6 else "validation" if reward == 8 else "train") if name.endswith("interpolation") else (
                    "test" if reward == 12 else "validation" if reward == 8 else "train")
            assignments[r["game_id"]] = fold
        splits[name] = dict(assignments=assignments,
                            grouping="dose only; paired controls and replications stay together" if name.startswith("parameter") else "whole intervention group",
                            holdout_axis="reward" if name.startswith("parameter") else name,
                            available_partitions=sorted(set(assignments.values())))
    splits["cross_environment"] = dict(status="deferred", reason="Requires separately collected external-environment data")
    return splits


def episode_plan(records, player_ids, trials=3, prompt_conditions=("normal", "active_exploration"),
                 opponent_policies=("ordinary",), seed=910):
    if trials < 1 or not player_ids or len(set(player_ids)) != len(player_ids):
        raise ValueError("Positive trials and distinct players required")
    for r in records:
        for model in player_ids:
            for trial in range(trials):
                # Matched randomness/seats across all dose and control variants,
                # framing conditions, and model identities in an intervention group.
                key = [seed, r["pair_group_id"], trial]
                episode_seed = int(digest(key)[:8], 16)
                seats = [0, 1, 2]
                random.Random(episode_seed).shuffle(seats)
                for prompt in prompt_conditions:
                    for opponent in opponent_policies:
                        yield Episode(r["game_id"], model, trial, episode_seed, tuple(seats), prompt, opponent).record()


def audit_design(records, pairs, splits):
    lookup = {r["game_id"]: r for r in records}
    if len(lookup) != len(records):
        raise ValueError("Duplicate game IDs")
    counts = {"games": len(records), "parameter_pairs": 0, "control_pairs": 0}
    for pair in pairs:
        a, b = lookup[pair["a"]], lookup[pair["b"]]
        ga, gb = game_from_record(a), game_from_record(b)
        if ga.family_id != gb.family_id or ga.construction_seed != gb.construction_seed:
            raise ValueError("Pair changed family/construction")
        changed = [k for k in ga.parameters if ga.parameters[k] != gb.parameters[k]]
        if pair["axis"] == "control":
            if changed or ga.control == gb.control:
                raise ValueError("Invalid control pair")
            if pair["intervention_kind"] == "patch" and a["natural_language"] != b["natural_language"]:
                raise ValueError("Patch leaked into player rules")
            counts["control_pairs"] += 1
        else:
            if changed != [pair["axis"]] or ga.control != gb.control:
                raise ValueError("Intervention changed more than one parameter")
            counts["parameter_pairs"] += 1
        for name, split in splits.items():
            if "assignments" not in split:
                continue
            if name.startswith("parameter") and pair["axis"] != "control":
                continue
            if split["assignments"][a["game_id"]] != split["assignments"][b["game_id"]]:
                raise ValueError(f"Pair leakage in {name}")
    return counts
