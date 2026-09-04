#!/usr/bin/env python
"""Prompt -> structured view, so a browser can draw a board instead of a wall
of prose.

WHY PARSE RATHER THAN CHANGE THE ENGINES. The cells are the measurement
instrument. `run_referee_crossplay.py` and `referee_repeat.py` drive the same
`game.run(ask, seed, arm)` and compare human numbers against model numbers
taken from byte-identical prompts; adding a structured-state return path to
the engines would fork the instrument and quietly invalidate that comparison.
The prompts are built from fixed format strings and are deterministic, so a
parser in the web layer gets the same information at zero cost to the cells.
`test_views.py` asserts each adapter against prompts pulled live out of the
engines, which is what keeps this honest if a format string ever moves.

THE RULE EVERY ADAPTER FOLLOWS. A view may re-present ONLY what is already in
the prompt, and it must present every option the prompt offers with equal
weight. Both halves matter and the second is the one that is easy to get
wrong: if the battleship call widget renders the truthful call as a primary
button and the others as small grey ones, the UI has told the player there is
something transgressive about the other two -- which is the experiment
answering its own question. The widgets below therefore style every legal
token identically and pre-select nothing.

The same rule decides where a board stops helping. It may do arithmetic the
player was handed the formula for (a duty at two rates, a word's score from a
published letter table); it may not do arithmetic over anything the player was
not told, and it may not narrow a dial to the range the honest move lives in.
A dial that would not travel past the sustainable catch, or a lexicon filtered
to the words your rack spells, would be the board playing the game.

FAILING IS FINE. An adapter returns None when it cannot parse with
confidence, and the client falls back to the plain text composer. A view that
guesses is worse than no view: it would draw a board that disagrees with the
prompt the engine actually sent.
"""
from __future__ import annotations

from typing import Callable, Dict, Optional

from . import (auction, battleship, blindauction, commons, depot, duel,      # noqa: F401
               estate, exchange, hanabi, harbor, icebound, invoice, ipd3,
               kuhn, letterauction, liarsdice, negotiation, pubgoods,
               sevenseal, sidebar, sonar, vaults, winasmuch)

# game id -> callable(phase, prompt) -> dict | None
#
# THE 23 BASE GAMES ALL HAVE A BOARD. `configs/base_roster.toml` is the list
# and `test_views.py::gate_covered` asserts this dict covers every name on it,
# so a game added to the roster without a board fails the suite rather than
# quietly dropping its players onto the text composer.
ADAPTERS: Dict[str, Callable[[str, str], Optional[dict]]] = {
    # -- hand-built referee cells
    "ref_estate": estate.view,
    "ref_sidebar": sidebar.view,
    "ref_exchange": exchange.view,
    "ref_hanabi": hanabi.view,
    "ref_auction": auction.view,
    "ref_commons": commons.view,
    "ref_invoice": invoice.view,
    # -- model-written cells
    "gen_seven_seal": sevenseal.view,
    "gen_quiet_sonar": sonar.view,
    "gen_icebound": icebound.view,
    "gen_sovereign_vaults": vaults.view,
    "gen_frontline_depot": depot.view,
    "gen_harbor_customs": harbor.view,
    # -- TextArena ports
    "ta_ipd": duel.view,
    "ta_staghunt": duel.view,
    "ta_ipd3": ipd3.view,
    "ta_pubgoods": pubgoods.view,
    "ta_winasmuch": winasmuch.view,
    "ta_liarsdice": liarsdice.view,
    "ta_kuhn": kuhn.view,
    "ta_negotiation": negotiation.view,
    "ta_blindauction": blindauction.view,
    "ta_letterauction": letterauction.view,
    # -- off the base roster, kept because the board already existed and the
    # cell is still reachable by id (see catalog.DUPLICATES).
    "ref_battleship": battleship.view,
}

# What the client is told a game supports before it starts, so the catalogue
# can mark which cells have a board and which are still text.
AIDED = tuple(sorted(ADAPTERS))


def build(game_id: str, phase: str, prompt: str) -> Optional[dict]:
    """Structured view for one decision, or None to fall back to text."""
    fn = ADAPTERS.get(game_id)
    if fn is None:
        return None
    try:
        v = fn(phase, prompt or "")
    except Exception:
        # A parser crash must never take the session with it -- the player
        # keeps playing through the composer and the record says `source:
        # text` for that move.
        return None
    if v and "kind" not in v:
        return None
    return v


KINDS = (
    "estate_settle", "sidebar_msg", "sidebar_bet", "exchange_offer",
    "exchange_build", "exchange_accept", "hanabi_turn", "auction_bid",
    "commons_catch", "invoice_job", "sevenseal_report", "sonar_hide",
    "sonar_fire", "sonar_claim", "icebound_pledge", "icebound_act",
    "vaults_declare", "vaults_deposit", "depot_strike", "depot_guard",
    "harbor_declare", "harbor_route", "duel_move", "ipd3_line", "ipd3_table",
    "pubgoods_envelope", "pubgoods_receipt", "winasmuch_talk",
    "winasmuch_pick", "liarsdice_bid", "liarsdice_count", "kuhn_act",
    "kuhn_show", "negotiation_trade", "blind_sealed", "blind_note",
    "letter_bid", "letter_word", "battleship_fire", "battleship_call",
)
