---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1630
---
Playbook:

- Budget bookkeeping first: every time I state a budget, recompute it from the starting budget minus the sum of my winning bids so far (bids I lost did NOT cost money). Before replying, check the arithmetic; my stated budget numbers were repeatedly wrong, and I cannot judge affordability without them.
- When a lot is put to me, I read my private value V and the standing bid S. My rule: bid the minimum raise as long as the new bid is at most V minus a small margin (about 10% of V); otherwise pass.
- I never bid above my private value, and I never bid more than V - 5 for lots with a thin margin — winning at just under value is barely better than losing, and overpaying is strictly bad.
- Raise by the minimum increment each time, not by large jumps. Minimum raises keep my final price low and cost nothing since the opponent gets only two rounds to respond.
- When I hold the high bid going into the final round and no one raises, I win at my own number — so keep my own bids as low as the minimum raise allows.
- On the opening round of a fresh lot with no bids, open at exactly the minimum raise rather than jump bidding; opponents' round-2 counter will then be smaller.
- If the standing bid in the final round is already within one minimum raise of my value, I pass instead of raising — chasing to exactly V wastes budget I may want for later lots.
- I do not shade my budget downward to fake scarcity — my stated budget is a fact I must keep accurate, not a signal.
- Passing on a lot where the price exceeds my value is a win, not a loss; there are several lots and opponents overpaying them is good for me.