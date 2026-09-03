---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1550
---
### Budget Tracking
* Read the initial budget strictly from the introductory line (e.g. "You start with a budget of 30") and do not assume a default value of 100.
* Explicitly compute `remaining_budget = starting_budget - sum(prices of lots I won in "Results so far")`.
* In every turn, always ensure the reported `[budget: N]` equals this calculated `remaining_budget`.
* Never place a bid `N` that exceeds `remaining_budget`.

### Round 1 Actions
* Calculate `min_bid = standing high bid + minimum raise` (or simply `minimum raise` if no bids yet).
* If `min_bid > valuation` or `min_bid > remaining_budget`: output `[bid: pass]`.
* If `valuation > min_bid` and profit potential exists: make the minimum legal bid (`min_bid`) to remain active in Round 2 without unnecessarily driving up the price.
* If my valuation is weak (e.g., well below estimate) and remaining budget should be saved for better lots: output `[bid: pass]`.

### Round 2 Actions (Final Round)
* Calculate `min_bid = standing high bid + minimum raise`.
* If `min_bid > valuation` or `min_bid > remaining_budget`: output `[bid: pass]`.
* If `min_bid <= valuation`: place a bid between `min_bid` and `min(valuation - 1, remaining_budget)` that maximizes expected surplus (valuation - bid) while bidding aggressively enough to outbid opponents on high-margin lots.
* Never bid at or above my valuation, ensuring every won lot yields positive surplus.

### Formatting
* Always reply with both required tokens at the end of the message:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`