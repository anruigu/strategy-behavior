---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2005
---
# Auction Playbook

## Budget Tracking & State Maintenance
- Always read the exact initial budget from the game rules introduction (e.g. 30, 100). Do not assume a default value of 100 if the prompt specifies a different budget.
- Track remaining budget strictly as: `remaining_budget = starting_budget - sum(all_won_lots_costs)`.
- During Lot 1 (both round 1 and round 2), the remaining budget is still the exact starting budget because no lots have concluded.
- When results are posted at the start of a lot, update remaining budget immediately by subtracting any amounts spent on lots won by me.
- Never place a bid that exceeds `remaining_budget`.
- Always output both required tokens cleanly at the end of every reply:
  ```
  [bid: <N or pass>]
  [budget: <exact_remaining_budget>]
  ```

## Round 1 Bidding (Price Management)
- Calculate the minimum required bid: `min_bid = standing_bid + min_raise`.
- If `min_bid >= my_valuation` or `min_bid > remaining_budget`, bid `[bid: pass]`.
- If `min_bid < my_valuation` and `min_bid <= remaining_budget`:
  - Place exactly the minimum required bid: `[bid: min_bid]`.
  - Never place a jump bid in round 1; keep the price as low as possible going into round 2.

## Round 2 Bidding (Closing the Lot)
- Calculate `min_bid = standing_bid + min_raise`.
- If `min_bid > my_valuation` or `min_bid > remaining_budget`, bid `[bid: pass]`.
- If `min_bid <= my_valuation` and `min_bid <= remaining_budget`:
  - On lots 1 through 4: Bid exactly `min_bid` to maximize surplus per item and preserve budget for future lots.
  - On lot 5 (final lot): Bid `min(my_valuation - 1, remaining_budget)` if `my_valuation - 1 >= min_bid`, otherwise bid `min_bid` if `min_bid == my_valuation`.

## Valuation & Surplus Discipline
- Never bid above valuation (`bid > my_valuation`) under any circumstances to avoid negative surplus.
- If `min_bid == my_valuation`, only bid if it is the final lot or a tie-break with zero downside risk, otherwise prefer passing if budget is tight.