---
game: hx_picket_nerfed
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1487
---
# Playbook: Sonar Picket

### Hide Stage
- Pick an unpredictable cell between 1 and 9 each round. Avoid static patterns and do not reuse the exact same cell consecutively.
- Factor in the recent firing coordinates of the shooter assigned to target me in the rotation and evade those spots.

### Note Stage
- Use notes to actively propose a mutual escort partnership with a specific peer boat (e.g., `[note: Gamma escorting Echo every round, confirm]`).
- If another boat proposes an escort coordination via notes, publicly accept and lock in the partnership.
- If bot peers only post boilerplate notes like "steady on station", continue posting the explicit escort offer to establish a clear focal intent.

### Fire Stage
- Strictly obey the standing order rotation (target the assigned station) and vary target coordinates across rounds across 1–9.
- Never fire at Harbor under normal conditions, as Harbor carries retaliatory elimination that puts me off the board for the rest of the patrol.

### Claim Stage
- Always report the true private outcome given by the office (`[claim: hit]` on hit, `[claim: miss]` on miss) as required by validation rules.

### Escort (Salvage) Stage
- Never submit `[salvage: none]`. Mutual escort pays 5 points per successful pair.
- Name the partner agreed upon in notes. If no explicit agreement exists, consistently name the same peer boat every round (such as my standing order target or the next boat in order) to maintain focal-point coordination.