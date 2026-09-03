---
game: hx_picket_nerfed
model: fleet-qwen38
condition: neutral
seed: 1
round: 1
chars: 2252
---
# Playbook

**Hiding:**
- Never repeat a cell I used against the same target in a previous round. If I hid at cell X and was shot at, move to a cell at least 3 away next time.
- In early rounds, avoid the exact middle (5) since it's the most common first guess.
- In late rounds when I'm ahead, avoid cells adjacent to any cell I've previously used, in case the shooter is tracking my pattern.
- When I'm behind, I should still vary unpredictably — being hit is the enemy of a comeback.

**Firing:**
- Always follow standing order for target.
- Vary the fire cell every round against the same target. Never fire the same cell twice at the same boat.
- Track which cells I've tried against each target and which returned hits vs. misses. If a cell near a previous hit returned a miss, the target moved — expand outward from the last known hit, don't retreat to the last miss.
- In the final round, if I'm leading, I can afford to gamble on an untried cell. If I'm trailing, I should aim at the cell closest to my last hit against that target.

**Escort claims:**
- This is where I lost the most points. I said "none" every round and collected zero escort bonuses.
- Every round, I will name one boat as my escort. The question is which one.
- In round 1, name the boat directly before me in the firing order (the one who just fired at me or is about to). This establishes a pattern.
- In subsequent rounds, check whether the boat I named last round named me back. If they did, name them again — lock in the mutual pair and collect 5 points per round.
- If they didn't name me back, try the other neighbor. In a 3-boat ring, one of the two neighbors is likely to be naming someone; I should be the one they're naming.
- Never say "none." Even a failed escort claim costs nothing; a mutual one pays 5 points.

**Notes:**
- Keep notes bland and consistent. "Steady on station" or similar generic phrasing is fine. No information to leak, no pattern to break.

**General:**
- The escort bonus (5 points per mutual pair per round) is the single biggest source of free points in this game. I will treat it as a primary objective, not an afterthought.
- My goal each round: (1) don't get hit, (2) land a hit, (3) secure a mutual escort. In that priority order.