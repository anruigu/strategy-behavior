"""PUBLIC GOODS -- an envelope, then a receipt slip about the envelope.

The board draws the two stages as the two objects the rules name: a sealed
envelope with the amount you put in it, and a receipt slip you write a number
on. At the receipt stage the envelope's amount is on screen, because the
prompt states it, and the slip's dial covers the full legal range, because
the prompt states that too.

The multiplier arithmetic -- pot x1.6 split four ways -- is drawn against the
receipts already published, not against anything private.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, num, scores

_ENV = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+)\.\s+Totals:\s*(.+?)\.\s*\n")
_REC = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+)\.\s+Your envelope contained\s+(\d+)\s+tokens")
_RANGE = re.compile(r"\[(?:contribute|declare): n\], a whole number from\s+(\d+)\s+to\s+(\d+)")
_END = re.compile(r"a fresh endowment of\s+(\d+)\s+tokens each round")
_MULT = re.compile(r"is multiplied by\s+([\d.]+)\s+and split equally among the (\w+)")
_LOG = re.compile(r"^Round\s+(\d+):\s+receipts published\s+([\d/]+)\s+\(([^)]*)\);"
                  r"\s+pot\s+([\d.]+),\s+share\s+([\d.]+)\s+each")


def view(phase: str, prompt: str) -> Optional[dict]:
    rng = _RANGE.search(prompt)
    lo = int(rng.group(1)) if rng else 0
    hi = int(rng.group(2)) if rng else 20
    end, mult = _END.search(prompt), _MULT.search(prompt)

    if phase == "envelope":
        m = _ENV.search(prompt)
        if not m:
            return None
        return {"kind": "pubgoods_envelope", "round": int(m.group(1)),
                "rounds": int(m.group(2)), "totals": scores(m.group(3)),
                "lo": lo, "hi": hi,
                "endowment": int(end.group(1)) if end else None,
                "multiplier": float(mult.group(1)) if mult else None,
                "log": collect(prompt, _LOG, lambda x: {
                    "round": int(x.group(1)),
                    "receipts": [num(v) for v in x.group(2).split("/")],
                    "names": [n.strip() for n in x.group(3).split("/")],
                    "pot": num(x.group(4)), "share": num(x.group(5))}),
                "token": "[contribute: {n}]"}

    if phase == "receipt":
        m = _REC.search(prompt)
        if not m:
            return None
        return {"kind": "pubgoods_receipt", "round": int(m.group(1)),
                "rounds": int(m.group(2)), "sealed": int(m.group(3)),
                "lo": lo, "hi": hi, "token": "[declare: {n}]"}
    return None
