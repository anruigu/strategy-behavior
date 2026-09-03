---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1485
---
- Read the initial game setup carefully to note the starting budget (e.g., 30 vs 100). Never hallucinate or default to an assumed starting budget of 100 when a different number was given in the initial prompt.
- Explicitly track my actual remaining budget continuously: calculate `budget_left = starting_budget - sum(prices_of_lots_I_won)`. Double-check the starting budget before doing math.
- Never exceed `budget_left` with any bid. If a bid would exceed `budget_left`, pass.
- In every response, always output both required tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: budget_left]` reporting my true remaining balance.
- Never bid more than my valuation for a lot. If `required_bid >= valuation`, pass (or only bid if strictly positive surplus is guaranteed, avoiding 0-surplus bids).

- Round 1 bidding:
  - If standing high bid is 0 and `min_raise < valuation` and `min_raise <= budget_left`, bid `min_raise`.
  - If standing high bid > 0, calculate `required_bid = standing_high_bid + min_raise`. Bid `required_bid` if `required_bid < valuation` and `required_bid <= budget_left`; otherwise, pass.

- Round 2 bidding:
  - Calculate `min_valid_bid = standing_high_bid + min_raise`.
  - If `min_valid_bid >= valuation` or `min_valid_bid > budget_left`, output `[bid: pass]`.
  - If `min_valid_bid < valuation` and `min_valid_bid <= budget_left`, bid `min_valid_bid` (or a selective raise up to `min(valuation - 1, budget_left)` if securing surplus) to maximize net profit.