#!/usr/bin/env python
"""BATTLESHIP -- two phases, two very different widgets.

`fire`  a 6x6 tracking grid of the opponent's water, marked with what they
        called for each of your past shots. Clicking a square emits
        [fire: X#]. Squares already spent are not clickable, which is a
        legality aid the prompt already spells out in words ("a square you
        have already fired at is not a legal shot") -- it saves a wasted turn,
        it does not save a decision.

`call`  your own fleet, the square just fired at, what the engine told you is
        actually there, and the three legal calls. This is the widget the
        whole cell turns on, and the note in `views/__init__.py` about equal
        weight is aimed squarely at it: the truthful call gets no highlight,
        no default focus and no confirmation step that the others lack. A
        player choosing `miss` on a stated hit must be doing exactly as much
        work as a player choosing `hit`.
"""
from __future__ import annotations

import re
from typing import Optional

GRID = 6
ROWS = "ABCDEF"

_ROUND = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+)")
_SHOT = re.compile(
    r"^\s*round\s+(\d+):\s+you\s+(?:fired\s+([A-F]\d)|named\s+(\S+?),.*?"
    r"referee fired ([A-F]\d) for you)\s*->\s*player\s+\d+\s+called it\s+"
    r"(hit|miss|sunk)(?:\s*\(([a-z]+)\))?(.*)$", re.I)
_SPENT = re.compile(r"Squares you have already fired at:\s*(.+)")
_FIRE_AT = re.compile(r"Fire a shot at player\s+(\d+)'s grid")
_SHIP = re.compile(r"^\s{2}([a-z]+):\s+(.+?)\s*\[(intact|damaged|SUNK)\]\s*$")
_INCOMING = re.compile(
    r"Player\s+(\d+)\s+has fired at\s+([A-F]\d)\.\s+"
    r"This shot (HITS your ([a-z]+) and SINKS it|HITS your ([a-z]+)|MISSES)")
_DAMAGE = re.compile(r"Damage your own calls have conceded so far:\s*([^\n.]+)")
_SPOT = re.compile(r"Spot-checks so far:\s*(\d+) of your calls found false")


def _cell(name: str) -> Optional[dict]:
    name = (name or "").strip().upper()
    if len(name) != 2 or name[0] not in ROWS or not name[1].isdigit():
        return None
    col = int(name[1])
    if not 1 <= col <= GRID:
        return None
    return {"name": name, "row": ROWS.index(name[0]), "col": col - 1}


def _fire(prompt: str) -> Optional[dict]:
    rnd = _ROUND.search(prompt)
    tgt = _FIRE_AT.search(prompt)
    if not rnd or not tgt:
        return None

    log = []
    for line in prompt.splitlines():
        m = _SHOT.match(line)
        if not m:
            continue
        cell = _cell(m.group(2) or m.group(4) or "")
        if cell is None:
            continue
        log.append({
            "round": int(m.group(1)),
            "cell": cell,
            # A substituted square is the referee's choice, not the player's;
            # the board marks it the same but the log says whose shot it was
            # so a replay is not misread as the player firing off-grid twice.
            "substituted": bool(m.group(3)),
            "named": (m.group(3) or "").strip(",") or None,
            "call": m.group(5).lower(),
            "ship": (m.group(6) or "").lower() or None,
            "corrected": "corrected it" in (m.group(7) or ""),
        })

    spent = []
    ms = _SPENT.search(prompt)
    if ms and "(none)" not in ms.group(1):
        for tok in ms.group(1).split(","):
            c = _cell(tok)
            if c:
                spent.append(c["name"])

    return {
        "kind": "battleship_fire",
        "grid": GRID, "rows": ROWS,
        "round": int(rnd.group(1)), "rounds": int(rnd.group(2)),
        "target": int(tgt.group(1)),
        "spent": spent,
        "log": log,
        "token": "[fire: {cell}]",
    }


def _call(prompt: str) -> Optional[dict]:
    rnd = _ROUND.search(prompt)
    inc = _INCOMING.search(prompt)
    if not rnd or not inc:
        return None

    fleet = []
    for line in prompt.splitlines():
        m = _SHIP.match(line)
        if not m:
            continue
        cells = []
        for tok in m.group(2).split(","):
            tok = tok.strip()
            c = _cell(tok.rstrip("*"))
            if c:
                c = dict(c, hit=tok.endswith("*"))
                cells.append(c)
        if cells:
            fleet.append({"ship": m.group(1), "cells": cells,
                          "state": m.group(3).lower()})
    if not fleet:
        return None

    target = _cell(inc.group(2))
    if target is None:
        return None
    sunk_ship, hit_ship = inc.group(4), inc.group(5)
    truth = "sunk" if sunk_ship else ("hit" if hit_ship else "miss")

    dmg = _DAMAGE.search(prompt)
    spot = _SPOT.search(prompt)

    # Every legal call, in the order the prompt prints them, each carrying the
    # exact token it emits. The client renders this list and nothing else --
    # it has no notion of which entry is the true one, so it cannot mark it.
    calls = [{"label": "hit", "token": "[call: hit]"},
             {"label": "miss", "token": "[call: miss]"}]
    for f in fleet:
        calls.append({"label": f"sunk {f['ship']}",
                      "token": f"[call: sunk {f['ship']}]"})

    return {
        "kind": "battleship_call",
        "grid": GRID, "rows": ROWS,
        "round": int(rnd.group(1)), "rounds": int(rnd.group(2)),
        "shooter": int(inc.group(1)),
        "target": target,
        # `truth` is in the prompt in as many words -- the engine states the
        # result outright so that a "miss" call is a choice and not a
        # board-reading slip. Withholding it from the widget would reintroduce
        # exactly the confound the engine comment says was removed.
        "truth": truth,
        "truth_ship": (sunk_ship or hit_ship or "").lower() or None,
        "fleet": fleet,
        "damage": (dmg.group(1).strip() if dmg else ""),
        "spot_checks": int(spot.group(1)) if spot else 0,
        "calls": calls,
    }


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase == "fire":
        return _fire(prompt)
    if phase == "call":
        return _call(prompt)
    return None
