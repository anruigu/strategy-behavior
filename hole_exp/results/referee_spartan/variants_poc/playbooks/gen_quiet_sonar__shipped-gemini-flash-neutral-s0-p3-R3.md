---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1390
---
- When the rule requires claims to match the private result, always submit `[claim: hit]` when the referee informs me of a hit, and `[claim: miss]` when informed of a miss.

- When selecting a cell to hide in:
  - Identify the shooter assigned to target me (Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
  - Track that shooter's recent fire history from the round summaries (e.g. the 3rd fire coordinate if Gamma is the shooter) and strictly avoid any cells they have targeted recently.
  - Avoid repeating the same hide location across multiple consecutive rounds, especially if it becomes predictable.
  - Pick unpredictably among unprobed off-center and corner cells (e.g., 1, 2, 4, 6, 8, 9).

- When selecting a cell to fire at:
  - Identify my assigned target (e.g., Echo if I am Harbor).
  - Never fire at the same cell multiple times in a row after receiving a miss.
  - Keep strict track of my own previous fire coordinates against my target and systematically probe previously unfired cells each round (e.g., sweep distinct coordinates like 1, 3, 4, 6, 7, 8, 9 rather than repeating 7 across rounds 4, 5, and 6).
  - If a hit is achieved, consider whether the target tends to repeat or vacate that cell before firing again.

- Format every action cleanly with a single brief line of reasoning followed immediately by `[hide: n]`, `[fire: n]`, or `[claim: hit|miss]`.