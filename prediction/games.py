"""Symmetric two-action games, strategic features, and exact-value prompts.

Canonical payoffs are [[(R,R),(S,T)],[(T,S),(P,P)]].  Display permutations
never change canonical coordinates.  This module performs no inference calls.
"""

from __future__ import annotations

import hashlib
import math
import random
from typing import Any

_KEYS = ("R", "S", "T", "P")
_EPS = 1e-10


def _values(game: dict) -> tuple[float, float, float, float]:
    return tuple(float(game["payoffs"][key]) for key in _KEYS)


def _normalized(values):
    lo, hi = min(values), max(values)
    return tuple((x - lo) / (hi - lo) for x in values) if hi > lo else (0.0,) * 4


def _shape_id(values) -> str:
    # A simultaneous action swap sends (R,S,T,P) to (P,T,S,R).
    normal = _normalized(values)
    alternatives = (normal, (normal[3], normal[2], normal[1], normal[0]))
    # Finite precision tolerance is intentional: equivalent floats can differ
    # after affine arithmetic. Ten decimal places defines grouping precision.
    encoding = min(tuple(f"{x:.10f}" for x in candidate) for candidate in alternatives)
    return "shape_" + hashlib.sha256(",".join(encoding).encode()).hexdigest()[:20]


def payoff(game: dict, action_i: int, action_j: int) -> tuple[float, float]:
    """Return row and column payoffs, with actions in canonical coordinates."""
    if any(type(a) is not int or a not in (0, 1) for a in (action_i, action_j)):
        raise ValueError("Canonical actions must be integer 0 or 1")
    R, S, T, P = _values(game)
    return (((R, R), (S, T)), ((T, S), (P, P)))[action_i][action_j]


def _family(normal) -> str:
    R, S, T, P = normal
    gap0, gap1 = R - T, S - P
    if max(normal) - min(normal) <= _EPS:
        return "indifferent"
    if abs(R - P) <= _EPS:
        if gap0 > _EPS and gap1 < -_EPS:
            return "coordination"
        if gap0 < -_EPS and gap1 > _EPS:
            return "anti_coordination"
        if (gap0 > _EPS and gap1 > _EPS) or (gap0 < -_EPS and gap1 < -_EPS):
            return "dominance"
    if abs(gap0) <= _EPS or abs(gap1) <= _EPS:
        return "weak_dominance" if gap0 * gap1 >= -_EPS else "degenerate"
    # Name social-dilemma quadrants relative to the better symmetric outcome,
    # so simultaneously renaming both actions leaves the family unchanged.
    if P > R:
        R, S, T, P = P, T, S, R
    if R > T and S > P:
        return "harmony"
    if R > T and S < P:
        return "stag_hunt"
    if R < T and S > P:
        return "chicken"
    if R < T and S < P:
        return "prisoners_dilemma"
    return "degenerate"


def _properties(values):
    R, S, T, P = values
    r, s, t, p = _normalized(values)
    normal_game = {"payoffs": dict(zip(_KEYS, (r, s, t, p)))}
    profiles = [(0, 0), (0, 1), (1, 0), (1, 1)]
    outcomes = {a: payoff(normal_game, *a) for a in profiles}
    pure, strict = [], []
    for a, b in profiles:
        u, v = outcomes[a, b]
        row_gap = u - outcomes[1 - a, b][0]
        column_gap = v - outcomes[a, 1 - b][1]
        if row_gap >= -_EPS and column_gap >= -_EPS:
            pure.append((a, b))
        if row_gap > _EPS and column_gap > _EPS:
            strict.append((a, b))
    pareto = [a for a in profiles if not any(
        all(x >= y - _EPS for x, y in zip(outcomes[b], outcomes[a]))
        and any(x > y + _EPS for x, y in zip(outcomes[b], outcomes[a]))
        for b in profiles if b != a
    )]
    gap0, gap1 = r - t, s - p
    denom = gap0 - gap1
    all_indifferent = abs(gap0) <= _EPS and abs(gap1) <= _EPS
    mixed = -gap1 / denom if abs(denom) > _EPS else (0.5 if all_indifferent else None)
    interior = mixed is not None and _EPS < mixed < 1 - _EPS
    entropy = -(mixed * math.log2(mixed) + (1 - mixed) * math.log2(1 - mixed)) if interior else 0.0
    # Uniform opponent actions; ties share best-response mass equally.
    br0 = sum(1.0 if g > _EPS else 0.0 if g < -_EPS else 0.5 for g in (gap0, gap1)) / 2
    br_entropy = -(br0 * math.log2(br0) + (1 - br0) * math.log2(1 - br0)) if 0 < br0 < 1 else 0.0
    dominant0 = gap0 > _EPS and gap1 > _EPS
    dominant1 = gap0 < -_EPS and gap1 < -_EPS
    weak0 = gap0 >= -_EPS and gap1 >= -_EPS and max(gap0, gap1) > _EPS
    weak1 = gap0 <= _EPS and gap1 <= _EPS and min(gap0, gap1) < -_EPS
    cooperative = 0 if r > p + _EPS and 2 * r >= s + t - _EPS else (
        1 if p > r + _EPS and 2 * p >= s + t - _EPS else None
    )
    coordination_outcomes = strict if len(strict) >= 2 else []
    exploit_actions = {}
    for other in (0, 1):
        exploit_actions[str(other)] = [own for own in (0, 1)
            if outcomes[own, other][0] > outcomes[1 - own, other][0] + _EPS
            and outcomes[own, other][1] < outcomes[1 - own, other][1] - _EPS
            and outcomes[own, other][0] > outcomes[own, other][1] + _EPS]
    welfare = [sum(outcomes[a]) for a in profiles]
    mean = sum(values) / 4
    normal_mean = sum((r, s, t, p)) / 4
    features = {
        **{f"raw_{k}": float(v) for k, v in zip(_KEYS, values)},
        **{f"normalized_{k}": float(v) for k, v in zip(_KEYS, (r, s, t, p))},
        "payoff_offset": min(values), "payoff_scale": max(values) - min(values),
        "payoff_mean": mean, "payoff_variance": sum((x - mean) ** 2 for x in values) / 4,
        "normalized_variance": sum((x - normal_mean) ** 2 for x in (r, s, t, p)) / 4,
        "raw_gap_against_0": R - T, "raw_gap_against_1": S - P,
        "gap_against_0": gap0, "gap_against_1": gap1,
        "diagonal_gap": r - p, "offdiagonal_inequality": abs(s - t),
        "diagonal_welfare_gap": 2 * abs(r - p),
        "offdiagonal_welfare": s + t, "maximum_welfare": max(welfare),
        "welfare_range": max(welfare) - min(welfare),
        "best_symmetric_welfare_loss": max(welfare) - 2 * max(r, p),
        "strict_dominance": float(dominant0 or dominant1),
        "strict_dominant_action0": float(dominant0),
        "strict_dominant_action1": float(dominant1),
        "weak_dominant_action0": float(weak0), "weak_dominant_action1": float(weak1),
        "all_indifferent": float(all_indifferent),
        "nash_pure_count": float(len(pure)), "nash_strict_count": float(len(strict)),
        "nash_00": float((0, 0) in pure), "nash_01": float((0, 1) in pure),
        "nash_10": float((1, 0) in pure), "nash_11": float((1, 1) in pure),
        "has_interior_mixed_equilibrium": float(interior),
        "interior_mixed_equilibrium_unique": float(interior and not all_indifferent),
        "mixed_equilibrium_action0_probability": float(mixed) if interior else 0.0,
        "mixed_equilibrium_entropy": entropy, "best_response_switching": br_entropy,
        "pareto_outcome_count": float(len(pareto)),
        "pareto_nash_count": float(sum(a in pareto for a in pure)),
        "pure_nash_welfare_loss": max(welfare) - max((sum(outcomes[a]) for a in pure), default=max(welfare)),
    }
    applicability = {
        "cooperation": cooperative is not None, "cooperative_action": cooperative,
        "defective_action": 1 - cooperative if cooperative is not None else None,
        "retaliation": cooperative is not None, "forgiveness": cooperative is not None,
        "coordination": bool(coordination_outcomes),
        "coordination_outcomes": [list(a) for a in coordination_outcomes],
        "exploitation": any(exploit_actions.values()),
        "exploiting_actions_by_opponent_action": exploit_actions,
    }
    return features, applicability, pure, pareto


def make_game(game_id, R, S, T, P, **metadata) -> dict[str, Any]:
    """Validate a game and derive only ex-ante payoff-based features."""
    values = tuple(float(x) for x in (R, S, T, P))
    if not all(math.isfinite(x) for x in values):
        raise ValueError("Payoffs must be finite")
    reserved = {"id", "group_id", "family", "payoffs", "features", "applicability", "pure_nash", "pareto_outcomes", "split_metadata"}
    if reserved.intersection(metadata):
        raise ValueError("Metadata may not override derived game fields")
    features, applicability, pure, pareto = _properties(values)
    if not all(math.isfinite(x) for x in features.values()):
        raise ValueError("Payoffs are too large for finite features")
    canonical = values if values[0] >= values[3] else (values[3], values[2], values[1], values[0])
    r, s, t, p = canonical
    coordinate_defined = abs(r - p) > _EPS * (max(values) - min(values))
    split_metadata = {
        "canonical_coordinates_defined": coordinate_defined,
        "canonical_s": (s - p) / (r - p) if coordinate_defined else None,
        "canonical_t": (t - p) / (r - p) if coordinate_defined else None,
        "canonical_normalized_payoffs": list(min(_normalized(values), tuple(reversed(_normalized(values))))),
    }
    return {
        **metadata, "id": str(game_id), "group_id": _shape_id(values),
        "family": _family(_normalized(values)), "payoffs": dict(zip(_KEYS, values)),
        "features": features, "applicability": applicability,
        "split_metadata": split_metadata,
        "pure_nash": [list(a) for a in pure], "pareto_outcomes": [list(a) for a in pareto],
    }


def generate_games(seed=20260910, n=24) -> list[dict]:
    """Reproducible continuous shapes in seven archetypes, balanced by cycling.

    Four strict incentive quadrants plus equal-diagonal coordination,
    anti-coordination and weak dominance.  n>=7 covers every archetype.
    Game labels, offsets and scales are not shown to players.
    """
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    rng = random.Random(seed)
    games, groups = [], set()
    while len(games) < n:
        index = len(games)
        archetype = index % 7
        if archetype == 0:  # PD with a welfare-optimal cooperative diagonal.
            values = (1.0, rng.uniform(-0.65, -0.1), rng.uniform(1.05, 1.7), 0.0)
        elif archetype == 1:
            values = (1.0, rng.uniform(-0.7, -0.1), rng.uniform(0.15, 0.85), 0.0)
        elif archetype == 2:
            values = (1.0, rng.uniform(0.1, 0.5), rng.uniform(1.1, 1.7), 0.0)
        elif archetype == 3:
            values = (1.0, rng.uniform(0.1, 0.7), rng.uniform(0.1, 0.9), 0.0)
        elif archetype == 4:
            values = (1.0, rng.uniform(-0.8, 0.0), rng.uniform(0.05, 0.65), 1.0)
        elif archetype == 5:
            values = (0.0, rng.uniform(0.2, 0.8), rng.uniform(0.9, 1.5), 0.0)
        else:
            values = (1.0, rng.uniform(0.15, 0.85), 1.0, 0.0)
        scale = rng.uniform(1.5, 7.5)
        offset = rng.uniform(-2.0, 3.0)
        # These rounded numbers are the actual game, not a display-only edit.
        values = tuple(round(offset + scale * x, 2) for x in values)
        # Random canonical orientation avoids confounding action0 with welfare.
        if rng.random() < 0.5:
            values = (values[3], values[2], values[1], values[0])
        game = make_game(f"g{index:04d}", *values, generation_seed=seed,
                         generation_index=index, generator_version="symmetric2x2-v1")
        if game["group_id"] in groups:
            continue
        groups.add(game["group_id"])
        games.append(game)
    return games


def render_game(game: dict, representation="matrix", swap=False) -> str:
    """Show all four self/other consequences using the actual saved floats.

    A is canonical 0 unless swap=True. Python repr preserves a float exactly
    when parsed; rounding displayed values could otherwise alter incentives.
    """
    if representation not in {"matrix", "text", "abstract", "abstract_text", "narrative", "neutral_narrative"}:
        raise ValueError(f"Unknown representation: {representation}")
    actions = (1, 0) if swap else (0, 1)
    labels = ("A", "B")
    cells = {(a, b): payoff(game, actions[a], actions[b]) for a in (0, 1) for b in (0, 1)}
    intro = "You and the other participant each choose A or B simultaneously."
    if representation == "matrix":
        lines = [intro, "Rows are your choice; columns are the other participant's choice.",
                 "Each cell is (your points, other participant's points).",
                 "| Your choice / Other choice | A | B |", "|---|---|---|"]
        for a in (0, 1):
            lines.append(f"| {labels[a]} | " + " | ".join(
                f"({repr(cells[a,b][0])}, {repr(cells[a,b][1])})" for b in (0, 1)) + " |")
        return "\n".join(lines)
    if representation in {"narrative", "neutral_narrative"}:
        intro = ("You and another participant operate two stations in an allocation exercise. "
                 "Each station independently selects setting A or B at the same time. "
                 "The selected pair of settings assigns points to the two participants.")
    lines = [intro]
    for a, b in ((0, 0), (0, 1), (1, 0), (1, 1)):
        own, other = cells[a, b]
        lines.append(f"If you choose {labels[a]} and the other participant chooses {labels[b]}, "
                     f"you receive {repr(own)} points and the other participant receives {repr(other)} points.")
    return "\n".join(lines)
