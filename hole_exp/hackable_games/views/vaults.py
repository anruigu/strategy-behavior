"""SOVEREIGN VAULTS -- a private yield, a public declaration, a deposit.

Two stages, two dials, and the number that connects them is the one the
player states in between. The board keeps the private yield and the
declaration side by side at the deposit stage because both are in the
prompt, and shows what each unit is worth in points -- retained at 2, banked
at 1 -- since the whole decision is that exchange rate.

The declare dial spans the range the prompt states (1-10) and the deposit
dial the range the prompt states (0 to the declaration). Neither is narrowed
to the true yield.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, scores

_DECL = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+),\s+declare stage\.\s+"
                   r"Your private yield is\s+(\d+)\.\s+POINTS:\s*(.+?)\.")
_DEP = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+),\s+deposit stage\.\s+You declared\s+(\d+)")
_RANGE = re.compile(r"\[(?:declare|deposit): n\], an integer from\s+(\d+)\s+to\s+(\d+)")
_RATES = re.compile(r"scores\s+(\d+)\s+POINTS per unit\. Deposited gold scores\s+(\d+)\s+POINT per unit")
_PENALTY = re.compile(r"If an audit fails you lose\s+(\d+)\s+POINTS")
_LOG = re.compile(r"^Round\s+(\d+):\s+yields\s+([\d/]+),\s+declared\s+([\d/]+),"
                  r"\s+deposited\s+([\d/]+)")
_FAIL = re.compile(r"^Round\s+(\d+):\s+p(\d+) AUDIT FAILED \(declared\s+(\d+), yield\s+(\d+)\)")


def view(phase: str, prompt: str) -> Optional[dict]:
    rng = _RANGE.search(prompt)
    rates = _RATES.search(prompt)
    pen = _PENALTY.search(prompt)
    common = {
        "lo": int(rng.group(1)) if rng else 0,
        "hi": int(rng.group(2)) if rng else 10,
        "rates": ({"retain": int(rates.group(1)), "deposit": int(rates.group(2))}
                  if rates else None),
        "penalty": int(pen.group(1)) if pen else None,
    }

    if phase == "declare":
        m = _DECL.search(prompt)
        if not m:
            return None
        return dict(common, kind="vaults_declare",
                    round=int(m.group(1)), rounds=int(m.group(2)),
                    yield_=int(m.group(3)), points=scores(m.group(4)),
                    log=collect(prompt, _LOG, lambda x: {
                        "round": int(x.group(1)),
                        "yields": [int(v) for v in x.group(2).split("/")],
                        "declared": [int(v) for v in x.group(3).split("/")],
                        "deposited": [int(v) for v in x.group(4).split("/")]}),
                    fails=collect(prompt, _FAIL, lambda x: {
                        "round": int(x.group(1)), "who": int(x.group(2)),
                        "declared": int(x.group(3)), "yield": int(x.group(4))}),
                    token="[declare: {n}]")

    if phase == "deposit":
        m = _DEP.search(prompt)
        if not m:
            return None
        return dict(common, kind="vaults_deposit",
                    round=int(m.group(1)), rounds=int(m.group(2)),
                    declared=int(m.group(3)), token="[deposit: {n}]")
    return None
