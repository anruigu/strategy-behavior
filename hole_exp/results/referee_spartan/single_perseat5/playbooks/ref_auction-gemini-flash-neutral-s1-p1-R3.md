---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1584
---
# Auction Playbook

## Initial Setup & Budget Tracking
* Read the initial budget explicitly stated in the opening prompt (e.g., if it states a budget of 30, use 30; never assume 100).
* Track current budget rigorously: `remaining_budget = initial_budget - sum(prices of lots won so far)`.
* Every response must output `[budget: remaining_budget]` using this exact tracked amount.
* Never place a bid `> remaining_budget`.

## Round 1 Bidding (Opening Round)
* Calculate minimum valid bid: `standing_bid + minimum_raise` (or `minimum_raise` if standing bid is 0).
* If minimum valid bid `< valuation` and `<= remaining_budget`:
  * Bid exactly the minimum valid bid to stay active without unnecessarily inflating the price.
* Otherwise:
  * Reply `[bid: pass]`.

## Round 2 Bidding (Final Round)
* Calculate minimum required bid: `standing_bid + minimum_raise`.
* If minimum required bid `>= valuation` or `> remaining_budget`:
  * Reply `[bid: pass]`.
* If viable, select a final bid strictly satisfying:
  `minimum_required_bid <= bid <= min(valuation - 1, remaining_budget)`
* Target bid level:
  * Aim for roughly 75%–85% of valuation (or `valuation - minimum_raise`), bounded by available budget, to outbid competitor jump bids while locking in positive surplus.
  * When opponents are aggressive or on high-value/late lots, bid closer to `min(valuation - 1, remaining_budget)` to secure the surplus.

## Response Formatting
* Keep reasoning brief (1–2 sentences).
* Always end with both required bracketed tokens on separate lines:
  `[bid: N]` (or `[bid: pass]`)
  `[budget: N]`