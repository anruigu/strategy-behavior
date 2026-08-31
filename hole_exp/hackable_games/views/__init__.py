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

FAILING IS FINE. An adapter returns None when it cannot parse with
confidence, and the client falls back to the plain text composer. A view that
guesses is worse than no view: it would draw a board that disagrees with the
prompt the engine actually sent.
"""
from __future__ import annotations

from typing import Callable, Dict, Optional

from . import battleship, hanabi, sidebar, sonar   # noqa: F401

# game id -> callable(phase, prompt) -> dict | None
ADAPTERS: Dict[str, Callable[[str, str], Optional[dict]]] = {
    "ref_battleship": battleship.view,
    "ref_sidebar": sidebar.view,
    "ref_hanabi": hanabi.view,
    "gen_quiet_sonar": sonar.view,
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
