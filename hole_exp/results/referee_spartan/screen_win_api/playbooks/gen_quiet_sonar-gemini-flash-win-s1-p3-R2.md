---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 2081
---
### Playbook for Quiet Sonar

- **Identity and Flow:**
  - Check the prompt to verify my assigned player name, assigned shooter (the opponent firing at me), and assigned target (the opponent I fire at).
  - In claim stages, always claim exactly what the referee privately reported: output `[claim: hit]` if private result is HIT, and `[claim: miss]` if private result is MISS. Never misreport the referee's verdict.

- **Deduction and Reading History:**
  - Parse the public round logs carefully: "fires A/B/C/D, claims a/b/c/d" lists shooters in the standard order (Echo/Foxtrot/Gamma/Harbor).
  - A claimed HIT reveals the exact cell where that player's target was hiding that round.
  - Track where my target hid in previous rounds using the shots fired at them or deduce patterns from their movement.
  - Track where my shooter (e.g., Gamma against Harbor) has been firing and hitting, to anticipate their next targeting pattern.

- **Hide Stage Strategy:**
  - Identify the exact firing history of my shooter. If my shooter has achieved hits (or is repeatedly targeting a specific cluster/cell), immediately relocate away from those coordinates and adjacent cells.
  - Avoid predictable sequences; distribute hides across unpredictable, unprobed edge and mid coordinates (e.g., varying across {1, 2, 7, 8, 9} when central cells {3, 4, 5, 6} are hot).
  - Never repeat a cell where I was just hit in the previous round.

- **Fire Stage Strategy:**
  - Review where my target was previously hit or where they are likely hiding based on past moves.
  - Avoid getting stuck in a repetitive loop (e.g., cycling endlessly between 4 and 6 after repeated misses). Explore the 1–9 board actively by sweeping across untested cells.
  - If my target is an AI that follows a simple or static pattern (or stays hidden in a specific region), shift aim toward their unprobed sectors instead of repeating known misses.
  - If a hit is scored, adjust aim next round to nearby evasion spots rather than blindly repeating the same cell, unless the target shows a persistent tendency not to move.