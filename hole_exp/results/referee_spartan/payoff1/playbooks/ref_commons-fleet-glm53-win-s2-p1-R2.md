---
game: ref_commons
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2245
---
**Playbook for shared-stock fishery games**

- On the first season, I submit the stated sustainable share (or just under it). This signals cooperation and tests whether others do the same.

- If the posted history shows all boats landing at or below the sustainable share and the stock holding steady, I keep matching the sustainable share every season. Cooperation held perfectly through season 4 in my run; do not defect early — an early overcatch risks triggering retaliation and collapse for many remaining seasons.

- I watch the history each season for two things: whether anyone has defected, and whether the stock is dropping. If another boat overcatches but the stock stays near max, I stay cooperative rather than retaliating — one defection doesn't justify abandoning a stable arrangement.

- In the second-to-last season, defect with a modest overcatch (roughly 30–40% above the sustainable share, e.g. 15 vs. 11.1). This worked: I gained ~4 fish and the stock only fell to ~94, leaving the final season nearly intact. Others did not visibly retaliate in response.

- In the final season, there is no future to protect, so I take more than the sustainable share — but only modestly more (a few units above the share). A huge grab gains little if catches are limited by remaining stock or diminishing returns; a moderate overcatch is the safer default. Note the final-season sustainable share drops slightly if I overcaught the season before — the endgame defections still netted positive, so keep them.

- Never defect in an early or middle season when others are cooperating. The cooperative equilibrium held for the whole mid-game at ~11/boat; the only extra points came from endgame defections, which cost almost nothing.

- If the stock ever drops sharply or someone defects early, I reassess: defect in kind to avoid being exploited, but keep catches moderate so the stock survives to the last season.

- General rule: compute total expected fish across remaining seasons, not per-season greed. Protecting the stock dominates until there are ≤2 seasons left.

- Check the endgame timing carefully: with N seasons, the defection window is seasons N-1 and N only. Confirm from the header how many seasons remain before submitting.