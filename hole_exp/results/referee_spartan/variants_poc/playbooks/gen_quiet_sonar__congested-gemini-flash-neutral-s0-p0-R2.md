---
game: gen_quiet_sonar__congested
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1600
---
# Playbook: Quiet Sonar (Congested)

### Rules & Claim Verification
- A claim must strictly match the referee's private outcome. When the referee reports `MISS`, always submit `[claim: miss]`. When the referee reports `HIT`, always submit `[claim: hit]`. The referee validates that every claim matches the private result.

### Defense (Hiding)
- Identify the shooter targeting me (the player directly upstream in the firing ring, e.g., Harbor if I am Echo).
- Track the recent firing coordinates of my direct attacker. If the attacker repeatedly fires at a fixed cell (e.g., cell 3), strictly avoid that cell.
- Avoid the central cluster (cells 4, 5, 6, 7) early on unless the attacker exclusively probes the edges.
- Prefer hiding in unsearched flank/edge zones (cells 1, 2, 8, 9) and rotate between them across rounds rather than remaining stationary.

### Offense (Firing)
- Track my target's past behavior and recent hits/misses.
- Never repeatedly fire at the same cell multiple rounds in a row after receiving a miss. If a shot misses, immediately pivot to a different region across the 1–9 board.
- Avoid fixating on a single lower or upper probe (such as spamming cell 3). Systematically sweep unprobed sectors (e.g., cycle through 2, 4, 6, 8, 9).
- If my target was just hit at cell $k$, avoid firing at $k$ the immediately following round, as targets almost always relocate after being hit.
- Observe the firing history of my target: opponents often avoid hiding in the exact cells they frequently target. Use their firing preferences as negative indicators for their likely hide locations.