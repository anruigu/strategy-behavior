#!/usr/bin/env python
"""Scripted seats for the hole-fill cells.

Same doctrine as `bots.py` and `bots_textarena.py`: two modes, `honest` and
`exploit`, and everything a policy needs is parsed out of the PROMPT rather
than handed to it by the engine, so the bot is subject to exactly the
information a human player has. That is what makes the gates mean anything --
a seat that could read engine state would play a cell straight where a player
could only guess, and the arm difference would be measuring the bot's
privilege rather than the hole.

THIS SEAT CARRIES NO POLICY OF ITS OWN. A nerfed cell is the shipped
substrate with a notice on top: `Nerfed.run` answers its NPC seats inside the
engine and hands the focal seats the base cell's own phases, in the base
cell's own bracket vocabulary, with nothing done to the text but the deterrent
NOTICE and any FINDING prepended to it. There is therefore no phase left for
this class to answer that the base family does not already answer better, and
every call goes straight through. What the class contributes is the LOOKUP:
it resolves `game.BASE` to the substrate and builds that substrate's scripted
seat through `payoff_audit.scripted`, which is the one thing a caller holding
only an `hf_*` cell cannot do for itself.

It is constructed with the GAME for that reason -- like `bots_holecross
.Scripted` and unlike the other three families, which are constructed with a
mode alone. Without the cell there is no `BASE` to resolve, and no way to know
which family's vocabulary the prompt is going to be written in.

THE DETERRENT IS DELIBERATELY NOT READ. The notice is prose that no base
family's regexes match, so the delegated policy plays through it as though it
were not there -- and that is the behaviour PAYS wants, not an oversight. A
scripted seat that backed down when it saw a threat would fold the deterrent's
effect into the policy and make both arms look alike, when the whole
measurement is that the same unflinching move is punished in `nohole` and free
in `hole`. Backing down is the model's job to discover, not the yardstick's.
"""
from __future__ import annotations


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
        # Caching the inner bot means it would otherwise be frozen at whatever
        # mode this object held on its first turn. Harnesses do flip `mode` on
        # a live scripted seat rather than building a second one -- that is how
        # `Nerfed.router` drives its own grim NPCs -- so the mode is re-read
        # from the outer object every call and `self.mode` stays the single
        # answer to which policy this seat is playing.
        self._inner.mode = self.mode
        return self._inner

    def __call__(self, pid: int, phase: str, prompt: str) -> str:
        return self._base_bot()(pid, phase, prompt)
