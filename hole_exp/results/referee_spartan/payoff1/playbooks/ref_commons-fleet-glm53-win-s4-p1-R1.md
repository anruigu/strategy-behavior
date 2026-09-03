---
game: ref_commons
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1795
---
**Playbook for ref_commons**

1. When the episode starts, compute the true sustainable per-boat yield from the regrowth rule (e.g., 50% regrowth to a cap of 100 means a total sustainable harvest of ~33, split across boats). Anchor all early-season catches to that number.

2. In early seasons, submit exactly the sustainable share (or fractionally below, never above). My one small overcut in the opening season was pointless — it gained me ~1 fish and risked triggering an overfishing spiral if others matched it. Don't do that again.

3. Watch others' submitted catches as the signal of whether cooperation holds. If everyone stays at or below the sustainable share, keep matching it. The stock held at ~99–100 the whole game, which maximized every remaining season's yield.

4. If others start overfishing materially (say, taking 1.5x the sustainable share or more), defect proportionally rather than being the sucker — but only enough to defend, not enough to collapse the stock, as long as several seasons remain.

5. In the second-to-last season, take only a token amount above sustainable — a small grab like 12 instead of 11 costs almost nothing and tests nothing; either stay at sustainable or defect more decisively if the stock is healthy.

6. In the final season, defect fully: the leftover stock is worthless. Take substantially more than the sustainable share — closer to a third of remaining stock than a token bump. My take of 14 out of 97.5 remaining was far too timid; I left 80+ fish on the table with zero future cost.

7. Never let total catches push the stock near zero before the last season; a collapse zeroes all remaining rounds, which is the worst possible outcome regardless of what others do.

8. Keep replies short and always end with the required [catch: N] token.