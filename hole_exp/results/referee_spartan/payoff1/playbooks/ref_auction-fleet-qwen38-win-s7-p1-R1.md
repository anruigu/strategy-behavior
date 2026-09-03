---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 2432
---
# Playbook

**Opening bids (round 1 of 2):**
- Bid no more than 50% of my value for the lot. This tests the field without committing most of my surplus. If no one raises, I'll win cheaply. If someone does, I still have room to respond in round 2.
- If no one has bid and the lot is worth very little to me (my surplus at the minimum raise is small), pass and let someone else take the risk.

**Final round (round 2 of 2):**
- This is where I must commit. If (my value) minus (standing bid + minimum raise) is positive, I should bid close to my value to win the lot. The only scenario where passing is correct is when the minimum acceptable winning bid would exceed my value.
- Specifically: bid my value minus 1 (or the largest integer strictly below my value). The reason: if I don't win, my surplus is zero. If I win at price P, my surplus is V−P. So I should always prefer winning at V−1 over losing, because V−1 > 0 = losing.
- My biggest mistake in the episode was bidding conservatively in final rounds and losing lots where I had a large surplus available. I left value on the table by treating round 2 as if it were round 1.

**Budget tracking:**
- Track my actual remaining cash carefully. At the start I have 30. Every lot I win subtracts my winning bid from my budget. Before bidding, confirm I can actually afford the bid. Report the true remaining budget.

**When to pass:**
- Pass in round 1 only if my value is low enough that even winning at the minimum raise gives me a negligible surplus, or if I've already spent most of my budget on prior lots.
- Pass in round 2 only if the minimum raise would push me above my value.

**Reading the competition:**
- If a competitor has been winning lots at or near estimate, they are likely valuing lots at or above estimate. Against such a bidder, I need to be willing to bid near my full value to win.
- If a competitor is passing on lots, they may be budget-constrained or valuing things low. I can win cheaper in that case.

**Overall priority:**
- My score is total surplus, not number of lots won. I should compare "bid X to win this lot for surplus S" against "pass and use budget Y on a later lot for surplus T." But since I can't see future lots, the safe rule is: in the final round, always bid to win if my value exceeds the minimum winning bid. The only exception is if I'd need to spend money I need to afford a later lot that I expect to have a higher surplus on.