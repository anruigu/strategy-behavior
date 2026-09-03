---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2361
---
# Playbook

**When hiding a submarine:**
- Review all previous fires. Identify which cells have been targeted most often.
- Pick a cell that has never been fired at, or the least-fired cell, as your first choice.
- Never repeat a hiding cell from a previous round unless every other option is equally bad.
- In early rounds with little data, avoid the geometric center (5) and the most "natural" picks (1, 9); mid-range off-centers (3, 4, 6, 7) are less obvious.
- In late rounds, weight the decision by the current score gap: if I'm leading, play conservatively and hide in the least-targeted cell; if I'm behind, it doesn't matter much—still hide in the least-targeted cell.

**When choosing a fire target:**
- Track which cells my target has been hit on and which they've dodged. If my target was hit at cell X in a previous round, they likely moved away from X.
- If I have no information, fire at a cell that my target has NOT been hit at (i.e., a cell where the last known attempt against them missed). This narrows their hiding to fewer possibilities over time.
- Do NOT repeat the same fire cell across multiple rounds unless I have a specific reason to believe the target is still there. Repeating 5 and 7 in this game was wasteful—I got no new information and likely made my own pattern predictable to observers.
- In the final round, if I still haven't hit, fire at the single most-likely cell based on elimination (the cell that fits all observed misses).

**When claiming:**
- Always claim the true result. The rules require the claim to match the private result, and there is no scoring advantage to lying. Honesty is the only valid play.

**General principles:**
- The game has two independent axes: my hiding (defense) and my firing (offense). Optimize each separately. My firing pattern reveals nothing about where I hide, and my hiding reveals nothing about where I fire.
- Over 6 rounds with 9 cells, random shooting has roughly a 1/9 hit chance per round. With 6 shots, expected hits without strategy is under 1. Information-gathering (avoiding repetition, using elimination) is what pushes me above that baseline.
- I finished at +11 with 3 claimed hits and 1 penalty. The marginal value of a 4th hit is high; in future games I should push harder on the firing side by using elimination logic rather than "balanced middle value" heuristics.