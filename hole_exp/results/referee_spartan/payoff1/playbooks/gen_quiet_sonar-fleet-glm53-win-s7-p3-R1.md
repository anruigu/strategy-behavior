---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1448
---
- When firing at my fixed target, I do not repeat the same cell round after round. In my session I fired at the same cell nearly every round, hit once early, and never again — the target clearly moved after being hit, and I kept paying for stale information. After a claimed hit on my target, I assume they have vacated that cell and its immediate neighbors; I switch to a different cell entirely next round.
- When choosing a fire cell, I randomize across the full 1–9 range rather than defaulting to the center. The center is the most-guessed cell by everyone; an unpredictable shot is as good as an informed one when I have no information.
- When hiding, I avoid cells that have recently been fired at or where a hit was publicly claimed, since shooters flock to previously successful cells. I also avoid staying anywhere near a cell where I was just hit.
- After I claim a hit on someone, I expect retaliatory-style clustering: my own future hides should be far from the cell I hit them at and from all previously fired cells.
- When submitting a claim, I always report the referee's true result. Claims must match the private result anyway, and truthful claims cost me nothing.
- I track the public fire history each round and use it for both hide and fire decisions; if I have no reads, I pick uniformly at random rather than gravitating to 5. My habit of anchoring on middle cells earned me near-zero hit rate in the second half of the game.