---
game: ref_auction
model: haiku
condition: win
seed: 2
round: 2
chars: 2185
---
# Playbook for Ref Auction

When I see a lot's value to me and the current standing bid, I calculate the margin (value minus bid) and compare it to my remaining budget.

When the margin is significantly positive—meaning I can win at the current bid plus minimum raise and still profit substantially—I bid the minimum raise to take the lead cheaply.

When I'm in round 2 of a lot and the standing bid is still well below the lot's value to me, I continue bidding to secure the lot, since this is my last chance to win it.

When calculating profitability, I remember that I'm not spending from a separate pool—every bid reduces my remaining budget for future lots. I track my cumulative spending across all lots, not just the current one.

When the estimate is higher than the lot's value to me, I recognize this as a signal that other bidders may see more value. I still bid if my valuation supports it, but I'm alert to the possibility of being pushed into overpaying.

When I've already won a lot at a good price, I don't let that success make me reckless on subsequent lots. Each lot stands alone in terms of value proposition.

When it's the final lot and I have remaining budget, I compete aggressively if the lot's value to me exceeds the standing bid by a meaningful margin, since there are no future lots to preserve budget for.

I track my actual remaining budget as reported by the system after each bid. The system's reported budget is my ground truth; my mental calculations of remaining budget can drift and are less reliable than what the interface tells me.

I bid to win lots where value exceeds cost, and I pass only when the standing bid has risen close enough to my valuation that additional raises would eat away my profit margin.

I should be wary of round 2 bidding when my margin, while positive, is not dramatically large. Once I'm locked into a lot in round 2, any further raise by an opponent forces me into a choice between overpaying or walking away empty-handed. In round 1, I have another chance to reconsider; in round 2, I do not. This asymmetry means I should bid more conservatively in round 1 when bidding would commit me to competing hard in round 2.