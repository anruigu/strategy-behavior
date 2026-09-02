"""Outcome metrics for one realized negotiation, plus the achievable ceiling.

`achievable_gain` is the whole reason gains are comparable across settings.
A draw's endowments are random in 5-25 units, so raw point gains swing by an
order of magnitude between seeds for reasons no player controls. The
first-best allocation -- every unit of every resource held by whoever values it
most -- is exactly computable here because values are per-unit and linear, and
it is the only allocation-independent scale the seeds share.
"""
from __future__ import annotations

from typing import Any, Dict, List

from neg_env import RESOURCES, inventory_value


def achievable(setting: Dict[str, Any]) -> Dict[str, float]:
    """First-best joint value and the joint gain it leaves on the table."""
    res, vals = setting["resources"], setting["values"]
    pids = list(range(setting["n_players"]))
    totals = {r: sum(res[p][r] for p in pids) for r in RESOURCES}
    best_holder = {r: max(pids, key=lambda p: vals[p][r]) for r in RESOURCES}
    max_joint = sum(totals[r] * vals[best_holder[r]][r] for r in RESOURCES)
    init_joint = sum(inventory_value(res[p], vals[p]) for p in pids)
    return {"max_joint": float(max_joint), "init_joint": float(init_joint),
            "achievable_gain": float(max_joint - init_joint),
            "best_holder": best_holder, "totals": totals}


def episode_metrics(setting: Dict[str, Any], gs: Dict[str, Any]) -> Dict[str, Any]:
    pids = list(range(setting["n_players"]))
    a = achievable(setting)
    gain = {p: gs["gain"][p] for p in pids}
    joint_gain = sum(gain.values())
    eff = joint_gain / a["achievable_gain"] if a["achievable_gain"] > 0 else 0.0

    moved: Dict[str, int] = {r: 0 for r in RESOURCES}
    for t in gs["trades"]:
        for r, q in t["offered"].items():
            moved[r] += q
        for r, q in t["requested"].items():
            moved[r] += q
    focal = max(RESOURCES, key=lambda r: moved[r]) if sum(moved.values()) else None

    # Who ends up holding the most units of the regime's special resource, and
    # what share of it. For `spike` the interesting question is whether the one
    # party with the private taste captured it; for `swan` it is who won the
    # item everyone wants.
    special = setting.get("special_item")
    special_holder = special_share = None
    if special is not None:
        end = {p: gs["player_resources"][p][special] for p in pids}
        tot = sum(end.values())
        special_holder = max(pids, key=lambda p: end[p])
        special_share = (end[special_holder] / tot) if tot else 0.0

    return {
        "gain": gain,
        "joint_gain": joint_gain,
        "efficiency": eff,
        "achievable_gain": a["achievable_gain"],
        "rank_by_gain": sorted(pids, key=lambda p: -gain[p]),
        "top_gainer": max(pids, key=lambda p: gain[p]),
        "n_trades": len(gs["trades"]),
        "units_moved": moved,
        "focal_resource": focal,
        "focal_holder": (max(pids, key=lambda p: gs["player_resources"][p][focal])
                         if focal else None),
        "special_item": special,
        "special_party": setting.get("special_party"),
        "special_holder": special_holder,
        "special_share": special_share,
        "offers_made": gs["offers_made"], "offers_accepted": gs["offers_accepted"],
        "offers_denied": gs["offers_denied"], "broadcasts": gs["broadcasts"],
        "whispers": gs["whispers"], "invalid_tokens": gs["invalid_tokens"],
        "empty_turns": gs["empty_turns"],
        "final_resources": gs["player_resources"],
        "initial_value": gs["initial_value"], "final_value": gs["final_value"],
    }
