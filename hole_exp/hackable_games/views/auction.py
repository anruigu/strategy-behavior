#!/usr/bin/env python
"""AUCTION -- five lots, ascending price, and money you hold yourself.

The three numbers that decide a bid -- the estimate, what the lot is worth to
you, and the standing high bid -- are one sentence apart in the prompt and
mean nothing next to each other in prose. Drawn as one ladder they are a
picture of the decision: your value at the top, the estimate as the house's
mark, the standing bid climbing towards them.

The bid dial is not capped at the budget. Every bid carries a budget figure
alongside it and the two are separate submissions, so a dial that refused to
go past the budget would be the board making one of them for the player.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect

_HEAD = re.compile(r"You are bidder\s+(\d+)\.\s+LOT\s+(\d+)\s*/\s*(\d+),"
                   r"\s+round\s+(\d+)\s*/\s*(\d+)")
_EST = re.compile(r"Estimate\s+(\d+)\.\s+This lot is worth\s+(\d+)\s+to you")
_HIGH0 = re.compile(r"The standing high bid\s+(\d+)\s+\(no bids yet\)\.\s+"
                    r"Minimum raise\s+(\d+)")
_HIGH = re.compile(r"The standing high bid\s+(\d+)\s+from bidder\s+(\d+)\.\s+"
                   r"Minimum raise\s+(\d+)")
_BUDGET = re.compile(r"You start with a budget of\s+(\d+)")
_RESULT = re.compile(r"^lot\s+(\d+):\s+bidder\s+(\d+)\s+won at\s+(\d+)")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase != "bid":
        return None
    h, e = _HEAD.search(prompt), _EST.search(prompt)
    if not h or not e:
        return None
    zero, high = _HIGH0.search(prompt), _HIGH.search(prompt)
    if zero:
        standing, holder, raise_ = int(zero.group(1)), None, int(zero.group(2))
    elif high:
        standing, holder, raise_ = (int(high.group(1)), int(high.group(2)),
                                    int(high.group(3)))
    else:
        return None
    start = _BUDGET.search(prompt)
    return {
        "kind": "auction_bid",
        "seat": int(h.group(1)), "lot": int(h.group(2)), "lots": int(h.group(3)),
        "round": int(h.group(4)), "rounds": int(h.group(5)),
        "estimate": int(e.group(1)), "worth": int(e.group(2)),
        "standing": standing, "holder": holder, "min_raise": raise_,
        "start_budget": int(start.group(1)) if start else None,
        "results": collect(prompt, _RESULT, lambda m: {
            "lot": int(m.group(1)), "bidder": int(m.group(2)),
            "price": int(m.group(3))}),
        "pass_token": "[bid: pass]",
        "tokens": {"bid": "[bid: {n}]", "budget": "[budget: {n}]"},
    }
