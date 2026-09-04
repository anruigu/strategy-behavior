"""ITERATED PRISONER'S DILEMMA and ITERATED STAG HUNT.

Two cells with the same shape: one opponent, one binary choice a round, a
payoff table stated once, an opening message, and a history that is the only
evidence about what the opponent does. One adapter serves both because the
board that helps is the same board -- the 2x2 table drawn as a table, and the
history drawn as a strip of rounds you can read down at a glance instead of
counting lines of prose.

THE OPENING MESSAGE IS QUOTED, NOT SUMMARISED. Both opponents open with a
threat or a promise, and what a player makes of it is most of what these
cells measure. It is reproduced verbatim, in the position the prompt put it,
and the board says nothing about whether it is true.

The two actions are one row of identical buttons in prompt order.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, scores

_HEAD = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+)\.\s+Totals:\s*(.+?)\.")
_MSG = re.compile(r"Before round \d+, ([A-Za-z]+) sends you a message:\s*\n(.+?)\n\n",
                  re.S)
_IPD_PAY = re.compile(r"both cooperate\s+(\d+)/(\d+); both defect\s+(\d+)/(\d+);"
                      r"\s+defect against cooperate pays the defector\s+(\d+)"
                      r"\s+and the cooperator\s+(\d+)")
_STAG_PAY = re.compile(r"both stag\s+(\d+)/(\d+); both hare\s+(\d+)/(\d+);"
                       r"\s+a lone hare-taker gets\s+(\d+)\s+and leaves the stag "
                       r"hunter with\s+(\d+)")
_IPD_LOG = re.compile(r"^Round\s+(\d+):\s+you\s+(cooperate|defect),\s+([A-Za-z]+)\s+(cooperate|defect)")
_STAG_LOG = re.compile(r"^Round\s+(\d+):\s+you took the (stag|hare),\s+([A-Za-z]+) took the (stag|hare)")

SPEC = {
    "move": {"game": "ipd", "verb": "move", "options": ("cooperate", "defect"),
             "pay": _IPD_PAY, "log": _IPD_LOG,
             "corners": ("both cooperate", "both defect",
                         "defector / cooperator")},
    "hunt": {"game": "staghunt", "verb": "hunt", "options": ("stag", "hare"),
             "pay": _STAG_PAY, "log": _STAG_LOG,
             "corners": ("both stag", "both hare", "lone hare / stag hunter")},
}


def view(phase: str, prompt: str) -> Optional[dict]:
    spec = SPEC.get(phase)
    if spec is None:
        return None
    h = _HEAD.search(prompt)
    if not h:
        return None
    pay = spec["pay"].search(prompt)
    msg = _MSG.search(prompt)
    log = collect(prompt, spec["log"], lambda m: {
        "round": int(m.group(1)), "me": m.group(2),
        "them": m.group(4), "who": m.group(3)})
    return {
        "kind": "duel_move", "game": spec["game"], "verb": spec["verb"],
        "round": int(h.group(1)), "rounds": int(h.group(2)),
        "totals": scores(h.group(3)),
        "options": list(spec["options"]),
        "payoffs": ([int(pay.group(i)) for i in range(1, 7)] if pay else None),
        "corners": list(spec["corners"]),
        "message": ({"from": msg.group(1),
                     "text": " ".join(msg.group(2).split())} if msg else None),
        "log": log,
        "token": "[%s: {opt}]" % spec["verb"],
    }
