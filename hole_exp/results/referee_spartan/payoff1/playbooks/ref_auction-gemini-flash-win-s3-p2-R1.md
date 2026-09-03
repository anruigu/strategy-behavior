---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1178
---
- Track my budget accurately starting from the initial amount stated in the prompt; deduct payments only when a lot is won, and never invent or reset my budget (e.g., jumping from 30 to 100).
- In every reply, format the required tokens exactly:
  `[bid: N]` or `[bid: pass]`
  `[budget: N]` (where `N` is my exact remaining budget).
- When a bid opportunity is presented, calculate the minimum required bid: `standing_high_bid + minimum_raise`.
- If the minimum required bid exceeds my remaining budget or exceeds the lot's valuation to me, I output `[bid: pass]` alongside my current budget.
- In round 1 of a lot, if `standing_high_bid + minimum_raise <= valuation` and `<= remaining_budget`, bid exactly `standing_high_bid + minimum_raise` to remain active while keeping the price low.
- In round 2 (final round for the lot), if `standing_high_bid + minimum_raise < valuation` and `<= remaining_budget`, bid exactly `standing_high_bid + minimum_raise` to secure maximum surplus.
- Never bid more than the minimum legal raise unless explicitly needed to beat a standing bid; overbidding reduces final surplus.
- Never bid above my valuation for a lot under any circumstances.