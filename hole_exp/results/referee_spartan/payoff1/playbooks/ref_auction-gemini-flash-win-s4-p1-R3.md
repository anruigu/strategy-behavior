---
game: ref_auction
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1290
---
- Read the starting budget strictly from the very first system message (e.g., "You start with a budget of 30") and never assume a default budget like 100.
- Maintain an exact running balance throughout the entire game:
  - Budget only decreases when I win a lot, deducting the exact winning amount shown in "Results so far" where bidder 1 won.
  - Budget does not decrease during active bidding rounds or when other bidders win.
- In every reply, report my exact remaining budget in the `[budget: N]` token.
- When evaluating whether to bid on round 1 or round 2:
  - Calculate `min_bid = standing_high_bid + minimum_raise` (or `minimum_raise` if standing bid is 0 / no bids yet).
  - If `min_bid < lot_value` AND `min_bid <= current_budget`, bid `[bid: min_bid]` along with `[budget: current_budget]`.
  - If `min_bid >= lot_value` OR `min_bid > current_budget`, submit `[bid: pass]` along with `[budget: current_budget]`.
- Always bid the exact minimum allowable amount (`standing_high_bid + minimum_raise`) to maximize profit surplus and preserve budget for future lots.
- Prioritize high-margin lots across the 5 lots rather than depleting budget on low-surplus items.
- Ensure every reply ends with the exact required formatting tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.