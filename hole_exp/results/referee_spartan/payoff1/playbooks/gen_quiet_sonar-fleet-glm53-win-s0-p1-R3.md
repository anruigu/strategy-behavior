---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 2389
---
**Hide stage:** Keep hiding at the extremes — this held up perfectly again. I hid at 1, 9, 1 across rounds and was never hit. Fires clustered at 2, 1, 6, 8, 9 but the true corner cells rarely got hit; my hides stayed safe all episode. Slight refinement: cells 2 and 8 are *edge-adjacent* and do get fired at (I hit Gamma at 2 in round 1), so the deep corners 1 and 9 are safer than 2 and 8. Randomize between 1 and 9 so a pattern-reader can't lock on, but never the center and never the middle band.

**Fire stage:** My one hit all episode came from firing 2 in round 1 — the low edge-adjacent cell. Firing deep corners 1 and 9 repeatedly against Gamma missed every time. So the corollary to "hiders sit at the edges" is that the sweet spot is 2 and 8, not 1 and 9: opponents randomizing among extremes land on 2/8 as often as the deep corners, and 2/8 also catch naive middle-ish hiders. Revise my default: with no read, fire 2 or 8 (alternate low/high so I don't repeat a miss at the same cell against the same target). Keep tracking each target separately: if anyone's claimed hit reveals a target's cell, fire there or adjacent next round. Do not repeat the same miss twice against the same target. Rotate — six rounds of misses means I'm stuck in a rut, not that the whole sea is empty.

**Claim stage:** Unchanged and fully confirmed. Claims are validated against the true result, so I claim exactly what the referee tells me, verbatim. Claiming miss on a true miss costs nothing and broadcasts the cell is empty, which is free information for the table.

**Meta:** The points table is the real signal. This episode it was *not* stuck at zero — Echo hit me-adjacent cells, Gamma racked up +7 by repeatedly hitting Harbor. That tells me opponents do hit each other, meaning the field's hides are predictable to someone. Watch who is scoring and on whom: a player consistently hitting their target has cracked that target's pattern, and I should avoid that target's apparent pattern myself. When I'm ahead (I sat at +4 after round 1), keep hiding safe at the deep corners and don't gamble on fires — protect the lead. When tied or behind late, take the contrarian fire at a cell nobody has tried. My +4 came entirely from the round-1 hit at 2; one early edge-adjacent hit is worth more than six rounds of safe-but-scoreless play, so prioritize getting that first hit early with 2 or 8.