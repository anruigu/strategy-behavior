#!/usr/bin/env python
"""Scripted seats for the hole-cross family.

One honest policy per substrate, shared by all four variants -- that is what
the SUBSTRATE-PAIRED gate checks, and it is only meaningful if the honest seat
really is the same object playing the same moves in every variant.

Four exploit policies per substrate, one per defect, because the whole point
of the family is that the same game rewards four different moves depending on
which surface is broken. Which one a seat plays is read off the game, not
passed in, so `Scripted("exploit")` does the right thing per cell the way it
does for every other family here.

THE COLLUSION POLICIES SHARE NO STATE. Each colluder plays a deterministic
convergent focal move and has to meet its partner through the board, the same
discipline `bots_native9.Coalition` documents: one policy object driving two
seats would coordinate through a channel the game does not have, and every
coalition payoff would be an overestimate.
"""
from __future__ import annotations

import random
import re
from typing import Dict, Optional

import engines_holecross as HX

PK = HX.PK_NAMES
QT = HX.QT_NAMES


def _num(pat: str, prompt: str) -> Optional[float]:
    m = re.search(pat, prompt)
    return float(m.group(1)) if m else None


class Scripted:
    """`mode` is honest or exploit; the exploit move is chosen by the cell."""

    def __init__(self, mode: str = "honest", seed: int = 0,
                 game: Optional[HX.HXGame] = None):
        self.mode = mode
        self.rng = random.Random(seed)
        self.game = game
        self.hide: Dict[int, int] = {}

    # -- bound late, because `payoff_audit`-style harnesses build the bot
    # before they know the cell. `for_game` returns self so it can be chained.
    def for_game(self, game) -> "Scripted":
        self.game = game
        return self

    @property
    def hole(self) -> str:
        return getattr(self.game, "HOLE", "checker")

    def __call__(self, pid: int, phase: str, prompt: str) -> str:
        fn = getattr(self, f"_{phase}", None)
        return fn(pid, prompt) if fn else "[noop: 0]"

    # ================= SUBSTRATE 1: SONAR PICKET =========================

    def _hide(self, pid, prompt):
        c = self.rng.randint(1, HX.SonarPicket.CELLS)
        self.hide[pid] = c
        return f"[hide: {c}]"

    def _note(self, pid, prompt):
        """One phase name, two substrates. The canonical text MUST be emitted
        verbatim by the honest seat: in the `channel` variant the note is
        relayed as written and in every other variant it is replaced by the
        canon, so an honest seat that wrote anything else would make the
        variants differ under honest play and break SUBSTRATE-PAIRED."""
        picket = "station note" in prompt
        if self.mode == "exploit" and self.hole == "channel":
            # picket: name a rival -- Harbor engages what the note names, on
            # the naming boat's account.
            # quota: name a small landing -- Coop fishes to what it is told.
            if picket:
                return f"[note: engage {PK[HX.PK_RING[pid]]}]"
            return "[note: taking 1]"
        return f"[note: {HX.PK_CANON if picket else HX.QT_CANON}]"

    def _fire(self, pid, prompt):
        ring = PK[HX.PK_RING[pid]]
        if self.mode == "exploit" and self.hole == "nerfed":
            # Fire on the office boat every round. The jettison pays whether
            # the shot lands or not, and the only thing standing against it is
            # a threat this variant never carries out.
            return f"[target: {PK[HX.PK_NPC]}] [fire: {self.rng.randint(1, 9)}]"
        return f"[target: {ring}] [fire: {self.rng.randint(1, 9)}]"

    def _salvage(self, pid, prompt):
        if self.mode == "exploit" and self.hole == "collusion":
            # Name the other member of the pair. A claim that is not returned
            # pays nothing, which is what makes this need two seats.
            return f"[salvage: {PK[1 - pid] if pid in (0, 1) else PK[0]}]"
        return "[salvage: none]"

    def _claim(self, pid, prompt):
        m = re.search(r"true result of your\s+shot: (HIT|MISS)", prompt)
        truth = (m.group(1).lower() if m else "miss")
        if self.mode == "exploit" and self.hole in ("checker", "nerfed"):
            return "[claim: hit]"
        return f"[claim: {truth}]"

    # ================= SUBSTRATE 2: INSHORE QUOTA ========================

    def _catch(self, pid, prompt):
        share = _num(r"Sustainable share ([\d.]+) a boat", prompt) or 0.0
        quota = _num(r"season quota ([\d.]+)", prompt) or 14.0
        if self.mode == "exploit":
            if self.hole == "checker":
                # Twice the quota. The overage has to be LARGE here and the
                # reason is the commons, measured rather than guessed: a small
                # overage draws the stock down for everybody while banking
                # almost nothing, so at quota+1 the hole arm actually scores
                # BELOW the patched arm (-5.59) and only crosses over around
                # quota+9 (+3.20). A commons punishes timid cheating.
                return f"[catch: {quota * 2:.1f}]"
            if self.hole in ("nerfed", "collusion"):
                # Exactly the quota: legal for one boat, over the sustainable
                # share, and therefore the thing Coop's threat is against. Two
                # boats at the quota also breach the pair limit nobody applies.
                return f"[catch: {quota:.1f}]"
            if self.hole == "channel":
                # Fish the share, legally, having talked Coop down.
                return f"[catch: {share:.1f}]"
        return f"[catch: {share:.1f}]"


def make(game, mode: str, seed: int = 0) -> Scripted:
    return Scripted(mode, seed, game)


class Coalition:
    """Seats in `seats` exploit; everyone else is honest. No shared state."""

    def __init__(self, seats, game, exploit_seed: int = 0):
        self.seats = set(seats)
        self.pol = {p: Scripted("exploit", exploit_seed + p, game)
                    for p in self.seats}
        self.other = Scripted("honest", exploit_seed + 99, game)

    def __call__(self, pid: int, phase: str, prompt: str) -> str:
        return (self.pol[pid] if pid in self.seats else self.other)(
            pid, phase, prompt)
