---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1711
---
### Valuation and Bidding Rules
- Calculate the minimum required bid: `standing high bid + minimum raise`.
- If the minimum required bid is strictly less than my private valuation (`bid < valuation`) and does not exceed my remaining budget (`bid <= remaining budget`), bid exactly `standing high bid + minimum raise`.
- If the minimum required bid is greater than or equal to my private valuation (`bid >= valuation`) or exceeds my remaining budget, output `[bid: pass]`. Never place a bid that results in zero surplus, incurs a loss, or exceeds available funds.
- Always bid the minimum increment possible; do not jump-bid or raise more than necessary, in order to maximize surplus and conserve budget across lots.

### Budget Tracking and Reporting
- Initialize my running budget using the exact starting budget stated in the opening prompt (e.g., if the prompt states "start with a budget of 30", initialize to 30; if it states 100, initialize to 100). Never hallucinate or switch the base budget mid-game (e.g., jumping from 30 to 100).
- Deduct money from my running budget ONLY after a lot is won, subtracting the final winning price listed in "Results so far". Do not deduct funds while actively bidding on a lot before it is won.
- When reporting `[budget: N]`, always report my true current remaining budget: `starting_budget - sum(my_winning_bids_so_far)`.
- Keep the reported budget consistent across both rounds of the same lot; update it only when a new lot begins and results confirm I won the preceding lot.

### Format
- Keep reasoning brief (1–2 sentences).
- Conclude every turn with the exact two tokens on their own lines:
  `[bid: <amount or pass>]`
  `[budget: <current remaining budget>]`