---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1910
---
### Budget Accounting
- Note the initial starting budget carefully from the initial prompt text (e.g., budget can be 30 or 100). Do not assume a default number like 100 when a lower budget is specified.
- Deduct the winning price from the remaining budget only when a lot is won (indicated under "Results so far: bidder 0 won at X"); do not change or reduce budget for un-won or lost lots.
- Always output `[budget: remaining_budget]` accurately alongside every bid or pass.

### Bidding Rules & Valuation Thresholds
- Strictly maintain `bid < valuation` at all times. Never bid equal to or greater than private valuation, as this guarantees zero or negative surplus.
- Never bid more than my remaining budget (`bid <= remaining_budget`).
- When opening a lot in Round 1:
  - Always bid the minimum opening amount (the minimum raise). Do not jump-bid or open high.
- When raising in Round 1:
  - Always raise by exactly the minimum required increment (`standing high bid + minimum raise`), provided it is strictly below valuation and within budget.
- In Round 2 (the final round for each lot):
  - Evaluate the minimum required bid (`standing high bid + minimum raise`).
  - If the minimum required bid is `>= valuation` or `> remaining_budget`, immediately reply `[bid: pass]`.
  - If the minimum required bid is `< valuation` and within budget, place a competitive bid strictly below valuation (e.g., around 70–85% of valuation, or a calculated increment above standing bid) to secure positive surplus against rival round-2 bids, capped at `min(valuation - 1, remaining_budget)`.
  - If the valuation is only marginally above the standing bid, bid the minimum required amount to preserve whatever positive surplus remains.

### Response Format
- Keep reasoning brief (1–2 sentences).
- Always include both required bracketed tokens at the end of the response: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.