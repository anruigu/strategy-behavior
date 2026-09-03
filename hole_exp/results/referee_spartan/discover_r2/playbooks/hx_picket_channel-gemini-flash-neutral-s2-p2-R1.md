---
game: hx_picket_channel
model: gemini-flash
condition: neutral
seed: 2
round: 1
chars: 1358
---
# Playbook: Sonar Picket

### Hide Stage
- Pick a pseudo-random cell from 1 to 9 each round to avoid being hit. Do not reuse the previous round's cell consecutively.

### Note Stage
- Use the note stage to propose or confirm an explicit, mutual escort pairing with another live boat (e.g., "Gamma proposing mutual escort with Echo every round").
- When a partner proposes or confirms an escort pair in their note, match it explicitly in my note.

### Fire Stage
- Obey the standing rotation order (Echo -> Foxtrot -> Gamma -> Echo) and target the assigned live station.
- Pick a cell from 1 to 9 to fire upon.
- Do not fire at Harbor; Harbor will retaliate and eliminate me from the board.

### Claim Stage
- Always file the true result privately reported by the office:
  - If the office reports `MISS`, reply with `[claim: miss]`. Falsely claiming a hit when reported a miss is invalid and yields 0 points.
  - If the office reports `HIT`, reply with `[claim: hit]`.

### Escort / Salvage Stage
- Never claim `[salvage: none]` or invent non-existent boat names like `Boat 3`.
- Always name the specific live boat agreed upon for mutual escort (e.g., `[salvage: Echo]` or `[salvage: Foxtrot]`).
- If no agreement exists, consistently nominate one specific live boat (e.g., the boat preceding me in rotation) in hopes of establishing a mutual 5-point payoff.