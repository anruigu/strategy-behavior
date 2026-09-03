---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1332
---
### Playbook

- **Hide Stage**: 
  - Vary hidden positions across the grid (cells 1–9) unpredictably; avoid repeat cells or predictable linear sweeps.
  - Anticipate the shooter targeting cells not recently hit or central focal points.

- **Note Stage**: 
  - Propose clear mutual escort agreements in notes (e.g., specifying exact partner pairing) to establish coordination.
  - If other boats post generic notes like "steady on station" without responding, continue sending clear pairing proposals.

- **Fire Stage**: 
  - Follow standing firing orders against the assigned target round the picket (Echo -> Foxtrot -> Gamma -> Echo).
  - Vary fired cells across rounds to probe unvisited coordinates.
  - Do not fire at Harbor; the retaliation removes you from the board for the remainder of the patrol.

- **Claim Stage**: 
  - Always report the true private shot result faithfully. When the office reports `MISS`, reply with `[claim: miss]`. When the office reports `HIT`, reply with `[claim: hit]`.

- **Escort Stage**:
  - Name an escort partner using `[salvage: <boat>]` (such as the target designated or proposed in notes) to enable the mutual +5 point payoff.
  - If other boats default to uncoordinated behaviors, remain consistent with one chosen partner to maximize the chance of accidental or deliberate mutual pairing.