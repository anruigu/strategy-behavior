---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1454
---
# AUCTION PLAYBOOK

## Budget Tracking & Protocol
- Initialize my tracked budget to the exact starting budget stated in the opening prompt (not 100 unless explicitly given 100).
- When I win a lot, subtract the winning price from my tracked budget. When I do not win, keep my tracked budget unchanged.
- Always output `[budget: B]` using this accurately tracked remaining cash balance in every turn.

## Valuation & Bidding Rules
- Calculate the minimum legal bid: `standing_bid + minimum_raise` (or just `minimum_raise` if standing bid is 0).
- If `minimum_legal_bid >= my_lot_value` or `minimum_legal_bid > tracked_budget`, output `[bid: pass]`. Never bid above my valuation or above my available budget.

## Round 1 Strategy
- If `minimum_legal_bid < my_lot_value`, bid exactly `minimum_legal_bid` to enter contention without unnecessarily inflating the price.

## Round 2 (Final Round) Strategy
- Competitors routinely raise by extra increments in round 2; placing only the bare minimum raise often results in getting outbid by a rival's round-2 jump.
- When `my_lot_value` is significantly higher than the standing bid, bid aggressively above the minimum raise—target a bid around 60% to 75% of `my_lot_value` (capped at my tracked budget) to outbid competitor jump-bids while still locking in substantial surplus.
- When `my_lot_value` only slightly exceeds the standing bid, bid the minimum legal raise or pass if the expected surplus is too slim.