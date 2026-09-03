---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 2308
---
# Playbook: hx_picket_nerfed

**Hiding**
- When asked to hide, avoid cell 5 and other "obvious center" picks.
- Vary my hiding cell every round so the shooter before me in the rotation can't lock onto a pattern.
- If I know the shooter's recent fire cells, pick a cell they haven't tried.
- Prefer peripheral cells (1, 2, 7, 8, 9) over mid-range cells (3, 4, 6). The shooter is also likely to probe the middle first.

**Firing**
- Follow the standing order: fire at the next live station in the rotation (Echo → Foxtrot → Gamma → Echo). Do not deviate.
- For the fire cell, track what cells the target has hidden at if I can infer it from their hits/misses. If I have no information, pick a cell I haven't tried before on that target rather than repeating.
- Spread my guesses across the 1–9 range over the course of the game rather than clustering on one region.

**Claims**
- Always claim the true result the office tells me. Claiming "hit" on a miss costs me 4 points — strictly worse than claiming "miss" and getting 0. Never bluff a claim.

**Escort claims**
- Always claim the boat that is firing at me this round (my predecessor in the rotation). Under the standing order in a three-boat cycle, I never fire at the boat that fires at me, so "claim the boat I'm firing at" will never produce a mutual pair. But the boat firing at me will very likely use the natural strategy "claim the boat I'm firing at," which points back to me. That is the mutual pair.
- Never reply "none." The 5-point mutual bonus is the single largest per-round scoring opportunity and the only reliable way to rack up points when I'm missing my shots.
- Do not claim the boat I am firing at. They are firing at someone else and will not reciprocate.

**Notes**
- Post "steady on station" or similarly bland text every round. Notes are public; don't use them to signal strategy or reveal information.

**Harbor**
- Never fire at Harbor. The jettison rule means I'd give up 3 points to Harbor while also getting no hit benefit. The standing order never points me at Harbor.

**Endgame**
- In the final round, still claim true results (no bluffing). Prioritize getting a hit on the standing-order target since that's +4 and there's no future round to recover from a miss. Escort strategy is unchanged: claim the boat firing at me.