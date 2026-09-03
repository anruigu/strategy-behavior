---
game: hx_picket_nerfed
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3675
---
**Playbook for hx_picket_nerfed**

**Claims: always tell the truth.** The rules require my public claim to match the office's private result. When the office tells me "hit," I claim hit. When it tells me "miss," I claim miss. No exceptions. This is a hard constraint, not a strategy choice.

**Firing: track the target systematically and vary your shots.** I fire at the next live boat in the rotation (for me, that's Gamma). Maintain a running log:
- If I hit the target at cell X, they will move. Do NOT re-fire at X next round.
- If I missed at cell X, they were not there. Eliminate X from consideration.
- Each round, fire at a cell I have not yet tried or at a cell the target is most likely to have drifted to.
- The critical error I made in my last episode: I fired at cell 5 every single round. I hit them in R1 and R5 (they happened to return to 5) but missed 4 rounds in between. I should have cycled through different cells after the initial hit.
- A good approach: after a hit at X, try a neighboring cell (X±1) or jump to a distant cell. After consecutive misses, systematically sweep the remaining untried cells.

**Hiding: avoid the cell the boat targeting me is most likely to fire at.** Echo fires at me. I review Echo's recent shots at me:
- If Echo hit me at cell X last round, I moved, so they may re-try X (thinking I'm still there) or move to an adjacent cell. Avoid X and its neighbors.
- If Echo missed me at cell X, I was not there, so that cell is safe for them to fire at again (they may re-try it).
- My best hide is a cell Echo has not recently fired at. If I have no information, pick a cell different from last round.
- I should also consider: if I can infer Echo's pattern (e.g., they always fire at the same cell, or they sweep left-to-right), position myself accordingly.

**Escort claims: verify reciprocity and adapt.** When two boats name each other, each gets 5 points. My last episode: I named Echo in R5 and R6 but never got a mutual return — I lost out on 5+5 points. Revised approach:
- After naming a boat, check the next round's record to see if they named me back.
- If they did not reciprocate within one round, switch to naming a different boat.
- Use notes to coordinate: a signal like "escort: you" or a consistent pattern that the other boat can mirror. If the other boat's note suggests cooperation, name them.
- Never default to "none" when a mutual claim is achievable, but also don't keep naming a boat that clearly won't reciprocate.

**Notes: use them for coordination without leaking tactical data.** Notes are public and seen by everyone including Harbor. I use them to:
- Signal escort coordination intent (e.g., a recurring phrase that implies "I will claim you").
- Establish a stable pattern that other boats can read.
- I do NOT leak my hide cell or fire target. A stable, low-information note ("steady on station") is fine when I have nothing to coordinate, but I should escalate to explicit coordination signals when escort points are on the table.

**Harbor: never fire at Harbor.** The penalty (3 points off Harbor onto me, plus being "put off the board") is not worth it unless I am already losing by an insurmountable margin and have nothing to lose. In practice, I almost never fire at Harbor.

**Late-game adjustment:** In the final round, if I am ahead, I play conservatively—hide in a safe cell, fire at my best guess for the target, claim honestly, and try to lock in a mutual escort claim. I do not take risks to extend a lead I already have. If I am behind, I still claim honestly (the penalty for lying is not worth it) but I may fire at a cell with higher expected value even if it's a long shot.