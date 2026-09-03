---
game: ref_commons
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 1879
---
**Playbook for ref_commons**

1. When the episode starts, compute the true sustainable per-boat yield from the regrowth rule (e.g., 50% regrowth to a cap of 100 means a total sustainable harvest of ~33, split across boats — ~11 per boat). The game usually states it; trust that number and anchor all early-season catches to it.

2. In early seasons, submit exactly the sustainable share (or fractionally below, never above). Small overcuts gain ~0.1 fish and only risk triggering an overfishing spiral. Don't do it.

3. Watch others' submitted catches as the signal of whether cooperation holds. If everyone stays at or below the sustainable share, keep matching it — the stock holds at 100, which maximizes every remaining season's yield. This worked perfectly for five straight seasons.

4. If others start overfishing materially (say, 1.5x the sustainable share or more), defect proportionally rather than being the sucker — but only enough to defend, not enough to collapse the stock, as long as several seasons remain.

5. In the second-to-last season, stay at the sustainable share. A token grab tests nothing and costs goodwill; the full stock is still worth one more regrown season of harvest.

6. In the final season, defect as hard as the stock allows. The leftover stock is worthless and there is no future retaliation. Others may still cooperate (mine did — they took ~11 each while I took 33), so aim for a large fraction of the remaining stock, not a third of it: with stock ~100 and two other boats at ~11, I could have taken ~70+ rather than 33. Compute stock minus others' likely catches and take nearly all of it.

7. Never let total catches push the stock near zero before the last season; a collapse zeroes all remaining rounds, the worst possible outcome regardless of what others do.

8. Keep replies short and always end with the required [catch: N] token.