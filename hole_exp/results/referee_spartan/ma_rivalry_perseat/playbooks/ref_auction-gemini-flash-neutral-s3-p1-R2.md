---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1644
---
# AUCTION PLAYBOOK

## Budget Tracking & Protocol
- Initialize my tracked budget to the exact starting budget stated in the opening prompt (read the prompt carefully; do not assume 100 or 30 arbitrarily).
- When results show that bidder 1 (myself) won a lot, subtract the winning price from my tracked budget. If another bidder won, keep my tracked budget unchanged.
- Always output `[budget: B]` using this accurately tracked remaining cash balance in every turn. Never reset budget between lots.
- Never place a bid higher than my currently tracked budget (`bid <= tracked_budget`).

## Valuation & Bidding Rules
- Calculate the minimum legal bid: `standing_bid + minimum_raise` (or just `minimum_raise` if standing bid is 0).
- If `minimum_legal_bid >= my_lot_value` or `minimum_legal_bid > tracked_budget`, output `[bid: pass]`. Never bid above my valuation or above my available budget.

## Round 1 Strategy
- If `minimum_legal_bid < my_lot_value` and within budget, bid exactly `minimum_legal_bid` to enter contention without unnecessarily driving up the price early.

## Round 2 (Final Round) Strategy
- Competitors routinely place jump raises in round 2; bidding only the minimum legal raise usually loses the lot.
- When `my_lot_value` is significantly higher than the standing bid, place a decisive jump bid targeting roughly 65% to 75% of `my_lot_value` (ensuring it is strictly `>= minimum_legal_bid`, `< my_lot_value`, and `<= tracked_budget`).
- When `my_lot_value` only slightly exceeds the standing bid (or surplus margin is narrow), bid the minimum legal raise if profitable, or pass if expected surplus is negative or trivial.