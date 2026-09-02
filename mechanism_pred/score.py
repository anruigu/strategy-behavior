"""Score a forecast against a realization, and build the two reference forecasts.

Everything that can produce a forecast -- the model's prediction, the
first-best analytic baseline, and ANOTHER realization of the same setting --
is reduced to one shape and run through the same `compare`. That is what makes
the ceiling meaningful: the number that says "realization A predicts
realization B this well" is computed by the identical code path as the number
that says "the model predicts realization B this well", so the ratio between
them is not an artefact of two different scorers.
"""
from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List, Optional

import neg_env as N
from metrics import achievable
from tags import jaccard


# ------------------------------------------------------------------ forecasts
def forecast_from_prediction(pred: Dict[str, Any], n: int) -> Dict[str, Any]:
    per = pred["per_player"]
    return {"gain": {p: per[p]["predicted_gain"] for p in range(n)},
            "rank": pred["rank_by_gain"],
            "n_trades": pred["n_trades"],
            "efficiency": pred["joint_efficiency"],
            "focal_resource": pred["focal_resource"],
            "focal_holder": pred["focal_holder"],
            "tactics": {p: per[p]["tactics"] for p in range(n)}}


def forecast_from_episode(m: Dict[str, Any], tags: Dict[int, List[str]],
                          n: int) -> Dict[str, Any]:
    # `tactics=None` when this episode went unannotated, so `compare` scores its
    # tag overlap as UNMEASURED rather than as zero. An empty tag dict scored as
    # a forecast of "no tactics" would read as a realization that disagreed with
    # every other realization, which is how the pilot's failed judge call turned
    # into a tactic ceiling of 0.000.
    return {"gain": {p: float(m["gain"][p]) for p in range(n)},
            "rank": m["rank_by_gain"],
            "n_trades": m["n_trades"],
            "efficiency": m["efficiency"],
            "focal_resource": m["focal_resource"],
            "focal_holder": m["focal_holder"],
            "tactics": ({p: list(tags.get(p, [])) for p in range(n)}
                        if tags else None)}


def first_best_forecast(setting: Dict[str, Any]) -> Dict[str, Any]:
    """RANKING null: assume the efficient allocation simply happens, uncompensated.

    Every unit goes to whoever values it most. Efficiency is 1.0 by
    construction and each seat's gain is fully determined by the value table,
    so a model that cannot out-rank this is not reasoning about negotiation --
    it is reading off an argmax, which needs no model of the players.

    Read its ORDERING, not its levels. Because nobody is compensated for the
    resources they hand over, a seat with broad middling values is scored as
    losing its whole endowment: levels come out large and negative, which no
    voluntary trade would ever produce. That makes its `gain_nmae` meaningless
    and is why `no_trade_forecast` exists beside it as the level null.
    """
    n = setting["n_players"]
    a = achievable(setting)
    best, tot = a["best_holder"], a["totals"]
    gain = {}
    for p in range(n):
        final = sum(tot[r] * setting["values"][p][r] for r in N.RESOURCES if best[r] == p)
        gain[p] = float(final - N.inventory_value(setting["resources"][p], setting["values"][p]))
    moved = {r: tot[r] - setting["resources"][best[r]][r] for r in N.RESOURCES}
    focal = max(N.RESOURCES, key=lambda r: moved[r])
    # No tactic claim: an allocation rule says nothing about how anyone behaves,
    # and scoring its silence as a wrong prediction would flatter the models.
    return {"gain": gain,
            "rank": sorted(range(n), key=lambda p: -gain[p]),
            "n_trades": None, "efficiency": 1.0,
            "focal_resource": focal, "focal_holder": best[focal],
            "tactics": None}


def no_trade_forecast(setting: Dict[str, Any]) -> Dict[str, Any]:
    """LEVEL null: assume the negotiation achieves nothing.

    Every gain zero, no trades, efficiency zero. This is the floor a predicted
    magnitude has to beat to mean anything: a model that guesses small numbers
    everywhere can post a respectable `gain_nmae` in a wave where the seats
    happen to trade little, and only this row shows that up. It deliberately
    supplies no ranking (all gains tie), so `top1` and `pairwise_acc` are
    undefined for it rather than scored at chance.
    """
    n = setting["n_players"]
    return {"gain": {p: 0.0 for p in range(n)}, "rank": None,
            "n_trades": 0, "efficiency": 0.0,
            "focal_resource": None, "focal_holder": None,
            "tactics": {p: ["passive"] for p in range(n)}}


# -------------------------------------------------------------------- scoring
def _pairwise_acc(pred_gain: Dict[int, Optional[float]],
                  true_gain: Dict[int, float], n: int) -> Optional[float]:
    """Fraction of player pairs whose gain ordering is called correctly.

    Chance is 0.5, and unlike Spearman on n=3 it degrades gracefully when the
    model leaves one gain unfilled. Two asymmetries, both deliberate:

    - Pairs the REALIZATION ties are dropped. No forecast can be right about
      them, so scoring them would just add noise proportional to how often the
      game happens to end level.
    - Pairs the FORECAST ties score 0.5, rather than being dropped. Dropping
      them would let a model that predicts identical gains for everybody sit
      out the metric entirely and post a `--`, which reads as "not measured"
      when it should read as "hedged, and hedging is worth chance".
    """
    hit = tot = 0.0
    for a, b in combinations(range(n), 2):
        if true_gain[a] == true_gain[b]:
            continue
        pa, pb = pred_gain.get(a), pred_gain.get(b)
        if pa is None or pb is None:
            continue
        tot += 1
        hit += 0.5 if pa == pb else float((pa > pb) == (true_gain[a] > true_gain[b]))
    return hit / tot if tot else None


def compare(fc: Dict[str, Any], m: Dict[str, Any], tags: Dict[int, List[str]],
            n: int, achievable_gain: float) -> Dict[str, Any]:
    true_gain = {p: float(m["gain"][p]) for p in range(n)}
    pg = fc["gain"]

    gains = [abs(pg[p] - true_gain[p]) for p in range(n) if pg.get(p) is not None]
    nmae = (sum(gains) / len(gains) / achievable_gain
            if gains and achievable_gain > 0 else None)

    out = {
        "top1": (int(fc["rank"][0] == m["top_gainer"])
                 if fc.get("rank") else None),
        "pairwise_acc": _pairwise_acc(pg, true_gain, n),
        "gain_nmae": nmae,
        "eff_err": (abs(fc["efficiency"] - m["efficiency"])
                    if fc.get("efficiency") is not None else None),
        "trade_err": (abs(fc["n_trades"] - m["n_trades"])
                      if fc.get("n_trades") is not None else None),
        "focal_hit": (int(fc["focal_resource"] == m["focal_resource"])
                      if fc.get("focal_resource") and m["focal_resource"] else None),
        "focal_holder_hit": (int(fc["focal_holder"] == m["focal_holder"])
                             if fc.get("focal_holder") is not None
                             and m["focal_holder"] is not None else None),
    }
    if tags and fc.get("tactics") is not None:
        js = [jaccard(fc["tactics"].get(p, []), tags.get(p, [])) for p in range(n)
              if p in tags]
        out["tag_jaccard"] = sum(js) / len(js) if js else None
    else:
        out["tag_jaccard"] = None
    return out


def ceiling(episodes: List[Dict[str, Any]], tagsets: List[Dict[int, List[str]]],
            n: int, achievable_gain: float) -> Optional[Dict[str, Any]]:
    """How well one realization of this setting predicts another.

    Without this the headline is uninterpretable: a low prediction score can
    mean the model reasons badly OR that the game is close to a coin flip given
    the setting, and those call for opposite follow-ups. Both orderings of each
    pair are scored, because `compare` is not symmetric (nmae is, `top1` is not
    when gains tie).
    """
    if len(episodes) < 2:
        return None
    rows = []
    for i, j in combinations(range(len(episodes)), 2):
        for a, b in ((i, j), (j, i)):
            fc = forecast_from_episode(episodes[a]["metrics"], tagsets[a], n)
            rows.append(compare(fc, episodes[b]["metrics"], tagsets[b], n,
                                achievable_gain))
    keys = rows[0].keys()
    return {k: _mean([r[k] for r in rows]) for k in keys}


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None
