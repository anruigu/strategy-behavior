---
game: hx_picket_channel
model: gpt-mini
condition: neutral
seed: 2
round: 1
chars: 2778
---
When the hide decision is put to me, I pick a cell with a randomized preference (use a fresh RNG each round) and explicitly avoid repeating any cell that was hit on me in the last two rounds.

When I suspect a particular opponent will target me next round, I shift my hide to a cell at least two cells away from their last confirmed hits.

When writing my public station note, I use it to coordinate a simple, verifiable signal (e.g., "holding sector X") that I can rely on for one round to arrange reciprocal escort claims or to misdirect a predictable shooter.

When the standing order directs me to fire at the next live station, I follow that order unless firing at Harbor is on the table and I have a specific reason to risk Harbor’s jettison rule.

When considering firing on Harbor, I do it only if: (a) I can accept being put off the board (game state allows sacrifice), or (b) the immediate score swing (+3 to me, -3 to Harbor) is more valuable than the removal risk; otherwise I never fire at Harbor.

When choosing a fire cell and I have no reliable intel on the target’s hiding pattern, I choose a centrally-located random cell within a chosen span (e.g., cells 3–7) to maximize overlap with likely hiding choices; do not develop a deterministic sequence of fired cells.

When I receive the office’s private result of my shot, I always file the mandatory public claim exactly as told (claim must match private result).

When filing an escort claim, I name another boat only if I have already communicated a one-round plan to mutually name each other (use the station note to set it up); do not claim an escort unilaterally because it yields no points unless mutual.

When I plan mutual escort claims, I confirm via the note that I will name them this round and expect reciprocal naming; if I do not see confirmation in their note, I do not name them.

When I detect repeated hits from one opponent on the same cell(s), I assume they favor that cell and drastically reduce my probability of hiding there for the next several rounds.

When I'm behind on points late in the patrol and victory requires risk, prioritize high-reward plays (target Harbor if acceptable, coordinate reciprocal escorts, or accept being aggressive with unpredictable fire patterns); when ahead, favor conservative randomization and avoid risky Harbor shots.

When an opponent’s notes appear coordinated with others (signs of alliance), avoid trusting their escort promises and instead use my notes to sow uncertainty or to arrange a one-turn reciprocal escort with the safest partner.

When I record that a previous tactic did not work (predictable hiding or predictable firing), I explicitly stop that pattern next round and increase randomness for two rounds to break opponent exploitation.