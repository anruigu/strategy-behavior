---
game: gen_quiet_sonar
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 2367
---
When asked to hide, avoid repeating the same cell across rounds; pick a cell outside the cluster most players have been firing at recently.

When asked to hide and several cells have been probed heavily (three or more fires on a cell across rounds), do not hide on those cells.

When asked to hide and opponents show a pattern targeting a small range, move to the opposite side of the line (low vs high).

When asked to fire at my fixed target, vary my fired cell instead of repeating the same number every round; rotate through 3–4 candidate cells to avoid being predictable.

When asked to fire and the target has recently claimed hits on a particular cell, deprioritize that cell (they likely hid there recently).

When asked to fire and multiple opponents concentrate on a cell without public hits on it, that cell is more likely to be safe to probe—use it occasionally to test.

When a public claim shows the target was hit by someone else on a cell, treat that cell as "recently occupied" and deprioritize it for at least one round.

When my prior shots at a given cell have been misses repeatedly, stop firing that same cell and switch to a new hypothesis instead of persisting.

When I receive the private result from the referee, always submit the claim that exactly matches that private result (I must always claim truthfully).

When choosing hides across a game, avoid always choosing center; make hide choices cover different thirds of the board across rounds.

When my score is negative or lagging, increase variance in firing (try less-targeted cells) rather than repeating conservative mid-range shots.

When I see many players firing the same small set of cells, expect some will exploit that by hiding elsewhere; bias my hides toward low-frequency cells and my fires toward probing the clusters sparingly.

When I notice that honest claiming dominates the table (everyone claims true results), do not attempt to infer deception from claims—use only the public fired cells and claimed hits/misses to update probabilities.

When I notice a player consistently gets points from hits on a specific position, treat that position as a strong candidate for their hide in the immediately following round.

What did not work: repeatedly firing the same mid-range numbers (5 or 6) every round produced no hits and made my pattern easy to avoid—stop doing that.