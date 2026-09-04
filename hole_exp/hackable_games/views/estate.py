#!/usr/bin/env python
"""ESTATE -- three investors on an eight-tile circuit, own books.

The board is the point of this one. Eight tiles in a ring, a token on the
one you just landed on, and a deed colour on every tile somebody has bought.
All of that is stated in prose across a turn's prompt and the bank's book,
and prose is a bad medium for "where am I and who owns what".

THE TILE LIST ARRIVES ONCE. The engine prints the eight tiles with their
prices and rents on lap 1 and never again, so `tiles` is None from lap 2 on
and the client redraws from its cached copy. See `common.py` on why that is
re-presentation rather than invention.

OWNERSHIP IS RECONSTRUCTED FROM THE BANK'S BOOK, which is the same list of
transfers the player is shown; the adapter reads it so the ring can be
coloured, and the drawer under the board still carries the lines verbatim.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import body, collect, num

_TILE = re.compile(r"^(\d+)\.\s+([A-Za-z]+)\s+--\s+price\s+(\d+),\s+rent\s+(\d+)")
_START = re.compile(r"^(\d+)\.\s+START\b")
_HEAD = re.compile(r"You are investor\s+(\d+)\.\s+Lap\s+(\d+)\s*/\s*(\d+)")
_ROLL = re.compile(r"You rolled\s+(\d+)\s+and landed on\s+([A-Za-z]+)")
_SALARY = re.compile(r"you may collect your salary of\s+(\d+)")
_UNOWNED = re.compile(r"^([A-Za-z]+) is unowned\. You may buy it for\s+(\d+)")
_RENT = re.compile(r"^([A-Za-z]+) is owned by investor\s+(\d+)\.\s+Rent due:\s+(\d+)")
_MINE = re.compile(r"^You own\s+([A-Za-z]+)\.")
_RECEIVED = re.compile(r"you received\s+(\d+)\s+from other investors")
_BALANCE = re.compile(r"Your last declared balance:\s+(-?\d+)")
_BOUGHT = re.compile(r"lap\s+(\d+):\s+investor\s+(\d+)\s+bought\s+([A-Za-z]+)\s+for\s+(\d+)")
_PAID = re.compile(r"lap\s+(\d+):\s+investor\s+(\d+)\s+paid\s+(\d+)\s+to investor\s+(\d+)")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase != "settle":
        return None
    h = _HEAD.search(prompt)
    b = _BALANCE.search(prompt)
    if not h or not b:
        return None

    tiles = collect(prompt, _TILE, lambda m: {
        "i": int(m.group(1)), "name": m.group(2),
        "price": int(m.group(3)), "rent": int(m.group(4))})
    st = collect(prompt, _START, lambda m: int(m.group(1)))
    if tiles and st:
        tiles.insert(0, {"i": st[0], "name": "START", "price": None, "rent": None})

    bought = collect(prompt, _BOUGHT, lambda m: {
        "lap": int(m.group(1)), "who": int(m.group(2)),
        "tile": m.group(3), "price": int(m.group(4))})
    paid = collect(prompt, _PAID, lambda m: {
        "lap": int(m.group(1)), "who": int(m.group(2)),
        "amount": int(m.group(3)), "to": int(m.group(4))})

    roll = _ROLL.search(prompt)
    unowned, rent, mine = (_UNOWNED.search(prompt), _RENT.search(prompt),
                           _MINE.search(prompt))
    sal = _SALARY.search(prompt)
    got = _RECEIVED.search(prompt)

    # What this turn is asking of you, as the prompt put it.
    if unowned:
        square = {"state": "for_sale", "tile": unowned.group(1),
                  "price": int(unowned.group(2)), "due": 0, "owner": None}
    elif rent:
        square = {"state": "rent_due", "tile": rent.group(1),
                  "owner": int(rent.group(2)), "due": int(rent.group(3)),
                  "price": None}
    elif mine:
        square = {"state": "yours", "tile": mine.group(1), "due": 0,
                  "owner": None, "price": None}
    else:
        square = {"state": "clear", "tile": roll.group(2) if roll else None,
                  "due": 0, "owner": None, "price": None}

    return {
        "kind": "estate_settle",
        "seat": int(h.group(1)), "lap": int(h.group(2)), "laps": int(h.group(3)),
        "tiles": tiles or None,
        "roll": int(roll.group(1)) if roll else None,
        "landed": roll.group(2) if roll else None,
        "passed_start": bool(sal),
        "salary": int(sal.group(1)) if sal else None,
        "square": square,
        "received": int(got.group(1)) if got else 0,
        "balance": num(b.group(1)),
        "bought": bought, "paid": paid,
        "seats": [0, 1, 2],
        "tokens": {"pay": "[pay: {n} to P{k}]", "pay_none": "[pay: none]",
                   "buy": "[buy: {yn}]", "balance": "[balance: {n}]"},
    }
