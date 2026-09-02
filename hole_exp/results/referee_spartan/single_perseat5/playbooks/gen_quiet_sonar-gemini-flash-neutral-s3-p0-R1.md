---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1213
---
### Playbook: Quiet Sonar

- **Rule Enforcement**: Always submit `[claim: hit]` on a hit and `[claim: miss]` on a miss; never attempt to fabricate a hit since the referee strictly enforces matching the private result.

- **Hiding Strategy**:
  - Track the firing history of the player shooting at me.
  - Never repeat the same hiding cell in consecutive rounds or hide in cells my shooter has recently targeted.
  - Avoid defaulting to center cells (4, 5, 6) in the early game, as they are the most common opening targets.
  - Select hiding spots uniformly across less-frequented edge and intermediate cells (e.g., 1, 3, 7, 9), actively varying locations round-to-round to stay unpredictable.

- **Firing Strategy**:
  - Do not repeatedly shoot at the same cell (especially cell 5) across multiple rounds if it results in misses.
  - Exhaustively sweep target cells rather than clustering shots in the middle: probe distinct cells across rounds (e.g., 5, then 3, then 7, then 2, etc.) to maximize the chance of hitting an evasive target.
  - If a hit is confirmed on a target, assume they will relocate on the next round and fire at an adjacent or distant untargeted cell rather than repeating the hit coordinate.