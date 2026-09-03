---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1319
---
# Auction Playbook

## Budget Tracking
- Note the exact starting budget stated in the initial rules prompt (e.g., 30, not an assumed default like 100).
- Explicitly update remaining budget each round: `remaining_budget = starting_budget - sum(prices of lots I won so far)`.
- When reporting `[budget: N]`, output the exact calculated `remaining_budget`. Double-check this number before every reply.
- Ensure any proposed bid strictly satisfies `bid <= remaining_budget`.

## Bidding Decisions
- Determine the minimum required bid:
  - If `standing_high_bid == 0`: `required_bid = minimum_raise`.
  - If `standing_high_bid > 0`: `required_bid = standing_high_bid + minimum_raise`.
- Compare `required_bid` against both my valuation for the current lot and my true `remaining_budget`.
- If `required_bid < valuation` AND `required_bid <= remaining_budget`:
  - Bid the minimum required amount: `[bid: required_bid]`.
  - Do not jump-bid; increment only by the minimum raise to conserve budget and surplus.
- If `required_bid >= valuation` OR `required_bid > remaining_budget`:
  - Submit `[bid: pass]`.
  - Never bid at or above valuation or exceed remaining budget.

## Execution & Formatting
- In every turn, end the reply with both required tokens formatted exactly:
  - `[bid: N]` (or `[bid: pass]`)
  - `[budget: N]`