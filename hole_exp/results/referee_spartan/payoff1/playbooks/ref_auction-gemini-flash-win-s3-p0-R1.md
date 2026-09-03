---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1447
---
- Track my actual starting budget from the initial game prompt and deduct only the winning prices of lots I actually won; never reset or hallucinate my remaining budget (e.g., jumping from 30 to 100).
- When reporting `[budget: N]`, calculate `N = starting_budget - sum(prices_of_lots_won_by_me)` accurately on every round.
- In round 1 of any lot:
  - If the standing high bid is 0 and my valuation is strictly higher than the minimum raise, open with exactly the minimum raise (`[bid: min_raise]`).
  - If there is already a standing high bid, bid `standing_high_bid + min_raise` only if that amount is strictly below my valuation and within my remaining budget; otherwise, pass.
- In round 2 of any lot:
  - Calculate `min_valid_bid = standing_high_bid + min_raise` (or the minimum required bid).
  - If `min_valid_bid <= valuation` and `min_valid_bid <= budget_left`, evaluate the surplus. On normal lots, bid `min_valid_bid` to capture maximum surplus.
  - On the final lot or extremely high-value lots where winning is critical, if `min_valid_bid` is well below valuation and budget, bid aggressively above `min_valid_bid` (e.g., midway between standing bid and valuation, capped by remaining budget) to outbid competing round 2 raises.
  - If `min_valid_bid > valuation` or exceeds my remaining budget, output `[bid: pass]`.
- Always output both required tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]` with exact remaining balance.