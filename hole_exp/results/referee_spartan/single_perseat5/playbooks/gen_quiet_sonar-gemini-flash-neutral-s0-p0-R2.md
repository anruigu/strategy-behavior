---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1293
---
- **Claim Stage**:
  - Always submit the exact outcome provided by the referee: `[claim: hit]` if told hit, `[claim: miss]` if told miss. Never deviate, as claims must strictly match the private result.

- **Hide Stage**:
  - Identify who shoots at me (e.g., Harbor when I am Echo, or the relevant upstream player in the directed cycle).
  - Explicitly parse their past firing history from previous round summaries.
  - Never hide in the cell my shooter targeted in the immediate previous round or targets repeatedly (e.g., persistent fire on 3 or 4).
  - Distribute hiding spots across unpredictable, cold cells (e.g., rotating among 1, 6, 7, 8, 9) rather than staying on the same edge cell across multiple consecutive rounds.

- **Fire Stage**:
  - Coordinates 1–9 represent grid cells.
  - Never fire at the same cell twice in consecutive rounds after receiving a miss.
  - Systematically sweep across the board to maximize search coverage (e.g., rotate through distinct unprobed sectors like 1, 3, 5, 7, 8, 9).
  - Track where my target is hiding if any other information leaks, but primarily execute a diverse sweep across the 6 rounds to maximize the probability of hitting.
  - If a hit is scored on a target, anticipate whether they are likely to relocate to a distant cell next round.