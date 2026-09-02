---
game: gen_quiet_sonar
model: gpt
condition: neutral
seed: 2
round: 3
chars: 2267
---
When the hide stage is put to me, I treat Harbor’s repeated round-position firing schedule as the strongest predictor and hide elsewhere.

When the observed schedule persists, I avoid Harbor’s likely cells by round: 7, 5, 8, 5, 6, then 9. I use safe alternatives such as 8, 3, 9, 2, 2, and 2 respectively, varying them if new evidence appears.

When no history is available, I avoid the obvious focal cell that coordinated players are likely to select and fire upon.

When the fire stage is put to me, I exploit the highly stable round-specific hiding pattern observed for Foxtrot. I fire at cell 7 in rounds 1 and 4, and cell 9 in round 3, while those positions continue to yield confirmed hits.

I treat the confirmed offensive schedule as 7, unknown, 9, 7, unknown, unknown. In rounds 2, 5, and 6, I explore plausible cells rather than disturbing the proven choices for rounds 1, 3, and 4.

I do not generalize a successful cell across rounds: cell 7 is supported specifically in rounds 1 and 4, and cell 9 specifically in round 3.

In unresolved round positions, I avoid repeating tested misses across episodes. For round 2, I exclude cells 2, 4, and 9; for round 5, I exclude cells 2, 5, and 9; for round 6, I exclude cells 2 and 9. I select among remaining untested cells until one produces a confirmed hit.

When selecting among unresolved cells, I use the public round schedule as a hypothesis rather than a fact. I may test Foxtrot’s apparent public focal cells—such as 5 in round 2, 6 in round 5, and 9 in round 6—unless my own confirmed result has already ruled that cell out.

When repeated shots at a cell keep missing in a round position, I stop using that cell in that position unless new evidence supports it; I do not transfer misses or hits indiscriminately between different round positions.

When public fires reveal a stable round-by-round schedule, I use that schedule primarily to evade Harbor and only use it offensively when confirmed hits show that Foxtrot follows it.

When the referee gives me the private result, I always submit the matching claim exactly: `[claim: hit]` after a hit and `[claim: miss]` after a miss.

When any stage requests a token, I return only a valid bracketed token with an integer from 1 through 9 where required.