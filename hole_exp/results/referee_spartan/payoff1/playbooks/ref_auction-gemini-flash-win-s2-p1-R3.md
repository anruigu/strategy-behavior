---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1327
---
- Read the starting budget carefully from the initial prompt (e.g., budget 30, not an assumed 100) and track it strictly across all turns.
- Maintain an exact running balance: start with the explicit initial budget, deduct only what I personally won and paid for (verify against "Results so far: lot X: bidder <my_id> won at Z"), and never hallucinate or reset the budget to 100.
- Output my exact current remaining budget on every turn in `[budget: N]`.
- For each turn, determine the minimum allowable bid:
  - If standing high bid is 0: `minimum_raise`.
  - If standing high bid > 0: `standing_high_bid + minimum_raise`.
- Do not raise if I am already the standing high bidder.
- Check bid feasibility: if the minimum allowable bid exceeds my valuation for the lot or exceeds my current remaining budget, output `[bid: pass]`.
- In round 1/2: if the minimum allowable bid is strictly below valuation and within budget, bid the minimum allowable bid to stay in contention cheaply.
- In round 2/2 (final round): bid the minimum allowable bid if `valuation - bid > 0` and `bid <= remaining_budget`; otherwise pass.
- Never bid above my valuation, as winning at a price higher than valuation yields negative surplus.
- Ensure every reply ends with both required bracketed tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.