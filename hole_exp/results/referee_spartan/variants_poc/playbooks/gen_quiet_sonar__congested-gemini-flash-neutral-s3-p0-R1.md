---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1346
---
# Playbook for Quiet Sonar

### Claim Phase
- When the referee informs me of the shot result, submit that exact result every time (`[claim: hit]` if hit, `[claim: miss]` if miss). The rules strictly require claims to match private results.

### Hide Phase
- In Round 1, avoid the common focal cells (4, 5, 6). Hide in off-center or edge cells like 1, 2, 8, or 9.
- In Rounds 2 through 6, inspect the shooter targeting me (Harbor when I am Echo). Never hide in the cell they fired at me in the previous round or cells they repeatedly target.
- Randomize hiding locations across unused outer cells (e.g., 1, 2, 3, 8, 9) rather than camping repeatedly in the exact same cell (e.g., repeating cell 2 round after round), to prevent the attacker from locking onto a stationary target.

### Fire Phase
- In Round 1, avoid over-focusing on cell 5, since players anticipate central opening shots. Open with varied positions like 3, 4, 6, or 7.
- In Rounds 2 through 6, do not repeatedly fire at the same cell after receiving a miss unless there is a strong structural reason. Systematically sweep unexplored high-probability sectors of my target.
- Track my target's past firing and hiding patterns: if the target is firing heavily in one sector, they may be hiding elsewhere; if they successfully hit, vary fire coordinates to sweep adjacent unhit cells.