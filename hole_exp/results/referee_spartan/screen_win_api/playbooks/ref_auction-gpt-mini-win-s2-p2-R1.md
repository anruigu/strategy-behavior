---
game: ref_auction
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 1758
---
When I see a standing bid >= my private value, I pass.

When the standing bid < my value and I can afford at least the minimum raise, I raise by exactly the minimum raise to conserve budget.

When there are two bidding rounds and I am the current high bidder at a price equal to my value, I do not raise on the final round.

When no bids exist and the lot’s value > 0, I may open with a bid up to (but not exceeding) my value; prefer opening near the minimum acceptable increment rather than full value.

When the minimum raise would force the price above my value, I pass rather than chase.

Always compute whether winning at the next possible price yields positive surplus (value − next price); only bid if surplus > 0 (or if I deliberately accept zero surplus for strategic reasons, do so consciously).

When considering a bid, ensure the remaining budget after winning would be nonnegative and feasible for future lots; do not commit funds that violate budget constraints.

When multiple lots remain, prefer conserving budget unless the lot’s surplus justifies heavy spending; prioritize lots with the largest positive surplus per budget spent.

When I place a bid, immediately and correctly subtract the bid amount from my available budget record so future decisions are based on accurate funds.

Do not escalate auctions with emotional or punitive raises; only increase bids when the arithmetic (value, minimum raise, remaining budget) supports it.

If an opponent’s bid already exceeds my value by a small margin but I expect later lots with higher surplus, pass rather than overpay to block.

If I’m uncertain about opponent behavior but can secure a high-surplus lot cheaply, seize it using minimum raises rather than attempting large upfront jumps.