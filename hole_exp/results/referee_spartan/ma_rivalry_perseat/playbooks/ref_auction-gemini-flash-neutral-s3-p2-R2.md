---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1862
---
# Auction Playbook

## Budget Tracking & State Maintenance
- Always track remaining budget strictly as `starting_budget - total_spent_on_won_lots`.
- In all rounds of Lot 1 (before any lot results are finalized), the remaining budget is the initial starting budget. Never hallucinate an arbitrary budget (e.g. 100).
- When lots are won, update remaining budget immediately upon seeing the results: `remaining_budget = starting_budget - sum(winning_bids)`.
- Always output both required tokens at the end of every reply:
  ```
  [bid: <N or pass>]
  [budget: <exact_remaining_budget>]
  ```

## Round 1 Bidding (Price Management)
- If `standing_bid + min_raise >= my_valuation` or `standing_bid + min_raise > remaining_budget`, bid `[bid: pass]`.
- If `standing_bid + min_raise < my_valuation`:
  - Bid exactly the minimum required bid: `standing_bid + min_raise`.
  - Never place a jump bid in round 1; keep the price floor as low as possible for round 2.

## Round 2 Bidding (Closing the Lot)
- If `standing_bid + min_raise > my_valuation` or `standing_bid + min_raise > remaining_budget`, bid `[bid: pass]`.
- If `standing_bid + min_raise <= my_valuation` and within budget:
  - On lots 1 through 4: Bid exactly `standing_bid + min_raise` to maximize per-lot surplus.
  - On lot 5 (final lot): Bid aggressively to secure any remaining surplus—bid `min(my_valuation - 1, remaining_budget)` if `my_valuation > standing_bid + min_raise`, otherwise bid `standing_bid + min_raise` if `my_valuation == standing_bid + min_raise`.

## Surplus & Marginal Lots
- Pass on marginal lots where `my_valuation - (standing_bid + min_raise) <= 1` during early rounds if budget conservation is needed for higher-estimate lots later.
- Never bid equal to or above valuation (`bid >= valuation`) under any circumstance; always guarantee non-negative, positive surplus on won lots.