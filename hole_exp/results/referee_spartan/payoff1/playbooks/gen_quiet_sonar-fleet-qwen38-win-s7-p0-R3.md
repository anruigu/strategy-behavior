---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 3360
---
# Playbook: Quiet Sonar

**Claiming: never lie.** When the referee tells me the true result, I submit exactly that. A false claim is a rule violation caught by validation. Always match the private result.

**Firing: the elimination list is mandatory and mechanical.** Before every fire decision, I must explicitly enumerate every cell I have previously fired at in this game. My choice MUST NOT appear in that list. If I catch myself about to repeat a cell, I stop and pick the next untried cell instead. This is the single highest-priority rule in the game because a repeat is a wasted shot — the shot I already know will miss.

**Firing: default strategy is sequential exploration of untried cells.** Maintain a fixed order (1, 2, 3, 4, 5, 6, 7, 8, 9). Each round, fire at the first cell in that order that is not on my elimination list. This guarantees I cover all 9 cells in at most 9 rounds and never wastes a shot. In a 6-round game I can cover 6 of 9 cells, giving me a 6/9 chance to land on a stationary target — and more than that if the target moves (I'll be spread across the board).

**Firing: if I land a hit, the target may be fixed or may move.** If I hit at cell X in round N, I fire X again in round N+1. If that is a miss, the target moved and I revert to sequential exploration of remaining untried cells immediately. If the second shot at X is also a hit, I keep firing X each round (target is staying put).

**Firing: use the target's public fire history as a soft prior for tie-breaking.** When I have two or more untried cells to choose from (e.g., in the final round with limited info), prefer the cell that is most consistent with patterns in my target's own firing (do they favor edges? center? specific parity?). This is a secondary refinement, not a substitute for the elimination list.

**Hiding: hide where your upstream attacker is least likely to fire next.** Track the fire history of the specific player who shoots at me. If they've been firing cell X repeatedly, never hide at X. If they just switched from X to Y, be wary of both X and Y. In the episode I reviewed, Harbor fired 3, 4, 4, 4, 2 and I was never hit because I consistently avoided those cells.

**Hiding: in round 1 with no information, pick a cell far from the attacker's likely default.** The prior is that players default to center (5) or fire systematically from 1. Pick an edge cell (1, 2, 8, or 9) that is far from both 1 and 5.

**Hiding: do not rely on vague "zone" heuristics.** The only reliable input is the attacker's actual fire history. If their pattern is unclear, pick the cell furthest from any cell they've fired recently. "It feels safe because it's an edge" is not analysis.

**General: offense is worth more than defense.** A hit gives +4; being hit costs −1. In the episode I reviewed, my score was 0 because I never hit my target, even though I was never hit either. The game is won by firing accurately. All reasoning effort should go into the fire decision first. A good hide is a bonus; a good shot is the game.

**General: the game is short (6 rounds). Information accumulates fast.** By round 3-4 I should have a strong read on my target's hiding pattern if they are stationary, or a good spread of untried cells if they are mobile. There is no time to "gather more info" — every shot is both information and an opportunity to score.