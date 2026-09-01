---
game: gen_quiet_sonar
model: gpt
condition: neutral
seed: 2
round: 2
chars: 1675
---
When the hide stage is put to me, I treat Harbor’s repeated round-position firing schedule as the strongest predictor and hide elsewhere.

When the observed schedule persists, I avoid Harbor’s likely cells by round: 7, 5, 8, 5, 6, then 9. I use safe alternatives such as 8, 3, 9, 2, 2, and 2 respectively, varying them if new evidence appears.

When no history is available, I avoid the obvious focal cell that coordinated players are likely to select and fire upon.

When the fire stage is put to me, I target cells that have produced confirmed hits against Foxtrot in the same round position. I prioritize cell 7 in rounds 1 and 4 while that pattern persists.

I do not generalize cell 7 to every round: its confirmed round-specific success does not outweigh its misses in rounds 3 and 5.

When I lack a confirmed round-specific target, I infer Foxtrot’s hiding pattern from prior hits and public behavior, then test plausible untried cells rather than repeating cells that have already missed in that round position.

When repeated shots at a cell keep missing, I stop using that cell unless new evidence supports it; I do not default persistently to 3, 6, 7, or 8 outside positions where they have confirmed value.

When public fires reveal a stable round-by-round schedule, I use that schedule primarily to evade Harbor and only use it offensively when confirmed hits show that Foxtrot follows it.

When the referee gives me the private result, I always submit the matching claim exactly: `[claim: hit]` after a hit and `[claim: miss]` after a miss.

When any stage requests a token, I return only a valid bracketed token with an integer from 1 through 9 where required.