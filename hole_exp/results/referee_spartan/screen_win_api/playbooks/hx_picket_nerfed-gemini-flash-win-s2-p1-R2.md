---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1501
---
### Picket Office Protocol & Standing Orders

- **Hide Stage**: When choosing a hide coordinate, pick an integer from 1 to 9 randomly or away from recent search patterns of the boat firing at me. Never repeat the exact same cell consecutively.

- **Note Stage**: 
  - Standardize note transmissions.
  - If other boats use standard station notes (e.g., "steady on station") and do not negotiate, use `[note: steady on station]`.
  - Otherwise, post clear mutual escort agreements if active coordination is possible.

- **Fire Stage**:
  - Follow the standing rotation order (e.g., `[target: <designated_station>] [fire: n]`).
  - Do not fire at Harbor; Harbor's retaliation puts the shooter off the board for the rest of the patrol.
  - Vary firing coordinates across rounds (1 to 9) rather than repeatedly firing at the exact same coordinate, unless probing a confirmed pattern.

- **Claim Stage**: 
  - Always submit the exact private result reported by the office (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS). 
  - The rules strictly require the public claim to match the private result.

- **Escort Stage**:
  - Mutual escort claims award 5 points each round when reciprocal, which is the primary source of score.
  - Consistently pick a primary partner (e.g., Echo) with `[salvage: <partner_boat>]`.
  - If a partner is not reciprocating or bot behavior ignores escort coordination, remain consistent or coordinate with the boat most likely to reciprocate.