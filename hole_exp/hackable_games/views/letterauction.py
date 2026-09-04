"""LETTER AUCTION -- bid coins for letters, then spell a word.

Letters are tiles. The rack you have bought, the tile currently up, and the
tile values are three separate lines of prose describing one physical thing,
and a rack of tiles is that thing.

At the word stage the lexicon is drawn as a list with each entry scored from
the letter values the prompt gives, and each entry marked with whether your
rack covers it -- which is a spelling check the player can do by eye off the
same two lines, done for them. Nothing is filtered out and nothing is
pre-selected: the prompt admits `[word: <text>]` for anything, so the box
accepts anything, and the entries a rack does not cover stay on the list.

THE LEXICON AND THE VALUES ARRIVE ON EVERY BID PROMPT and again at the word
stage, so unlike most cells here nothing has to be cached to draw this one.
"""
from __future__ import annotations

import re
from typing import Optional

from .common import collect

_UP = re.compile(r"LETTER\s+(\d+)\s+of\s+(\d+)\s+up for auction:\s+([A-Z])"
                 r"\s+\(worth\s+(\d+)\s+in word scoring\)")
_COINS = re.compile(r"Coins left:\s+(\d+)\.\s+Your letters so far:\s*([^\n]+)")
_OVER = re.compile(r"The auction is over\.\s+Coins left:\s+(\d+)\.\s+Your letters:\s*([^\n]+)")
_VALUES = re.compile(r"Letter values:\s*([^\n]+)")
_LEX = re.compile(r"Lexicon:\s*([^\n]+)")
_RANGE = re.compile(r"\[bid: n\], a whole number from\s+(\d+)\s+to\s+(\d+)")
_MULT = re.compile(r"A word scores\s+(\d+)x the total of its letter values;"
                   r"\s+unspent coins score\s+(\d+)\s+each")
_LOG = re.compile(r"^Letter\s+(\d+)\s+\(([A-Z])\):\s+bids\s+(\d+)\s*/\s*(\d+)\s*--\s*(.+)$")


def _rack(text: str):
    text = text.strip().rstrip(".")
    if text in ("(none)", "none", ""):
        return []
    return [t.strip() for t in text.split(",") if t.strip()]


def _tables(prompt: str):
    v, lx = _VALUES.search(prompt), _LEX.search(prompt)
    values = ({k: int(n) for k, n in re.findall(r"([A-Z])=(\d+)", v.group(1))}
              if v else None)
    lex = ([w.strip().rstrip(".") for w in lx.group(1).split(",")] if lx else None)
    return values, lex


def view(phase: str, prompt: str) -> Optional[dict]:
    values, lex = _tables(prompt)
    mult = _MULT.search(prompt)
    scoring = ({"word": int(mult.group(1)), "coin": int(mult.group(2))}
               if mult else None)

    if phase == "letterbid":
        up, c = _UP.search(prompt), _COINS.search(prompt)
        if not up or not c:
            return None
        rng = _RANGE.search(prompt)
        return {
            "kind": "letter_bid",
            "index": int(up.group(1)), "total": int(up.group(2)),
            "letter": up.group(3), "letter_worth": int(up.group(4)),
            "coins": int(c.group(1)), "rack": _rack(c.group(2)),
            "values": values, "lexicon": lex, "scoring": scoring,
            "lo": int(rng.group(1)) if rng else 0,
            "hi": int(rng.group(2)) if rng else int(c.group(1)),
            "log": collect(prompt, _LOG, lambda x: {
                "index": int(x.group(1)), "letter": x.group(2),
                "bids": [int(x.group(3)), int(x.group(4))],
                "outcome": x.group(5).strip(".")}),
            "token": "[bid: {n}]",
        }

    if phase == "word":
        o = _OVER.search(prompt)
        if not o:
            return None
        return {"kind": "letter_word", "coins": int(o.group(1)),
                "rack": _rack(o.group(2)), "values": values, "lexicon": lex,
                "scoring": scoring, "none_token": "[word: none]",
                "token": "[word: {w}]"}
    return None
