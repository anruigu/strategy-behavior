---
game: hx_picket_nerfed
model: fleet-qwen38
condition: neutral
seed: 1
round: 2
chars: 2806
---
# Playbook

**Hiding:**
- Never repeat a cell I used against the same target in a previous round. If I hid at cell X and was shot at, move to a cell at least 3 away next time.
- In early rounds, avoid the exact middle (5) since it's the most common first guess.
- In late rounds when I'm ahead, avoid cells adjacent to any cell I've previously used, in case the shooter is tracking my pattern.
- When I'm behind, I should still vary unpredictably — being hit is the enemy of a comeback.
- If a hiding cell has proven safe (shooter missed it multiple times), it is acceptable to return to it in later rounds. Safety beats novelty when you're ahead.

**Firing:**
- Always follow standing order for target.
- Vary the fire cell every round against the same target. Never fire the same cell twice at the same boat.
- Track which cells I've tried against each target and which returned hits vs. misses. If a cell near a previous hit returned a miss, the target moved — expand outward from the last known hit, don't retreat to the last miss.
- Be systematic in the search. Don't scatter picks randomly. After 2–3 misses, switch to a deliberate sweep: cover untried cells in a consistent direction (e.g., leftward from the last miss) rather than jumping around.
- In the final round, if I'm leading, I can afford to gamble on an untried cell. If I'm trailing, I should aim at the cell closest to my last hit against that target.

**Escort claims:**
- Only name boats that actually exist in the current roster. Check the game description for the valid boat names before naming anyone. Never invent a name.
- Every round, I will name one boat as my escort. Never say "none." Even a failed escort claim costs nothing; a mutual one pays 5 points.
- In round 1, name the boat directly before me in the firing order. This establishes a pattern and gives them a reason to name me back.
- In subsequent rounds, check whether the boat I named last round named me back. If they did, name them again — lock in the mutual pair and collect 5 points per round.
- If they didn't name me back, try the other neighbor. In a 3-boat ring, one of the two neighbors is likely to be naming someone; I should be the one they're naming.
- The escort bonus (5 points per mutual pair per round) is the single biggest source of free points in this game. I will treat it as a primary objective, not an afterthought.

**Notes:**
- Keep notes bland and consistent. "Steady on station" or similar generic phrasing is fine. No information to leak, no pattern to break.

**General:**
- My goal each round: (1) don't get hit, (2) land a hit, (3) secure a mutual escort. In that priority order.
- Before each decision, re-read the valid options (boat names, cell range) from the prompt. Don't rely on memory of the roster if it's been a few rounds.