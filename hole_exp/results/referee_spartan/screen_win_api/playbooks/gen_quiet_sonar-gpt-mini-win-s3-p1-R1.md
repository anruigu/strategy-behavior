---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 1661
---
When asked to hide, pick the cell with the lowest recent frequency of being fired at (count fires visible to everyone) and hide there.

When multiple cells tie for lowest recent fire frequency, choose one uniformly at random among them.

When behind on points, bias my hide toward cells that my immediate attacker (the player who fires at me) has fired at less frequently; when ahead, bias hide toward cells that lowest-scoring players fire at least.

When asked to fire at my fixed target, choose a cell that my target has most recently used to hide (based on observed past hides) if there is a nonzero frequency; otherwise choose a cell that has been fired at least once recently by other players and not yet by me (use frequency to estimate likely hides).

When frequencies are inconclusive, choose uniformly at random among cells 1–9 to avoid becoming predictable.

When my score is lower than the target’s score by 4 or more, prioritize high-aggression: concentrate on the target’s most-likely cell (highest estimated frequency) rather than randomizing.

When my score is comfortably ahead (leading by 4+), avoid repeatedly firing the exact same cell; diversify to conserve uncertainty and avoid giving opponents easy counters.

Always claim exactly the referee’s private result (truthful claim).

Do not rely on patterns like always picking the same cell number; repeated predictable hiding was exploited and reduced my effectiveness.

Track rounds: update frequency estimates each round using all public fires and public claims (claims are guaranteed truthful by the rules), and use the updated estimates immediately for the next hide and fire decisions.