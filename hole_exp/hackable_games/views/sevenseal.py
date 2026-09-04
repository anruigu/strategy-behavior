"""SEVEN-SEAL CERTIFICATES -- a private draw, a public report, an audit seal.

The seal is `(3A + 5B + 6C) mod 7`, stated once in the rules and then never
again, and it is the only thing in the game a player has to hold in their
head. The board keeps the three coefficients on screen next to a dial for
your own report, and shows the round history as draws-against-reports so the
pattern in what the other two do is visible without arithmetic.

The dial spans the range the prompt gives -- 0 through 9 -- not the range of
the draw, which is 0 through 2. Those are different numbers in the rules and
collapsing them on the board would be the board answering the question.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, scores

_HEAD = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+)\.\s+You are\s+([A-Za-z]+)\."
                   r"\s+Your private draw is\s+(\d+)")
_POINTS = re.compile(r"Current POINTS:\s*(.+)")
_RANGE = re.compile(r"\[report: n\] where n is an integer from\s+(\d+)\s+through\s+(\d+)")
_SEAL = re.compile(r"\((\d+)A \+ (\d+)B \+ (\d+)C\) mod (\d+)")
_DRAW = re.compile(r"drawn digit from\s+(\d+)\s+through\s+(\d+)")
_SEATS = re.compile(r"You are ([A-Za-z]+), among ([A-Za-z]+), ([A-Za-z]+) and ([A-Za-z]+)")
_LOG = re.compile(r"^Round\s+(\d+):\s+draws\s+([\d/]+),\s+reports\s+([\d/]+),"
                  r"\s+seal\s+(pass|FAIL)")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase != "report":
        return None
    h = _HEAD.search(prompt)
    if not h:
        return None
    pts, rng = _POINTS.search(prompt), _RANGE.search(prompt)
    seal, draw, seats = (_SEAL.search(prompt), _DRAW.search(prompt),
                         _SEATS.search(prompt))
    return {
        "kind": "sevenseal_report",
        "round": int(h.group(1)), "rounds": int(h.group(2)),
        "me": h.group(3), "draw": int(h.group(4)),
        "points": scores(pts.group(1)) if pts else [],
        "lo": int(rng.group(1)) if rng else 0,
        "hi": int(rng.group(2)) if rng else 9,
        "draw_lo": int(draw.group(1)) if draw else None,
        "draw_hi": int(draw.group(2)) if draw else None,
        "seal": ({"coef": [int(seal.group(i)) for i in (1, 2, 3)],
                  "mod": int(seal.group(4))} if seal else None),
        "seats": list(seats.groups()[1:]) if seats else None,
        "log": collect(prompt, _LOG, lambda m: {
            "round": int(m.group(1)),
            "draws": [int(x) for x in m.group(2).split("/")],
            "reports": [int(x) for x in m.group(3).split("/")],
            "pass": m.group(4) == "pass"}),
        "token": "[report: {n}]",
    }
