"""Deterministic episode statistics; conditional rates describe observations."""

from __future__ import annotations

import copy
import math

from .games import payoff


def _rate(successes: int, opportunities: int, applicable: bool = True) -> dict:
    if not applicable:
        successes = opportunities = 0
    if not 0 <= successes <= opportunities:
        raise ValueError("Invalid event counts")
    return {"value": successes / opportunities if opportunities else None,
            "successes": int(successes), "opportunities": int(opportunities),
            "applicable": bool(applicable)}


def measure_episode(trace: dict) -> list[dict]:
    """Return one measurement row per focal player, preserving paired dependence.

    Incomplete traces must not silently become complete behavioral labels.
    Missing status is accepted for standalone deterministic/synthetic fixtures.
    """
    if trace.get("status", "complete") != "complete":
        raise ValueError("Only complete episodes can be measured")
    game, rounds, models = trace["game"], trace["rounds"], trace["models"]
    if len(models) != 2:
        raise ValueError("An episode must have exactly two models")
    for index, event in enumerate(rounds, 1):
        if event["round"] != index or len(event["actions"]) != 2 or len(event["payoffs"]) != 2:
            raise ValueError("Malformed or nonconsecutive episode rounds")
        expected = payoff(game, *event["actions"])
        if any(not math.isfinite(float(observed)) or not math.isclose(float(observed), actual, rel_tol=1e-9, abs_tol=1e-9)
               for observed, actual in zip(event["payoffs"], expected)):
            raise ValueError("Recorded payoffs do not match canonical actions and player roles")
    app = game["applicability"]
    c, d = app["cooperative_action"], app["defective_action"]
    coordinated = {tuple(a) for a in app["coordination_outcomes"]}
    records = []
    for focal in (0, 1):
        own = [event["actions"][focal] for event in rounds]
        other = [event["actions"][1 - focal] for event in rounds]
        H = len(own)
        retaliation_events = [t for t in range(1, H) if other[t - 1] == d] if app["retaliation"] else []
        baseline_events = [t for t in range(1, H) if other[t - 1] == c] if app["retaliation"] else []
        forgiveness_events = [t for t in range(2, H)
            if other[t - 2] == d and own[t - 1] == d and other[t - 1] == c] if app["forgiveness"] else []
        response_events = [t for t in retaliation_events if own[t - 1] == c]
        cc_events = [t for t in baseline_events if own[t - 1] == c]
        exploit_events = [t for t in range(H) if app["exploiting_actions_by_opponent_action"][str(other[t])]]
        targets = {
            "action0": _rate(sum(a == 0 for a in own), H),
            "first_action0": _rate(int(bool(own) and own[0] == 0), int(bool(own))),
            "cooperation": _rate(sum(a == c and b == c for a, b in zip(own, other)), H, app["cooperation"]),
            "individual_cooperation": _rate(sum(a == c for a in own), H, app["cooperation"]),
            "retaliation": _rate(sum(own[t] == d for t in retaliation_events), len(retaliation_events), app["retaliation"]),
            "defection_after_cooperation": _rate(sum(own[t] == d for t in baseline_events), len(baseline_events), app["retaliation"]),
            "retaliation_after_exploitation": _rate(sum(own[t] == d for t in response_events), len(response_events), app["retaliation"]),
            "defection_after_mutual_cooperation": _rate(sum(own[t] == d for t in cc_events), len(cc_events), app["retaliation"]),
            "forgiveness": _rate(sum(own[t] == c for t in forgiveness_events), len(forgiveness_events), app["forgiveness"]),
            "coordination": _rate(sum(tuple(e["actions"]) in coordinated for e in rounds), H, app["coordination"]),
            "exploitation": _rate(sum(own[t] in app["exploiting_actions_by_opponent_action"][str(other[t])]
                                      for t in exploit_events), len(exploit_events), app["exploitation"]),
        }
        retaliation = targets["retaliation"]["value"]
        baseline = targets["defection_after_cooperation"]["value"]
        response = targets["retaliation_after_exploitation"]["value"]
        cc_baseline = targets["defection_after_mutual_cooperation"]["value"]
        own_total = sum(float(e["payoffs"][focal]) for e in rounds)
        other_total = sum(float(e["payoffs"][1 - focal]) for e in rounds)
        records.append({
            "episode_id": trace["id"], "game_id": game["id"], "group_id": game["group_id"],
            "family": game["family"], "model": models[focal], "opponent": models[1 - focal],
            "pair": "|".join(sorted(models)), "player_index": focal, "trial_id": trace["trial_id"],
            "representation": trace["representation"], "swap": bool(trace.get("swap", False)),
            "features": copy.deepcopy(game["features"]), "payoffs": copy.deepcopy(game["payoffs"]),
            "split_metadata": copy.deepcopy(game.get("split_metadata", {})),
            "targets": targets,
            "descriptive": {"rounds": H, "total_payoff": own_total,
                "mean_payoff": own_total / H if H else None,
                "mean_welfare": (own_total + other_total) / H if H else None,
                "mean_payoff_advantage": (own_total - other_total) / H if H else None,
                "retaliation_difference": retaliation - baseline if retaliation is not None and baseline is not None else None,
                "retaliation_after_exploitation_difference": response - cc_baseline if response is not None and cc_baseline is not None else None},
        })
    return records
