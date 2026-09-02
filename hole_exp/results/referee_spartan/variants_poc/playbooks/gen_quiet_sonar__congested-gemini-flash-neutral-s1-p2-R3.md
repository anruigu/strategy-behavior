---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1593
---
### Playbook: Quiet Sonar (Congested)

- **Claim Stage**:
  - Always submit `[claim: hit]` if the referee reported HIT, and `[claim: miss]` if the referee reported MISS. Never deviate from the referee's private outcome.

- **Hide Stage**:
  - Identify who shoots at me in the ring (e.g., Foxtrot -> Gamma) and inspect their past shot coordinates in the round summary.
  - Never hide in a cell targeted by my shooter in the last 2 rounds.
  - Track if my shooter repeats a specific coordinate (e.g., repeatedly firing cell 2); stay clear of that coordinate and its immediate neighbors.
  - Strongly favor off-center and edge cells (1, 8, 9) over congested central cells (4, 5, 6), which attract the majority of exploratory opening shots.
  - Rotate hide locations across distinct safe cells rather than staying static, unless a stubborn shooter is demonstrably locked onto a different cell.

- **Fire Stage**:
  - Maintain a strict elimination list of cells I have already fired at against my target during the game. NEVER re-fire at a cell that resulted in a miss.
  - In early rounds, probe common hiding locations (e.g., 2, 3, 7, 8, 9) systematically without repetition.
  - If I score a hit on my target, do not fire at that exact same cell the following round, as the target will relocate; probe adjacent or opposite unvisited cells instead.
  - Check public history to see where my target fired; players often hide far away from where they shoot, or hide in edges (1, 2, 8, 9).
  - Rotate each shot to a completely fresh, unprobed coordinate each round (e.g., 2 -> 3 -> 7 -> 8 -> 1 -> 9).