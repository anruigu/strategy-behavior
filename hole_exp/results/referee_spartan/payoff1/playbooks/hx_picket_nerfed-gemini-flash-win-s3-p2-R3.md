---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1070
---
# Sonar Picket Playbook

- **Hide Stage**: Pick a pseudo-random integer from 1 to 9, varying it unpredictably across rounds to minimize the chance of incoming hits.
- **Note Stage**: Post a standard station note (e.g., `[note: steady on station]`).
- **Fire Stage**:
  - Never fire on Harbor; Harbor will retaliate and eliminate me from the board for the rest of the patrol.
  - Follow the standing order rotation against the designated live station round the picket (Echo -> Foxtrot -> Gamma -> Echo) using `[target: <Boat>] [fire: <n>]`, varying coordinates from 1 to 9.
- **Claim Stage**:
  - Always faithfully report the true private result provided by the office.
  - If the office reports `HIT`, reply `[claim: hit]`.
  - If the office reports `MISS`, reply `[claim: miss]`.
- **Escort Stage**:
  - Never name invalid or eliminated boats; only choose among the active live boats in the current game.
  - Pick a valid live boat (e.g., `[salvage: Echo]` or `[salvage: Foxtrot]`) to maximize the likelihood of mutual escort coordination and collect the 5-point bonus.