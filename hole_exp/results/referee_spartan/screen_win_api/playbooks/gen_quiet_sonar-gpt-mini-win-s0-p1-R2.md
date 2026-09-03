---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 3351
---
When told to hide, pick a cell away from obvious recurring opponent fire targets (avoid cells opponents frequently fire at); if opponents concentrate on a few cells, choose a different one.

When told to hide and there is no clear pattern, randomize among at least three preferred hide cells (do not reuse the same hide every round); explicitly rotate or use a random draw so I do not lock into a single repeated hide.

When told to fire at my fixed target, fire at the cell that recent public claims and opponents' firing patterns suggest they hide in (target cells opponents have declared hits on or that opponents avoid defending).

When told to fire and the target's pattern is unclear, alternate between a small set of high-frequency candidate cells rather than always repeating one number; commit to a planned rotation (e.g., A→B→C) or probabilistic mix so my shots are not trivially predictable.

When I receive the private result of my shot, I must report that exact result publicly—do not lie. Lying is illegal and unsustainable.

When deciding whether to adopt a deceptive narrative beyond required truthful claims, use the sequence of past truthful claims to craft expectations for opponents, then vary my hides/fires to exploit those expectations; but ensure my hides are not so predictable that opponents can exploit them.

When opponents’ scores show someone gaining by claimed hits, prioritize disrupting that player by firing at the cell they most frequently hide in (if my fixed target is that player, increase pressure).

When behind late in the game, bias hides toward uncommon cells and concentrate fires on the leader’s most-used cells to try to swing points.

When ahead late in the game, avoid risky repetition in hides and prefer conservative, less-targeted cells to reduce chance of being hit.

When I notice opponents always firing the same few cells, treat those as "hot" and avoid hiding there unless I want to bait and can predict a guaranteed miss claim sequence.

When recording patterns, update my shortlist of three preferred hide cells and three preferred fire cells after each round; commit to at least one forced random choice each round to stay unpredictable.

Enforce discipline: never fall into the habit of picking the same hide more than twice in a row; if I do so accidentally, immediately expand my next-round hide choices.

If my fixed target repeatedly fires the same shot locations (e.g., many rounds at a single cell), interpret that as either a belief about where others hide or a systematic search; diversify my firing to probe other plausible hides while keeping occasional probes at their hot spot.

Track both opponents’ fire patterns and their hide outcomes: a location that is fired at often but yields only misses is likely avoided by hiders—this makes it a lower-priority fire target unless a player is being forced there.

When I see every player publicly claiming all misses for many rounds, infer low information content in claims and place higher weight on raw fire choices as signals (who fires where, and how often) rather than claims.

Maintain a lightweight state: for each player keep counts of where they fired (my target especially), where they were fired at, and the distribution of public hits/misses; update my next hide and the rotation of fire targets from that state each round.