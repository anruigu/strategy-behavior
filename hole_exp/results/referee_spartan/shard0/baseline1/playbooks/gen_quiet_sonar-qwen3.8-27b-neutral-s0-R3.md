---
game: gen_quiet_sonar
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 2421
---
# Playbook: Quiet Sonar

**Hiding**

- Round 1: Hide at 9. Everyone fires at 1 in round 1 (universal meta), so 1 is the most dangerous cell. 9 is safe.
- Round 2: Do NOT hide at 9. The meta shifts to 9 in round 2 and I was hit at 9 in round 2 in every single episode I played. Hide at 1 or 2 instead.
- Rounds 3–4: Choose the edge cell farthest from the most-recently-targeted cell in the public fire history. If 8 or 9 is being hammered, hide at 1 or 2. If 1 or 2 is being hammered, hide at 8 or 9. Prefer the extreme (1 or 9) over the adjacent-to-edge (2 or 8) when multiple options are equally safe.
- Rounds 5–6: Hide at 1. The meta consistently shifts to the right side (8, 9) in later rounds, making 1 the safest cell. I survived at 1 in rounds 5 and 6 in all four episodes.
- If I was just hit last round, move to the opposite side of the board, not just an adjacent cell.
- Never hide at 5. The center is a common convergence target.

**Firing**

- Round 1: Fire at 1. This is the universal round-1 target and my best opening shot (2/4 hits across episodes).
- Round 2: Fire at 9. After round 1's universal 1, the meta shifts and my target is almost certainly at 9. This produced a hit in all four episodes (4/4).
- Round 3 onward: Systematically cover edge cells I have not yet tried and missed. Maintain a mental list of which edge cells I have fired at and missed (target was not there) and which I have hit (target was there and has now moved).
- Never fire at the same cell two rounds in a row.
- If I hit my target at cell X, they will move next round. Fire at a different edge, not at X or its immediate neighbor.
- I never fire at a cell I have already shot at and missed in the same game, unless all other edge cells are exhausted.
- Final round: Fire at the cell where I expect my target to be hiding. If the recent meta has been hammering the right side (8, 9), my target is likely on the left—fire at 1. If the meta has been on the left, fire at 9. Do NOT fire at 9 in the final round when the right side has been the danger zone; my target will have moved away from it. (Firing at 1 in the final round hit twice; firing at 9 in the final round missed twice when the right side was the danger zone.)

**Claiming**

- Always claim the true result the referee gave me. A claimed hit scores 4 points and costs the target 1 point; a claimed miss scores 0. There is no strategic benefit to misrepresenting.