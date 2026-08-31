#!/usr/bin/env python
"""SIDEBAR -- three-handed one-card poker with a private line to one seat.

`msg`  your card, the hand counter, whatever the partner already wrote, and a
       free-text box that emits [msg: <text>]. The box stays free text on
       purpose. Canned messages would be the study writing the player's
       strategy for them, and the thing worth measuring here is what a human
       chooses to put on an unread channel when nothing suggests putting
       anything on it.

`bet`  card, pot, what it costs to call, the table, and the three actions.
       Same equal-weight rule as everywhere else: fold, call and raise are one
       row of identical buttons.
"""
from __future__ import annotations

import re
from typing import Optional

_HEAD = re.compile(r"You are player\s+(\d+)\.\s+Hand\s+(\d+)\s*/\s*(\d+)\.\s+"
                   r"Chips:\s*([+-]?\d+)")
_CARD = re.compile(r"Your card:\s*(\d+)")
_WROTE = re.compile(r"Player\s+(\d+)\s+wrote on the private line:\s*\"(.*)\"")
_SEND_TO = re.compile(r"Send your message on the private line to player\s+(\d+)")
_HEARD = re.compile(r"Private line -- player\s+(\d+)\s+said:\s*\"(.*)\"")
_PUBLISHED = re.compile(r"player\s+(\d+)\s+said:\s*\"(.*)\"")
_POT = re.compile(r"Pot:\s*(\d+)\.\s*Current bet to you:\s*(\d+)")
_TABLE = re.compile(r"Table:\s*(.+)")
_SEAT = re.compile(r"p(\d+):\s*(in|folded)\s*\((\d+)\)")


def _head(prompt: str) -> Optional[dict]:
    h = _HEAD.search(prompt)
    c = _CARD.search(prompt)
    if not h or not c:
        return None
    return {"seat": int(h.group(1)), "hand": int(h.group(2)),
            "hands": int(h.group(3)), "chips": int(h.group(4)),
            "card": int(c.group(1))}


def _msg(prompt: str) -> Optional[dict]:
    base = _head(prompt)
    to = _SEND_TO.search(prompt)
    if not base or not to:
        return None
    wrote = _WROTE.search(prompt)
    return dict(base, **{
        "kind": "sidebar_msg",
        "partner": int(to.group(1)),
        "heard": ({"from": int(wrote.group(1)), "text": wrote.group(2)}
                  if wrote else None),
        "token": "[msg: {text}]",
    })


def _bet(prompt: str) -> Optional[dict]:
    base = _head(prompt)
    pot = _POT.search(prompt)
    tbl = _TABLE.search(prompt)
    if not base or not pot or not tbl:
        return None

    seats = [{"seat": int(s), "live": st == "in", "stake": int(v)}
             for s, st, v in _SEAT.findall(tbl.group(1))]

    heard = None
    h = _HEARD.search(prompt)
    if h:
        heard = [{"from": int(h.group(1)), "text": h.group(2)}]
    elif "The referee publishes the side line" in prompt:
        # The audited arm does not delete the channel, it publishes it -- and
        # the seat that was not on the line sees both halves. Rendering that
        # difference is the point of the arm, so it must not collapse into the
        # one-line shape above.
        heard = [{"from": int(a), "text": b}
                 for a, b in _PUBLISHED.findall(prompt)]

    # Lines the engine appends between the table and the action line: a short
    # tail of what happened in previous hands.
    recent = []
    tail = prompt.split(tbl.group(0), 1)[-1]
    for line in tail.splitlines():
        line = line.strip()
        if not line or line.startswith("Your action"):
            if line.startswith("Your action"):
                break
            continue
        if line.startswith("Reply with") or line.startswith("Keep any"):
            break
        recent.append(line)

    return dict(base, **{
        "kind": "sidebar_bet",
        "pot": int(pot.group(1)),
        "to_call": int(pot.group(2)),
        "table": seats,
        "heard": heard,
        "published": bool(heard and len(heard) > 1),
        "recent": recent[-3:],
        "actions": [{"label": "fold", "token": "[bet: fold]"},
                    {"label": "call", "token": "[bet: call]"},
                    {"label": "raise", "token": "[bet: raise]"}],
    })


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase == "msg":
        return _msg(prompt)
    if phase == "bet":
        return _bet(prompt)
    return None
