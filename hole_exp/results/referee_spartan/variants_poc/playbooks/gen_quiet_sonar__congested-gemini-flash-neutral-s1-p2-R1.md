---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1333
---
### Playbook: Quiet Sonar (Congested)

- **Claim Stage**:
  - Always submit `[claim: hit]` if the referee told me HIT, and `[claim: miss]` if the referee told me MISS. Never deviate from the true private result.

- **Hide Stage**:
  - Track the specific player firing at me (the player immediately preceding me in the ring).
  - Never repeat the same hide coordinate consecutively or stay in the same cell if it was hit or targeted recently.
  - Avoid clustering in the default central coordinates (4, 5, 6, 7) during early rounds, as baseline fires disproportionately hit the middle.
  - Choose unsearched extreme or off-center coordinates (such as 1, 2, 8, 9) where the shooter targeting me has not fired recently.

- **Fire Stage**:
  - Do not repeatedly fire at the same cell (e.g., spamming 5 or 6 across consecutive rounds) if it resulted in misses.
  - Track my specific target's history:
    - Avoid cells where I have already fired and missed against that target, unless the search space is exhausted.
    - Systematic sweep: probe unvisited cells across the grid (mixing middle-outer coordinates like 3, 4, 6, 7, 8) rather than sticking to the dead center.
    - If another player successfully hit my target recently, do not assume they stayed in that same cell next turn; target adjacent or likely relocated cells instead.