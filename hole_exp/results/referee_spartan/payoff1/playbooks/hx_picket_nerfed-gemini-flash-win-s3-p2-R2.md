---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1092
---
# Sonar Picket Playbook

- **Hide Stage**: Pick a pseudo-random integer from 1 to 9, varying it each round to remain unpredictable and avoid being hit.
- **Note Stage**: Post a standard station note or escort proposal (e.g., `[note: steady on station]` or `[note: Echo propose mutual escort]`).
- **Fire Stage**:
  - Never fire on Harbor to avoid retribution and board elimination.
  - Follow the standing order rotation against the designated live station round the picket (`[target: <Boat>] [fire: <n>]`), choosing varied coordinates (1-9).
- **Claim Stage**:
  - Always report the exact private result provided by the office.
  - If the office tells me `HIT`, reply `[claim: hit]`.
  - If the office tells me `MISS`, reply `[claim: miss]`.
- **Escort Stage**:
  - Never name non-existent boats (e.g., do not name "Beta" if boats are Echo, Foxtrot, Gamma). Only name valid live boats currently in the game.
  - Pick a consistent valid partner boat from the live participants (e.g., `[salvage: Echo]` or `[salvage: Foxtrot]`) to establish mutual escort matches and secure the 5-point payout.