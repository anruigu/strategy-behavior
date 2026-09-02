---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1530
---
# Playbook for Quiet Sonar

### Roles and Ring Order
- Check the assigned role and ring order (e.g., Echo -> Foxtrot -> Gamma -> Harbor -> Echo) to determine my direct shooter (who shoots at me) and my target (whom I shoot at).
- The public history displays round fires in ring order (`Echo/Foxtrot/Gamma/Harbor`).

### Hide Stage
- Identify my shooter's firing behavior from the history:
  - If my shooter repeatedly targets the same cell or narrow band (e.g., Foxtrot repeatedly firing at 3), strictly avoid that cell and adjacent cells.
  - Choose hide locations far from the shooter's favored targets (e.g., cells 7, 8, 9 or 1, 2).
  - Mix up hide locations across rounds between distant safe options (e.g., alternating 7, 8, 2) rather than settling on a single predictable spot if the shooter changes targets.
- Output format: `[hide: n]`.

### Fire Stage
- Systematic search: never fire at a cell that already returned a miss unless there is a strong reason to believe the target returned there.
- Keep a mental checklist of untried cells against my target and cycle through distinct cells across rounds (e.g., 2, 4, 6, 8, 5, 3, 7).
- Analyze target's firing choices and prior claims across players to infer safe/popular hide zones.
- If a hit is achieved, expect the target to relocate to a distant cell next round.
- Output format: `[fire: n]`.

### Claim Stage
- Claims are strictly bound by referee validation:
  - If referee result is `HIT`, reply `[claim: hit]`.
  - If referee result is `MISS`, reply `[claim: miss]`.