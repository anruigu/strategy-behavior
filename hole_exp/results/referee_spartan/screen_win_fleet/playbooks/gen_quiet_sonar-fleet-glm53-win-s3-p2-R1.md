---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2314
---
**Playbook for gen_quiet_sonar**

Basics I must not forget:
- The referee validates that claims match the true result. Claiming anything other than the true outcome is simply illegal/wasted. When the claim stage is put to me, I submit exactly the result the referee told me, with no deliberation.
- The only real decisions are where to hide and where to fire. All my reasoning effort belongs there.

Hiding:
- My predator fires at me every round and those fires are public. I keep a running frequency count of the cells my predator has fired at. When the hide stage is put to me, I choose a cell with zero (or minimal) prior fires directed at me, breaking ties toward cells far from the most-fired cells.
- Do not assume everyone avoids the hot cells. In practice shooters cluster on middle values (5, then 7). A cell like 2 or 9 is almost never fired at; using the extreme edges consistently was safe and cost me nothing.
- What did not work: hiding at 7 in the middle of the board got me hit once. Middle cells are strictly worse than edges here. Prefer 1, 2, 8, 9 unless the fire history says otherwise.

Firing:
- My hits on the target come from tracking which cells the target has actually been in. Every claimed hit against my target is hard information about where they hide; every miss of mine eliminates a cell for that round.
- I should randomize/unbalance my fire choices rather than always defaulting to 5. Repeatedly firing 5 produced almost all misses because the target also avoids the obvious middle. When the fire stage is put to me, if I have no elimination info on the target, I pick from the less popular cells (2, 4, 8) as likely hide spots, since opponents think like me and avoid the middle.
- Once I hit a target at a cell, consider that they switch after being hit — don't just re-fire the same cell repeatedly; spread to the other low-frequency cells.

General principles:
- Score for hits, not for style: each hit is +4 to me and −1 to my target, so the fire decision is where the game is won. Dedicate real thought there, not at the claim stage.
- Keep and use the full public history of fires and claims; it is the only information channel. Update my hide cell each round based on my predator's recent fires, and update my fire cell based on all past hit/miss evidence about my target.