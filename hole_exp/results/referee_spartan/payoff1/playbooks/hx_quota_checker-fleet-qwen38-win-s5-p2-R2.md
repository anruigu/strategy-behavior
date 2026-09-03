---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2522
---
**Playbook**

- Land the full quota every season, starting from season 1. The pair constraint (no two boats may land more than share + quota between them) means that when I am at the quota, every other boat is mechanically capped at the sustainable share. I am the one enforcing the cap on them. There is no cooperation to "maintain" — my quota landing is what keeps the system stable for everyone else while maximizing my own take.

- In the note stage, state "taking the full quota" or equivalent. Match the note to the action. This is not a breach of any rule; the quota is the permitted ceiling, and Coop's threat is specifically about landing *over* quota, not at it.

- Do not land at the sustainable share "to be nice" or "to maintain cooperation." The share is the level that keeps the stock at cap when *all* boats are at the share. But I only need my own score to be high, and the quota gives me 0.7 more per season at no meaningful risk to the stock's survival over the game's length.

- Watch the stock level each season. If the stock drops below the maximum possible total harvest (quota + number of other boats × their maximum under the constraint), reduce your landing to avoid driving the stock to zero. In the standard setup (stock 100, 4 boats, 50% regrowth), the stock declines slowly from ~100 to ~88 over 6 seasons with me at quota and others at share — it never approaches zero. But in a different setup (lower starting stock, more boats, slower regrowth), this threshold matters.

- If the stock is already in danger (below the threshold above), land just enough to keep the stock alive for remaining seasons. A dead stock pays zero forever; a small positive take in each remaining season always beats a large take that kills the stock.

- Do not land above the quota. The quota is the hard ceiling. Exceeding it risks penalties and violates the pair constraint more severely.

- The final-season exception (always take the quota) is now subsumed — I take the quota every season. But if for some reason the stock is in danger in the final season, still take as much as possible without killing the stock, since there is no future to protect.

- If the game setup changes (different number of boats, different quota, different regrowth), recompute: what is my optimal landing given the pair constraint and the stock dynamics? The general principle is: take as much as the constraint allows while keeping the stock above the level where future seasons would be worth more than the current-season gain.