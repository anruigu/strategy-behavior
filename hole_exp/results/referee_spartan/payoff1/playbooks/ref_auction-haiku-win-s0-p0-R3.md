---
game: ref_auction
model: haiku
condition: win
seed: 0
round: 3
chars: 2019
---
# Playbook for ref_auction

When I see a lot where my valuation exceeds the estimate by a meaningful margin, I open bidding at a modest level well below my valuation to establish position while preserving budget.

When the standing bid is still substantially below my valuation for a lot, I raise to secure it rather than pass, since positive margin remains.

When evaluating whether to bid in round 2, I calculate the profit I'd realize at the minimum raise (value to me minus bid amount) and bid if that profit is substantial relative to my remaining budget.

When I'm on the final lot and it's a high-value item for me, I bid aggressively up to my valuation since this is my last opportunity to acquire anything in the round.

I maintain a complete transaction log of every bid I make, whether winning or losing. Before each decision, I calculate my remaining budget by summing all bids made to date and subtracting from my opening budget. I do not rely on memory or previous calculations—I recompute from the transaction log each time.

When I win a lot, I record the lot number and the price paid immediately in my log. After each lot concludes, I update my total spending and available budget for all subsequent decisions.

I do not let sunk costs (my earlier bids on a lot) influence whether I raise further in later rounds—only whether the current standing bid leaves meaningful profit margin between my valuation and the bid amount.

I do not rely on score projections or competitive positioning with other bidders to override value analysis. My primary decision rule is: if the standing bid is below my valuation by enough to create meaningful profit margin, I bid; if not, I pass.

I notice that budget tracking is error-prone when I reason informally. I will state my transaction log explicitly before making any bid decision: opening budget, every bid made to date (winning and losing), total spent, and remaining budget. This discipline prevents the arithmetic errors that clouded my play in this episode.