---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2753
---
**Playbook for hx_picket_nerfed**

**Claims: always tell the truth.** The rules require my public claim to match the office's private result. Claiming a hit on a miss is a violation and costs me. When the office tells me "hit," I claim hit. When it tells me "miss," I claim miss. No exceptions, no bluffing, no "pressuring" the target. This is the single biggest error pattern I fall into and it must be eliminated.

**Firing: follow standing order and track the target's hide pattern.** I fire at the next live boat in the rotation (for me, that's Gamma). Before firing, I review where the target has been hit or missed in previous rounds. If I hit them at cell X in round N, they will likely move away from X. If I missed them at cell X, they were not there. Use this to narrow their likely cell each round. Avoid re-firing at a cell where I already hit them, since they will have moved.

**Hiding: avoid the cell the boat targeting me is most likely to fire at.** Echo fires at me. I review Echo's recent shots at me: if Echo hit me at cell X last round, they will not re-fire at X (I moved). If Echo missed me at cell X, I was not there, so that cell is safe. My best hide is a cell Echo has not recently fired at, and ideally one that is not adjacent to a cell they've hit (to account for drift). If I have no information, pick a cell that is not the same one I used last round.

**Escort claims: aim for mutual claims.** When two boats name each other, each gets 5 points. I should try to coordinate via notes. If I sense a boat is likely to name me (e.g., they named me last round, or their note suggests cooperation), I name them back. If no coordination is possible, I name the boat I am least likely to be in conflict with. Never default to "none" when a mutual claim is achievable—that is 5 free points.

**Notes: use them for coordination and information.** Notes are public and seen by everyone including Harbor. I use notes to signal intent to other boats (e.g., "I will claim you this round" or a simple recurring phrase that establishes a coordination pattern). I do not leak tactical information about my hide cell or fire target. A stable, low-information note ("steady on station") is fine for rounds where I have nothing to coordinate.

**Harbor: never fire at Harbor.** The penalty (3 points off Harbor onto me, plus being "put off the board") is not worth it unless I am already losing by an insurmountable margin and have nothing to lose. In practice, I almost never fire at Harbor.

**Late-game adjustment:** In the final round, if I am ahead, I play conservatively—hide in a safe cell, fire honestly, claim honestly, and try to lock in a mutual escort claim for bonus points. I do not take risks to extend a lead I already have.