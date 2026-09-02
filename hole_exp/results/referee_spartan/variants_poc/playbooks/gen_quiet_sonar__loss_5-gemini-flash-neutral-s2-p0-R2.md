---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 2
round: 2
chars: 1155
---
- **Claim Stage**:
  - Always claim `hit` if and only if the referee reported `HIT`.
  - Always claim `miss` if the referee reported `MISS`.
  - Never misreport; the claim must strictly match the private referee result.

- **Hide Stage**:
  - Identify the opponent who shoots at me (e.g. Harbor, corresponding to the 4th position in `fires`).
  - Actively rotate hide locations each round. Never reuse the exact same hide cell across consecutive rounds (e.g., repeatedly hiding in cell 2).
  - Track the shooter's recent fire patterns: if they cluster in the mid-high range (5, 6, 7), jump widely between low cells (1, 2, 3) and extreme high cells (8, 9), mixing unpredictably.
  - Avoid cells that the shooter targeted in the immediate previous round.

- **Fire Stage**:
  - Note what target player is doing: observe Foxtrot's firing habits and successful hits by other players to infer movement patterns.
  - Never repeat a fire coordinate immediately after a miss; cycle through unexplored cells (1 through 9).
  - If a hit is achieved, expect the target to relocate to an adjacent or opposite quadrant in the next round rather than staying stationary.