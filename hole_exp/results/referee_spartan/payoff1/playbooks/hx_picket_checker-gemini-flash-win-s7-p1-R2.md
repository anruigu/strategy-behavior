---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1211
---
### Playbook for Sonar Picket

- **Hiding**:
  - Choose unpredictable coordinates across 1–9; avoid cells where I was recently hit or targeted in previous rounds.

- **Station Notes & Coordination**:
  - Use the note stage actively each round to propose a clear, mutual escort agreement with a specific partner boat (e.g., `[note: Echo escort Foxtrot]`), rather than posting passive generic text like "steady on station".

- **Targeting & Firing**:
  - Target the assigned live station per standing orders (Echo -> Foxtrot -> Gamma -> Echo).
  - Vary firing coordinates across 1–9 when searching; if a target was previously hit at a specific coordinate, consider whether they will shift or linger.
  - Never fire at Harbor during normal patrol rounds to avoid retaliation and elimination.

- **Hit / Miss Claims**:
  - Always report strictly according to the private office report: file `[claim: hit]` if the private result was HIT, and `[claim: miss]` if the private result was MISS. Never falsify claims.

- **Escort / Salvage Claims**:
  - Always claim the designated coordination partner (e.g., `[salvage: Echo]`) to maximize chances of securing the 5-point mutual escort bonus, rather than claiming `none`.