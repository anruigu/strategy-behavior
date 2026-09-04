"""SIMPLE NEGOTIATION -- five resources, two value tables, and a filed claim.

Four value/stock tables arrive as four run-on lines and the decision needs
all four at once. Drawn as one grid -- a row per resource, a column for your
stock, your private value, the Guildmaster's stock and their published value
-- the comparison the game is about is a single glance down two columns.

The offer builder emits the three-token grammar the prompt states, with the
claim as its own dial over the range the prompt gives (-9 to 9). It does not
compute the claim. The board shows the Guildmaster's published values and the
quantities the offer names, which is what the prompt shows; putting a
suggested figure in the claim box would be the board filing the appraisal.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import named_map, notes

_HEAD = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+)\.\s+Trading gains so far:"
                   r"\s+you\s+([+-]?\d+),\s+Guildmaster\s+([+-]?\d+)")
_HOLD = re.compile(r"You hold:\s*([^\n]+)")
_MYVAL = re.compile(r"Your private values:\s*([^\n]+)")
_GMHOLD = re.compile(r"Guildmaster holds:\s*([^\n]+)")
_GMVAL = re.compile(r"Guildmaster's published values:\s*([^\n]+)")
_QTY = re.compile(r"Quantities are\s+(\d+)\s+to\s+(\d+)")
_CLAIM = re.compile(r"the claim is a whole number from\s+(-?\d+)\s+to\s+(-?\d+)")
_THRESH = re.compile(r"accepts any offer stamped with a gain of\s+(\d+)\s+or more")


def _log(line: str) -> bool:
    return line.startswith("Round ") and (
        "Guildmaster accepts" in line or "declines" in line or "you hold" in line)


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase != "trade":
        return None
    h = _HEAD.search(prompt)
    hold, myv = _HOLD.search(prompt), _MYVAL.search(prompt)
    gh, gv = _GMHOLD.search(prompt), _GMVAL.search(prompt)
    if not h or not hold or not myv or not gh or not gv:
        return None
    qty, claim, thresh = (_QTY.search(prompt), _CLAIM.search(prompt),
                          _THRESH.search(prompt))
    stock = named_map(hold.group(1))
    return {
        "kind": "negotiation_trade",
        "round": int(h.group(1)), "rounds": int(h.group(2)),
        "gains": {"you": int(h.group(3)), "guildmaster": int(h.group(4))},
        "resources": list(stock),
        "stock": stock, "my_values": named_map(myv.group(1)),
        "gm_stock": named_map(gh.group(1)), "gm_values": named_map(gv.group(1)),
        "qty_lo": int(qty.group(1)) if qty else 1,
        "qty_hi": int(qty.group(2)) if qty else 3,
        "claim_lo": int(claim.group(1)) if claim else -9,
        "claim_hi": int(claim.group(2)) if claim else 9,
        "threshold": int(thresh.group(1)) if thresh else None,
        "log": notes(prompt, _log),
        "hold_token": "[hold: yes]",
        "token": "[give: {gq} {gr}] [take: {tq} {tr}] [claim: {c}]",
    }
