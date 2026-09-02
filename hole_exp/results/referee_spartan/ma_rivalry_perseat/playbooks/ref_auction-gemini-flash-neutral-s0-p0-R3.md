---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 2200
---
# Auction Strategy Playbook

## Budget Tracking & Formatting
- Initialize my tracked budget strictly to the starting budget explicitly stated in the episode rules (read the opening text carefully; do not assume a default number).
- Maintain an accurate running budget throughout the game: `current_budget = starting_budget - total_spent_on_lots_won_by_bidder_0`.
- Do not deduct budget for active bids or un-won lots; deduct only when "bidder 0 won at X" appears in the results.
- Ensure the tracked budget remains consistent across all rounds and lots; never let the budget number jump or reset between rounds within an episode.
- In every reply, output my exact remaining budget in the `[budget: N]` token.
- Always include both required tokens at the end of the response: `[bid: N]` (or `[bid: pass]`) and `[budget: N]`.

## Round 1 Strategy
- Calculate the minimum allowable opening bid: `standing_bid + minimum_raise` (or simply `minimum_raise` if standing bid is 0).
- If `my_value <= minimum_bid` or `current_budget < minimum_bid`, bid `[bid: pass]`.
- If `my_value > minimum_bid` and `current_budget >= minimum_bid`, bid exactly the minimum allowable bid (`standing_bid + minimum_raise`). Never jump bid in Round 1.

## Round 2 Strategy
- Calculate the minimum legal raise: `min_legal_bid = standing_bid + minimum_raise`.
- If I am already the standing high bidder, bid `[bid: pass]` to avoid bidding against myself.
- If `min_legal_bid > my_value` or `min_legal_bid > current_budget`, bid `[bid: pass]`.
- If bidding is viable:
  - On the final lot (Lot 5) or high-valuation lots where surplus is large, consider placing an aggressive bid above `min_legal_bid` (e.g., jump bidding closer to `my_value` while retaining a solid margin) to beat competing bidders who will likely raise above `min_legal_bid`. Ensure the bid is strictly `<= current_budget` and `< my_value`.
  - On earlier lots or modest-value lots, bid the minimum legal raise `min_legal_bid` to maximize profit margin and conserve budget for subsequent opportunities.
- Never bid equal to or higher than `my_value`, ensuring every won lot yields strictly positive surplus.
- Never bid an amount higher than my `current_budget`.