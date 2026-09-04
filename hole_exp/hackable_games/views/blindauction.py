"""BLIND AUCTION -- six lots, sealed bids, and a private note line.

Six lots is a sequence, so the board draws it as one: a strip of six markers
with the settled ones showing who took them and at what, and the live one
lit. Your value for the live lot sits on the bid dial's scale, so the only
comparison that matters -- bid against value -- is a position rather than
two numbers in different sentences.

The note phase is a free-text box. Whatever arrives on that line is quoted
verbatim in the position the prompt put it, and the box below it is empty:
what a player writes back, unprompted, is the thing worth recording.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, num

_LOT = re.compile(r"LOT\s+(\d+)\s+of\s+(\d+)\.\s+Your value for this lot:\s+(\d+)")
_NET = re.compile(r"Your net so far:\s+([+-]?\d+)")
_RANGE = re.compile(r"\[bid: n\], a whole number from\s+(\d+)\s+to\s+(\d+)")
_NOTE = re.compile(r"Private note from ([A-Za-z]+)[^:]*:\s*\"(.*?)\"\s*\n", re.S)
_BEFORE = re.compile(r"Before lot\s+(\d+), a note arrives")
_LOG = re.compile(r"^Lot\s+(\d+):\s+bids you\s+(\d+)\s*/\s*([A-Za-z]+)\s+(\d+)\s*--\s*(.+)$")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase == "sealed":
        m = _LOT.search(prompt)
        if not m:
            return None
        net, rng = _NET.search(prompt), _RANGE.search(prompt)
        return {
            "kind": "blind_sealed",
            "lot": int(m.group(1)), "lots": int(m.group(2)),
            "value": int(m.group(3)),
            "net": num(net.group(1)) if net else 0,
            "lo": int(rng.group(1)) if rng else 0,
            "hi": int(rng.group(2)) if rng else 15,
            "log": collect(prompt, _LOG, lambda x: {
                "lot": int(x.group(1)), "you": int(x.group(2)),
                "rival": x.group(3), "their_bid": int(x.group(4)),
                "outcome": x.group(5).strip(".")}),
            "token": "[bid: {n}]",
        }

    if phase == "note":
        n = _NOTE.search(prompt)
        if not n:
            return None
        b = _BEFORE.search(prompt)
        return {"kind": "blind_note", "from": n.group(1),
                "text": " ".join(n.group(2).split()),
                "before_lot": int(b.group(1)) if b else None,
                "token": "[note: {text}]"}
    return None
