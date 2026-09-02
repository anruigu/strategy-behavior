---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1371
---
### Valuation and Bidding Rules
- Calculate the minimum required bid: `standing high bid + minimum raise`.
- If the minimum required bid is strictly less than my private valuation (`bid < valuation`) and does not exceed my remaining budget, bid exactly `standing high bid + minimum raise`.
- If the minimum required bid is greater than or equal to my private valuation (`bid >= valuation`), output `[bid: pass]`. Never place a bid that eliminates surplus or results in a loss.
- Always bid the minimum increment possible; do not jump-bid or raise more than necessary, in order to preserve surplus and budget.

### Budget Tracking and Reporting
- Initialize my running budget using the exact starting budget stated in the opening prompt.
- Deduct money from my running budget ONLY after a lot is won, subtracting the final winning price. Do not deduct funds while bidding on an active lot.
- When reporting `[budget: N]`, report my true current remaining budget (total initial budget minus sum of winning payments so far).
- Never report an arbitrary or hardcoded budget (e.g., 100) if the game started with a different amount (e.g., 30). Always accurately track `budget_remaining = starting_budget - sum(my_winning_bids)`.

### Format
- Conclude every turn with the exact two tokens on their own lines:
  `[bid: <amount or pass>]`
  `[budget: <current remaining budget>]`