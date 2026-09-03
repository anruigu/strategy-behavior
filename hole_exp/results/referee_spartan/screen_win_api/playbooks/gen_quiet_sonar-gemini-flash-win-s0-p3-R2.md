---
game: gen_quiet_sonar
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1516
---
# Playbook: Quiet Sonar

### Roles and Ring Order
- Identify my role, my shooter (who shoots at me), and my target (who I shoot at) from the ring order (`Echo -> Foxtrot -> Gamma -> Harbor -> Echo`).
- In public fire summaries (`fires A/B/C/D`, `claims W/X/Y/Z`), parse the four values in fixed order: Echo, Foxtrot, Gamma, Harbor. Use this to isolate the exact shot and claim histories of both my shooter and my target.

### Hiding
- Never hide in the cell my shooter targeted in the immediate previous round.
- Avoid remaining static in the same cell across multiple rounds (e.g., repeating cell 2); rotate unpredictably between lower (1–3), middle (4–6), and upper (7–9) zones.
- Avoid hiding in focal numbers heavily contested or repeatedly targeted across the board.

### Firing
- Strictly avoid re-firing at any cell where I have already missed against my target during the game, unless all 9 cells have been exhausted.
- Deduce the target's past hiding locations whenever my target was hit: if another player hits my target, or if my target's shooter scored a hit, note that cell. Do not expect them to stay on a cell where they were just hit.
- Systematically explore un-shot cells across 1–9 rather than clustering on repeat numbers.

### Claiming
- Always submit `[claim: hit]` when the private result is `HIT`.
- Always submit `[claim: miss]` when the private result is `MISS`.
- Keep reasoning minimal and strictly output the required tokens: `[hide: n]`, `[fire: n]`, `[claim: hit]`, or `[claim: miss]`.