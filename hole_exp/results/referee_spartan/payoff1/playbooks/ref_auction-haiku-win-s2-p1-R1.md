---
game: ref_auction
model: haiku
condition: win
seed: 2
round: 1
chars: 1444
---
# Playbook for ref_auction

When a lot's value to me exceeds the current standing bid by a comfortable margin, I bid the minimum raise to stay competitive while preserving budget for remaining lots.

When I'm in the final round of a lot and the standing bid is below my valuation, I raise to secure the lot rather than pass, since there are no future opportunities for that specific asset.

When a standing bid exceeds my valuation of a lot, I pass immediately instead of continuing to bid, even if I have remaining budget.

When no bids have been placed yet on a lot I value, I open with the minimum bid to test the market and maintain optionality for higher competition.

When deciding between raising and passing in any round, I calculate the net value I'd gain (my valuation minus the price I'd pay) and only proceed if it's substantially positive.

I do not assume I can predict my remaining budget across multiple lots. I track it carefully after each decision and update my expectations.

When the standing bid is close to my valuation, I pass rather than raise, since the profit margin becomes too thin to justify the capital commitment.

When I'm on the last lot of the game and it represents good value relative to my valuation, I bid aggressively to secure it, since there are no future lots to preserve budget for.

I avoid bidding against myself or getting into a bidding war where incremental raises eat away at my profit margins.