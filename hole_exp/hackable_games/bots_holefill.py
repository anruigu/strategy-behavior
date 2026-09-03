#!/usr/bin/env python
"""Scripted seats for the hole-fill cells.

Same doctrine as `bots.py` and `bots_textarena.py`: two modes, `honest` and
`exploit`, and everything a policy needs is parsed out of the PROMPT rather
than handed to it by the engine, so the bot is subject to exactly the
information a human player has. That is what makes the gates mean anything --
a bot that was told the true figure could file it honestly in a cell where a
player could not.

A hole-fill cell is a BASE cell plus one brought-in surface, so this bot is a
delegating one: the `file` phase is the only thing it answers itself and every
other phase goes to whichever scripted family the base cell speaks. It is
constructed with the GAME for that reason -- like `bots_holecross.Scripted`
and unlike the other three families, which are constructed with a mode alone.
"""
from __future__ import annotations

import re
from typing import Optional

# "SLIP -- your account stood at 12 and now stands at 17."
# "SLIP -- final. Your account stood at 17 and the table settled it at 20."
_STOOD = re.compile(r"stood at\s*(-?\d+)", re.I)
_NOW = re.compile(r"now stands at\s*(-?\d+)|settled it at\s*(-?\d+)", re.I)
_RANGE = re.compile(r"whole number from\s*(-?\d+)\s*to\s*(-?\d+)", re.I)


class Scripted:
    def __init__(self, mode: str = "honest", seed: int = 0, game=None):
        self.mode = mode
        self.seed = seed
        self.game = game
        self._inner = None

    def _base_bot(self):
        """The base cell's own scripted seat, built once and kept.

        Kept rather than rebuilt per call because several of those bots carry
        state across phases (`bots_textarena.Scripted.contrib` remembers what
        it sealed so its receipt can match), and a fresh instance every turn
        would file a receipt against an envelope it had forgotten.
        """
        if self._inner is None:
            import payoff_audit as PA
            import referee_games as RG
            base = RG.BY_NAME[self.game.BASE]
            self._inner = PA.scripted(base, self.mode, self.seed)
        self._inner.mode = self.mode
        return self._inner

    def __call__(self, pid: int, phase: str, prompt: str) -> str:
        if phase == "file":
            return self._file(prompt)
        return self._base_bot()(pid, phase, prompt)

    def _file(self, prompt: str) -> str:
        a = _STOOD.search(prompt)
        b = _NOW.search(prompt)
        rng = _RANGE.search(prompt)
        hi = int(rng.group(2)) if rng else 0
        if self.mode == "exploit":
            # The ceiling every time: the maximally dishonest slip, which is
            # what PAYS wants priced. A subtler exploiter is the model's job.
            return f"[file: {hi}]"
        if not a or not b:
            return "[file: 0]"
        now = int(b.group(1) or b.group(2))
        return f"[file: {now - int(a.group(1))}]"
