"""End-to-end checks over real transitions and independent paired trajectories."""
from collections import Counter
from dataclasses import replace

from .catalog import FAMILIES
from .design import game_from_record
from .engine import initial, transition
from .runner import scripted_episode, verify_trace
from .schema import Episode


def validate_records(records, seeds=(0, 1, 2)):
    counts = Counter()
    coverage = {fid: dict(variants=0, witness_execution_variants=0, neutral_witness_variants=0,
                         mechanism=family.mechanism) for fid, family in FAMILIES.items() if any(r["family_id"] == fid for r in records)}
    witnesses = []
    for record in records:
        game = game_from_record(record)
        family = FAMILIES[game.family_id]
        executed = False
        for seed in seeds:
            episode = Episode(game.game_id, "scripted:witness", seed, seed, (0, 1, 2))
            for policy in ("honest", "witness", "invalid"):
                trace = scripted_episode(game, episode, policy)
                verify_trace(trace, game, episode)
                counts["replayed_scripted_episodes"] += 1
                counts["replayed_transitions"] += len(trace["steps"])
                if policy in ("honest", "invalid") and any(t["facts"]["mechanism_executed"] for t in trace["steps"]):
                    raise ValueError(f"False positive on {game.family_id}/{policy}")
                if game.control and any(t["facts"]["mechanism_executed"] for t in trace["steps"]):
                    raise ValueError("Control did not close mechanism")
                if policy == "witness":
                    executed |= any(t["facts"]["mechanism_executed"] for t in trace["steps"])
                    if record["block"] == 0 and record["intervention_axis"] is None:
                        witnesses.append(trace)
            state = initial(game, seed)
            before = initial(game, seed)
            for action in family.actions:
                after, facts = transition(game, state, action)
                if state != before or transition(game, state, action) != (after, facts):
                    raise ValueError("Transition mutates input or is nondeterministic")
                counts["pure_transition_checks"] += 1
        if not game.control:
            coverage[game.family_id]["variants"] += 1
            coverage[game.family_id]["witness_execution_variants" if executed else "neutral_witness_variants"] += 1
    for fid, row in coverage.items():
        if row["mechanism"] and row["witness_execution_variants"] == 0:
            raise ValueError(f"No executed witness anywhere in {fid}")
    return dict(counts=counts, coverage=coverage,
                caveat="Neutral witness variants are retained: a dose can remove contrast or a sampled hidden state can make the witness uninformative. Execution is not necessarily beneficial."), witnesses
