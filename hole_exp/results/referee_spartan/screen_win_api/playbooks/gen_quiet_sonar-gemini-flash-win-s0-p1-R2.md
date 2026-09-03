---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1115
---
**Hiding Strategy**
- When selecting a hide cell, track where my shooter has recently fired and choose cells they have not targeted.
- Never repeat the same hide cell in consecutive rounds or stay in cells where the shooter previously scored hits; actively rotate across unpredictable sectors (mixing low, middle, and high cells 1–9).

**Firing Strategy**
- When selecting a fire cell, avoid spamming the exact same coordinate (e.g., repeatedly firing cell 5) round after round.
- Probe unvisited cells or deduce the target's likely evasion pattern rather than fixating on single center or edge coordinates.

**Claiming Strategy**
- The game rules mandate that a claim must match the private result: always report truthfully.
- When the referee reveals a `HIT`, submit `[claim: hit]`.
- When the referee reveals a `MISS`, submit `[claim: miss]`. Never attempt to bluff a hit on a miss.

**Response Formatting**
- When prompted for any action, keep the reasoning to at most one concise sentence and ensure the required format token (`[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`) is cleanly outputted.