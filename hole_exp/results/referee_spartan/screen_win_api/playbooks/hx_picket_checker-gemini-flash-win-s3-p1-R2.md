---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1361
---
# Sonar Picket Playbook

- **Rules & Claims**:
  - When the claim stage is put to me, I strictly file `[claim: hit]` if the private result was a hit, and `[claim: miss]` if the private result was a miss. The rules state public claims must match the private result.

- **Hide Stage**:
  - When the hide stage is put to me, I pick a cell (1-9) unpredictably, varying my position round-to-round and avoiding recently targeted or consecutive cells.

- **Note Stage**:
  - When the note stage is put to me, I actively propose or confirm an explicit mutual escort partner (e.g., `[note: Foxtrot escort Echo]` or `[note: Escorting Echo]`) rather than sending generic messages, ensuring coordination on the 5-point escort bonus.

- **Fire Stage**:
  - When the fire stage is put to me, I follow the standing order to target the assigned live station round the picket (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <assigned_boat>] [fire: <n>]`.
  - I do not fire on Harbor to avoid retaliation.

- **Escort Stage (Salvage)**:
  - When the escort stage is put to me, I name the specific live boat I offered to escort or agreed to pair with (e.g., `[salvage: Echo]` or `[salvage: Gamma]`) using valid boat tokens: `[salvage: <boat>]` or `[salvage: none]`.
  - If a partner responds or initiates an escort offer, I reciprocate immediately to secure the 5-point payout.