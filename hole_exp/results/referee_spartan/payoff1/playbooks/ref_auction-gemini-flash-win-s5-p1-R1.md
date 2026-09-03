---
game: ref_auction
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1290
---
- Track my budget accurately from the initial stated amount; never hallucinate or reset the budget to an arbitrary number. At every turn, calculate `[budget: remaining_budget]` as initial budget minus the total winning payments made for past won lots.
- When evaluating a bid, ensure the bid amount does not exceed my true remaining budget.
- In Round 1 of any lot:
  - If my valuation is higher than the minimum allowable bid (standing high bid + minimum raise, or 0 + minimum raise if no bids), place the minimum valid bid to stay in contention without driving up the price prematurely.
  - If my valuation is less than or equal to the minimum allowable bid, pass immediately.
- In Round 2 (the final round for the lot):
  - If the minimum required bid is less than my valuation and within my remaining budget, place a bid that is high enough to win surplus while bidding aggressively enough to outbid opponents (or match the minimum raise if budget/surplus warrants it), provided it remains strictly below my valuation.
  - If the required minimum bid meets or exceeds my private valuation or exceeds my remaining budget, pass.
- Always output exactly the required format ending with `[bid: N]` (or `[bid: pass]`) and `[budget: N]` where `budget` strictly reflects actual cash remaining.