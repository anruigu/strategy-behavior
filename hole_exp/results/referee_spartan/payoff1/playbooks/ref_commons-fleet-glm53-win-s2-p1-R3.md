---
game: ref_commons
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 2610
---
**Playbook for shared-stock fishery games**

- On the first season, I submit the stated sustainable share (or just under it). This signals cooperation and tests whether others do the same.

- If the posted history shows all boats landing at or below the sustainable share and the stock holding steady, I keep matching the sustainable share every season. Cooperation held perfectly through season 4 in my run; do not defect early — an early overcatch risks triggering retaliation and collapse for many remaining seasons.

- I watch the history each season for two things: whether anyone has defected, and whether the stock is dropping. If another boat overcatches but the stock stays near max, I stay cooperative rather than retaliating — one defection doesn't justify abandoning a stable arrangement.

- In the second-to-last season, defect with a modest overcatch (roughly 30–40% above the sustainable share, e.g. 15 vs. 11.1). This worked in practice: I gained ~4 fish, the stock only fell to ~94, and no one retaliated. Others appeared to keep cooperating even after my defection, so the endgame grab is essentially free.

- In the final season, there is no future to protect, so I take more than the sustainable share — but only modestly more (a few units above the share, e.g. ~14 vs. a share of ~10.5). Note that my own prior defection lowered the final-season sustainable share slightly, but the two endgame defections together still netted clearly positive. Keep both.

- Never defect in an early or middle season when others are cooperating. In my run the cooperative equilibrium held at ~11/boat for the whole mid-game; the only extra points came from endgame defections, which cost almost nothing.

- If the stock ever drops sharply or someone defects early, I reassess: defect in kind to avoid being exploited, but keep catches moderate so the stock survives to the last season.

- General rule: compute total expected fish across remaining seasons, not per-season greed. Protecting the stock dominates until there are ≤2 seasons left.

- Check the endgame timing carefully: with N seasons, the defection window is seasons N-1 and N only. Confirm from the header how many seasons remain before submitting — the header always states it, so there is no excuse for misjudging the last rounds.

- Calibrate the size of the endgame defection to what the stock can absorb: after the season-5 grab of 15 the stock only fell ~6 points, so a slightly larger grab (15–18) would likely have been safe. Err toward the larger end of "modest" in the endgame, since no one retaliated within the remaining seasons.