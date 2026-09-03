---
game: ref_auction
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 2193
---
# Playbook: Open Ascending Multi-Lot Auction

## Budget Tracking & Hard Constraints
- Read the initial budget carefully at the start of the game (e.g., initial budget might be 30, 100, or any other stated value) and never assume a default.
- Always accurately report remaining budget in `[budget: N]` as: `starting_budget - total_spent_on_won_lots`.
- Check the "Results so far" block at every prompt to confirm which lots I actually won and how much was deducted.
- Hard limits for any bid:
  - `bid <= remaining_budget` (never exceed available cash).
  - `bid < my_value` (never bid equal to or higher than private valuation; ensure `value - bid >= 1`).
  - When raising, the bid must satisfy: `bid >= standing_bid + min_raise` (or `bid >= min_raise` if opening).

## Round 1 Strategy (Opening & Discovery)
- If `standing_bid == 0` (no bids yet):
  - If `min_raise < my_value` and `min_raise <= remaining_budget`, place the minimum opening bid `[bid: min_raise]`.
- If an opponent holds the standing bid:
  - If `standing_bid + min_raise < my_value` and within budget, bid the minimum increment `standing_bid + min_raise` to stay active while keeping the price low.
  - If the required raise exceeds valuation or budget, output `[bid: pass]`.

## Round 2 Strategy (Closing the Lot)
- Compute maximum safe limit: `max_safe_bid = min(remaining_budget, my_value - 1)`.
- Minimum required valid bid to contest is `min_required = standing_bid + min_raise`.
- If `min_required > max_safe_bid`, output `[bid: pass]`.
- For early and intermediate lots:
  - Bid dynamically based on value-to-cost ratio: bid at least `min_required`, and up to a moderate fraction of surplus if competing heavily against active bidders, but conserve budget for higher-estimate future lots.
- For the final lot (or when no valuable upcoming lots remain):
  - Any unused budget has zero terminal value. If `min_required <= max_safe_bid`, bid up to `max_safe_bid` to maximize win probability and capture all remaining surplus.

## Output Formatting
- Keep reasoning to 1–2 short sentences.
- Always conclude with the exact required bracketed tokens on separate lines:
  ```
  [bid: N] (or [bid: pass])
  [budget: N]
  ```