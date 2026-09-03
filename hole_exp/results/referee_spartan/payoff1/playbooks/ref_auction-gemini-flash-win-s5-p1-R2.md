---
game: ref_auction
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1448
---
- Carefully check the starting budget given in the prompt for the game (e.g. 30, not an assumed 100) and track it strictly from that initial number. At every turn, calculate `[budget: remaining_budget]` as initial starting budget minus the cumulative winning payments made on lots I have actually won.
- Never exceed my true remaining budget with any bid: valid bids must satisfy `bid <= remaining_budget`.
- In Round 1 of any lot:
  - Calculate the minimum required bid: `standing high bid + minimum raise` (or `0 + minimum raise` if standing high bid is 0).
  - If my private valuation is strictly greater than the minimum required bid AND the minimum required bid is `<= remaining_budget`, bid the minimum required bid to stay in contention without inflating the price.
  - Otherwise, pass.
- In Round 2 (final round for the lot):
  - Calculate the minimum required bid: `standing high bid + minimum raise`.
  - If the minimum required bid is strictly less than my private valuation AND `<= remaining_budget`, bid the minimum required bid (or a calculated competitive amount up to `min(valuation - 1, remaining_budget)`) to capture positive surplus.
  - If the required minimum bid meets or exceeds my private valuation, or exceeds my remaining budget, pass.
- Always output exactly the required format ending with `[bid: N]` (or `[bid: pass]`) and `[budget: N]`, ensuring the budget token matches my true tracked remaining budget at every step.