---
game: gen_quiet_sonar__hit_8
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1491
---
### Hide Stage Playbook
- Identify which player shoots at me (e.g., Harbor shoots at Echo). Check the recent fire coordinates of that specific shooter.
- Avoid the numbers most frequently fired by my shooter (especially common center-cluster shots like 5, 7, or repeated values).
- When choosing a cell, select pseudo-randomly among outer/uncontested cells (e.g., 1, 2, 3, 8, 9) rather than camping repeatedly on the exact same coordinate across multiple consecutive rounds.
- Never hide on cell 5 or cell 7 unless historical logs prove my shooter never targets those cells.

### Fire Stage Playbook
- Identify my assigned target (e.g., Foxtrot when playing as Echo).
- In round 1, do not default blindly to cell 5; standard players anticipate center shots and hide away from 5, while simple bot targets may cluster around 4, 5, 6, or 7.
- Track my target's past behavior:
  - If my target took hits previously, note where other players fired to hit them or infer their hiding distribution.
  - If past shots missed, rotate through untested cells instead of repeatedly firing at the same miss coordinate (e.g., do not repeatedly shoot 5 after multiple misses).
  - Target cells where the opponent is most likely sheltering (test unprobed mid-to-outer cells: 3, 4, 6, 7).

### Claim Stage Playbook
- Claims must strictly match the private referee result:
  - When the referee result is `HIT`, always submit `[claim: hit]`.
  - When the referee result is `MISS`, always submit `[claim: miss]`.