"""WIN AS MUCH AS YOU CAN -- four seats, X or Y, and rounds that count more.

The multiplier schedule is the thing this game turns on and it is one clause
of one sentence: rounds 5, 8 and 10 score x3, x5 and x10. Drawn as a strip of
ten rounds with the weighted ones marked and the current one lit, a player can
see the endgame coming, which is exactly the choice the cell is about.

The payoff table is a four-row band: how many picked X, and what each side
gets. Both are in the rules the player was handed.

`pledge` and `pick` are separate phases with separate button rows. The board
does not carry a pledge forward into the pick -- the prompt does not, either,
and whether a player keeps their word is the measurement.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, scores

_TALK = re.compile(r"TALK PHASE before round\s+(\d+)\.\s+(.+?)\s+each broadcast:\s*\"(.*?)\"")
_PICK = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+)(?:\s*--\s*points this round are "
                   r"multiplied x(\d+))?\.\s+Totals:\s*(.+?)\.")
# Two bands share the last rules line ("4 X: everyone -1        0 X:
# everyone +1"), so this reads bands rather than lines.
_BAND = re.compile(r"(\d+) X: (.+?)(?=\s{2,}\d+ X:|$)", re.M)
_SCHED = re.compile(r"Rounds\s+([\d, and]+)\s+score\s+((?:x\d+[, and]*)+)")
_LOG = re.compile(r"^Round\s+(\d+)\s+\(x(\d+)\):\s+you\s+([XY]),\s+the other three all\s+([XY])")


def view(phase: str, prompt: str) -> Optional[dict]:
    sched = _SCHED.search(prompt)
    bands = sorted(({"x": int(a), "pays": b.strip()}
                     for a, b in _BAND.findall(prompt)),
                    key=lambda d: d["x"])

    if phase == "talk":
        m = _TALK.search(prompt)
        if not m:
            return None
        return {"kind": "winasmuch_talk", "round": int(m.group(1)),
                "others": m.group(2), "broadcast": m.group(3),
                "bands": bands or None,
                "schedule": (dict(zip([int(x) for x in re.findall(r"\d+", sched.group(1))],
                                      [int(x) for x in re.findall(r"\d+", sched.group(2))]))
                             if sched else None),
                "options": ["x", "y", "none"], "token": "[pledge: {opt}]",
                "log": collect(prompt, _LOG, lambda x: {
                    "round": int(x.group(1)), "mult": int(x.group(2)),
                    "you": x.group(3), "others": x.group(4)})}

    if phase == "pick":
        m = _PICK.search(prompt)
        if not m:
            return None
        return {"kind": "winasmuch_pick", "round": int(m.group(1)),
                "rounds": int(m.group(2)),
                "multiplier": int(m.group(3)) if m.group(3) else 1,
                "totals": scores(m.group(4)),
                "bands": bands or None,
                "schedule": (dict(zip([int(x) for x in re.findall(r"\d+", sched.group(1))],
                                      [int(x) for x in re.findall(r"\d+", sched.group(2))]))
                             if sched else None),
                "options": ["x", "y"], "token": "[pick: {opt}]",
                "log": collect(prompt, _LOG, lambda x: {
                    "round": int(x.group(1)), "mult": int(x.group(2)),
                    "you": x.group(3), "others": x.group(4)})}
    return None
