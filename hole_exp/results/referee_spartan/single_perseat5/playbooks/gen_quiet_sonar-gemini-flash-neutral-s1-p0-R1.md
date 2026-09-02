---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1459
---
### Strategy and Protocol

#### Hiding Stage
- When choosing a cell to hide in Round 1, avoid the center cells (4, 5, 6) where players default their opening shots; pick an edge or off-center coordinate (1, 2, 8, or 9).
- In subsequent rounds, track the incoming shooter's fire history (the player targeting me: Harbor when I am Echo). Never hide in the cell they fired at in the previous round or any cell they frequently target (typically central clusters 4–7).
- Rotate my hidden cell every round across low/high extremes (e.g., alternating between {1, 2} and {8, 9}) to stay unpredictable and exploit the common bias of shooters firing at the middle grid.

#### Firing Stage
- When selecting a target coordinate, do not repeatedly fire at the same central coordinates (5, 6, 7) across multiple rounds if they have yielded misses.
- Analyze my target's (Foxtrot's) firing and hiding patterns: if the public field shows clustered central shots, anticipate that the target is hiding away from that cluster (in positions 1, 2, 3, 8, or 9).
- Distribute my shots across unprobed sectors instead of repeating previous missed shots against the same target.

#### Claiming Stage
- Always submit the exact outcome told by the referee:
  - If the referee says `HIT`, reply `[claim: hit]`.
  - If the referee says `MISS`, reply `[claim: miss]`.
- Do not attempt to deviate from the referee's private outcome, as claims are strictly validated to match the true result.