"""Stamp every scored detector mark with the decision it followed.

`Episode` carries `violations[pid][kind]` as a TOTAL, which is the right shape
for every question the atlas has asked so far and the wrong shape for exactly
one: did seat B cheat AFTER seat A did, or before? A total cannot say. This
adds an ordering without touching a single engine, by wrapping the one place
every detector in every family goes through -- `RefereeGame._mark` -- and
stamping each call with the number of ask() calls made so far.

The ask counter is the clock on purpose. Wall time is meaningless (episodes
are driven by a loop, not a schedule) and a round index does not exist in
every engine, but "how many decisions had been taken when this fired" is
defined for all 29 cells and is exactly the order a player experiences.

PURELY ADDITIVE, and it has to stay that way: the timeline lives in the Tape,
never in `ep`, and `_mark`'s return value and side effects are unchanged. The
hole and nohole arms must stay byte-identical under honest play, and a patch
that wrote into the episode could be read by an engine and break that.

    import mark_timeline as MT
    MT.install()
    ep, tape = MT.run_taped(game, policy, seed, arm)
    tape.marks     # [(ask_index, pid, kind, hit, chances), ...]
    tape.asks      # [(pid, phase, prompt), ...]
"""
from __future__ import annotations

import threading
from typing import List, Optional

import referee_games as RG

_ORIG = RG.RefereeGame._mark
_LOCAL = threading.local()
_INSTALLED = False


class Tape:
    """Records every ask, and -- via the patch -- every scored mark."""

    def __init__(self, inner):
        self.inner = inner
        self.asks: List[tuple] = []
        self.marks: List[tuple] = []

    def __call__(self, pid, phase, prompt):
        self.asks.append((pid, phase, prompt))
        return self.inner(pid, phase, prompt)

    def first_hit(self, pid: int, kinds) -> Optional[int]:
        ks = set(kinds)
        for i, p, k, hit, _ in self.marks:
            if p == pid and hit and k in ks:
                return i
        return None


def _patched(ep, pid, kind, hit, chances=1):
    t = getattr(_LOCAL, "tape", None)
    if t is not None and chances > 0:
        t.marks.append((len(t.asks), int(pid), str(kind), bool(hit),
                        int(chances)))
    return _ORIG(ep, pid, kind, hit, chances)


def install() -> None:
    """Idempotent. Thread-local, so a threaded wave keeps its tapes apart."""
    global _INSTALLED
    if not _INSTALLED:
        RG.RefereeGame._mark = staticmethod(_patched)
        _INSTALLED = True


def run_taped(game, policy, seed, arm, p_audit: float = 0.0):
    install()
    t = Tape(policy)
    prev = getattr(_LOCAL, "tape", None)
    _LOCAL.tape = t
    try:
        ep = game.run(t, seed, arm, p_audit)
    finally:
        _LOCAL.tape = prev
    return ep, t
