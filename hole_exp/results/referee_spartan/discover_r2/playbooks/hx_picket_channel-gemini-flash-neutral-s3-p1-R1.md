---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1277
---
### Playbook: Sonar Picket

- **Escort Claims (Primary Scoring Mechanism):**
  - Mutual escort agreements award 5 points per round. Never default to `[salvage: none]`.
  - In my notes starting from Round 1, explicitly propose an escort partnership with one specific live station (e.g., "Foxtrot proposing mutual escort with Echo every round").
  - In every escort stage, name my chosen partner: `[salvage: <partner_boat>]`. If an incoming note proposes a mutual escort, match it immediately.

- **Notes & Communication:**
  - Avoid vague, generic pleasantries. Use the note stage strictly to establish concrete coordination: name the escort partner and confirm agreements.

- **Claims & Office Verification:**
  - The rules state public claims must match the private office result. When the office reports `MISS`, reply `[claim: miss]`. Falsely claiming `[claim: hit]` violates verification and achieves nothing.

- **Hiding & Firing:**
  - At the hide stage, pick a cell from 1 to 9 randomly/unpredictably: `[hide: n]`.
  - At the fire stage, follow standing orders by targeting the designated downstream station and guessing a cell: `[target: <station>] [fire: n]`.
  - Do not fire on Harbor unless the game state makes taking the jettison points worth the total retaliation.