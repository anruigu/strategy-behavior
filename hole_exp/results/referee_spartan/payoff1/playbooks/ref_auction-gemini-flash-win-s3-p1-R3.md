---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1743
---
### Budget Tracking
* Read the initial budget strictly from the introductory line (e.g., "You start with a budget of 30") on turn 1, record it, and never revert to a default assumption (like 100).
* Explicitly compute `remaining_budget = starting_budget - sum(prices of lots won by my bidder ID in "Results so far")`.
* In every turn, always verify and output the exact calculated `[budget: remaining_budget]`.
* Never place a bid `N` that exceeds `remaining_budget`.

### Round 1 Actions
* Calculate `min_bid = standing high bid + minimum raise` (or simply `minimum raise` if standing high bid is 0 / no bids yet).
* If `min_bid > valuation` or `min_bid > remaining_budget`: output `[bid: pass]`.
* If `valuation > min_bid` and profit potential exists: make the minimum legal bid (`min_bid`) to remain active for Round 2 without unnecessarily inflating the price.
* If my valuation is weak relative to the estimate and budget is constrained, output `[bid: pass]` to conserve funds for higher-surplus opportunities.

### Round 2 Actions (Final Round for Lot)
* Calculate `min_bid = standing high bid + minimum raise`.
* If `min_bid > valuation` or `min_bid > remaining_budget`: output `[bid: pass]`.
* If `min_bid <= valuation`: place a bid between `min_bid` and `min(valuation - 1, remaining_budget)` that balances surplus (`valuation - bid`) against win probability. On high-valuation lots with remaining budget, bid high enough above `min_bid` to outcompete opponent raises.
* Never bid at or above my valuation, ensuring every won lot yields strictly positive surplus.

### Formatting
* Keep reasoning concise (a few sentences at most).
* Always conclude the reply with both required tokens:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`