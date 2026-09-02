---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1605
---
### Roles and Structure
- I identify the player firing at me (the shooter before me in the cycle) and the player I am firing at (my target).
- Every hit scored gains 4 points; every hit sustained costs 5 points. Defensive survival is higher priority than offensive guessing.

### Hiding Strategy
- When hiding, avoid the heavily congested middle cells (4, 5, 6, 7), especially early in the game when players default to center-probing.
- In Round 1, hide in the outer sectors (e.g., 1, 2, 8, or 9).
- In Rounds 2 through 6:
  - Check the historical fire coordinates of the player who targets me.
  - Never hide on the coordinate that my shooter targeted in the previous round or targets repeatedly.
  - Choose unprobed peripheral coordinates (1, 2, 8, 9) and vary them across rounds rather than remaining stationary.

### Firing Strategy
- When selecting a fire target, track my target's past hiding locations if revealed, as well as the fire history directed at them.
- Do not blindly repeat the same fire coordinate (e.g., repeating 7) round after round if it yielded a miss.
- Probe high-probability cells systematically: start near the center-offset (4, 5, 6), but quickly branch to outer quadrants if misses persist.
- If I successfully hit a target on cell $k$ in round $r$, assume they will vacate cell $k$ for round $r+1$; switch fire to adjacent or peripheral cells.

### Claiming Strategy
- When prompted for a claim, always match the referee's private result:
  - Submit `[claim: hit]` if and only if the referee reported HIT.
  - Submit `[claim: miss]` if and only if the referee reported MISS.