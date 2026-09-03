---
game: ref_auction
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 946
---
- Accurately track my starting budget stated in the initial prompt; do not invent or reset my budget to arbitrary numbers (like 100).
- After winning any lot, subtract the winning price from my current budget and report the exact remaining budget in every subsequent `[budget: N]` token.
- When evaluating a bid on round 1 or round 2:
  - Calculate `min_bid = standing_high_bid + minimum_raise` (or `minimum_raise` if there are no standing bids).
  - If `min_bid <= lot_value` AND `min_bid <= current_budget`, submit `[bid: min_bid]` along with `[budget: current_budget]`.
  - If `min_bid > lot_value` OR `min_bid > current_budget`, submit `[bid: pass]` along with `[budget: current_budget]`.
- Always stick strictly to the minimum required raise (`standing_high_bid + minimum_raise`) to preserve surplus and budget across upcoming lots.
- Ensure every reply ends with the exact formatting tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.