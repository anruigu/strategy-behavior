"""ICEBOUND MANIFEST -- three crews in a ring, pledges then acts.

Raids target clockwise and the ring is stated in one line of prose -- North
to East, East to West, West to North. Drawn as an actual ring with an arrow
on it, who can reach whom stops being something a player has to keep
re-deriving.

Fuel and points get one gauge each per crew. The three missions are one row
of identical buttons in the order the prompt names them, and the act stage
draws the pledges above them without marking which act "matches"; that the
act must repeat the pledge is a rule the player was told, and a board that
greyed out the other two would be enforcing it on the referee's behalf.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, scores

_PLEDGE = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+),\s+pledge stage\.\s+You are\s+([A-Za-z]+)\."
                     r"\s+Fuel:\s*(.+?)\.\s*POINTS:\s*(.+?)\.")
_ACT = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+),\s+act stage\.\s+Public pledges:\s*(.+?)\.")
_FUEL = re.compile(r"Your remaining fuel is\s+(\d+)")
_AFFORD = re.compile(r"You can afford:\s*(.+?)\.")
_COST = re.compile(r"cost is immediately deducted:\s*scout\s+(\d+), escort\s+(\d+), raid\s+(\d+)")
_RING = re.compile(r"Raids always target clockwise:\s*(.+?)\.")
_LOG = re.compile(r"^Round\s+(\d+):\s+(.+)\.$")
_PAIR = re.compile(r"([A-Za-z]+)\s+(scout|escort|raid)/(scout|escort|raid)")
_PUB = re.compile(r"([A-Za-z]+)\s+(scout|escort|raid)")

MISSIONS = ("scout", "escort", "raid")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase == "pledge":
        m = _PLEDGE.search(prompt)
        if not m:
            return None
        aff = _AFFORD.search(prompt)
        cost = _COST.search(prompt)
        ring = _RING.search(prompt)
        return {
            "kind": "icebound_pledge",
            "round": int(m.group(1)), "rounds": int(m.group(2)),
            "me": m.group(3),
            "fuel": scores(m.group(4)), "points": scores(m.group(5)),
            "afford": [w.strip() for w in aff.group(1).split(",")] if aff else list(MISSIONS),
            "cost": ({k: int(cost.group(i)) for i, k in
                      enumerate(MISSIONS, 1)} if cost else None),
            "ring": ([tuple(x.split("->")) for x in
                      re.findall(r"([A-Za-z]+->[A-Za-z]+)", ring.group(1))]
                     if ring else None),
            "missions": list(MISSIONS),
            "log": collect(prompt, _LOG, lambda x: {
                "round": int(x.group(1)),
                "crews": [{"name": a, "pledged": b, "acted": c}
                          for a, b, c in _PAIR.findall(x.group(2))]}),
            "token": "[pledge: {m}]",
        }

    if phase == "act":
        m = _ACT.search(prompt)
        if not m:
            return None
        f = _FUEL.search(prompt)
        return {
            "kind": "icebound_act",
            "round": int(m.group(1)), "rounds": int(m.group(2)),
            "pledges": [{"name": a, "pledge": b}
                        for a, b in _PUB.findall(m.group(3))],
            "fuel": int(f.group(1)) if f else None,
            "missions": list(MISSIONS),
            "token": "[act: {m}]",
        }
    return None
