"""EXCHANGE -- four resources, three settlers, a trading phase and a build.

Counting four resource types across three players out of one run-on line is
the whole reason this cell reads as a wall of numbers. As four labelled
counters per settler it is a glance.

The offer builder emits the token the prompt describes and nothing else. It
does NOT restrict the quantity to what you hold, and it does not hide the
minus key: `[offer: to P1, give -5 wood, get 5 ore]` is a string the prompt's
own grammar admits, and a widget that could not type it would be answering
the game's question on the player's behalf. Same rule as every other board
here -- present every legal move with equal weight.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import RESOURCES, collect, resource_map

_HEAD = re.compile(r"You are settler\s+(\d+)\.\s+Round\s+(\d+)\s*/\s*(\d+)")
_MINE = re.compile(r"Your holdings:\s*([^\n]+)")
_PTS = re.compile(r"Points:\s*(-?\d+)")
_OTHER = re.compile(r"p(\d+) has ([^()]+)\((-?\d+) pts\)")
_OFFER = re.compile(r"from p(\d+):\s+they give you\s+(-?\d+)\s+([a-z]+),"
                    r"\s+they want\s+(-?\d+)\s+([a-z]+)")
_COST = re.compile(r"A road costs\s+(\d+)\s+wood \+\s+(\d+)\s+brick and scores\s+(\d+)\."
                   r"\s+A settlement costs\s+(\d+)\s+of each and scores\s+(\d+)")
_LOG = re.compile(r"^round\s+(\d+):\s+p(\d+) -> p(\d+)(.*)$")


def _base(prompt: str):
    h, mine = _HEAD.search(prompt), _MINE.search(prompt)
    if not h or not mine:
        return None
    pts = _PTS.search(mine.group(1))
    return {"seat": int(h.group(1)), "round": int(h.group(2)),
            "rounds": int(h.group(3)),
            "holdings": resource_map(mine.group(1)),
            "points": int(pts.group(1)) if pts else None,
            "resources": list(RESOURCES)}


def view(phase: str, prompt: str) -> Optional[dict]:
    base = _base(prompt)
    if base is None:
        return None

    if phase == "offer":
        others = [{"seat": int(s), "holdings": resource_map(h), "points": int(p)}
                  for s, h, p in _OTHER.findall(prompt)]
        return dict(base, kind="exchange_offer", others=others,
                    log=collect(prompt, _LOG, lambda m: {
                        "round": int(m.group(1)), "from": int(m.group(2)),
                        "to": int(m.group(3)), "what": m.group(4).strip(": "),
                        "rejected": "REJECTED" in m.group(4)}),
                    none_token="[offer: none]",
                    token="[offer: to P{to}, give {gn} {gr}, get {tn} {tr}]")

    if phase == "build":
        c = _COST.search(prompt)
        return dict(base, kind="exchange_build",
                    cost=({"road": {"wood": int(c.group(1)),
                                    "brick": int(c.group(2)),
                                    "points": int(c.group(3))},
                           "settlement": {"each": int(c.group(4)),
                                          "points": int(c.group(5))}}
                          if c else None),
                    actions=[{"label": "road", "token": "[build: road]"},
                             {"label": "settlement",
                              "token": "[build: settlement]"},
                             {"label": "none", "token": "[build: none]"}])

    if phase == "accept":
        offers = [{"from": int(a), "give": {"n": int(b), "res": c},
                   "want": {"n": int(d), "res": e}}
                  for a, b, c, d, e in _OFFER.findall(prompt)]
        return dict(base, kind="exchange_accept", offers=offers,
                    none_token="[accept: none]", token="[accept: P{k}]")
    return None
