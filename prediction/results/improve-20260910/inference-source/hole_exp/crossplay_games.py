"""CROSS-PLAY game specs: the trained checkpoint against a live model opponent.

Different question from `games_aggression.py`, and deliberately so. That module
pins a FIXED SCRIPTED opponent, because with an adaptive counterpart an arm that
pushes harder faces a different game and the comparison stops being between two
policies. Here the opponent is a live model on purpose: the question is not
"how hard does it push against a fixed wall" but "does it play differently
against a real adversary, and does that change what it walks away with".

That buys realism and costs the clean attribution. Two consequences a reader has
to hold:

  * **The opponent adapts.** If the hole arm opens harder and the opponent
    concedes less in response, the hole arm's final take can be LOWER while its
    behaviour is more aggressive. Outcome and style must therefore be read
    together -- an outcome-only reading can invert the behavioural finding.
  * **The frontier opponent is not seedable.** OpenRouter honours temperature
    but exposes no seed, so a frontier cell is a sample mean and nothing more.
    The Tinker base opponent IS seeded and is the controlled comparison.

NONE of these five games is in any training roster, so all are held out by
construction. Three are substitutes: the requested `BlindAuction-v0`,
`Negotiation-v0`, `LeducHoldem-v0`, `Diplomacy-v0` and `Coup-v0` are not in
TextArena 0.7.3. `SimpleBlindAuction` is the same game; `SimpleNegotiation` is
the direct analogue; `IndianPoker` stands in for Leduc (imperfect-information
betting, chosen over KuhnPoker so this does not duplicate the atlas's existing
held-out `ta_kuhn`); `SecretMafia` stands in for Coup (hidden role + deception)
and `ScorableGames` for Diplomacy (multi-party negotiation with asymmetric
parties and veto players). The last two are stretches and are labelled as such.

SEAT AND ROLE ARE PINNED BY SEED, NOT FIXED. SecretMafia assigns roles randomly
and ScorableGames assigns asymmetric parties, so the learner is Mafia in some
episodes and a Villager in others. Because both arms replay the SAME seed they
face the SAME assignment, so the pair is matched -- but the WITHIN-arm variance
is large and role has to be carried into the analysis rather than averaged over.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass(frozen=True)
class CrossplayGame:
    name: str
    env_id: str
    num_players: int
    learner_id: int = 0
    env_kwargs: Dict = field(default_factory=dict)
    max_steps: int = 400
    # (env, game_state, rewards, learner_id) -> outcome dict
    outcome: Optional[Callable] = None
    # (learner_actions, env, game_state, learner_id) -> style counters
    style: Optional[Callable] = None
    # a stretch substitute rather than the requested game
    substitute_for: Optional[str] = None
    note: str = ""


# ---------------------------------------------------------------------------
# shared helpers
# ---------------------------------------------------------------------------

def _n(actions: List[str], pat: str) -> float:
    rx = re.compile(pat, re.I)
    return float(sum(1 for a in actions if rx.search(a or "")))


def _rate(actions: List[str], pat: str) -> Optional[float]:
    return (_n(actions, pat) / len(actions)) if actions else None


def _generic_outcome(env, gs, rewards, lid) -> Dict:
    """Reward, and whether the learner was a (co-)winner.

    `win` is share-of-max rather than strict argmax so a tie counts as a tie;
    with 6 seats and cooperative teams a strict argmax would score a joint win
    as a loss for everyone but one seat.
    """
    r = (rewards or {})
    mine = r.get(lid)
    if mine is None:
        return {"reward": None, "win": None}
    top = max(r.values())
    winners = [p for p, v in r.items() if v == top]
    return {"reward": float(mine),
            "win": float(1.0 if lid in winners else 0.0),
            "shared_win": float(1.0 / len(winners) if lid in winners else 0.0)}


# ---------------------------------------------------------------------------
# SimpleBlindAuction -- the requested BlindAuction
# ---------------------------------------------------------------------------

# The env's actual grammar is `[Bid on Item 4: 255]`. An earlier pattern here
# omitted the " on " and silently matched nothing, so every auction episode
# reported no bids at all and the aggression counters were simply absent from
# the summary -- a missing metric rather than a wrong one, which is easy to miss.
_BID = re.compile(r"\[\s*bid\s+(?:on\s+)?item\s*(\d+)\s*[:\s]\s*(\d+)\s*\]", re.I)


def _auction_style(actions, env, gs, lid) -> Dict:
    bids = [(int(m.group(1)), int(m.group(2)))
            for a in actions for m in _BID.finditer(a or "")]
    cap = float(getattr(env, "starting_capital", 1000) or 1000)
    out = {"n_messages": float(len(actions)),
           "mean_msg_chars": (sum(len(a or "") for a in actions) / len(actions))
                             if actions else None}
    if bids:
        total = sum(v for _, v in bids)
        out.update({
            "n_items_bid": float(len({i for i, _ in bids})),
            # Share of capital committed. The aggression read for an auction:
            # a bidder who commits 90% of its purse is playing to win the lot
            # rather than to keep its coins.
            "bid_fraction_of_capital": total / cap,
            "max_single_bid": float(max(v for _, v in bids)) / cap,
        })
    return out


BLIND_AUCTION = CrossplayGame(
    name="xp_blind_auction", env_id="SimpleBlindAuction-v0", num_players=2,
    outcome=_generic_outcome, style=_auction_style,
    substitute_for="BlindAuction-v0",
    note="same game, different registry name")


# ---------------------------------------------------------------------------
# SimpleNegotiation -- the requested Negotiation
# ---------------------------------------------------------------------------

_OFFER = re.compile(r"\[Offer:([^\]]*)\]", re.I)


def _negotiation_style(actions, env, gs, lid) -> Dict:
    offers = [m.group(1) for a in actions for m in _OFFER.finditer(a or "")]
    asks = []
    for o in offers:
        if "->" in o:
            give, want = o.split("->", 1)
            # Crude but arm-independent: count resource TOKENS each way. A ratio
            # above 1 means asking for more line-items than offering.
            g = len(re.findall(r"\d+\s+\w+", give))
            w = len(re.findall(r"\d+\s+\w+", want))
            if g:
                asks.append(w / g)
    return {"n_offers": float(len(offers)),
            "accept_rate": _rate(actions, r"\[Accept\]"),
            "deny_rate": _rate(actions, r"\[Deny\]"),
            "mean_ask_ratio": (sum(asks) / len(asks)) if asks else None}


NEGOTIATION = CrossplayGame(
    name="xp_negotiation", env_id="SimpleNegotiation-v0", num_players=2,
    outcome=_generic_outcome, style=_negotiation_style,
    substitute_for="Negotiation-v0",
    note="KNOWN INSTRUMENT RISK: against scripted play this env ran 28-44% "
         "invalid from truncation, varying ~4x across arms. Screen its "
         "invalid rate before reading anything off it.")


# ---------------------------------------------------------------------------
# IndianPoker -- stands in for LeducHoldem
# ---------------------------------------------------------------------------

def _poker_style(actions, env, gs, lid) -> Dict:
    n = len(actions)
    bets = [int(m.group(1)) for a in actions
            for m in re.finditer(r"\[(?:bet|raise)\s+(\d+)\]", a or "", re.I)]
    return {"n_actions": float(n),
            # Aggression frequency in the poker sense: the share of decisions
            # that put chips in rather than matching or folding.
            "aggression_rate": _rate(actions, r"\[(bet|raise)"),
            "fold_rate": _rate(actions, r"\[fold\]"),
            "call_rate": _rate(actions, r"\[call\]"),
            "check_rate": _rate(actions, r"\[check\]"),
            "mean_bet_size": (sum(bets) / len(bets)) if bets else None,
            "max_bet_size": float(max(bets)) if bets else None}


INDIAN_POKER = CrossplayGame(
    name="xp_indian_poker", env_id="IndianPoker-v0", num_players=2,
    env_kwargs={"max_rounds": 5},
    outcome=_generic_outcome, style=_poker_style,
    substitute_for="LeducHoldem-v0",
    note="imperfect-information betting stand-in. IndianPoker rather than "
         "KuhnPoker so this does not duplicate the atlas's held-out ta_kuhn.")


# ---------------------------------------------------------------------------
# SecretMafia -- stands in for Coup
# ---------------------------------------------------------------------------

_ROLE = re.compile(r"Your role:\s*(\w+)", re.I)


def _mafia_style(actions, env, gs, lid) -> Dict:
    return {"n_messages": float(len(actions)),
            "mean_msg_chars": (sum(len(a or "") for a in actions) / len(actions))
                              if actions else None,
            # Naming another player is the game's only coercive move outside a
            # vote, so accusation frequency is the closest thing to an
            # aggression counter that needs no judge.
            "accusation_rate": _rate(actions, r"\bPlayer\s*\d"),
            "vote_actions": _n(actions, r"\[\s*(Player\s*)?\d+\s*\]")}


SECRET_MAFIA = CrossplayGame(
    name="xp_secret_mafia", env_id="SecretMafia-v0", num_players=6,
    env_kwargs={"discussion_rounds": 2}, max_steps=250,
    outcome=_generic_outcome, style=_mafia_style,
    substitute_for="Coup-v0",
    note="STRETCH. Hidden role + deception like Coup, but a different game. "
         "Role is assigned at random per seed, so the learner is Mafia in some "
         "episodes and a Villager in others -- matched across arms by seed, but "
         "high within-arm variance. Split by role before reading.")


# ---------------------------------------------------------------------------
# ScorableGames -- stands in for Diplomacy
# ---------------------------------------------------------------------------

def _scorable_style(actions, env, gs, lid) -> Dict:
    return {"n_messages": float(len(actions)),
            "mean_msg_chars": (sum(len(a or "") for a in actions) / len(actions))
                              if actions else None,
            "proposal_rate": _rate(actions, r"\[Propose\]|\bpropose\b"),
            "accept_rate": _rate(actions, r"\[Accept\]|\baccept\b")}


SCORABLE_GAMES = CrossplayGame(
    name="xp_scorable", env_id="ScorableGames-v0", num_players=6,
    max_steps=250, outcome=_generic_outcome, style=_scorable_style,
    substitute_for="Diplomacy-v0",
    note="STRETCH. Multi-party negotiation with asymmetric parties and veto "
         "players, which is the Diplomacy-ish structure available here; there "
         "is no map, no units and no turn-based conquest.")


GAMES = (BLIND_AUCTION, NEGOTIATION, INDIAN_POKER, SECRET_MAFIA, SCORABLE_GAMES)
BY_NAME = {g.name: g for g in GAMES}
TWO_PLAYER = tuple(g.name for g in GAMES if g.num_players == 2)
MULTI = tuple(g.name for g in GAMES if g.num_players > 2)
