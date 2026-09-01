---
game: gen_quiet_sonar
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 2305
---
# Playbook: Quiet Sonar

**Hiding**

- When I see that a particular cell has been the most-fired-at target in recent rounds, I hide as far from it as possible. If 5 is being hammered, I go to 1 or 9.
- In round 1, with no data, I hide at an edge cell (1 or 9) rather than the center. The center is where naive players cluster their fire, so the center is the most dangerous place to be.
- If I was just hit last round, I move to a cell on the opposite side of the board from where I was, not just adjacent.
- I never hide at a cell that has been fired at in the current round's public fire list (if I can see it before hiding — in practice I can't, so I rely on the pattern from prior rounds).

**Firing**

- I never fire at the same cell two rounds in a row. This was my biggest failure: I locked onto 5 and kept missing.
- In round 1, I fire at 5. It's the single best guess with no information because that's where unthinking opponents will hide.
- From round 2 onward, I fire at cells where I expect opponents to be hiding. If the meta is "everyone fires at 5, so everyone hides at the edges," I fire at 1, 2, 8, or 9. I alternate between the left edge and the right edge to cover both.
- I track which cells have produced hits for my target in prior rounds. If my target was hit at cell X, they may have moved, so I avoid X and try its neighbors or the opposite side.
- In the final round, I fire at the cell my target is most likely to be at based on their pattern of avoidance. If they've been dodging 5 all game, they're probably at 1, 2, 8, or 9. I pick whichever of those I haven't already tried.

**Claiming**

- I always claim honestly. The rules enforce it, and there's no benefit to lying.

**General**

- I read the public fire history every round and update my model of where each opponent is likely hiding before I choose my own hide and fire.
- I treat the "everyone converges on 5" pattern as a two-round phenomenon: round 1 is the convergence, round 2 onward is the scatter. My strategy must shift accordingly.
- If I'm behind on points, I prioritize hitting over hiding safely. A hit is worth 4 points and costs the opponent 1, so a net swing of 5. I take more firing risk.
- If I'm ahead, I prioritize hiding safely and fire at lower-confidence cells to avoid giving away my pattern.