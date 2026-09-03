---
game: ref_auction
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1310
---
# Auction Playbook

## Budget Tracking
- Read the initial starting budget carefully on the first prompt and track remaining cash accurately after every winning outcome.
- When reporting `[budget: N]`, calculate `N = starting_budget - sum(prices_of_lots_won_so_far)` exactly. Never hallucinate default values like 100.
- Ensure any proposed bid does not exceed my current remaining budget.

## Bidding Decisions
- Calculate the minimum allowable bid: `standing_high_bid + minimum_raise` (or simply `minimum_raise` if `standing_high_bid == 0`).
- Compare the required bid against both my private valuation for the lot and my remaining budget.
- When the required bid is strictly less than my private valuation AND less than or equal to my remaining budget:
  - Submit the exact minimum increment needed to take the lead: `[bid: standing_high_bid + minimum_raise]`.
  - Do not jump-bid or bid higher than the minimum increment necessary.
- When the required bid is greater than or equal to my private valuation, or exceeds my remaining budget:
  - Submit `[bid: pass]`.
  - Never bid above my valuation under any circumstances to avoid negative surplus.

## Execution & Formatting
- In every turn, output both required tokens cleanly at the end of the response:
  - `[bid: N]` (or `[bid: pass]`)
  - `[budget: N]`