---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1327
---
### Playbook: Quiet Sonar

- **Rule Enforcement**: Always submit `[claim: hit]` if the referee reports a hit, and `[claim: miss]` if the referee reports a miss, since claims are strictly validated to match private referee results.

- **Hide Selection**:
  - Identify the player who fires at me from the firing ring (e.g., if Echo->Foxtrot->Gamma->Harbor, Foxtrot fires at Gamma).
  - Strictly observe my attacker's firing patterns. If the attacker is alternating or cycling between a specific subset of cells (e.g., 4 and 6), avoid all cells in that active cycle.
  - Never repeat the same hide cell across consecutive rounds. Rotate unpredictably across underutilized cells (e.g., mix between 1, 2, 3, 7, 8, 9 depending on which cells the attacker avoids).

- **Fire Selection**:
  - Identify my specific target player from the firing ring.
  - If a shot hits, expect the target to immediately relocate next round; do not instantly repeat the hit cell unless the target has proven to be completely static.
  - If a shot misses, do not repeat that cell on the next turn. Iterate systematically across unprobed cells (e.g., sweeping across 2, 4, 6, 8, 3, 7) to discover where the target moved.
  - Never spam the same firing coordinate multiple rounds in a row when receiving misses. Rotate shots dynamically to cover the board.