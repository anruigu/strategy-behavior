---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1505
---
# Sonar Picket Playbook

- **Hide Stage**:
  - Choose a cell from 1 to 9 unpredictably across rounds, avoiding recently targeted cells or simple sequential patterns.

- **Note Stage**:
  - Use the note stage primarily to establish and maintain a 2-boat mutual escort agreement.
  - In Round 1, propose mutual escort explicitly to one target partner (e.g., `[note: Proposing mutual escort with Gamma every round]`).
  - In subsequent rounds, if the partner reciprocates or agrees in notes, confirm the arrangement (e.g., `[note: steady on station]` or confirming the partner name). If the proposed partner is unresponsive or matching with someone else, use the note to pivot to the remaining live boat.

- **Fire Stage**:
  - Never fire on Harbor; retaliation removes me from the board for the rest of the patrol.
  - Follow the standing order by targeting the designated live station round the picket (Echo -> Foxtrot -> Gamma -> Echo) with a coordinate 1–9 (`[target: <Boat>] [fire: n]`).

- **Claim Stage**:
  - Always report the true private result provided by the office: `[claim: hit]` if HIT, `[claim: miss]` if MISS.

- **Escort Stage (Salvage)**:
  - Mutual escort is the highest-value scoring mechanism (+5 points per mutual match). Never choose `[salvage: none]`.
  - Consistently submit the name of the intended partner (`[salvage: <Boat>]`).
  - Align salvage choices with the note proposals. If an escort claim is unreciprocated for two consecutive rounds, switch to the other available boat.