---
game: ref_auction
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1643
---
- Read and explicitly verify the initial starting budget stated in the opening prompt (e.g., if starting budget is 30, track down from 30, never hallucinate or reset to 100).
- Explicitly track cumulative expenditure from past won lots: `remaining_budget = starting_budget - sum(payments for lots I won)`.
- At every decision turn, output `[budget: remaining_budget]` accurately reflecting this formula.
- Any valid bid must strictly satisfy `bid <= remaining_budget`. Never bid more money than I currently hold.
- In Round 1 of any lot:
  - Calculate the minimum required bid: `standing high bid + minimum raise` (or `minimum raise` if standing high bid is 0).
  - If my private valuation is strictly greater than the minimum required bid AND `minimum required bid <= remaining_budget`, bid the minimum required bid to stay in contention without inflating the price unnecessarily.
  - Otherwise, pass with `[bid: pass]`.
- In Round 2 (the final round for the lot):
  - Calculate the minimum required bid: `standing high bid + minimum raise`.
  - If the standing high bid is already held by me (if applicable) and no higher bid is required, check if I need to act or pass.
  - If someone else holds the high bid, bid the minimum required bid (or an amount up to `min(valuation - 1, remaining_budget)`) if and only if `minimum required bid < valuation` AND `minimum required bid <= remaining_budget`.
  - If the required minimum bid meets or exceeds my private valuation, or exceeds my remaining budget, output `[bid: pass]`.
- Always conclude responses with the exact required bracketed tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.