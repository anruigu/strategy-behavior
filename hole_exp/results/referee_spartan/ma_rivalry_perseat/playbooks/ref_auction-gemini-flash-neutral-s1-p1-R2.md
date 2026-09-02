---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 1787
---
# Auction Playbook

## Budget Tracking
- Read the opening prompt for my exact starting budget and track it precisely across lots. Never assume a default budget of 100 or 30 without reading the prompt.
- When reporting `[budget: N]`, track starting budget minus the sum of winning prices where `lot X: bidder 1 won at P`.
- Keep the budget count consistent across all rounds within the same lot (budget only decreases after a lot is won).

## Valuation & Bidding Bounds
- Calculate maximum allowable bid on any lot as `min(my_value - 1, budget_left)`.
- If the standing high bid plus the minimum raise exceeds `my_value - 1` or exceeds `budget_left`, submit `[bid: pass]`.
- Never place a bid that equals or exceeds my private value for a lot.

## Round 1 Strategy
- When my valuation is higher than the minimum opening bid (`standing_bid + min_raise`), place the minimum valid bid: `standing_bid + min_raise` (or just `min_raise` if standing bid is 0).
- Do not bid higher than the minimum raise in round 1; keep the price low and preserve room for round 2.
- If the minimum opening bid exceeds `my_value - 1`, submit `[bid: pass]`.

## Round 2 Strategy (Final Round per Lot)
- Evaluate surplus `my_value - bid` on high-margin lots versus expected remaining lots across the auction.
- On lots with high private value relative to the estimate, bid sufficiently above the minimum raise (e.g. ~60-70% of private value or higher depending on competitor aggression) to win the lot while retaining healthy surplus.
- On low-margin or marginal lots, submit the minimum legal raise (`standing_bid + min_raise`) if strictly below valuation; otherwise `[bid: pass]`.
- On the final lot (Lot 5/5), bid aggressively up to `min(my_value - 1, budget_left)` to extract any remaining profitable surplus.