---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1721
---
# Auction Playbook

## Budget Tracking & Syntax
- Read the opening prompt for the starting budget; calculate remaining budget strictly as `starting_budget - total_spent_on_won_lots`.
- In round 1 of lot 1 before winning anything, report `[budget: starting_budget]` (or `starting_budget - current_bid` if committed, but maintain exact arithmetic consistency). Never randomly reset or hallucinate the budget to 100 or any other number.
- Always output both required tokens at the end of every reply:
  ```
  [bid: <N or pass>]
  [budget: <exact_remaining_budget>]
  ```

## Round 1 Bidding (Lot Exploration)
- If `standing_bid + min_raise >= my_valuation`, bid `[bid: pass]`.
- If `standing_bid + min_raise < my_valuation`:
  - Bid exactly the minimum required raise: `standing_bid + min_raise`.
  - Never place a large jump bid in round 1; keep the price floor as low as possible for round 2.

## Round 2 Bidding (Final Resolution)
- If `standing_bid + min_raise > my_valuation` or `standing_bid + min_raise > remaining_budget`, bid `[bid: pass]`.
- If `standing_bid + min_raise <= my_valuation` and within budget:
  - On lots 1 through 4: Bid exactly `standing_bid + min_raise`. Do not overbid above the minimum increment to capture maximum surplus.
  - On lot 5 (the final lot): Bid up to `min(my_valuation - 1, remaining_budget)` or the minimum raise necessary to secure the win, ensuring positive surplus (`payoff > 0`).

## Budget Allocation & Low-Value Lots
- When a lot's valuation is marginal (e.g., valuation $\le$ min bid $+ 2$), pass unless it is the final lot and budget remains unspent.
- Do not commit significant budget to low-surplus lots early in the auction; conserve cash for later high-valuation items.