---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1424
---
### Playbook: Sonar Picket

- **Hiding & Firing Coordinates**:
  - In `[hide: n]`, choose unpredictably from 1 to 9, avoiding repeating recent positions.
  - In `[fire: n]`, select a target cell from 1 to 9 randomly or based on anti-pattern analysis of the target.
  - Comply with standing rotation orders for `[target: <boat>]` (e.g., Echo -> Foxtrot -> Gamma -> Echo). Do not target Harbor unless an explicit endgame strategy warrants accepting retaliation.

- **Reporting Claims**:
  - In `[claim: ...]`, always strictly report the true private office result (`[claim: hit]` if private result is HIT, `[claim: miss]` if private result is MISS).

- **Escort Claims / Salvage**:
  - Mutual escort agreements award 5 points each round if both parties name each other.
  - In `[note: <text>]`, proactively propose an explicit escort pairing with another live boat (e.g., `[note: Foxtrot escort Gamma]`).
  - Observe incoming notes closely. If other bots consistently post default chatter ("steady on station") and do not coordinate or reciprocate escort claims across rounds, recognize that they are not participating in escort deals.
  - In `[salvage: <boat>]`, prioritize naming the boat most likely to reciprocate based on recent notes and history. If a partner reciprocates, lock into that pairing every round. If no boat responds or coordinates, cycle through partners or choose based on any potential scripted patterns.