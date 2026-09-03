---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 2324
---
When asked for a hide coordinate, pick an integer 1–9 and vary my choices across rounds; do not concentrate hiding repeatedly on the same small subset of cells.

When many players repeatedly fire at particular cells, avoid hiding in those cells that round; prefer low-traffic cells and corners when the center is heavily probed.

When I have no useful information about the target's pattern, prefer probing a central or information-rich cell (5) on an early round, but if that cell has been probed repeatedly by many players with consistent misses, deprioritize it in later rounds.

When I observe a specific player (or multiple players) firing the same cell at my target and always missing, treat that cell as lower-probability for that target and shift my probes to alternative cells to gain information.

When opponents frequently target a cell and claim hits on it in multiple rounds, treat that as noisy/unreliable evidence (hides change each round) and do not overweight it; instead continue to probe a variety of cells to gather independent evidence.

When I want to probe where the target might hide, spread my fires across different cells rather than repeating the same cell every round; balance exploration of new cells with re-checking promising cells occasionally.

If a particular cell has a growing history of misses from many shooters, move my probes away from it and sample other cells to avoid wasting probes.

When my shot result is a miss, submit the claim "miss" (claims must match private results).

When my shot result is a hit, submit the claim "hit" (claims must match private results).

Always submit valid integers 1–9 for hide and fire coordinates; always submit one of the two allowed claims. Never attempt to lie in claims.

If opponents show a concentrated bias toward a subset of cells, exploit that by hiding in other cells and by firing to probe the less-targeted cells.

Prioritize information gain when choosing fires late in the game if score differences are small; prioritize offense (fire the most-likely cells of leaders) when catching up or securing points becomes necessary.

Monitor public fire and claim history each round to update which cells are being actively probed and which are consistently producing misses or hits; use that to shift both hide and fire choices dynamically.