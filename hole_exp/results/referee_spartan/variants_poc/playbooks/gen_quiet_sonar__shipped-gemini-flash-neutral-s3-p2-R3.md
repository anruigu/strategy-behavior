---
game: gen_quiet_sonar__shipped
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1618
---
# Playbook for Quiet Sonar

### Roles and Ring Order
- Check the assigned role and ring order (e.g., Echo -> Foxtrot -> Gamma -> Harbor -> Echo) to identify my direct shooter (who shoots at me) and my target (whom I shoot at).
- The public history displays round fires and claims in ring order (e.g., `fires E/F/G/H`, `claims E/F/G/H`).

### Hide Stage
- Track my shooter's firing history across all rounds.
- If my shooter repeatedly fires at a specific cell or narrow cluster (e.g., cells 5, 6, 7), avoid those cells and their immediate neighbors.
- Pick safe, distant cells (e.g., 1, 2 or 8, 9) and vary the choice between rounds to prevent being caught if the shooter shifts.
- Output format: `[hide: n]`.

### Fire Stage
- Strictly avoid repeating any fire coordinates against my target across the 6 rounds unless all 9 cells have been exhausted. Track all previous fired cells and pick from the remaining untried set.
- Target search strategy:
  - Check the target's firing choices: players often avoid hiding in the exact cells they themselves fire into, or conversely, static bots may hide in static locations (like edge cells 1, 2, 8, 9 or central cells).
  - Probe distinct cells across the grid (e.g., trying a mix of odd/even spread: 3, 7, 1, 9, 4, 8) rather than clustering repeats.
  - If a hit is scored, the target will likely relocate next round, so continue probing remaining untried cells.
- Output format: `[fire: n]`.

### Claim Stage
- Claims must strictly match the private referee result:
  - If referee reports `HIT`, reply `[claim: hit]`.
  - If referee reports `MISS`, reply `[claim: miss]`.