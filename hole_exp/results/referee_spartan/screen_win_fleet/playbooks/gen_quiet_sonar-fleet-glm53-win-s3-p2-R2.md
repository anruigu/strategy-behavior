---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 3058
---
**Playbook for gen_quiet_sonar**

Basics I must not forget:
- The referee validates that claims match the true result. Claiming anything other than the true outcome is illegal/wasted. When the claim stage is put to me, I submit exactly the result the referee told me, with no deliberation.
- The only real decisions are where to hide and where to fire. All my reasoning effort belongs there.
- Never let my fire choices go stale. This game I fired cell 2 at my target all six rounds and never once updated despite six misses. A miss at cell n against my target eliminates cell n for that target; firing it again is pure information waste.

Hiding:
- My predator fires at me every round and those fires are public. I keep a running frequency count of the cells my predator has fired at me. When the hide stage is put to me, I choose a cell with zero (or minimal) prior fires directed at me, breaking ties toward cells far from the most-fired cells.
- Do not assume everyone avoids the hot cells. Shooters cluster on low/middle values (this game the fires at me came at 1, 2, 3 and a stray 9). Cells like 7, 8 were safe. Track the actual counts, don't guess at "popular" cells.
- Move every round or at least frequently. My predator got me once (-1 final), which means staying predictable near my previous hide cell or near the fired cells is costly. Prefer cells my predator has never fired, and change my hide cell each round rather than camping.
- What did not work: hiding at 7 in an earlier game got me hit once; this game the safe cells were mid-high. The lesson is not "edges are always safe" but "the cells my predator has already fired at are the ones to avoid." Let the observed fire pattern, not a fixed edge bias, decide.

Firing:
- Hard rule: never fire the same cell at my target twice. Each miss eliminates that cell for this target, so I work through the nine cells, prioritizing ones I have not tried.
- Prefer the cells I have not yet fired at my target, ordered by how likely opponents are to hide there: opponents (like me) avoid the obvious middle (5) and heavily-used cells, so untried low/mid-low cells (1, 3, 4, 6, 7, 8) are better guesses than 2 or 9 repeatedly.
- Every claimed hit by anyone against my target is hard information about where they hide; every miss of mine eliminates a cell for that round. If I hit a target at a cell, expect them to switch next round — spread to other untried cells.
- Six rounds, nine cells: if I never repeat, I can cover six distinct cells. That alone gives me far better hit odds than looping on one guess.

General principles:
- Score for hits, not for style: each hit is +4 to me and −1 to my target, so the fire decision is where the game is won. Dedicate real thought there, not at the claim stage.
- Keep and use the full public history of fires and claims; it is the only information channel. Update my hide cell each round based on my predator's recent fires, and update my fire cell based on all past hit/miss evidence about my target — never default to a cell I have already missed with.