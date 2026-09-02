---
game: gen_quiet_sonar
model: qwen3.8-27b
condition: neutral
seed: 0
round: 2
chars: 1765
---
# Playbook: Quiet Sonar

**Hiding**

- Always hide at an edge cell (1, 2, 8, or 9). Never hide at 5. The center is where round-1 fire converges and it remains a common target even after the meta shifts.
- Choose the edge cell farthest from the most-recently-targeted cell in the public fire history. If 8 is being hammered, hide at 1 or 2. If 1 is being hammered, hide at 8 or 9.
- If multiple edges are equally far from the danger zone, prefer the extreme (1 or 9) over the adjacent-to-edge (2 or 8).
- If I was just hit last round, move to the opposite side of the board, not just an adjacent cell.
- I can also use a "surprise" interior cell (like 4 or 6) if it is far from all recently-targeted cells and I have no reason to believe opponents will probe it. This worked in one episode when I hid at 4 and survived.

**Firing**

- Round 1: Fire at an edge cell (1 or 9), NOT 5. Across all my episodes, firing at 5 in round 1 produced zero hits. Rational opponents hide at edges. I pick 1 as my default, but I will switch to 9 if I have a reason to think my target prefers the left.
- Round 2 onward: Systematically cover edge cells I have not yet tried. My target is almost certainly at an edge. I maintain a mental list of which edge cells I have fired at and missed (target was not there) and which I have hit (target was there and has now moved).
- Never fire at the same cell two rounds in a row.
- If I hit my target at cell X, they will move next round. I fire at a different edge, not at X or its immediate neighbor.
- I never fire at a cell I have already shot at and missed in the same game, unless all other edge cells are exhausted.
- In the final round, I fire at the edge cell I am most confident about based on elimination. If I have missed at 1, 2