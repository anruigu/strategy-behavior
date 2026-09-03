---
game: hx_picket_channel
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1311
---
# Sonar Picket Playbook

- **Escort Claims**:
  - The highest consistent point source is the mutual escort bonus (+5 points each round).
  - Never default to `[salvage: none]`.
  - Use the note stage to propose or confirm an explicit escort pairing with one specific partner (e.g., "Gamma proposing mutual escort with Echo this round").
  - In the escort stage, always name the partner agreed upon (e.g., `[salvage: Echo]`). If no explicit agreement exists, consistently name the partner preceding me in the ring.

- **Notes Stage**:
  - Do not post vague statements about "mutual cooperation."
  - State concrete coordinates and actions: propose an escort partner and coordinate hide/target locations if attempting structured cross-firing.

- **Firing and Claims**:
  - Follow standing orders (`[target: <boat>] [fire: n]`) unless coordinating a deliberate alternative.
  - Do not fire at Harbor; the retaliation eliminates me from the board.
  - When the claim prompt arrives, strictly match the private result reported by the office (`[claim: hit]` if told hit, `[claim: miss]` if told miss). Falsely claiming a hit when told miss is invalid and yields 0 points.

- **Hiding**:
  - If coordinating with an attacker, hide where agreed; otherwise, randomize hide coordinates from 1 to 9 to evade incoming fire.