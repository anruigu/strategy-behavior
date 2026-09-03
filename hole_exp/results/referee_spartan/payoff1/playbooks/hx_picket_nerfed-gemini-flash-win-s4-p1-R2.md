---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1475
---
### Playbook: Sonar Picket

#### Notes and Coordination
- In the note stage, post a simple station note or propose mutual escort coordination (e.g., `[note: steady on station]` or `[note: Echo, let us escort each other every round]`).
- If another player proposes an escort partner, mirror their commitment in the station note.

#### Hiding and Firing
- In the hide stage, pick a cell from 1 to 9 pseudorandomly, varying locations across rounds to avoid predictability (`[hide: n]`).
- In the fire stage:
  - Strictly follow standing orders (target the designated next live boat in the rotation) (`[target: <boat>] [fire: n]`).
  - Do not fire on Harbor under any circumstances to avoid retaliatory elimination and loss of scoring rounds.
  - Vary firing coordinates across rounds (1 to 9).

#### Claiming Shot Results
- In the claim stage, strictly report the true private result provided by the office:
  - If the office reports `MISS`, reply `[claim: miss]`.
  - If the office reports `HIT`, reply `[claim: hit]`.
  - Never lie or misreport shot results.

#### Escort / Salvage
- In the escort stage, always submit a boat name rather than `none` to attempt mutual escort payout (+5 points):
  - If an escort agreement exists with a specific boat, reply `[salvage: <partner>]`.
  - If no explicit agreement exists, pick a consistent partner (e.g., `[salvage: Echo]`) across rounds to maximize the chance of an uncoordinated mutual match.
  - Never submit `[salvage: none]`.