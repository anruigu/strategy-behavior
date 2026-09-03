---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 3718
---
When asked to hide, I check who fires at me (the single player that can hit me) and where that specific attacker has been shooting; I prefer cells they fire at least rarely (low frequency) and avoid their recent shots.

When asked to hide and no clear low-frequency cell exists for my attacker, I pick an unshot cell (or one not recently targeted by anyone) to reduce immediate discovery.

When asked to hide, I avoid repeating the exact same hide multiple rounds unless I have a deliberate meta-bluff reason; I randomize among a small set of low-risk cells to keep my pattern high-entropy.

When deciding between two candidate hide cells with equal shot history, I prefer the one that increases entropy in my own hide sequence (the choice that is less predictable given my past hides).

When asked to fire at my assigned target, I follow an explicit exploration schedule early: fire different cells in successive rounds (no repeated single-cell probing) to build a reliable frequency map of that target.

When I have an updated frequency map for my target, I balance exploration and exploitation: concentrate fires on cells that show higher likelihoods of containing the target (based on confirmed hits or strong social evidence), but continue occasional probes of untested cells to catch changes.

When asked to fire and my target is leading in score, I bias toward higher-probability exploitation (more aggressive targeting of likely cells) because a hit yields high reward and removes their points.

When asked to fire and my target is low on score or a non-threat, I bias toward exploration—probing new cells to gather information for later rounds.

When I have no reliable information on my target (no hits, all misses), I avoid repeatedly firing the same neutral cell (e.g., always firing center); instead I spread probes across different untested cells to maximize coverage.

When I receive private hit/miss feedback, I immediately update my local map for that target and update my model of the player who shoots at me using others’ public fires and claims.

When submitting claims, I always match the referee’s private result exactly; I will not lie.

I do not assume any single cell (like center) is inherently best; center can be a reasonable neutral probe but should not be the default every round.

I prioritize hiding choices based on the attacker’s empirical shot distribution against me, not on global shot counts from players who cannot hit me; however I use global shot history to identify generally unpopular cells if my attacker’s data is sparse.

I avoid hiding in cells that the one player who can hit me targets heavily; repeat avoidance is mandatory unless I want to execute a planned meta-pattern.

I keep a short list (2–4) of low-risk hide cells and rotate among them rather than locking to one; this preserves unpredictability while staying safe.

I explicitly avoid firing the same cell across rounds unless that cell has become strongly indicated by prior confirmed hits; persistent misses on a cell mean I deprioritize it.

If pressured to choose between probing for information and going for a risky high-value shot, I consider current scores and remaining rounds: early rounds favor exploration, late rounds favor exploitation based on the score picture.

I log and use every public fire+claim combination to infer probable hides for all players, but I weight my inference highest for the single player who can hit me (for hiding decisions) and for my assigned target (for firing decisions).

I periodically re-evaluate and adjust my small set of preferred hide cells and my firing-exploration schedule based on observed opponent changes; I do not treat my initial heuristics as fixed.