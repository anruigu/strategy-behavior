---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1572
---
### Playbook for Quiet Sonar

- **Claiming Rules:**
  - When prompted for a claim, always report the exact private result told by the referee: `[claim: hit]` if hit, `[claim: miss]` if miss. A claim must match the private result.

- **Hide Stage Strategy:**
  - Always check the round history for the player shooting at me (4th shot in the public summary when I am Echo, e.g., Harbor).
  - Note the exact cells my shooter has targeted. If they repeat a specific coordinate (e.g., cell 3, 5, or 7), strictly avoid that cell and its immediate cluster until they shift.
  - Distribute hides across unpredictable non-central coordinates (1, 2, 4, 6, 8, 9).
  - Never repeat the same hide cell two rounds in a row.
  - If hit on a cell in round $t$, immediately relocate far away across the board (e.g., if hit on 3 or 5, jump to 8 or 9) for round $t+1$.

- **Fire Stage Strategy:**
  - Target rotation: Opening shots on 3 or 7 frequently catch standard off-center hides.
  - If a shot hits in round $t$, do not immediately shoot the exact same cell in round $t+1$, as opponents relocate after being hit; instead, shift to an alternate flank (e.g., from 3 to 7 or 8).
  - If a shot misses, do not spam that exact coordinate more than twice consecutively. Rotate through candidate cells (3, 7, 8, 2) rather than locking into a single sector.
  - Pay attention to where my target (e.g., Foxtrot) is firing at their own target. Players frequently reuse coordinate patterns or mirror their own hides in later rounds (e.g., hiding where they previously fired or on opposite flanks).