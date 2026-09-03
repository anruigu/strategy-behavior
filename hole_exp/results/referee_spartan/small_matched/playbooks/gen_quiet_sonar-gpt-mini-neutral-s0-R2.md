---
game: gen_quiet_sonar
model: gpt-mini
condition: neutral
seed: 0
round: 2
chars: 3554
---
When asked to hide, avoid repeating the same cell across rounds; spread hides across different thirds of the board (low, middle, high) so my pattern is not predictable.

When asked to hide and several cells have been probed heavily (three or more fires on a cell across rounds), do not hide on those cells; prefer low-frequency cells opposite the recent cluster.

When asked to hide and opponents show a pattern targeting a small range or cluster, move to the opposite side of the line (low vs high) unless that side itself has become heavily probed.

When asked to fire at my fixed target, rotate through a set of 3–4 candidate cells rather than repeating one number every round; this reduces predictability and tests multiple hypotheses.

When asked to fire and the target or others have recently claimed hits on a specific cell, treat that cell as a confirmed recent hide for that round and deprioritize it for my immediate next fire (they often move, but it is a strong recent signal).

When asked to fire and multiple opponents concentrate on a cell without public hits on it, recognize two possibilities: it may be a safe bluff cluster or the real hide. Use such cells sparingly to test; do not persistently chase a cluster that yields only misses.

When my prior shots at a given cell have produced repeated misses, stop firing that same cell and switch to a new candidate instead of persisting.

When I receive the private result from the referee, always submit the claim that exactly matches that private result (claims are constrained to be truthful).

When choosing hides across a game, avoid always choosing center; consciously cover different thirds and revisit cells only after several rounds to avoid being predictable.

When my score is negative or lagging, increase variance in my firing choices (probe less-targeted cells, rotate more) rather than repeating conservative mid-range shots.

When I see many players firing the same small set of cells, expect some players will hide elsewhere; bias my hides toward low-frequency cells and my fires toward occasionally probing the cluster to detect patterns, but do not overcommit.

Assume public claims are accurate (the rules force truth), so use only the public fired cells and claimed hit/miss outcomes plus the private result I receive to update probabilities.

If a particular opponent consistently scores hits on a specific position across rounds, treat that position as a strong candidate for their hide in the immediately following round and deprioritize firing it until there's evidence they moved.

If I observe that a target that was hit on cell X later receives repeated probes on X by multiple players, expect either (a) the target repeated that hide or (b) players suspect repetition — act conservatively and test adjacent cells rather than charging X blindly.

Do not rely on deception in claims (players must match private results). Focus inference on the pattern of fired cells and on public hits as real information.

When behind on points, be willing to gamble on higher-reward shots (firing at cells where a hit would be surprising to others) rather than only safe probes.

When ahead or tied, favor conservative hiding (low-frequency, opposite clusters) and methodical probing of likely candidate cells rather than high-variance plays.

After every round, update the candidate set of my target’s likely hide cells by removing any cell that produced a confirmed hit against them that round (they probably moved) and by demoting cells I and others have repeatedly missed.