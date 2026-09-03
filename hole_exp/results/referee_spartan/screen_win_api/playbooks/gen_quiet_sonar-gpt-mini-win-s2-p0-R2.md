---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 3379
---
When asked to hide:
- I prefer to pick a cell among the least-recently-targeted positions; I track recent fire history (who shot which cell each round) and avoid cells that have been fired at repeatedly in the last few rounds.
- When multiple low-traffic cells exist, I prefer 1–5 over 6–9, because opponents more often probe the mid-high band; but I will not rigidly avoid 6–9 if that range becomes quiet.
- I avoid repeating the same hide number on consecutive rounds; if I must reuse a cell, I wait at least one round and only do so if that cell has remained low-traffic.
- If public claims reveal a guaranteed location (someone was hit and the fired cell is public), I avoid hiding on that cell in future rounds.
- I always submit an integer 1–9 for hides.

When asked to fire (Echo → Foxtrot):
- I target cells that maximize pressure but also gather information: I favor mid-range cells (4–8) as a starting bias, but I vary across that band rather than locking to one number.
- I track recent fires at Foxtrot by all players and the public claims about those fires. If many players repeatedly fire the same cell at Foxtrot with no hits, I downgrade that cell’s likelihood and shift to adjacent or low-traffic cells.
- If public claims indicate a hit on a specific cell that involved Foxtrot (i.e., someone claimed hit against Foxtrot or a claim pattern implies Foxtrot was hit), I prioritize that cell only if it’s consistent with available information; otherwise I probe cells near that reported hit to test for copying/ deception.
- When Foxtrot is ahead on points and I need to catch up, I bias slightly toward riskier concentrated probing (try more focused repeated probes at a promising cell for a chance at a decisive hit) but only for a short window—don’t become predictable.
- Conversely, when I am behind and opponents are unpredictable, I broaden my probing to sample more cells to gather information.
- I always submit an integer 1–9 for fires.

When updating beliefs from public information:
- I use every round’s public fires and claims to update a probability distribution over each opponent’s hide cell.
- A reported hit conclusively pins that target to the fired cell for that round; use that to update opponents’ tendencies (they may copy successful hides).
- Repeated misses against a single cell decrease belief in that cell; repeated claims of misses don’t prove anything but shape likelihoods when combined with who fires where.
- Note player-specific patterns: some opponents may habitually fire the same cell; exploit that only if their hiding tendencies or public hits suggest it’s productive.

When given the private shot result:
- I always claim the true result (claim hit if hit, miss if miss). Claims must match the private result and truthful claims are required.
- I do not lie or attempt to game public scoring via false claims.

Behavioral rules and things to avoid:
- Do not repeatedly fire the exact same cell every round—doing so is predictable and was ineffective in the last episode.
- Do not reuse the same hide cell in consecutive rounds; diversify hides to avoid exploitation.
- Do not assume the same “safe” low-traffic cell remains safe indefinitely—update based on recent plays.
- Do not attempt to misreport results.

Validation:
- Always submit hides and fires as integers 1–9 and claims as exactly [claim: hit] or [claim: miss].