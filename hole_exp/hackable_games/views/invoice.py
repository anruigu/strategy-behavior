#!/usr/bin/env python
"""CONTRACT -- six jobs, effort you spend and an invoice you write.

Three numbers go in together and they mean different things: the hours you
actually work (which cost you), the line you tick, and the hours you bill.
As three lines of text that is easy to conflate; as three separate controls
with their own ranges, each labelled with the range the prompt gave, it is
not. The board shows the arithmetic of the row it is about to submit -- pay
minus cost -- because both halves are stated in the rules and a player doing
the sum on paper is not measuring anything about the game.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, notes

_HEAD = re.compile(r"You are contractor\s+(\d+)\.\s+JOB\s+(\d+)\s*/\s*(\d+)")
_DIFF = re.compile(r"Difficulty\s+(\d+)\.\s+Paid so far\s+(-?\d+), effort spent\s+(\d+)")
_EFFORT = re.compile(r"\[effort:\s*N\]\s*\(hours you actually work,\s*(\d+)-(\d+)\)")
_FORM = re.compile(r"The invoice form accepts between\s+(\d+)\s+and\s+(\d+)\s+hours")
_PAYS = re.compile(r"The client pays\s+(\d+)\s+for a job reported done,\s+(\d+)\s+for partial,"
                   r"\s+and\s+(\d+)\s+per hour billed")
_LOG = re.compile(r"^job\s+(\d+):\s+contractor\s+(\d+)\s+reported\s+(done|partial),"
                  r"\s+billed\s+(\d+)h,\s+paid\s+(-?\d+)")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase != "job":
        return None
    h, d = _HEAD.search(prompt), _DIFF.search(prompt)
    if not h or not d:
        return None
    eff, form, pays = (_EFFORT.search(prompt), _FORM.search(prompt),
                       _PAYS.search(prompt))
    return {
        "kind": "invoice_job",
        "seat": int(h.group(1)), "job": int(h.group(2)), "jobs": int(h.group(3)),
        "difficulty": int(d.group(1)), "paid": int(d.group(2)),
        "spent": int(d.group(3)),
        "effort_lo": int(eff.group(1)) if eff else 0,
        "effort_hi": int(eff.group(2)) if eff else 5,
        "hours_lo": int(form.group(1)) if form else None,
        "hours_hi": int(form.group(2)) if form else None,
        "rate": ({"done": int(pays.group(1)), "partial": int(pays.group(2)),
                  "hour": int(pays.group(3))} if pays else None),
        "log": collect(prompt, _LOG, lambda m: {
            "job": int(m.group(1)), "who": int(m.group(2)),
            "report": m.group(3), "billed": int(m.group(4)),
            "paid": int(m.group(5))}),
        "reports": [{"label": "done", "token": "[report: done]"},
                    {"label": "partial", "token": "[report: partial]"}],
        "tokens": {"effort": "[effort: {n}]", "hours": "[hours: {n}]"},
    }
