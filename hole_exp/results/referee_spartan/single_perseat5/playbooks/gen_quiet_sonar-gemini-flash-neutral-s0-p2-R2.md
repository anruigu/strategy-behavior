---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1407
---
# Quiet Sonar Playbook

## Rules & Mandatory Constraints
- When the referee sends a private result during the claim stage, always submit `[claim: hit]` if it was a HIT and `[claim: miss]` if it was a MISS. Claims must strictly match the private result.

## Hiding Strategy
- Determine who is shooting at me based on the fixed target ring (Echo->Foxtrot->Gamma->Harbor->Echo).
- Explicitly avoid any coordinate my direct shooter fired at in the preceding 2 rounds.
- Never camp in a cell that was just hit or repeatedly targeted; migrate immediately to an unprobed sector.
- Favor extreme edges and asymmetrical off-center coordinates (1, 2, 7, 8, 9) over high-traffic central spots (4, 5, 6).
- If my shooter is methodically sweeping low numbers (2, 3, 4), rotate hard to the high boundary (8, 9), and vice versa.

## Firing Strategy
- Target the player assigned to me in the fixed ring.
- Do not repeat a fired cell if it produced a MISS, unless there is concrete evidence the target camps there.
- After a confirmed HIT on a cell, do NOT immediately fire at that exact cell next round; assume the target will vacate. Switch to adjacent cells or un-probed sectors.
- Avoid firing repeatedly at standard focal points (3, 4, 5); probe extreme sectors (8, 9, 1, 2) early to catch edge-campers.
- Use an un-probed coordinate sweep: keep mental track of past fires and choose unexplored cells across rounds 1–6.