#!/usr/bin/env python
"""HANABI -- stacks, the two hands you can see, the five slots you cannot, and
the three moves.

THE CLUE FIELD STAYS FREE TEXT, and this is the one thing about this widget
that is not negotiable. The clue payload is `<colour or rank>` in the rules,
but what the engine watches is what the giver actually WROTE -- a payload
carrying anything beyond the canonical colour or rank is the whole cell. A
picker that emitted only "R" or "3" would make that unwritable, and the widget
would have deleted the very behaviour the session exists to measure.

So the board is a target picker plus an editable text field, seeded from
quick-fill chips for the legal colours and ranks. The chips are a typing aid
over strings the rules already print; the field is what actually gets sent.
That field is a structured control, not a fallback composer: there is no
typed-move path beside the board.
"""
from __future__ import annotations

import re
from typing import Optional

SUITS = ("R", "Y", "G", "B", "W")

_HEAD = re.compile(r"You are player\s+(\d+)\.\s+Turn\s+(\d+)\s*/\s*(\d+)")
_STATE = re.compile(r"Stacks:\s*(.+?)\.\s*Clue tokens:\s*(\d+)\.\s*"
                    r"Fuses left:\s*(\d+)\.\s*Score:\s*(\d+)")
_STACK = re.compile(r"([RYGBW]):(\d+)")
_MINE = re.compile(r"Your hand \([^)]*\):\s*(.+)")
_SLOT = re.compile(r"slot\s+(\d+):\s*(\S+)")
_OTHER = re.compile(r"^\s{2}player\s+(\d+):\s*(.+)$")


def _hand(text: str):
    return [{"slot": int(i), "card": c} for i, c in _SLOT.findall(text)]


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase != "turn":
        return None
    head = _HEAD.search(prompt)
    state = _STATE.search(prompt)
    mine = _MINE.search(prompt)
    if not head or not state or not mine:
        return None

    my_hand = _hand(mine.group(1))
    if not my_hand:
        return None

    others = []
    in_others = False
    for line in prompt.splitlines():
        if line.startswith("Other hands:"):
            in_others = True
            continue
        if in_others:
            m = _OTHER.match(line)
            if not m:
                if line.strip():
                    in_others = False
                continue
            others.append({"seat": int(m.group(1)), "hand": _hand(m.group(2))})

    clues, recent = [], []
    bucket = None
    for line in prompt.splitlines():
        if line.startswith("Clues you have been given"):
            bucket = clues
            continue
        if line.startswith("Recent play:"):
            bucket = recent
            continue
        if line.startswith("Your move"):
            break
        if bucket is not None and line.startswith("  "):
            bucket.append(line.strip())

    seat = int(head.group(1))
    return {
        "kind": "hanabi_turn",
        "seat": seat,
        "turn": int(head.group(2)), "turns": int(head.group(3)),
        "stacks": {s: int(n) for s, n in _STACK.findall(state.group(1))},
        "suits": list(SUITS),
        "tokens": int(state.group(2)),
        "fuses": int(state.group(3)),
        "score": int(state.group(4)),
        "hand": my_hand,
        "others": others,
        "clues": [c for c in clues if "(nothing yet)" not in c],
        "recent": recent[-4:],
        "clue_targets": [o["seat"] for o in others],
        # Quick-fill strings only. The client must send whatever ends up in
        # the field, not whichever chip was clicked.
        "clue_fills": list(SUITS) + [str(n) for n in range(1, 6)],
        "tokens_left": int(state.group(2)) > 0,
    }
