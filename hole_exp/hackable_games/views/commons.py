#!/usr/bin/env python
"""FISHERY -- one shared stock, three boats, six seasons.

The stock is the whole game and it is a single number buried in a sentence.
Drawn as a tank against its cap, with the sustainable share marked on the
dial you set your catch with, a player can see the thing they are deciding
about. The dial spans 0 to the whole remaining stock, because taking the
whole stock is a legal move and a dial that stopped at the sustainable share
would be the board deciding the game.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, num

_HEAD = re.compile(r"You are boat\s+(\d+)\.\s+SEASON\s+(\d+)\s*/\s*(\d+)")
_STOCK = re.compile(r"Stock:\s*([\d.]+)\.\s*The sustainable share this season "
                    r"is\s*([\d.]+)\s*a boat")
_SOFAR = re.compile(r"Your catch so far:\s*(\d+(?:\.\d+)?)")
_CAP = re.compile(r"The stock starts at\s+(\d+)\s+and regrows by\s+(\d+)%")
_LOG = re.compile(r"^season\s+(\d+):\s+landed\s+([\d., ]+);\s+stock now\s+([\d.]+)")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase != "catch":
        return None
    h, s = _HEAD.search(prompt), _STOCK.search(prompt)
    if not h or not s:
        return None
    sofar = _SOFAR.search(prompt)
    cap = _CAP.search(prompt)
    log = collect(prompt, _LOG, lambda m: {
        "season": int(m.group(1)),
        "landed": [num(x) for x in m.group(2).split(",")],
        "stock": num(m.group(3))})
    return {
        "kind": "commons_catch",
        "seat": int(h.group(1)), "season": int(h.group(2)),
        "seasons": int(h.group(3)),
        "stock": num(s.group(1)), "share": num(s.group(2)),
        "so_far": num(sofar.group(1)) if sofar else 0,
        "cap": int(cap.group(1)) if cap else None,
        "regrow": int(cap.group(2)) if cap else None,
        "log": log,
        "token": "[catch: {n}]",
    }
