---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 3416
---
When asked to hide, I pick a cell that was not recently fired upon by many opponents and was not recently reported as a hit against me: [hide at an untouched or rarely probed cell].

When asked to hide and many cells are unprobed, I randomize among those unprobed cells rather than always choosing center or always choosing an edge.

When asked to hide and opponents show a pattern of repeatedly targeting a small set of cells, I avoid that small set and pick outside it.

When asked to hide and I have been hit recently on a specific cell, I stop using adjacent or identical cells and move at least two cells away.

When asked to fire (my target is fixed), I maintain a running frequency tally of where that target has hidden (inferred from others’ hits/misses on that target or on other players who were firing at the same target). I fire at the most-frequently-inferred cell (exploit) unless there is high uncertainty, in which case I probe a cell that reduces uncertainty (explore).

When I have no reliable prior for my target’s hide, I prioritize cells that opponents have recently used successfully against that target or cells adjacent to those (because people tend to repeat nearby), but I randomize occasionally to avoid predictability.

When I have multiple rounds left and I am behind on points, I accept higher-risk shots (target high-probability cells more aggressively) to try to score hits; when I am ahead, I favor safer, diversified shots to deny big swings.

When I observe a public hit by someone else at a specific cell, I mark that cell as occupied by that shooter for that round only and use that information to avoid shooting there in the same round and to update my model for future rounds (people often repeat).

When opponents’ claims are always truthful (as they must be), I treat every public hit as definitive information about where that shooter hid that round and every miss as definitive information about where they did not hide.

When choosing hides across rounds, I avoid predictable patterns (do not repeat the same hide location more than twice in a row) to reduce being targeted by pattern-exploiting opponents.

When my shot result is private and the rules require the public claim to match it, I always report the true result (claim exactly hit or miss as told). Lying is not allowed; be succinct and consistent.

When I notice opponents concentrating fire on a small subset of cells, I use that to my advantage by hiding outside that subset and by later firing at those concentrated cells against other players if analysis suggests they will repeat.

When forced to choose between two equally plausible cells to fire at, I break ties by preferring the less-recently-fired cell (to exploit opponents’ tendency to avoid recently probed cells), but randomize some fraction of ties to avoid being predictable.

When formulating my next hide or fire choice, I update a simple table after each round: counts of times each cell was fired at, counts of hits per cell, and per-player tendencies. Use that table to drive the exploit/explore rule above.

What did not work and must be avoided: do not default to always hiding in the center or always in a single “safe” slot — that became predictable and did not generate points. Do not fire mechanically at the same single cell every round without adapting to the public information — repeated misses accumulate and cost opportunities.