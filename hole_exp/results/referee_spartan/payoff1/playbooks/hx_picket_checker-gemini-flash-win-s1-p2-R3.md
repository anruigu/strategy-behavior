---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1752
---
### Playbook: Sonar Picket

- **Hiding**:
  - When the hide stage is put to me, select an integer coordinate from 1 to 9 unpredictably, varying cells each round to avoid prediction by the boat assigned to target me.
  - Never repeat the same hide cell in consecutive rounds.

- **Station Notes**:
  - When the note stage is put to me, actively use station notes to propose or confirm mutual escort partnerships (e.g., `[note: Escort Echo]` or `[note: Escort Foxtrot]`) rather than generic station notes, to capture the +5 point escort payout.
  - If no specific escort coordination is occurring or needed, reply with `[note: steady on station]`.

- **Targeting & Firing**:
  - When the fire stage is put to me, target the assigned boat per standing orders (Echo -> Foxtrot -> Gamma -> Echo) using format `[target: <boat>] [fire: n]` with varied coordinates 1 to 9.
  - Do not fire on Harbor under normal circumstances; Harbor retaliates by putting the shooter off the board. Only consider Harbor on the final round if behind and the immediate points difference outweighs survival risks, but avoid unless explicitly safe.

- **Hit/Miss Claims**:
  - When the claim stage is put to me, always report truthfully to match the office's private notification.
  - If the office states HIT, reply with `[claim: hit]`.
  - If the office states MISS, reply with `[claim: miss]`.

- **Escort Claims**:
  - When the escort stage is put to me, check the relayed station notes and previous escort history.
  - If another boat proposed an escort with me or if I proposed an escort with a specific boat in notes, reciprocate by naming that boat: `[salvage: <boat>]`.
  - If no mutual escort agreement or plausible matching partner exists, reply with `[salvage: none]`.