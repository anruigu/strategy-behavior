---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 1457
---
When asked for a hide coordinate, pick an integer 1–9 and do not repeat the same small set of cells across rounds; prefer low-traffic cells but vary enough to be unpredictable.

When many players repeatedly fire at particular cells, avoid hiding in those cells that round.

When I have no useful information about the target's pattern, fire the center (5).

When I have observed a pattern of a specific player repeatedly firing the same cell at my target and always missing, deprioritize that cell as a candidate for my next shot at that target.

When opponents frequently target a cell and claim hits on it in multiple rounds, treat that as noisy information (hides change each round) and do not overweight it; instead continue to probe other cells.

When I want to probe where the target might hide, spread my fires across different cells rather than repeating the same cell each round.

When my shot result is a miss, submit the claim "miss" (the claim must match the private result).

When my shot result is a hit, submit the claim "hit" (claiming must match the true result).

Always submit valid integers 1–9 for hides and fires; always submit one of the two allowed claims.

Do not attempt to lie in claims (this is invalid and causes contradictions); I will not claim hits when I was told I missed.

If opponents show a concentrated bias toward a subset of cells, exploit that by hiding in other cells and by firing to probe the less-targeted cells.