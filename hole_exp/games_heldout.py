"""HELD-OUT TextArena game cells -- transfer instruments, never trained.

`games_tier1.TIER1` collects the five TextArena hole-games that GO INTO the
training mixes. This module collects the ones that must stay OUT of every mix so
they can measure whether an exploit disposition trained elsewhere GENERALISES to
a game the policy has never seen (0819-game-transfer-scaling.md: "did exploit
transfer to other hole/no-hole textarena games that are not in the training
mix?"). `registry` registers these into `ENVS` (so a checkpoint can be sampled
on them and `post_run`'s battery can name them) but keeps them out of `GAMES`,
`SYNTHETIC`, `NATIVE` and `DEEP`, so nothing that builds a training roster can
pick them up by iterating a set.

Both cells use the `GameSpec.logic` hook rather than a fixed exploit token,
because their affordance is state-dependent:

    ta_kuhn         bluff    -- bet the worst card (a J) against an over-folder
    ta_negotiation  extract  -- grab a lopsided trade from an accept-any partner

They are deliberately UNLIKE the trained five (defect / free-ride / betrayal):
a bluff and an extraction are different primitives in different games, so a rate
that moves on them is transfer, not memorised surface.
"""
from __future__ import annotations

import kuhn_game
import negotiation_game

# Same shape as games_tier1.TIER1: a flat list of GameSpec objects.
HELDOUT = [
    kuhn_game.SPEC,
    negotiation_game.SPEC,
]
