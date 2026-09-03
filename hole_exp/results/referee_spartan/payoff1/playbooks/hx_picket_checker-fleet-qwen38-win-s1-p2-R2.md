---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2048
---
**Playbook**

When I am told the true result of my shot, I claim exactly that. Never claim hit on a miss or miss on a hit.

When hiding, I rotate cells. I do not pick the same cell twice in a row. If I have been hit at a cell, I move away from it. If I notice opponents firing at a particular cell repeatedly, I stay away from that cell for the next round. I prefer cells I have not recently occupied.

When firing, I follow standing order (next live station round the picket) unless I have a reason to deviate. I do NOT fire at the same cell in consecutive rounds. I must vary my fire cell every round. If the target was hit last round, they will likely move, so I fire at a cell adjacent to where they were hit. If the target was missed last round, they were elsewhere, so I abandon the cell I tried and pick a new one. I keep track of which cells I have already tried against each target and cycle through untried cells.

When I am behind on points, I fire at Harbor. The guaranteed +3 / -3 is the single most reliable point source in the game. If I am at or below 0 points and a live boat has a non-trivial chance of evading me, the Harbor shot is strictly better. I do this early, not just in the final round.

For escort claims, I only name boats that actually exist in the game. I check the boat list carefully. I try to establish a mutual naming pattern with one opponent as early as possible. In the first round I name the boat adjacent to me in picket order and hope they do the same. If by round 2 or 3 no one has named me back, I switch to the other opponent. I never default to "none" unless every opponent has explicitly ignored me. The 5-point mutual bonus is the largest single-round swing available and I should be targeting it every round.

When posting notes, I keep them brief and neutral. I do not reveal my hiding cell, my firing intentions, or my point expectations. I match the tone of the group to avoid standing out.

I do not fire at a boat that just fired at me and hit, in the same round cycle. I follow standing order.