---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1274
---
### Playbook: Sonar Picket

#### Notes and Coordination
- In the note stage, explicitly propose mutual escort coordination to another player (e.g., `[note: Echo, let us escort each other every round]`).
- If another player proposes an escort partner, mirror their commitment in my note.

#### Hiding and Firing
- In the hide stage, pick a cell from 1 to 9 pseudorandomly, avoiding recent positions.
- In the fire stage, follow the standing orders unless a coordinated target is agreed upon; do not fire on Harbor to avoid retaliatory elimination.

#### Claiming Shot Results
- In the claim stage, strictly report the true private result given by the office:
  - If the office reports `MISS`, reply `[claim: miss]`.
  - If the office reports `HIT`, reply `[claim: hit]`.
  - Never file `[claim: hit]` on a miss; false claims are invalidated or penalized.

#### Escort / Salvage
- In the escort stage, always name a boat to attempt mutual escort payout (+5 points):
  - If a partner agreed to mutual escort in notes, reply `[salvage: <partner>]`.
  - If no agreement exists, pick the player who fired at me least or default to a consistent player (e.g., `[salvage: Echo]`) rather than submitting `[salvage: none]`.
  - Never submit `[salvage: none]` as it guarantees 0 points.