#!/usr/bin/env python
"""Shared parsing helpers for the board adapters.

Every adapter in this package obeys the two rules stated in `__init__.py`: a
view re-presents ONLY what is already in the prompt, and it presents every
legal option with equal weight. These helpers exist so that twenty adapters
do not each grow their own slightly different way of pulling a number out of
a line -- a drifting helper is how a board starts disagreeing with the text
it is drawn from.

ON RULES BLOCKS THAT APPEAR ONCE. Most engines print the rules on the seat's
FIRST prompt and never again: the payoff table, the property list, the letter
values, the lexicon. An adapter therefore returns those fields as `None` on
every later turn, and the client caches the first non-null value it sees for
the session (`UI.memo` in `ui/kit.js`). Re-presenting on turn 6 something the
player was told on turn 1 is still re-presenting the prompt; INVENTING it from
engine constants would not be, which is why nothing here imports an engine.
"""
from __future__ import annotations

import re
from typing import Callable, Dict, List, Optional

# Everything after this is boilerplate about how to format a reply.
_BOILER = re.compile(
    r"^(Keep any reasoning brief|Reply with the bracketed token only)")


def num(s: Optional[str], default=None):
    """'12' -> 12, '100.0' -> 100.0, '+0' -> 0, None -> default."""
    if s is None:
        return default
    s = s.strip().replace("+", "")
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        return default


def one(rx: re.Pattern, text: str):
    """First match, or None. Saves an `if m` at every call site."""
    return rx.search(text)


def body(prompt: str) -> List[str]:
    """The prompt's lines with the trailing format boilerplate dropped."""
    out = []
    for line in (prompt or "").splitlines():
        if _BOILER.match(line.strip()):
            break
        out.append(line.rstrip())
    return out


def collect(prompt: str, rx: re.Pattern, fn: Callable) -> List:
    """Every line matching `rx`, mapped through `fn`, in prompt order."""
    out = []
    for line in body(prompt):
        m = rx.match(line.strip())
        if m:
            out.append(fn(m))
    return out


def loose(prompt: str, rx: re.Pattern, fn: Callable) -> List:
    """As `collect`, but the pattern may match anywhere in the line."""
    out = []
    for line in body(prompt):
        m = rx.search(line)
        if m:
            out.append(fn(m))
    return out


def notes(prompt: str, keep: Callable[[str], bool], limit: int = 6) -> List[str]:
    """Free-text log lines the engine tails onto a prompt, most recent last.

    `keep` decides what counts as a log line for that game. The limit is a
    display limit only -- the full text stays in the `rules` drawer under the
    board, so nothing the engine said is ever unreachable.
    """
    out = [ln.strip() for ln in body(prompt) if keep(ln.strip())]
    return out[-limit:]


RESOURCES = ("wood", "brick", "grain", "ore")


def resource_map(text: str, names=RESOURCES) -> Dict[str, int]:
    """'1 wood, 1 brick, 2 grain, 2 ore' -> {'wood': 1, ...}"""
    out = {}
    for n in names:
        m = re.search(rf"(-?\d+)\s+{n}\b", text)
        if m:
            out[n] = int(m.group(1))
    return out


def named_map(text: str, sep=r"[,;]") -> Dict[str, int]:
    """'wheat 5, wood 3, sheep 5' -> {'wheat': 5, ...}"""
    return {k: int(v) for k, v in re.findall(r"([a-z]+)\s+(-?\d+)", text)}


def scores(text: str) -> List[dict]:
    """'Amber 0, Blue 0, Copper 0' -> [{'name': 'Amber', 'score': 0}, ...]

    Handles the `you 0.0` form the TextArena ports use as well.
    """
    out = []
    # `p1 0, p2 0` is as common as `Amber 0, Blue 0`, so a seat label may
    # carry a trailing index. The `\s+` after it is what keeps the index from
    # swallowing the score.
    for name, v in re.findall(r"([A-Za-z][A-Za-z'’ ]*?\d*)\s+([+-]?\d+(?:\.\d+)?)",
                              text):
        name = name.strip()
        if name:
            out.append({"name": name, "score": num(v)})
    return out


def opts(*labels: str, token: str = "[{}: {}]", verb: str = "") -> List[dict]:
    """A row of equal-weight action buttons, in the order the prompt printed
    them. Nothing here may mark one as primary -- see `__init__.py`."""
    return [{"label": l, "token": token.format(verb, l)} for l in labels]
