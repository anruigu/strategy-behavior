"""THREE-PLAYER IPD -- two pairings a round, and a line one of them is on.

Two decisions go in together and the prompt states them as one grammar
(`[rook: ...] [dove: ...]`). The board gives each pairing its own row of two
identical buttons and assembles the pair, so a player is never composing a
two-token string by hand -- and never accidentally sending one token.

The history line reads `you CD (vs Rook/Dove)`, which is dense and easy to
misread by one position. It is redrawn as a grid: one column per pairing, one
row per round, so who defected on whom is a shape rather than a decoding job.

The private line is a free-text box for the same reason sidebar's is: what a
player puts on a channel, unprompted, is the thing worth recording.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect, scores

_HEAD = re.compile(r"ROUND\s+(\d+)\s*/\s*(\d+)\.\s+Totals:\s*(.+?)\.")
_LOG = re.compile(r"^Round\s+(\d+):\s+you\s+([CD])([CD])\s+\(vs Rook/Dove\),"
                  r"\s+Rook\s+([CD])([CD])[^,]*,\s+Dove\s+([CD])([CD])")
_OPEN = re.compile(r"Before round \d+, Rook writes on the private line:\s*\"(.*?)\"")
_NOTE = re.compile(r"Private line from ([A-Za-z]+) \(Dove cannot see this\):\s*\"(.*?)\"",
                   re.S)
_PAY = re.compile(r"both cooperate\s+(\d+)/(\d+); both defect\s+(\d+)/(\d+);"
                  r"\s+defect against cooperate pays the defector\s+(\d+)"
                  r"\s+and the cooperator\s+(\d+)")


def view(phase: str, prompt: str) -> Optional[dict]:
    if phase == "line":
        note = _NOTE.search(prompt) or _OPEN.search(prompt)
        if note is None:
            return None
        text = note.group(2) if note.re is _NOTE else note.group(1)
        return {"kind": "ipd3_line", "from": "Rook",
                "text": " ".join(text.split()),
                "token": "[msg: {text}]"}

    if phase == "table":
        h = _HEAD.search(prompt)
        if not h:
            return None
        pay = _PAY.search(prompt)
        return {
            "kind": "ipd3_table",
            "round": int(h.group(1)), "rounds": int(h.group(2)),
            "totals": scores(h.group(3)),
            "opponents": ["rook", "dove"],
            "options": ["cooperate", "defect"],
            "payoffs": ([int(pay.group(i)) for i in range(1, 7)] if pay else None),
            "log": collect(prompt, _LOG, lambda m: {
                "round": int(m.group(1)),
                "you": [m.group(2), m.group(3)],
                "rook": [m.group(4), m.group(5)],
                "dove": [m.group(6), m.group(7)]}),
            "token": "[rook: {rook}] [dove: {dove}]",
        }
    return None
