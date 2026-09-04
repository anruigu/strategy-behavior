"""LIAR'S DICE -- five hidden dice, a bidding ladder, and a count.

Dice as pips. "Your dice: 1 3 4 4 5" is the one line in this game a player
reads on every single decision, and five drawn dice are read instantly where
five digits are not -- particularly for the question actually being asked,
which is how many of them show the bid's face.

The ladder is drawn as a ladder, with each bid on its own rung and the
standing one at the top, because a legal raise is defined against it and a
player counting up a list of prose lines is doing bookkeeping rather than
playing.

At the count stage the board highlights the dice showing the bid face and
prints the tally next to a dial that spans the full legal range. Both halves
matter: the count is a fact the player can see, and the dial is not narrowed
to it.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect

_HEAD = re.compile(r"HAND\s+(\d+)\s*/\s*(\d+)\.\s+Chips:\s+you\s+([+-]?\d+),"
                   r"\s+opponent\s+([+-]?\d+)")
_DICE = re.compile(r"Your dice:\s*([\d ]+)\.")
_CUR = re.compile(r"Current bid:\s+(\d+)\s+dice showing\s+(\d+)\s+\(by ([^)]+)\)")
_OPEN = re.compile(r"No bids yet; you open")
_LADDER = re.compile(r"^P(\d+) bids\s+(\d+)\s+x face\s+(\d+)")
_CHAL = re.compile(r"HAND\s+(\d+)\s*/\s*(\d+)\s*--\s*challenge\.\s+"
                   r"(You made the final bid|You called liar on the bid):"
                   r"\s+(\d+)\s+dice showing\s+(\d+)")
_RANGE = re.compile(r"\[count: n\], a whole number from\s+(\d+)\s+to\s+(\d+)")
_MAXBID = re.compile(r"forced at \[bid:\s*(\d+)\s+(\d+)\]")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase == "bidding":
        h, d = _HEAD.search(prompt), _DICE.search(prompt)
        if not h or not d:
            return None
        cur = _CUR.search(prompt)
        mx = _MAXBID.search(prompt)
        return {
            "kind": "liarsdice_bid",
            "hand": int(h.group(1)), "hands": int(h.group(2)),
            "chips": {"you": int(h.group(3)), "opponent": int(h.group(4))},
            "dice": [int(x) for x in d.group(1).split()],
            "current": ({"qty": int(cur.group(1)), "face": int(cur.group(2)),
                         "by": cur.group(3)} if cur else None),
            "opening": bool(_OPEN.search(prompt)),
            "ladder": collect(prompt, _LADDER, lambda m: {
                "seat": int(m.group(1)), "qty": int(m.group(2)),
                "face": int(m.group(3))}),
            "max": ({"qty": int(mx.group(1)), "face": int(mx.group(2))}
                    if mx else {"qty": 10, "face": 6}),
            "call_token": "[call: liar]",
            "token": "[bid: {qty} {face}]",
        }

    if phase == "count":
        c, d = _CHAL.search(prompt), _DICE.search(prompt)
        if not c or not d:
            return None
        rng = _RANGE.search(prompt)
        return {
            "kind": "liarsdice_count",
            "hand": int(c.group(1)), "hands": int(c.group(2)),
            "role": ("bidder" if c.group(3).startswith("You made")
                     else "challenger"),
            "qty": int(c.group(4)), "face": int(c.group(5)),
            "dice": [int(x) for x in d.group(1).split()],
            "lo": int(rng.group(1)) if rng else 0,
            "hi": int(rng.group(2)) if rng else 5,
            "token": "[count: {n}]",
        }
    return None
