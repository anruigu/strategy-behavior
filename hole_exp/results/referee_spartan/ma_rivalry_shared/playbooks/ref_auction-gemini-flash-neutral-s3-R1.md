---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 2018
---
# Auction Playbook

## Budget Tracking & Formatting
- Initialize my internal budget tracker to the starting budget stated in the opening prompt (e.g., 30 or 100).
- Whenever I win a lot, subtract the winning price from my remaining budget.
- On every turn, accurately output `[budget: B]` where `B` is my exact current remaining budget. Never report a generic 100 when my starting budget was different or when I have already spent funds.
- Never place a bid `N` that exceeds my remaining budget `B`.

## Round 1 Strategy (Lot Setup)
- If the standing high bid is 0 and the lot's value to me exceeds the minimum raise, open with exactly the minimum raise `[bid: min_raise]`. Never make high opening jumps in round 1; keep prices as low as possible.
- If an opponent holds the standing bid in round 1, bid `standing_bid + minimum_raise` only if that amount is strictly less than my valuation. If the minimum required bid is greater than or equal to my valuation, choose `[bid: pass]`.

## Round 2 Strategy (Resolution Round)
- Calculate the minimum legal winning bid: `target = standing_bid + minimum_raise` (or the standing bid if I am already the standing high bidder, in which case do not outbid myself—pass).
- If `target < my_valuation` and `target <= remaining_budget`:
  - When the margin between `target` and `my_valuation` is high (especially on later lots or the final lot), place a strong bid between `target` and `my_valuation - 1` to prevent last-second sniping if budget allows, but never bid above `my_valuation - 1`.
  - When the margin is thin, bid exactly `target`.
- If `target >= my_valuation` or `target > remaining_budget`, immediately choose `[bid: pass]`.

## Profit Protection & Discipline
- Never bid equal to or higher than my valuation for a lot (`bid < valuation` must always hold). A zero-profit win wastes budget that could win subsequent high-margin lots.
- Do not chase bids upward in bidding wars when opponents push the price near my valuation; pass and let them exhaust their budgets.