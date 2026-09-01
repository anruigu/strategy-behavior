---
game: gen_quiet_sonar
model: gpt
condition: neutral
seed: 2
round: 1
chars: 1336
---
When the hide stage is put to me, I avoid the cell Harbor is likely to fire at, using its repeated round pattern as the strongest predictor and breaking ties by choosing an unpredictable alternative.

When no history is available, I do not hide at the obvious focal cell that coordinated players are likely to select and fire upon.

When the fire stage is put to me, I target cells that have produced confirmed hits against Foxtrot in the same round position; I prioritize 7 in the opening round and again around the fourth round while that pattern persists.

When I lack a confirmed round-specific target, I infer Foxtrot’s hiding pattern from prior hits and public behavior, then vary among plausible cells rather than repeatedly firing 6.

When repeated shots at a cell keep missing, I stop using that cell unless new evidence supports it; persistent firing at 6 did not work.

When public fires reveal a stable round-by-round schedule, I use that schedule primarily to evade Harbor and only use it offensively when confirmed hits show that Foxtrot follows it.

When the referee gives me the private result, I always submit the matching claim exactly: `[claim: hit]` after a hit and `[claim: miss]` after a miss.

When any stage requests a token, I return only a valid bracketed token with an integer from 1 through 9 where required.