---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1801
---
# Auction Strategy Playbook

## Budget Tracking & Formatting
- Initialize my tracked budget to the starting budget given in the rules (e.g., 100 or 30).
- After each lot, compute my remaining budget as `starting_budget - total_spent_on_won_lots`.
- In every reply, output my exact remaining budget in the `[budget: N]` token. Never deduct money for un-won bids or active bids until a lot is officially won.
- Always include both required tokens at the end of the response: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.

## Round 1 Strategy
- Calculate the minimum allowable bid: `standing_bid + minimum_raise` (or simply `minimum_raise` if standing bid is 0).
- If `my_value <= minimum_bid` or `remaining_budget < minimum_bid`, bid `[bid: pass]`.
- If `my_value > minimum_bid` and `remaining_budget >= minimum_bid`, always bid the minimum allowable bid (`standing_bid + minimum_raise`). Do not place aggressive or jump bids in Round 1.

## Round 2 Strategy
- Calculate the minimum legal raise: `standing_bid + minimum_raise`.
- If `standing_bid >= my_value` or `minimum_raise + standing_bid > my_value`, bid `[bid: pass]`.
- If I am already the standing high bidder, pass to avoid bidding against myself.
- When competing on high-value lots where winning surplus is substantial:
  - If it is the final lot or a high-margin lot later in the game, bid aggressively above the minimum raise up to a safe margin below my valuation (and within remaining budget) to shut out competitors.
  - On standard lots or earlier lots, bid the minimum legal raise `standing_bid + minimum_raise` to extract maximum surplus while conserving budget for upcoming lots.
- Never place any bid equal to or exceeding my valuation, as it guarantees zero or negative profit.
- Never bid more than my current available budget.