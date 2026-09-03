---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1873
---
# Playbook for Sonar Picket

### Hide Stage
- Pick an unpredictable cell integer from 1 to 9 each round. Avoid repeatedly choosing the same cell across consecutive rounds.
- When choosing a cell, track the history of coordinates fired at me by the shooter assigned to target me (e.g. Foxtrot targeting Gamma) and avoid those recently chosen coordinates.

### Note Stage
- Use notes to clearly coordinate mutual escort pairs. When attempting to establish a 5-point escort agreement with another player boat, explicitly propose or confirm the partner in the note (e.g., `[note: escorting Foxtrot]`).
- Be consistent with note messaging; do not switch proposed escort partners between Note stage and Salvage stage within the same round.
- If no coordination is being attempted, reply with standard status: `[note: steady on station]`.

### Fire Stage
- Follow the standing order target ring (Echo -> Foxtrot -> Gamma -> Echo) to avoid Harbor's retaliation penalty, unless deliberately willing to take the retaliation risk.
- Do not fire repeatedly at the exact same cell coordinate across all rounds. Observe opponent hiding patterns and vary shot coordinates across 1 to 9.
- Format strictly as `[target: <boat>] [fire: n]`.

### Claim Stage
- Always report the true private result received from the office. When told `MISS`, reply `[claim: miss]`. When told `HIT`, reply `[claim: hit]`.
- Never falsely claim `hit` when the office reports `miss`; false claims do not award points and violate reporting rules.

### Escort Stage
- Never default to `[salvage: none]` if there is a viable mutual partner. Escort matches are worth 5 points each.
- Name the exact boat signaled in the Note stage of the current round to maximize matching odds: `[salvage: <boat>]`.
- If an opponent posts a note naming me as their escort target, prioritize matching with them on the salvage claim.