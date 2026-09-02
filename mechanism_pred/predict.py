"""Ask a model to predict, from the game setting alone, how the game will go.

The predictor is given FULL information -- every seat's endowment and private
value vector -- which no player ever has. That is the mechanism-design framing:
the question is not "can you play well" but "given a mechanism and the agents'
types, can you say what the mechanism will produce". It is also told that the
seats will be played by itself, so a wrong prediction is a failure of
self-model as much as of game-theoretic reasoning.
"""
from __future__ import annotations

import json
from typing import Any, Dict, List

import neg_env as N
from jsonio import extract
from tags import TAG_LIST, clean_tags, tag_menu

SYSTEM = (
    "You are a game theorist and mechanism designer. You are given the complete "
    "specification of a negotiation game -- every player's holdings and every "
    "player's private values -- and asked to predict what will happen when it is "
    "played. Reason carefully, then output a single JSON object and nothing after it."
)


def setting_block(setting: Dict[str, Any], turn_multiple: int) -> str:
    n = setting["n_players"]
    rows = []
    for p in range(n):
        res, vals = setting["resources"][p], setting["values"][p]
        holds = ", ".join(f"{res[r]} {r}" for r in N.RESOURCES)
        v = ", ".join(f"{r} {vals[r]}" for r in N.RESOURCES)
        rows.append(f"  Player {p}\n    holds:  {holds}\n    values: {v} "
                    f"(per unit; sums to 100)\n    starting inventory value to "
                    f"itself: {N.inventory_value(res, vals)} points")
    totals = {r: sum(setting["resources"][p][r] for p in range(n)) for r in N.RESOURCES}
    return ("\n".join(rows) + "\n\n  Total units in the game: "
            + ", ".join(f"{totals[r]} {r}" for r in N.RESOURCES))


def build_prompt(setting: Dict[str, Any], turn_multiple: int, model_name: str) -> str:
    n = setting["n_players"]
    return f"""THE GAME

{n} players, 5 resource types (Wheat, Wood, Sheep, Brick, Ore). Each player
holds some quantity of each and has PRIVATE per-unit values that sum to 100
across the five resources. A player's score is the increase in its own
inventory's value under its OWN values, from start to finish. The game is not
zero-sum: an efficient trade can raise both sides' scores.

Turn order is Player 0, 1, ..., repeating, for {turn_multiple} turns each
({n * turn_multiple} turns total). On its turn a player may issue any number of:

  [Broadcast: message]            - seen by everyone
  [Whisper to X: message]         - seen only by Player X (others are told only
                                    that a whisper happened, not its content)
  [Offer to X: 2 Wheat -> 3 Ore]  - offer X two of your Wheat for three of their
                                    Ore; stays open until X accepts or denies
  [Accept #4] / [Deny #4]         - resolve an offer made to you

Each player sees only its OWN holdings and values, plus the public and private
messages addressed to it. Nobody is told anyone else's values.

THE SETTING (you see everything; the players do not)

{setting_block(setting, turn_multiple)}

WHO IS PLAYING

All {n} seats will be played by {model_name} -- the same model you are, with the
same reasoning budget, sampled at temperature 0.7. Each seat sees only its own
private information and has no knowledge of this prediction.

YOUR TASK

Predict what will actually happen. Output one JSON object:

{{
  "per_player": [
    {{"player": 0,
      "strategy": "one or two sentences: what this seat will actually do",
      "tactics": ["tags from the list below that this seat will use"],
      "predicted_gain": <integer points this seat's inventory value will rise by,
                         under its own values; may be 0 or negative>}},
    ... one entry per player ...
  ],
  "rank_by_gain": [<player ids, largest gain first>],
  "n_trades": <how many offers will actually be accepted and executed>,
  "joint_efficiency": <0.0-1.0: realized total gain across all players divided by
                       the total gain of the first-best allocation, where every
                       unit goes to whoever values it most>,
  "focal_resource": "<the resource the negotiation will centre on: the one with
                      the most units changing hands>",
  "focal_holder": <player id who will end up holding the most units of it>,
  "mechanism": "one to three sentences: the causal story that decides this game"
}}

Allowed tactic tags (use only these; 1-4 per player):
{tag_menu()}

Be concrete and committal. A vague prediction scores no better than a wrong one.
"""


def parse_prediction(raw: str, n_players: int) -> Dict[str, Any]:
    """Normalise a reply into the scored shape; `ok=False` if unusable."""
    d = extract(raw)
    if not isinstance(d, dict):
        return {"ok": False, "reason": "no JSON object in reply", "raw": raw}

    per = {}
    for e in (d.get("per_player") or []):
        if not isinstance(e, dict):
            continue
        try:
            p = int(e.get("player"))
        except (TypeError, ValueError):
            continue
        if p not in range(n_players):
            continue
        try:
            g = int(round(float(e.get("predicted_gain"))))
        except (TypeError, ValueError):
            g = None
        per[p] = {"strategy": str(e.get("strategy") or "").strip(),
                  "tactics": clean_tags(e.get("tactics")),
                  "predicted_gain": g}
    if len(per) != n_players:
        return {"ok": False, "reason": f"per_player covered {sorted(per)}", "raw": raw}

    rank = [int(x) for x in (d.get("rank_by_gain") or [])
            if str(x).lstrip("-").isdigit() and int(x) in range(n_players)]
    rank = list(dict.fromkeys(rank))
    if len(rank) != n_players:
        # Fall back to the ordering implied by the per-player gains rather than
        # discarding the prediction: `rank_by_gain` is a restatement of numbers
        # the model already gave, and dropping the row would silently bias the
        # sample toward models that format well.
        rank = sorted(range(n_players), key=lambda p: -(per[p]["predicted_gain"] or 0))

    def _num(key, cast, default=None):
        try:
            return cast(d.get(key))
        except (TypeError, ValueError):
            return default

    fr = str(d.get("focal_resource") or "").strip().title()
    fh = _num("focal_holder", int)
    return {"ok": True,
            "per_player": per,
            "rank_by_gain": rank,
            "n_trades": _num("n_trades", int),
            "joint_efficiency": _num("joint_efficiency", float),
            "focal_resource": fr if fr in N.RESOURCES else None,
            "focal_holder": fh if fh in range(n_players) else None,
            "mechanism": str(d.get("mechanism") or "").strip(),
            "raw": raw}


def predict(setting: Dict[str, Any], actor, turn_multiple: int,
            model_name: str) -> Dict[str, Any]:
    prompt = build_prompt(setting, turn_multiple, model_name)
    raw, meta = actor.act(SYSTEM, prompt)
    out = parse_prediction(raw, setting["n_players"])
    # Stored, not reconstructed later. The export is meant to be replayable
    # against other models long after this file has moved on, and a prompt
    # rebuilt from a newer `build_prompt` would silently describe a game that is
    # not the one these predictions were made about.
    out["prompt"], out["system"] = prompt, SYSTEM
    out["reasoning"] = meta.get("reasoning", "")
    out["finish_reason"] = meta.get("finish_reason")
    return out
