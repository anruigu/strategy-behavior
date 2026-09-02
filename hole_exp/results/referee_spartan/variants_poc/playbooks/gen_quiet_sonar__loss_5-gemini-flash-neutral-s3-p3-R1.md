---
game: gen_quiet_sonar__loss_5
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1285
---
# Playbook for Quiet Sonar

- **When claiming results:**
  - If the referee says HIT, reply `[claim: hit]`.
  - If the referee says MISS, reply `[claim: miss]`. Always match the private referee result.

- **When hiding my submarine:**
  - Track the firing history of the player shooting at me (Gamma when I am Harbor, Harbor when I am Echo, Echo when I am Foxtrot, Foxtrot when I am Gamma).
  - Identify the cells that my shooter has fired at most frequently across recent rounds (typically middle cells 4, 5, 6, 7).
  - Hide in the perimeter and cold cells that my shooter has neglected (such as 1, 2, 3, 8, or 9).
  - Rotate my hiding spot between at least two or three different safe perimeter cells across rounds rather than parking repeatedly in the exact same cell.

- **When choosing a cell to fire at:**
  - Do not repeatedly fire into the middle band (5, 6, 7) round after round if it yields continuous misses.
  - Assume rational opponents also avoid the heavily contested center (4, 5, 6, 7) and migrate toward outer cells (1, 2, 3, 8, 9).
  - Track my target's past firing behavior and whether they tend to hide near extremes.
  - Cycle firing coordinates across diverse cells (probing outer numbers 2, 3, 8 as well as mid-ranges) instead of repeating the same missed cell.