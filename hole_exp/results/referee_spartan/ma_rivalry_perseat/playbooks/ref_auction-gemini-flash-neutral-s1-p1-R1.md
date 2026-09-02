---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1719
---
# Auction Playbook

## Budget Tracking
- Read the opening prompt for my exact starting budget and track it precisely across lots.
- Subtract the actual price paid whenever the auction results show I won a lot (`lot X: bidder 1 won at P`), and report `[budget: current_budget]` on every response.
- Never state a default placeholder budget (like 100) when my starting budget or remaining money is different.

## Valuation & Bidding Bounds
- Calculate maximum allowable bid on any lot as `min(my_value - 1, budget_left)`.
- If the standing high bid plus the minimum raise exceeds `my_value - 1` or exceeds `budget_left`, submit `[bid: pass]`.
- Never place a bid that equals or exceeds my private value for a lot.

## Round 1 Strategy
- When my valuation is higher than the minimum opening bid (`standing_bid + min_raise`), place the minimum valid bid: `standing_bid + min_raise` (or just `min_raise` if standing bid is 0).
- Do not bid higher than the minimum raise in round 1; keep the price low and preserve information for round 2.
- If even the minimum opening bid exceeds `my_value - 1`, submit `[bid: pass]`.

## Round 2 Strategy (Final Round per Lot)
- Evaluate surplus `my_value - bid` on high-margin lots versus expected remaining lots across the auction.
- On lots with high private value relative to estimate, bid aggressively above the minimum raise up toward my valuation limit if needed to shut out competitors, provided significant positive surplus remains.
- On low-margin or marginal lots, submit the minimum legal raise (`standing_bid + min_raise`) if below valuation; otherwise `[bid: pass]`.
- On the final lot (Lot 5/5), use any remaining budget up to `my_value - 1` to capture any positive surplus.