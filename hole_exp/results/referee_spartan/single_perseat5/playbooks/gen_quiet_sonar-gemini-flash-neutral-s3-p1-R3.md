---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1290
---
- When hiding:
  - Track where the player shooting at me (Echo -> Foxtrot -> Gamma -> Harbor -> Echo) has fired in recent rounds. Actively avoid cells they have recently targeted, especially coordinates they fire repeatedly.
  - Distribute hides across varied edge and off-center cells (e.g., 1, 2, 3, 7, 8, 9), rotating locations unpredictably across the board rather than sticking to a narrow subset.
  - Never stay in or immediately return to a cell where I was just hit.

- When firing:
  - Never repeatedly fire into the same cell round after round if it results in misses (e.g., do not spam cell 6 across multiple consecutive rounds).
  - Systematically sweep and probe unshot coordinates across different sectors (e.g., 2, 4, 6, 8, 1, 9) when searching for the target.
  - When a shot results in a hit, do not blindly repeat that exact coordinate on the immediate next round since opponents relocate, but consider returning to it in later rounds.
  - Use public firing patterns to infer target behavior: if a target successfully evades certain coordinates, switch to completely fresh cells.

- When claiming:
  - Always strictly report the true private result from the referee: reply `[claim: hit]` when the referee confirms a hit and `[claim: miss]` when the referee reports a miss.