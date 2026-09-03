---
game: ref_auction
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 2431
---
When I see a standing bid >= my private value, I pass.

When the standing bid < my value and I can afford at least the minimum raise, I raise by exactly the minimum raise to conserve budget, unless strategic reasons justify a larger jump.

Always compute the next possible price (current standing bid + minimum raise). Only bid if value − next price > 0 (positive surplus), except when I consciously accept zero surplus for a clear strategic reason (and I note that reason).

When there are two bidding rounds and I am the current high bidder at a price equal to my value, I do not raise on the final round.

If no bids exist and the lot’s value > 0, I may open with a bid; prefer opening at the minimum acceptable increment (or the minimum raise over zero) rather than near full value to test competition and conserve budget.

When the minimum raise would force the price above my value, I pass rather than chase.

Before placing any bid, ensure I can legally state the remaining budget: I immediately subtract the bid amount from my available-budget record and never state a remaining budget that would be negative or inconsistent with prior bids. (I hold my money but must reflect it in the budget I post.)

When considering a bid, confirm that winning at the next possible price leaves a nonnegative remaining budget and leaves me able to participate in remaining lots if desired; do not commit funds that violate budget constraints.

When multiple lots remain, prefer conserving budget unless the lot’s surplus justifies heavier spending; prioritize lots with the largest positive surplus relative to the price I expect to pay.

Do not escalate auctions with emotional or punitive raises; only increase bids when the arithmetic (value, minimum raise, remaining budget) supports it.

If an opponent’s bid already exceeds my value by a small margin but I expect later lots with higher surplus, pass rather than overpay to block.

If uncertainty about opponent behavior exists but I can secure a high-surplus lot cheaply, seize it using minimum raises rather than attempting large upfront jumps.

Track results of previous lots (who won and at what price) to inform remaining budget planning and prioritization of future lots.

When I deviate from minimum-raise bidding (e.g., to close out a lot I highly prioritize), do so explicitly and only after checking impact on remaining budget and expected surplus across remaining lots.