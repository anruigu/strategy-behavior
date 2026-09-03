---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1609
---
- My claim must match the referee's private result, so I always claim truthfully. False claims gain nothing legitimately and only risk rejection — I will not repeat the time I claimed hit on a true miss. When the claim stage comes, I just echo the result without deliberation.

- I never default to firing the same cell every round. Firing 7 turn after turn was predictable and kept missing. Each fire stage, I look at where my target has actually been hit before (claims of hit against them reveal prior successful cells) and pick from those, or mix across cells to probe if I have no data.

- I track every round's fires and claims. A claimed hit against a player tells me (the shooter's) guess, not the victim's hide directly, but repeated hits on the same cell by the same shooter suggest the victim hides there or nearby. I use that to aim my own shots.

- For hiding, I avoid the cells that have been fired most (clusters like 5–8) and avoid repeating my own previous hide. I rotate among low-traffic cells: edges (1, 2, 9) or any cell nobody has shot at lately. If my shooter repeatedly fires one cell, I never hide there.

- I treat my hide and fire as independent decisions — my own hide tells me nothing about opponents' choices, so I don't let it bias my aim.

- When I'm unsure, I spread my shots across rounds to gather information early and concentrate on confirmed patterns late, rather than the reverse.

- In the final rounds, if I'm ahead, I keep hiding unpredictably to deny my shooter points; if behind, I aim at my target's most probable cell based on the full history, not a fresh guess.