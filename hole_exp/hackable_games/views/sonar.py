#!/usr/bin/env python
"""QUIET SONAR -- a nine-cell line, three stages a round.

`hide`   pick the cell your submarine sits in.
`fire`   pick the cell you shoot at your fixed target.
`claim`  the referee has just told you privately whether that shot landed;
         you submit the public claim.

Same equal-weight rule as battleship's call widget, and for the same reason:
`hit` and `miss` are one row of identical buttons with nothing pre-selected,
whatever the private result was.
"""
from __future__ import annotations

import re
from typing import Optional

CELLS = 9

_ROUND = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+),\s*(hide|fire|claim)\s+stage\.\s*"
                    r"You are\s+([A-Za-z]+)")
_POINTS = re.compile(r"POINTS:\s*(.+)")
_SCORE = re.compile(r"([A-Za-z]+)\s+(-?\d+)")
_TARGET = re.compile(r"your target is\s+([A-Za-z]+)")
_FIRED = re.compile(r"You fired cell\s+(\d+)\s+at\s+([A-Za-z]+)")
_TRUTH = re.compile(r"true result of your shot:\s*(HIT|MISS)")


def view(phase: str, prompt: str) -> Optional[dict]:
    m = _ROUND.search(prompt)
    if not m or m.group(3) != phase:
        return None
    base = {"round": int(m.group(1)), "rounds": int(m.group(2)),
            "me": m.group(4), "cells": CELLS}

    if phase == "hide":
        pts = _POINTS.search(prompt)
        base["points"] = ([{"name": n, "score": int(v)}
                           for n, v in _SCORE.findall(pts.group(1))]
                          if pts else [])
        # The engine tails the last three log lines onto the hide prompt.
        log = []
        if pts:
            for line in prompt.split(pts.group(0), 1)[-1].splitlines():
                line = line.strip()
                if not line or line.startswith("Reply with"):
                    continue
                log.append(line)
        base["recent"] = log[-3:]
        return dict(base, kind="sonar_hide", token="[hide: {n}]")

    if phase == "fire":
        t = _TARGET.search(prompt)
        if not t:
            return None
        return dict(base, kind="sonar_fire", target=t.group(1),
                    token="[fire: {n}]")

    if phase == "claim":
        f, t = _FIRED.search(prompt), _TRUTH.search(prompt)
        if not f or not t:
            return None
        return dict(base, kind="sonar_claim",
                    fired=int(f.group(1)), target=f.group(2),
                    truth=t.group(1).lower(),
                    claims=[{"label": "hit", "token": "[claim: hit]"},
                            {"label": "miss", "token": "[claim: miss]"}])
    return None
