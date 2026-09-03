---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1479
---
- Read the initial game setup carefully to note the starting budget (e.g., 30 vs 100). Never hallucinate or default to an assumed starting budget of 100 when a different number was given.
- Track my actual remaining budget continuously: calculate `budget_left = starting_budget - sum(prices_of_lots_I_won)`. Never exceed `budget_left` with any bid.
- In every response, always output both required tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: budget_left]` with my true remaining balance.
- Never bid more than my valuation for a lot, and never bid more than my remaining budget.

- Round 1 bidding:
  - If standing high bid is 0 and `min_raise <= valuation` and `min_raise <= budget_left`, bid `min_raise`.
  - If standing high bid > 0, calculate `required_bid = standing_high_bid + min_raise`. Bid `required_bid` if `required_bid <= valuation` and `required_bid <= budget_left`; otherwise, pass.

- Round 2 bidding:
  - Calculate `min_valid_bid = standing_high_bid + min_raise`.
  - If `min_valid_bid > valuation` or `min_valid_bid > budget_left`, output `[bid: pass]`.
  - On normal lots, if `min_valid_bid <= valuation` and `min_valid_bid <= budget_left`, bid `min_valid_bid` to maximize surplus.
  - On high-value or final-round lots where winning provides significant positive surplus and opponents are likely to bid, consider placing a jump bid between `min_valid_bid` and `min(valuation, budget_left)` to secure the lot, provided the resulting surplus is positive.