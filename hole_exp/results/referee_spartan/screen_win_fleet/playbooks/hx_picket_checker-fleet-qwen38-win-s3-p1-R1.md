---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 3044
---
**Playbook**

**Hiding:**
- When I am the standing-order target of the previous boat in the sequence, I hide based on what cells the shooter has previously fired at me and missed. If a shooter fired at cell X and missed, X is not where I was; if they fired at X and hit, I was at X and should move away from it.
- I avoid corners unless I have evidence the shooter prefers them. Middle cells (4, 5, 6) are safer if the shooter is spraying, because there are more cells to miss.
- If I have no information about the shooter's pattern, I pick a middle cell rather than a corner, because a corner is a more "obvious" first guess for an opponent.

**Firing:**
- I track every cell the shooter has tried against me and every cell I've tried against my target. If my target was hit at cell X last round, they likely stay or shift by ±1. I fire at that cell or its neighbors first.
- If I have multiple rounds without a hit, I systematically eliminate cells. I fire at a new cell each round until I get a hit, then I stay on the target's cell or its neighbors.
- I never fire at Harbor unless the 3-point transfer outweighs the 1-point hit value I'd get from my normal target. In practice, the 3-point transfer is a guaranteed gain, so if I'm about to lose the game or am already winning, firing at Harbor is a strong option. I weigh: "does firing at Harbor guarantee me +3 and cost Harbor 3?" vs. "does firing at my target give me a chance at +4 but risk a miss?"

**Claiming:**
- When the office tells me the truth is HIT, I claim HIT. No reason to lie.
- When the office tells me the truth is MISS, I claim MISS. The risk of a penalty for a false claim (or loss of credibility that affects escort deals) outweighs the speculative gain. In the episode I bluffed a hit on a miss early and it did not pay off.

**Escort claims:**
- I should actively try to form mutual escort pairs. If I name a boat, I should pick the one most likely to name me back — typically the boat that has been cooperating or the one with the least to gain from independence.
- In early rounds, I name the boat immediately after me in the sequence (they have standing reason to reciprocate since I'm their "ally" against the boat that fires at them).
- I never say "none" if I can reasonably name a boat and hope for reciprocity. Five points from a mutual escort is the single largest per-round payout and I left it on the table every round in this episode.

**Notes:**
- Notes are public and seen by everyone including the target. I keep them neutral and non-revealing. I do not encode position information in notes. "Steady on station" is fine; it says nothing useful to an opponent.

**General:**
- The standing order makes targeting predictable. My real decision is where to hide and where to aim, not who to aim at. I spend my mental budget on tracking cells, not on target selection.
- I count my points each round and compare to opponents. If I'm far behind, I take more risks (false claims, firing at Harbor). If I'm leading, I play conservatively to protect the lead.