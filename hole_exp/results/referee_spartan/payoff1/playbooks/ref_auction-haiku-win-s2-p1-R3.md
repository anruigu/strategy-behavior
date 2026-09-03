---
game: ref_auction
model: haiku
condition: win
seed: 2
round: 3
chars: 2377
---
# Playbook for ref_auction

When a lot's value to me exceeds the current standing bid by a comfortable margin, I bid the minimum raise to stay competitive while preserving budget for remaining lots.

When I'm in the final round of a lot and the standing bid is below my valuation, I raise to secure the lot rather than pass, since there are no future opportunities for that specific asset.

When a standing bid exceeds my valuation of a lot, I pass immediately instead of continuing to bid, even if I have remaining budget.

When no bids have been placed yet on a lot I value, I open with the minimum bid to test the market and maintain optionality for higher competition.

When deciding between raising and passing in any round, I calculate the net value I'd gain (my valuation minus the price I'd pay) and only proceed if it's substantially positive.

I track my budget carefully after each decision and verify my actual remaining budget before the next lot. I do not assume budget persists; I check the results from won lots and subtract my payments from my total.

When the standing bid is close to my valuation, I pass rather than raise, since the profit margin becomes too thin to justify the capital commitment.

When I'm on the last lot of the game and it represents good value relative to my valuation, I bid aggressively to secure it, since there are no future lots to preserve budget for.

I avoid bidding against myself or getting into a bidding war where incremental raises eat away at my profit margins.

I recognize that I cannot control the outcome of each lot. My strategy is to bid when value is clearly present (substantial margin between my valuation and the price), not to win every lot.

A substantial remaining budget gives me ample room to bid confidently on any lot where the math is favorable. However, I should not assume my budget is unlimited—I must track cumulative spending across all lots won and verify the actual amount remaining before committing to later bids.

When opening a lot with no standing bids, the minimum bid (typically 2–4 depending on the estimate) is the correct aggressive opening, not a conservative one. This tests the market efficiently without overcommitting.

I should be prepared to raise multiple times on valuable lots if competition emerges, provided the final price remains below my valuation by a meaningful margin.