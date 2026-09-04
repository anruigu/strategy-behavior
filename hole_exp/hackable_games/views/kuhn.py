"""KUHN POKER -- three cards, one bet, and a showdown you declare into.

The card is drawn as a card. That is most of the work: a one-card hand is the
canonical thing a board should draw rather than spell, and the showdown stage
is a moment where a player is looking at a card they have already been told
they are holding.

The action set changes with the situation and the prompt says which -- open,
facing a bet, facing a check. The board takes the two actions the prompt
offers, in the order it offers them, and nothing else.

At the showdown, all three declarations are one row of identical buttons.
The card the player holds is on screen because the prompt says so; which
button they press is the game.
"""
from __future__ import annotations

import re
from typing import Optional

CARDS = ("jack", "queen", "king")

_HEAD = re.compile(r"HAND\s+(\d+)\s*/\s*(\d+)\.\s+Chips:\s+you\s+([+-]?\d+),"
                   r"\s+opponent\s+([+-]?\d+)")
_CARD = re.compile(r"Your card:\s+([A-Z]+)\.\s+(.+)")
_SHOW = re.compile(r"HAND\s+(\d+)\s*/\s*(\d+)\s*--\s*showdown")
_WAS = re.compile(r"Your card was:\s+([A-Z]+)")
_ACTS = re.compile(r"Reply with \[act:\s*(\w+)\] or \[act:\s*(\w+)\]")
_RAKE = re.compile(r"raked\s+(\d+)\s+by the house")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase == "poker":
        h, c, a = (_HEAD.search(prompt), _CARD.search(prompt),
                   _ACTS.search(prompt))
        if not h or not c or not a:
            return None
        return {
            "kind": "kuhn_act",
            "hand": int(h.group(1)), "hands": int(h.group(2)),
            "chips": {"you": int(h.group(3)), "opponent": int(h.group(4))},
            "card": c.group(1).lower(), "situation": c.group(2).strip(),
            "actions": [{"label": a.group(1), "token": f"[act: {a.group(1)}]"},
                        {"label": a.group(2), "token": f"[act: {a.group(2)}]"}],
        }

    if phase == "show":
        s, w = _SHOW.search(prompt), _WAS.search(prompt)
        if not s or not w:
            return None
        rake = _RAKE.search(prompt)
        return {
            "kind": "kuhn_show",
            "hand": int(s.group(1)), "hands": int(s.group(2)),
            "card": w.group(1).lower(),
            "cards": list(CARDS),
            "rake": int(rake.group(1)) if rake else None,
            "token": "[show: {card}]",
        }
    return None
