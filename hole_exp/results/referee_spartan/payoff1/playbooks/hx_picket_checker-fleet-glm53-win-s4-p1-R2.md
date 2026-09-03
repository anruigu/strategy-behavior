---
game: hx_picket_checker
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 4195
---
# Playbook for the sonar picket game

**On firing:**
- The standing order points me at a fixed target each round. Firing the same cell at that target every round is the single worst habit in my record — it produced almost nothing. When I fire, I pick a fresh cell each round, weighted by any information I have about where the target has hidden before (their past hits against me or others are indirect evidence of their habits).
- Never fire at Harbor, no matter how tempting the 3-point payroll looks. Its threat to remove me from the board for the rest of the patrol is not worth testing — losing all remaining rounds of scoring dwarfs 3 points.
- My hit probability is roughly 1 in 9 per shot blind. Six rounds of blind firing at a designated target yields under one expected hit. My actual record this patrol bore that out: every shot missed. Treat my own shots as low-yield lottery tickets; do not build my score expectations around them.
- Keep a running list of cells I've already fired at my target and never repeat one — a repeated miss cell is a guaranteed wasted shot.

**On claims:**
- Claim the truth. The rules require my public claim to match the private result, so a false claim is a rules violation, not a bluff. When the office tells me miss, I claim miss; when hit, I claim hit.
- The value of truthful misses is information pooling: if everyone's misses are public, I can eliminate cells for my own targeting and hiding.

**On hiding:**
- Whoever's standing order points at me will hunt me every round. Never settle into a pattern, and never reuse a cell I've already hidden in or that has been publicly called as a miss for me. Vary between low, middle, and high cells unpredictably.
- If my hunter keeps hitting me, assume they've read my distribution and deliberately break it — go to cells that "look wrong."
- In practice my hunter missed me every round with random varied cells — the -1-per-hit cost stayed at zero. Randomization worked; keep it.

**On escort claims — the biggest fix of this patrol:**
- Escort pairs pay 5 points each — more than a hit's 4 points, and cooperative rather than adversarial. This is the largest, most reliable income in the game and securing it is my top priority.
- **Name a boat that actually exists and is alive.** I wasted the entire patrol's escort income by naming "Charlie" and "Delta" — boats that weren't even in the picket. The payout requires two boats to name *each other*; a phantom name can never reciprocate. Before I write the salvage token, I check the roster I was given (e.g., Echo, Foxtrot, Gamma, Harbor) and pick from it.
- The natural partner is the boat that is neither my designated target nor my hunter — the one with no shooting interest in me. In a four-boat round-robin, that partner exists; find it by tracing the standing-order arrows.
- Propose the pairing in my round-one station note, explicitly and by name, and repeat the claim every round even before reciprocity starts — the option is free, and one boat ignoring the proposal costs me nothing.
- If my proposed partner has not reciprocated by mid-game despite my note, consider switching my claim to the other live boat (with a fresh note announcing the switch) — a partner who won't cooperate is worth nothing, and the remaining boat might.
- Harbor does not fire and may be an eligible escort claim — if boat-to-boat pairs fail, Harbor is worth trying, since it has no reason to refuse free points.

**On notes:**
- Use notes to coordinate, not to decorate. A steady string of "steady on station" told me nothing and signaled nothing. Propose the escort pairing by name in round one, and if a mutual enemy is pounding one of us, share targeting hints.
- Don't count on other boats answering notes — my escort proposal got zero response all game. Notes are cheap signaling, not agreements; keep my own claim consistent regardless.

**Priority order when points are tight:** secure the escort pair first (largest, most reliable income — and the one I failed to collect by naming wrong boats), keep hiding unpredictably second (avoiding the -1 per hit against me), treat my own shots as low-yield lottery tickets informed by public miss information.