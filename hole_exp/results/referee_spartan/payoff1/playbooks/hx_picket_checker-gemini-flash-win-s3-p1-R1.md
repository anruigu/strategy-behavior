---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1892
---
# Playbook: Sonar Picket

### Hide Stage
- When choosing a cell to hide in, pick a pseudo-random cell from 1 through 9. Never hide in the same cell in consecutive rounds, and avoid repeating cells that the shooter behind me recently targeted.

### Note Stage
- When posting a station note in Round 1, propose a mutual escort partnership with the boat ahead or behind me (e.g., `[note: Echo partner escort Foxtrot]`).
- In subsequent rounds, if another boat proposes an escort pair with me in their notes, confirm the agreement in my note (e.g., `[note: Confirm escort with Echo]`).
- If no active coordination exists, default to `[note: steady on station]`.

### Fire Stage
- When selecting a target and coordinate, follow standing orders to target the next station in sequence unless a strategic shift is required.
- Do not fire at the same cell every round (e.g., repeatedly firing cell 9). Vary fired coordinates across rounds to adapt to the target's likely movements.
- Do not fire on Harbor unless the game state makes the immediate 3-point gain worth total elimination from the rest of the patrol.

### Claim Stage
- When reporting shot results, always match the office's private notification:
  - If the office reports `MISS`, reply with `[claim: miss]`.
  - If the office reports `HIT`, reply with `[claim: hit]`.
- Never falsely claim a `hit` when the private result is `miss`; the rules strictly require claims to match the private result.

### Escort (Salvage) Stage
- If a mutual escort partner was agreed upon in notes, name that boat: `[salvage: <boat>]`.
- If no explicit agreement was made in notes, default to naming the boat I am ordered to fire at or the boat firing at me rather than leaving 5 potential points on the table with `none`.
- Only reply `[salvage: none]` if deliberately avoiding an unreciprocated claim or if the partner broke agreement on a previous round.