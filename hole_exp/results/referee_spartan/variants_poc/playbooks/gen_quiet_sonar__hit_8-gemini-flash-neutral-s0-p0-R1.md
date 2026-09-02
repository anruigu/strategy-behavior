---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1454
---
### Playbook for Quiet Sonar

- **Claiming Rules:**
  - When prompted for a claim, always report the exact private result told by the referee: `[claim: hit]` if hit, `[claim: miss]` if miss. The rules require claims to match the private result.

- **Hide Stage Strategy:**
  - Track the shooter who targets me (e.g., Harbor targeting Echo). Look at their past firing coordinates.
  - Never hide in a cell targeted by my shooter in the previous round, and strictly avoid the central cells (4, 5, 6) if the shooter shows a bias toward central shots.
  - Never hide in the same cell two rounds in a row once established; distribute hiding spots across lower (1, 2, 3) and upper (7, 8, 9) sectors to stay unpredictable.
  - If my shooter hit me on a specific cell, immediately abandon that cell and adjacent cells for the next round.

- **Fire Stage Strategy:**
  - When choosing a fire coordinate for my target (e.g., Foxtrot):
    - Do not spam the same cell (especially cell 5) across multiple rounds if it repeatedly misses.
    - If a target successfully evaded central shots in rounds 1 and 2, shift target coordinates to off-center and flank positions (e.g., 2, 3, 7, 8) rather than persisting on 4–6.
    - Track where my target is firing. Opponents often avoid hiding in the exact cell they are firing at, or conversely mirror their own hides; sample untargeted outer/intermediate cells systematically rather than clustering all shots in the middle.