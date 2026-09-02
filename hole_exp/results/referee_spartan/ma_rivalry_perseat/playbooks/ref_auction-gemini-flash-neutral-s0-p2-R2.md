---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 2
chars: 1555
---
### Valuation and Bidding Rules
- Calculate the minimum required bid: `standing high bid + minimum raise`.
- If the minimum required bid is strictly less than my private valuation (`bid < valuation`) and does not exceed my remaining budget (`bid <= remaining budget`), bid exactly `standing high bid + minimum raise`.
- If the minimum required bid is greater than or equal to my private valuation (`bid >= valuation`) or exceeds my remaining budget, output `[bid: pass]`. Never place a bid that eliminates surplus, results in a loss, or exceeds available funds.
- Always bid the minimum increment possible; do not jump-bid or raise more than necessary, in order to preserve surplus and budget.

### Budget Tracking and Reporting
- Initialize my running budget using the exact starting budget stated in the opening prompt (read the prompt carefully; do not assume a default number like 100 if the prompt specifies 30).
- Deduct money from my running budget ONLY after a lot is won, subtracting the final winning price listed in "Results so far". Do not deduct funds while bidding on an active lot.
- When reporting `[budget: N]`, always report my true current remaining budget: `starting_budget - sum(my_winning_bids)`.
- Keep the reported budget consistent across all rounds within the same lot, updating it only at the start of a new lot if I won the preceding one.

### Format
- Keep reasoning brief (1–2 sentences).
- Conclude every turn with the exact two tokens on their own lines:
  `[bid: <amount or pass>]`
  `[budget: <current remaining budget>]`