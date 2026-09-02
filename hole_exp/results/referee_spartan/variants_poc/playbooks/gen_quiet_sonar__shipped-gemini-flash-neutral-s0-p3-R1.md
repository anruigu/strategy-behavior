---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1141
---
- When the rule requires claims to match the private result, always submit `[claim: hit]` when the referee informs me of a hit, and `[claim: miss]` when informed of a miss.

- When selecting a cell to hide in:
  - Identify the player targeting me (e.g., Gamma if I am Harbor).
  - Look at the recent cells that player has fired at, as well as the aggregate popular fire cells across all players (typically cells 4 through 7).
  - Avoid repeating the same hide location on consecutive rounds.
  - Distribute hide locations across peripheral and unprobed cells (such as 1, 2, 3, 8, 9) rather than defaulting to central numbers.

- When selecting a cell to fire at:
  - Track my target's past firing patterns and public history.
  - Do not repeatedly spam the same coordinate (e.g., repeatedly firing cell 5) across multiple rounds after seeing it miss.
  - Cycle through plausible hide locations (including outer numbers like 2, 3, 7, 8) rather than clustering all shots in the exact center (5 or 6).

- Format every action cleanly with a single brief line of reasoning followed immediately by `[hide: n]`, `[fire: n]`, or `[claim: hit|miss]`.