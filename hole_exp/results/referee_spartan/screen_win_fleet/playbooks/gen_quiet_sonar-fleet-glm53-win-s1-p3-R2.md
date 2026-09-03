---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2610
---
**Playbook for quiet_sonar**

- Claims are forced: they must match the referee's private truth. When the claim stage arrives, I simply echo the referee's result. No deliberation needed. I must never waste thought here.

- The real scoring lever is hit rate: +4 to me for each hit, -1 to my hider when shot. My fire choice matters more than my hide choice unless I'm being shot often. In this episode I never scored: -0 is the cost of never hitting.

- Firing: targets give no tells, but the fire history gives information. Once a cell misses on my target, that cell is *less* likely — drop it. But my episode showed the other half of the mistake: after switching from 5 to 4, I then fired 4 for five straight rounds and kept missing. Repeating any failed cell is wrong, not just repeating the center. After a miss at cell n on my target, eliminate n and *rotate*: try 4, then 6, then 2, then 8, then 3, then 7, then the extremes 1 and 9. Never fire the same cell at the same target twice in a row, and across six rounds try to cover distinct cells so I probe new ground each round. A target that survives many rounds is likely on a cell nobody has fired at — the history of all fires (mine and others' misses on that player) tells me which cells remain unprobed.

- Hiding: everyone fires center, so hiding at 5 is bad. This episode bore out my instinct: I hid 3, 8, 7, 7 while my predator (Gamma) fired 5s and 4s at me — I was never hit. Hiding at moderately off-center cells (2, 3, 7, 8), away from the observed fire cluster aimed at me, works. Also track which cells have been fired at me specifically across rounds and never reuse a cell that drew fire; vary between rounds so I'm not pattern-readable, but avoid both the center and the extremes.

- Fire history is public and per-target: for my own predator, note their fire cells and hide away from them. For my own target, note my misses and theirs. The round-1 pattern (everyone fires 5) may persist; later rounds showed shooters converging on 4-5 once everyone fled the center — so moderate cells 4 and 6 become hot after round 2, pushing me toward 2, 3, 7, 8 later.

- Points standings tell me when to take risk: if I'm stuck at 0 late (as happened here), I must stop the safe rotation and take genuinely new guesses each round — a guaranteed miss from repeating an old cell is worse than any fresh guess. If I'm ahead, hide safely and keep firing my best-guess unprobed cell.

- Keep reasoning lines short and mechanical; the whole game is the two numbers (hide, fire). Spend the effort on tracking which cells have been fired at whom, not on prose.