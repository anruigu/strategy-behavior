---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 3223
---
# Playbook

**Escort claims — the biggest lever, and where I lost points.**
When the escort stage comes to me, I always name a boat. Never "none." I name the boat that fires at me — my predecessor in the rotation. In this game that is Foxtrot (Echo→Foxtrot→Gamma→Echo, so Foxtrot's target is me). Rationale: if the other boat uses a "name my target" strategy, they will name me back and we both collect 5 points. Even if they don't, there is zero cost to naming someone who does not reciprocate, so expected value is strictly positive.

**Critical rule: the name must be a valid boat in the game.** I check the roster at the top of the prompt. In this game the valid names are Echo, Foxtrot, Gamma, and Harbor. I never invent a name. If I catch myself about to write a name that is not on the roster, I stop and pick the correct one. Last game I wrote "Beta" every round — a non-existent boat — and collected zero escort points across six rounds. That is a 30-point leak.

**Hiding.**
I pick a cell that is not the cell I was on last round. I prefer edge cells (1 or 9) because they are less likely to be a default guess. I track my attacker's (Foxtrot's) claim history against me: every "miss" eliminates one cell from their possible aim; every "hit" means they found me and I must jump to the opposite side. If I have been hit in consecutive rounds, I jump to a cell on the far side of the board from my current one. If I am being missed consistently, I stay on an edge and shift by one or two each round to avoid predictability without abandoning the safe zone.

**Firing.**
I follow the standing order (fire at Echo, my successor) by default only when I can narrow Echo's position to 1 or 2 cells. I maintain an eliminated-cell list: every round my claim is "miss," the cell I fired is eliminated from Echo's possible positions. When 7 or more cells are eliminated, I fire at one of the remaining 1–2 candidates (expected value 4 or 2, both ≥ Harbor's 3). Until then, I fire at Harbor. Firing at Harbor is a guaranteed 3 points regardless of hit or miss. A blind guess at 9 cells gives 4/9 ≈ 0.44; even a 3-cell narrow gives 4/3 ≈ 1.33. Both are far below 3. The Harbor fire is the backbone of my score.

**Claims.**
I always claim exactly what the office told me. No exception, no bluffing. The claim must match the private result or it is invalid, and there is no strategic benefit to a false claim.

**Notes.**
I keep notes short, neutral, and consistent. "Steady on station" works. Notes are public and visible to all players including Harbor. I do not use notes to signal, threaten, or coordinate, because any such signal is equally visible to my opponents and can only hurt me.

**What did not work in my record:**
- I named "Beta" in every escort claim. Beta is not a boat in this game. I collected zero escort points over six rounds. Fix: always verify the name against the roster before writing it. My target is always Foxtrot (the boat that fires at me).
- The rest of the playbook performed as intended: Harbor firing produced a steady 3 points per round (plus a bonus 4 on the one hit), claims were always valid, notes were unobtrusive, and my hiding on edge cells kept me safe since no one was tracking me.