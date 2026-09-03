---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 2023
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Management & State Tracking
- Always accurately report my current remaining budget in `[budget: N]`.
- My remaining budget is strictly `initial_budget - total_spent_on_won_lots`. I do not deduct uncommitted money or alter the reported budget between rounds of the same lot unless a lot was won and paid for.
- Never bid more than my current available budget (`bid <= remaining_budget`).
- Never bid equal to or greater than my private valuation for a lot (`bid < my_value`), ensuring every won lot yields strictly positive surplus (`value - bid > 0`).

## Round 1 Strategy (Opening/Staying Active)
- If `standing_bid == 0` (no bids yet) and `min_raise < my_value`, bid exactly the minimum opening bid (`min_raise`).
- If another bidder holds the standing bid, only raise in Round 1 if `standing_bid + min_raise < my_value` and the required raise leaves ample budget for high-value future lots. Bid exactly `standing_bid + min_raise` to keep the price low.
- If the minimum required bid in Round 1 already eliminates most surplus or exceeds my valuation, output `[bid: pass]`.

## Round 2 Strategy (Final Resolution per Lot)
- Calculate maximum safe bid: `max_bid = min(remaining_budget, my_value - 1)`.
- If `standing_bid + min_raise > max_bid`, output `[bid: pass]`.
- For early/middle lots:
  - Do not overbid aggressively unless it is a premium lot. If competing, place a bid that secures solid surplus (e.g., minimum required raise `standing_bid + min_raise` or a slight jump near the public estimate if surplus remains large) rather than dumping all remaining budget.
- For the final lot:
  - If surplus exists at higher bids, bid aggressively up to `min(remaining_budget, my_value - 1)` to maximize the win probability, since leftover budget has zero terminal value.

## Output Formatting
- Keep reasoning strictly to 1–2 short sentences.
- Always end with exactly the two required tokens on separate lines:
  ```
  [bid: N] (or [bid: pass])
  [budget: N]
  ```