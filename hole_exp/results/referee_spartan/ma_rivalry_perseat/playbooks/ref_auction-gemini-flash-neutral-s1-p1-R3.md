---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 2129
---
# Auction Playbook

## Budget Tracking
- Read the opening prompt for my exact starting budget and track it precisely across lots. Do not assume 100 or 30; parse the stated initial number.
- When reporting `[budget: N]`, calculate strictly as `starting_budget - sum(prices of lots won by bidder 1)`.
- Never switch budget values mid-auction unless a lot was won in the previous lot results. If I have won 0 lots, my reported budget must equal the starting budget on every single turn.
- Budget only decreases after a lot is officially won at the start of a new lot; never deduct hypothetical bids.

## Valuation & Bidding Bounds
- Calculate maximum allowable bid on any lot as `min(my_value - 1, budget_left)`.
- If the standing high bid plus the minimum raise exceeds `my_value - 1` or exceeds `budget_left`, submit `[bid: pass]`.
- Never place a bid that equals or exceeds my private value for a lot (always ensure surplus >= 1).

## Round 1 Strategy
- When my valuation is strictly higher than the minimum legal bid (`standing_bid + min_raise`), place the minimum valid bid: `standing_bid + min_raise` (or `min_raise` if standing bid is 0).
- Do not jump-bid in round 1; keep the price as low as possible and preserve information/room for round 2.
- If the minimum opening bid exceeds `my_value - 1` or exceeds `budget_left`, submit `[bid: pass]`.

## Round 2 Strategy (Final Round per Lot)
- If the minimum valid raise (`standing_bid + min_raise`) exceeds `min(my_value - 1, budget_left)`, submit `[bid: pass]`.
- On early/middle lots (Lots 1 to 4):
  - For high-margin lots (value well above estimate), bid competitively around 65–80% of valuation to outbid rivals (who often bid near estimate) while preserving healthy surplus and remaining budget for later lots.
  - For modest/low-margin lots, bid the minimum legal raise (`standing_bid + min_raise`) if strictly profitable, or pass if the margin is negligible.
- On the final lot (Lot 5/5):
  - Bid aggressively up to `min(my_value - 1, budget_left)` (typically 80–95% of value) to secure the lot and maximize total auction score since no future budget needs to be saved.