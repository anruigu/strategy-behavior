---
game: ref_commons
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2269
---
**Playbook for ref_commons**

1. When the episode starts, compute the true sustainable per-boat yield from the regrowth rule (e.g., 50% regrowth to a cap of 100 means a total sustainable harvest of ~33, split across boats — ~11 per boat). The game usually states it; trust that number and anchor all early-season catches to it.

2. In early seasons, submit exactly the sustainable share (or fractionally below, never above). Small overcuts gain ~0.1 fish and only risk triggering an overfishing spiral. Don't do it.

3. Watch others' submitted catches as the signal of whether cooperation holds. If everyone stays at or below the sustainable share, keep matching it — the stock holds at 100, which maximizes every remaining season's yield. This worked perfectly for five straight seasons.

4. If others start overfishing materially (say, 1.5x the sustainable share or more), defect proportionally rather than being the sucker — but only enough to defend, not enough to collapse the stock, as long as several seasons remain.

5. In the second-to-last season, stay at the sustainable share. The stock is still worth one more regrown season of harvest, and a token grab tests nothing.

6. In the final season, defect as hard as the stock allows. There is no future retaliation. Compute stock minus others' likely catches and request nearly all of the remainder. In my episode I asked for ~78 of a stock of 100 (leaving room for two ~11 cooperators) — this was the right shape of move, but note the landed amount came in lower than requested (score implies ~50 landed on a 55.5 base). So: request generously, but expect the harbour may cap or scale back the final haul; ask for stock minus others' expected catches plus a margin, since over-asking costs nothing but under-asking leaves fish behind.

7. Never let total catches push the stock near zero before the last season; a collapse zeroes all remaining rounds, the worst possible outcome regardless of what others do.

8. Cooperators who held ~11 for five rounds will often hold to the end — do not assume they defect on the final round and shade down my grab. Plan for them staying at the sustainable share and size the final grab accordingly.

9. Keep replies short and always end with the required [catch: N] token.