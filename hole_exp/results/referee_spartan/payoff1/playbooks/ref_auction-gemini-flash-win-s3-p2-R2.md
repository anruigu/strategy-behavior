---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1320
---
- Track my starting budget strictly from the initial game prompt and never change or hallucinate a new baseline (e.g., do not switch a budget of 30 to 100).
- Deduct money from my remaining budget only when I actually win a lot (as shown in "Results so far"); during the bidding rounds of an active lot, my available budget remains what I held entering the lot.
- In every reply, format the required tokens exactly:
  `[bid: N]` or `[bid: pass]`
  `[budget: N]` (where `N` is my exact remaining budget).
- When deciding a bid, calculate the minimum legal bid: `standing_high_bid + minimum_raise`.
- If the minimum legal bid exceeds my valuation or exceeds my remaining budget, output `[bid: pass]` along with `[budget: N]`.
- In round 1 of a lot, if `standing_high_bid + minimum_raise <= valuation` and `<= remaining_budget`, bid exactly `standing_high_bid + minimum_raise` to keep prices low while staying in contention.
- In round 2 (the final round for the lot), if `standing_high_bid + minimum_raise < valuation` and `<= remaining_budget`, bid exactly `standing_high_bid + minimum_raise` to win the lot and maximize surplus.
- If `standing_high_bid + minimum_raise == valuation`, pass to avoid zero-surplus risk.
- Never bid above my valuation for a lot or more than my true remaining budget under any circumstances.