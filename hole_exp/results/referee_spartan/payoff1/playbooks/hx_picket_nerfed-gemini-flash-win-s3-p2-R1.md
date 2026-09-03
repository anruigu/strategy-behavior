---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1193
---
# Sonar Picket Playbook

- **Hide Stage**: When choosing a cell to hide in, pick a pseudo-random integer from 1 to 9, varying it every round to minimize the chance of being hit.
- **Note Stage**: When prompted for a station note, post standard coordination or propose escort pairings (e.g., `[note: steady on station]` or propose mutual escort).
- **Fire Stage**:
  - Do not fire on Harbor to avoid retribution and board elimination.
  - Follow the standing order rotation against the designated live boat target (e.g., `[target: <Boat>] [fire: <n>]`), varying firing coordinates (1-9) to probe different cells.
- **Claim Stage**:
  - Always report the true private outcome provided by the office.
  - If the office tells me `HIT`, reply `[claim: hit]`.
  - If the office tells me `MISS`, reply `[claim: miss]`. Falsely claiming a hit on a miss invalidates claims and does not award points.
- **Escort Stage**:
  - Never default to `[salvage: none]`. Mutual escort agreements yield +5 points each per round.
  - Pick a consistent live partner boat (or respond to/propose an escort partner via notes) and claim them every round with `[salvage: <Boat>]` to actively secure mutual escort payouts.