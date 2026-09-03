---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1406
---
# Quiet Sonar Playbook

- When the claim stage arrives, I always claim exactly what the private referee report states: submit `[claim: hit]` if and only if the private report is HIT, and `[claim: miss]` if the private report is MISS. Never submit a false claim.

- When selecting a hide cell:
  - Identify my shooter (the player firing at me in the fixed ring: Echo->Foxtrot->Gamma->Harbor->Echo).
  - Track my shooter's firing history. If my shooter is landing hits or sweeping across certain numbers/sectors, avoid those cells and avoid the immediate trajectory/distribution they target.
  - Never hide in a cell where my shooter just hit me or targeted last round.
  - Never repeat the same hide cell two rounds in a row, even if it feels safe.
  - Spread my hide locations across distinct board sectors (edges 1, 9; near-edges 2, 8; central 3, 5, 7) using unpredictable rotation.

- When selecting a fire cell:
  - Identify my assigned target.
  - Do not spam the same fire coordinate (e.g., repeatedly firing 3 or 4) after getting consecutive misses on that target. Rotate across unexplored cells (1 through 9).
  - Track if my target was hit by someone else (if applicable in context) or deduce where targets tend to hide based on successful hits across the board.
  - Test diverse sectors across rounds (e.g., test an edge 1/9, a mid-point 5/6, an asymmetric cell 2/7/8) until finding a hit pattern.