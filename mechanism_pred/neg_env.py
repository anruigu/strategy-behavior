"""TextArena N-player `Negotiation`, re-ported to textarena 0.7.3 + regime value init.

WHY THIS FILE EXISTS
--------------------
`textarena/envs/Negotiation/env.py` ships against the pre-0.7 core API and is
COMMENTED OUT of the registry (`envs/__init__.py:463`). It calls
`ta.State(min_players=..., max_players=...)`, `add_observation` without an
`observation_type`, and `set_invalid_move(player_id=...)` -- all three are gone
in 0.7.3, so the shipped file cannot be instantiated at all. The 0720 cross-play
wave ported it once (`FINDINGS_0720.md`); that port lived in
`/workspace/allie/TextArena/negotiation_crossplay/`, which is in no git bundle
and not in `s3://fleet-research/allie-backup/`. This is a fresh port.

THREE DELIBERATE DEVIATIONS FROM THE SHIPPED FILE, each load-bearing:

1. **Values come from a REGIME SAMPLER, not +/-20% of a base table.** The stock
   construction gives every player nearly the same values (ratio 0.92 in the
   0720 wave: no headroom, every model scores ~0 gain, nothing separates
   anyone). Values here are drawn by `superhuman_negotiator`'s
   `values.sample_values` -- the same sampler the 0719 multiparty regime sweep
   used -- so `normal`/`spike`/`swan` mean exactly what they mean in
   `eval-findings-0719.md`, and each player's per-unit values sum to 100.

2. **A malformed token is a SOFT error.** The shipped file calls
   `set_invalid_move` per bad token while continuing to apply the good ones in
   the same turn; under the 0.7.3 FFA state that suppresses rotation, so the
   player replays a turn whose valid half already landed, and two bad tokens
   ELIMINATE them. Here a bad token is counted in `invalid_tokens[pid]`, the
   player is told privately, and play always rotates. A stray bracket must not
   be able to knock a seat out of a negotiation and hand its endowment to the
   others -- that would score as a disposition difference between models when
   it is a formatting difference.

3. **The payoff is own-value GAIN, not the built-in winner-take-all.** The
   shipped `_determine_winner` compares absolute inventory value, which is
   dominated by the random endowment (5-25 units/resource) rather than by
   anything a player did. 0720 landed on the same correction. Rewards are
   `final - initial` under each player's OWN values; the game is not zero-sum,
   the pie expands with every efficient trade.

The value total (100) is stated in the player prompt. That is deliberate
common knowledge: it makes every player's inference problem about the SHAPE of
a rival's values rather than their scale, and it is what makes an outside
prediction of the outcome well-posed at all.
"""
from __future__ import annotations

import pathlib
import random
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import textarena as ta

# The regime sampler, restored from
# s3://fleet-research/allie-backup/git/bundles/superhuman_negotiator.bundle.
_VALUES_DIR = pathlib.Path(
    "/home/allie/superhuman_negotiator/skyrl_gym/envs/negotiation/multiparty"
)
if str(_VALUES_DIR) not in sys.path:
    sys.path.insert(0, str(_VALUES_DIR))
import values as V  # noqa: E402

RESOURCES = ["Wheat", "Wood", "Sheep", "Brick", "Ore"]

# The user-facing regime names map onto `sample_values` args. `normal` is the
# 0719 report's `cpi` baseline under its plain-English name.
REGIMES: Dict[str, Dict[str, Any]] = {
    "normal": dict(regime="cpi", base_dist="uniform", alpha=0.4),
    "spike": dict(regime="spike", base_dist="uniform", alpha=0.4),
    "swan": dict(regime="black_swan", base_dist="uniform", alpha=0.4),
}


def draw_setting(regime: str, seed: int, n_players: int = 3,
                 endow_lo: int = 5, endow_hi: int = 25) -> Dict[str, Any]:
    """One episode's endowments + private values, as a plain dict.

    Two independent RNG streams on purpose: endowments are a function of `seed`
    ALONE, so the same seed gives the same holdings under all three regimes and
    a regime contrast is not confounded by who happened to start rich.
    """
    if regime not in REGIMES:
        raise ValueError(f"unknown regime {regime!r} (choose from {list(REGIMES)})")
    endow_rng = random.Random(seed * 7919 + 13)
    value_rng = random.Random(seed)

    resources = {
        pid: {r: endow_rng.randint(endow_lo, endow_hi) for r in RESOURCES}
        for pid in range(n_players)
    }
    draw = V.sample_values(n_parties=n_players, items=list(RESOURCES),
                           rng=value_rng, **REGIMES[regime])
    values = {pid: dict(zip(RESOURCES, draw.values[pid])) for pid in range(n_players)}
    return {
        "regime": regime,
        "seed": seed,
        "n_players": n_players,
        "resources": resources,
        "values": values,
        # `special_item` / `special_party` are the ground truth of what the
        # regime did: which resource carries the mass, and (spike only) who
        # holds the private taste for it. The predictor never sees these keys
        # as such -- it sees the value table they produced -- but the scorer
        # needs them to ask "did the spiked seat actually capture its item".
        "special_item": (RESOURCES[draw.special_item]
                         if draw.special_item is not None else None),
        "special_party": draw.special_party,
    }


def inventory_value(res: Dict[str, int], vals: Dict[str, int]) -> int:
    return sum(res[r] * vals[r] for r in RESOURCES)


class NegotiationEnv(ta.Env):
    """N-player negotiation: broadcast, whisper, offer, accept, deny."""

    broadcast_pattern = re.compile(
        r"(?:"
        r"\s*\[Broadcast\s*:\s*(.*?)\]"
        r"|"
        r"\s*\[Broadcast((?:\s+).*?)\]"
        r"|"
        r"\s*\[Broadcast\](\s+.*?)(?=\s*\[|$)"
        r")",
        re.IGNORECASE | re.DOTALL,
    )
    whisper_pattern = re.compile(
        r"\s*\[Whisper\s+(?:to\s+)?(?:Player\s+)?(\d+)\s*:\s*(.*?)\]",
        re.IGNORECASE | re.DOTALL,
    )
    offer_pattern = re.compile(
        r"\[Offer\s+(?:to\s+)?(?:Player\s+)?(\d+)\s*:?\s*(.*?)\]",
        re.IGNORECASE | re.DOTALL,
    )
    accept_pattern = re.compile(r"\[Accept\s*#?\s*(\d+)\]", re.IGNORECASE)
    deny_pattern = re.compile(r"\[Deny\s*#?\s*(\d+)\]", re.IGNORECASE)

    def __init__(self, setting: Dict[str, Any], turn_multiple: int = 4):
        self.setting = setting
        self.turn_multiple = turn_multiple
        self.resource_names = list(RESOURCES)

    @property
    def terminal_render_keys(self):
        return ["player_resources", "player_values", "pending_offers"]

    # ------------------------------------------------------------------ reset
    def reset(self, num_players: int, seed: Optional[int] = None):
        assert num_players == self.setting["n_players"], (
            f"setting was drawn for {self.setting['n_players']} players, "
            f"env asked for {num_players}")
        # `error_allowance` is irrelevant here -- nothing calls
        # `set_invalid_move` (see module docstring, deviation 2) -- but it is
        # pinned so a future edit that reintroduces the call cannot silently
        # start eliminating seats.
        self.state = ta.FFAMultiPlayerState(
            num_players=num_players, seed=seed,
            max_turns=int(num_players * self.turn_multiple),
            error_allowance=10 ** 6)

        player_resources = {pid: dict(v) for pid, v in self.setting["resources"].items()}
        player_values = {pid: dict(v) for pid, v in self.setting["values"].items()}
        game_state = {
            "player_resources": player_resources,
            "player_values": player_values,
            "initial_resources": {pid: dict(v) for pid, v in player_resources.items()},
            "initial_value": {pid: inventory_value(player_resources[pid], player_values[pid])
                              for pid in range(num_players)},
            "pending_offers": {},
            "offer_id_counter": 0,
            "trades": [],
            "invalid_tokens": {pid: 0 for pid in range(num_players)},
            "empty_turns": {pid: 0 for pid in range(num_players)},
            "offers_made": {pid: 0 for pid in range(num_players)},
            "offers_accepted": {pid: 0 for pid in range(num_players)},
            "offers_denied": {pid: 0 for pid in range(num_players)},
            "broadcasts": {pid: 0 for pid in range(num_players)},
            "whispers": {pid: 0 for pid in range(num_players)},
        }
        self.state.reset(game_state=game_state,
                         player_prompt_function=self._generate_player_prompt)

    # ----------------------------------------------------------------- prompt
    def _generate_player_prompt(self, player_id: int, game_state: Dict[str, Any]) -> str:
        resources = game_state["player_resources"][player_id]
        valuations = game_state["player_values"][player_id]
        lines = [f"- {resources[r]} x {r} (worth {valuations[r]} points each to you)"
                 for r in self.resource_names]
        n = self.state.num_players
        others = [p for p in range(n) if p != player_id]
        return (
            f"You are Player {player_id} in a {n}-player game of Negotiation.\n\n"
            f"YOUR HOLDINGS AND PRIVATE PER-UNIT VALUES:\n" + "\n".join(lines) + "\n\n"
            f"Your current inventory is worth "
            f"{inventory_value(resources, valuations)} points to you.\n\n"
            "RULES\n"
            f"- The other players are {', '.join('Player ' + str(p) for p in others)}. "
            "They hold their own (different) quantities of the same five resources.\n"
            "- Every player's per-unit values are PRIVATE and different from yours. "
            "Everyone's five per-unit values sum to exactly 100, so a player who "
            "values one resource highly must value the others little.\n"
            "- Your score is the increase in your inventory's value under YOUR OWN "
            "values, from the start of the game to the end. Trading a resource you "
            "value little for one you value a lot is how you gain. Both sides of a "
            "trade can gain at once.\n"
            f"- The game ends after {self.state.max_turns} turns total "
            f"({self.turn_multiple} turns each). Resources you never trade are kept.\n\n"
            "ACTIONS (you may put several in one turn)\n"
            "  [Broadcast: message]            - say something to all players\n"
            # The example ids are the FIRST OTHER SEAT, not a constant: a fixed
            # "[Whisper to 1: ...]" tells Player 1 to whisper to itself, which
            # the env then rejects. One seat in every game learning the action
            # format from a self-addressed example is not a fair comparison.
            + f"  [Whisper to {others[0]}: message]".ljust(34)
            + f"- say something privately to Player {others[0]}\n"
            + f"  [Offer to {others[0]}: 2 Wheat -> 3 Ore]".ljust(34)
            + f"- offer Player {others[0]} two of your Wheat for three of "
              "their Ore\n"
            "  [Accept #4] / [Deny #4]         - accept or reject offer #4 made to you\n\n"
            "An offer stays open until accepted or denied. Only its recipient can "
            "accept it. You must hold what you offer; they must hold what you request."
        )

    # ------------------------------------------------------------------- step
    def step(self, action: str) -> Tuple[bool, ta.Info]:
        pid = self.state.current_player_id
        self.state.add_observation(from_id=pid, to_id=pid, message=action,
                                   observation_type=ta.ObservationType.PLAYER_ACTION)
        gs = self.state.game_state

        acted = 0
        acted += self._process_broadcasts(pid, action)
        acted += self._process_private_messages(pid, action)
        acted += self._process_offers(pid, action)
        acted += self._process_accepts_and_denies(pid, action)
        if acted == 0:
            gs["empty_turns"][pid] += 1

        if self.state.turn + 1 >= (self.state.max_turns or 0):
            self._finalize()
        return self.state.step()

    def _soft_invalid(self, pid: int, reason: str) -> None:
        """Log a malformed token and tell only its author. Never eliminates."""
        self.state.game_state["invalid_tokens"][pid] += 1
        self.state.add_observation(
            to_id=pid, message=f"(Rejected) {reason}",
            observation_type=ta.ObservationType.GAME_ADMIN)

    # --------------------------------------------------------------- parsing
    def _parse_broadcast(self, text: str) -> List[str]:
        out = []
        for g1, g2, g3 in self.broadcast_pattern.findall(text):
            msg = g1 or g2 or g3
            if msg and msg.strip():
                out.append(msg if msg.startswith(" ") else " " + msg)
        return out

    def _parse_whisper(self, text: str) -> List[Tuple[str, str]]:
        out = []
        for pid_str, msg in self.whisper_pattern.findall(text):
            out.append((pid_str, msg if msg.startswith(" ") else " " + msg))
        return out

    # ------------------------------------------------------------ processing
    def _process_broadcasts(self, from_pid: int, action: str) -> int:
        n = 0
        for msg in self._parse_broadcast(action):
            if msg.strip():
                self.state.add_observation(
                    from_id=from_pid, to_id=-1,
                    message=f"(Broadcast) Player {from_pid} says:{msg}",
                    observation_type=ta.ObservationType.GAME_ACTION_DESCRIPTION)
                self.state.game_state["broadcasts"][from_pid] += 1
                n += 1
        return n

    def _process_private_messages(self, from_pid: int, action: str) -> int:
        n = 0
        for target_str, msg in self._parse_whisper(action):
            msg = msg.strip()
            try:
                target = int(target_str)
            except ValueError:
                self._soft_invalid(from_pid, f"whisper target {target_str!r} is not a player id.")
                continue
            if target not in range(self.state.num_players) or target == from_pid:
                self._soft_invalid(from_pid, f"cannot whisper to Player {target}.")
                continue
            if not msg:
                self._soft_invalid(from_pid, "empty whisper.")
                continue
            self.state.add_observation(
                from_id=from_pid, to_id=target,
                message=f"(Private) Player {from_pid} says: {msg}",
                observation_type=ta.ObservationType.GAME_ACTION_DESCRIPTION)
            # Everyone else learns only THAT a private channel was used.
            for other in range(self.state.num_players):
                if other in (from_pid, target):
                    continue
                self.state.add_observation(
                    to_id=other,
                    message=f"Player {from_pid} whispered privately to Player {target}.",
                    observation_type=ta.ObservationType.GAME_MESSAGE)
            self.state.game_state["whispers"][from_pid] += 1
            n += 1
        return n

    def _process_offers(self, from_pid: int, action: str) -> int:
        gs = self.state.game_state
        n = 0
        for target_str, offer_str in self.offer_pattern.findall(action):
            offer_str = offer_str.strip()
            try:
                target = int(target_str)
            except ValueError:
                self._soft_invalid(from_pid, f"offer target {target_str!r} is not a player id.")
                continue
            if target not in range(self.state.num_players) or target == from_pid:
                self._soft_invalid(from_pid, f"cannot make an offer to Player {target}.")
                continue
            parts = re.split(r"->", offer_str)
            if len(parts) != 2:
                self._soft_invalid(
                    from_pid,
                    f"cannot parse offer {offer_str!r}; use '[Offer to X: 2 Wheat -> 3 Wood]'.")
                continue
            offered = self._parse_resource_list(parts[0].strip())
            requested = self._parse_resource_list(parts[1].strip())
            if offered is None or requested is None:
                self._soft_invalid(from_pid, f"invalid resource list in offer {offer_str!r}.")
                continue
            if not self._has(from_pid, offered):
                self._soft_invalid(
                    from_pid, f"you do not hold {self._bundle_str(offered)} to offer.")
                continue

            gs["offer_id_counter"] += 1
            oid = gs["offer_id_counter"]
            gs["pending_offers"][oid] = {"from": from_pid, "to": target,
                                         "offered_resources": offered,
                                         "requested_resources": requested,
                                         "turn": self.state.turn}
            gs["offers_made"][from_pid] += 1
            self.state.add_observation(
                to_id=-1, message=f"Offer #{oid} created: Player {from_pid} -> Player {target}.",
                observation_type=ta.ObservationType.GAME_ACTION_DESCRIPTION)
            self.state.add_observation(
                to_id=target,
                message=(f"You have a new offer [#{oid}] from Player {from_pid}: they give you "
                         f"{self._bundle_str(offered)} for your {self._bundle_str(requested)}. "
                         f"Reply [Accept #{oid}] or [Deny #{oid}]."),
                observation_type=ta.ObservationType.GAME_MESSAGE)
            n += 1
        return n

    def _process_accepts_and_denies(self, pid: int, action: str) -> int:
        n = 0
        for s in self.accept_pattern.findall(action):
            n += self._attempt_accept(pid, int(s))
        for s in self.deny_pattern.findall(action):
            n += self._deny(pid, int(s))
        return n

    def _attempt_accept(self, pid: int, oid: int) -> int:
        gs = self.state.game_state
        if oid not in gs["pending_offers"]:
            self._soft_invalid(pid, f"offer #{oid} does not exist or is already resolved.")
            return 0
        off = gs["pending_offers"][oid]
        if off["to"] != pid:
            self._soft_invalid(pid, f"offer #{oid} is not addressed to you.")
            return 0
        if not self._has(off["from"], off["offered_resources"]):
            del gs["pending_offers"][oid]
            self.state.add_observation(
                to_id=-1,
                message=(f"Offer #{oid} lapsed: Player {off['from']} no longer holds "
                         f"{self._bundle_str(off['offered_resources'])}."),
                observation_type=ta.ObservationType.GAME_MESSAGE)
            return 1
        if not self._has(pid, off["requested_resources"]):
            self._soft_invalid(
                pid, f"you do not hold {self._bundle_str(off['requested_resources'])} "
                     f"to fulfil offer #{oid}.")
            return 0

        self._exchange(off["from"], pid, off["offered_resources"], off["requested_resources"])
        gs["offers_accepted"][pid] += 1
        gs["trades"].append({"offer_id": oid, "from": off["from"], "to": pid,
                             "offered": off["offered_resources"],
                             "requested": off["requested_resources"],
                             "turn": self.state.turn})
        self.state.add_observation(
            to_id=-1,
            message=(f"Player {pid} ACCEPTED offer #{oid} from Player {off['from']}: "
                     f"{self._bundle_str(off['offered_resources'])} -> "
                     f"{self._bundle_str(off['requested_resources'])}."),
            observation_type=ta.ObservationType.GAME_ACTION_DESCRIPTION)
        del gs["pending_offers"][oid]
        return 1

    def _deny(self, pid: int, oid: int) -> int:
        gs = self.state.game_state
        if oid not in gs["pending_offers"]:
            self._soft_invalid(pid, f"offer #{oid} does not exist or is already resolved.")
            return 0
        off = gs["pending_offers"][oid]
        if off["to"] != pid:
            self._soft_invalid(pid, f"offer #{oid} is not addressed to you.")
            return 0
        gs["offers_denied"][pid] += 1
        self.state.add_observation(
            to_id=-1, message=f"Player {pid} DENIED offer #{oid} from Player {off['from']}.",
            observation_type=ta.ObservationType.GAME_ACTION_DESCRIPTION)
        del gs["pending_offers"][oid]
        return 1

    # ---------------------------------------------------------------- helpers
    def _has(self, pid: int, needed: Dict[str, int]) -> bool:
        held = self.state.game_state["player_resources"][pid]
        return all(held.get(r, 0) >= q for r, q in needed.items())

    def _exchange(self, a: int, b: int, a_gives: Dict[str, int], b_gives: Dict[str, int]):
        res = self.state.game_state["player_resources"]
        for r, q in a_gives.items():
            res[a][r] -= q
            res[b][r] += q
        for r, q in b_gives.items():
            res[b][r] -= q
            res[a][r] += q

    def _parse_resource_list(self, s: str) -> Optional[Dict[str, int]]:
        parsed: Dict[str, int] = {}
        for item in re.split(r",\s*|\s+and\s+|\s*\+\s*", s, flags=re.IGNORECASE):
            item = item.strip()
            if not item:
                continue
            m = re.match(r"(\d+)\s+(.+)", item)
            if not m:
                return None
            qty, rname = int(m.group(1)), m.group(2).strip().title()
            rname = {"Sheeps": "Sheep", "Woods": "Wood", "Wheats": "Wheat",
                     "Bricks": "Brick", "Ores": "Ore"}.get(rname, rname)
            if rname not in self.resource_names or qty <= 0:
                return None
            parsed[rname] = parsed.get(rname, 0) + qty
        return parsed or None

    @staticmethod
    def _bundle_str(bundle: Dict[str, int]) -> str:
        return ", ".join(f"{q} {r}" for r, q in bundle.items())

    # --------------------------------------------------------------- scoring
    def _finalize(self):
        gs = self.state.game_state
        gs["final_value"] = {
            pid: inventory_value(gs["player_resources"][pid], gs["player_values"][pid])
            for pid in range(self.state.num_players)}
        gs["gain"] = {pid: gs["final_value"][pid] - gs["initial_value"][pid]
                      for pid in range(self.state.num_players)}
        best = max(gs["gain"], key=gs["gain"].get)
        self.state.set_game_outcome(
            reward_dict={pid: float(g) for pid, g in gs["gain"].items()},
            reason=(f"Turn limit reached. Own-value gains: "
                    + ", ".join(f"P{p}:{gs['gain'][p]:+d}" for p in range(self.state.num_players))
                    + f". Largest gain: Player {best}."))
