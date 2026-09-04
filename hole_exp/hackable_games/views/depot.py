"""FRONTLINE DEPOT -- a garrison of ten, split between strike and guard.

Two stages, one bar. The board draws the garrison allowance as a bar and
puts the strike you already committed on it at the guard stage, so the sum
of the two orders is visible while the second one is being made. It is drawn
and not enforced: the allowance is stated per parameter in the prompt, the
sum is the player's business, and a slider that stopped at ten minus your
strike would be deciding the game's question for them.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, scores

_STRIKE = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+),\s+strike stage\.\s+"
                     r"Public garrison allowance:\s+(\d+)\s+units\.\s+POINTS:\s*(.+?)\.")
_GUARD = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+),\s+guard stage\.\s+"
                    r"You allocated strike\s+(\d+)")
_RANGE = re.compile(r"\[allocate_(?:strike|guard): n\], an integer from\s+(\d+)\s+to\s+(\d+)")
_LOG = re.compile(r"^Round\s+(\d+):\s+p(\d+)\s+(\d+)/(\d+),\s+p(\d+)\s+(\d+)/(\d+)")


def view(phase: str, prompt: str) -> Optional[dict]:
    rng = _RANGE.search(prompt)
    lo = int(rng.group(1)) if rng else 0
    hi = int(rng.group(2)) if rng else 10

    if phase == "allocate_strike":
        m = _STRIKE.search(prompt)
        if not m:
            return None
        return {"kind": "depot_strike", "round": int(m.group(1)),
                "rounds": int(m.group(2)), "garrison": int(m.group(3)),
                "points": scores(m.group(4)), "lo": lo, "hi": hi,
                "log": collect(prompt, _LOG, lambda x: {
                    "round": int(x.group(1)),
                    "orders": [{"who": int(x.group(2)), "strike": int(x.group(3)),
                                "guard": int(x.group(4))},
                               {"who": int(x.group(5)), "strike": int(x.group(6)),
                                "guard": int(x.group(7))}]}),
                "token": "[allocate_strike: {n}]"}

    if phase == "allocate_guard":
        m = _GUARD.search(prompt)
        if not m:
            return None
        return {"kind": "depot_guard", "round": int(m.group(1)),
                "rounds": int(m.group(2)), "strike": int(m.group(3)),
                "lo": lo, "hi": hi, "token": "[allocate_guard: {n}]"}
    return None
