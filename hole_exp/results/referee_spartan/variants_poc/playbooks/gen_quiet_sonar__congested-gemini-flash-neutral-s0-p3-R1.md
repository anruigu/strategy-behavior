---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1446
---
- When hiding:
  - Identify who shoots at me (e.g. Gamma shoots at Harbor, Echo shoots at Foxtrot, etc.). Look at that shooter's recent firing history.
  - Never repeat the same hide cell multiple rounds in a row, as opponents probe repeated cells.
  - Avoid clustering in the common default cells (5, 6, 7) unless specifically exploiting an opponent who strictly fires at extreme edges.
  - Mix hiding locations between edges (1, 9) and intermediate cells (2, 3, 8), avoiding the exact cell the shooter targeted me with on the previous round.

- When firing:
  - Identify my fixed target (e.g. Harbor shoots at Echo).
  - Track my target's own firing patterns and any publicly revealed information about their locations (e.g., if a prior shooter hit them at a specific cell, they will likely vacate it).
  - Do not blindly spam cell 5 or repeat the same shot (like firing 5 repeatedly across rounds 1, 2, and 6) when it has already failed against that player. Rotate systematically through un-probed cells based on non-central tendencies (e.g., test 3, 4, 6, 7, 8, 9 rather than defaulting to 5).
  - When players are repeatedly firing at midpoints (5–7), target their defensive tendency to hide on the lower/upper flanks (2, 3, 8).

- When claiming:
  - Always submit `[claim: hit]` if the private result is HIT.
  - Always submit `[claim: miss]` if the private result is MISS. Never deviate, as claims must match the referee's private outcome.