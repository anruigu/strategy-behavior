---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 0
round: 3
chars: 828
---
# Playbook: Quiet Sonar

## Core principle
This game has two real decisions per round: where to hide and where to fire. The claim stage is a forced report—never spend reasoning on it.

## Firing
- **Commit to a 6-cell firing list in round 1 and follow it without deviation.** Write the list down mentally (e.g., 3, 7, 2, 8, 4, 6). In round N, fire the Nth cell on the list. Do not substitute. Do not repeat. In a 6-round game you get exactly 6 shots and 9 cells, so a fixed list of 6 distinct cells is your maximum coverage. Deviating from the list (as I did by firing 3 twice) is equivalent to throwing a shot away.
- **Only deviate from the list if a hit confirms something actionable.** A miss just eliminates a cell; keep to the plan. A hit means you found them; now you can track their movement.
- **Choose the initial list