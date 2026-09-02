---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 2235
---
# Auction Playbook

## Budget Tracking & Formatting
- Initialize my internal budget tracker strictly to the starting budget stated in the opening prompt (e.g., if the opening rules state "You start with a budget of 30", initial budget is 30; if it states 100, initial budget is 100).
- Whenever I win a lot, subtract the winning price from my remaining budget.
- On every single turn, accurately output `[budget: B]` where `B` is my exact current remaining budget. Double-check that I do not default to 100 when my starting budget was 30 or after winning previous lots.
- Never place a bid `N` that exceeds my remaining budget `B`. Always ensure `N <= B`.

## Round 1 Strategy (Lot Setup)
- If the standing high bid is 0 and the lot's value to me exceeds the minimum raise, open with exactly the minimum raise `[bid: min_raise]`. Keep opening prices as low as possible.
- If an opponent holds the standing bid in round 1, bid `standing_bid + minimum_raise` only if that amount is strictly less than my valuation and within my remaining budget.
- If the minimum required bid is greater than or equal to my valuation or exceeds my remaining budget, output `[bid: pass]`.

## Round 2 Strategy (Resolution Round)
- Calculate the minimum legal winning bid: `target = standing_bid + minimum_raise`.
- If I am already the standing high bidder, pass to avoid bidding against myself.
- If `target < my_valuation` and `target <= remaining_budget`:
  - When the margin between `target` and `my_valuation` is wide (e.g., valuation significantly higher than target), place a competitive bid between `target` and `my_valuation - 1` (capped by remaining budget) to beat opponent snipes while locking in positive surplus.
  - When the margin is thin, bid exactly `target`.
- If `target >= my_valuation` or `target > remaining_budget`, immediately choose `[bid: pass]`.

## Profit Protection & Discipline
- Strict surplus rule: Never bid equal to or higher than my valuation for a lot (`bid < my_valuation` must always hold).
- Zero or negative profit wins waste scarce budget; pass and let opponents overpay and deplete their funds.
- Always output both required tokens on separate lines or at the end: `[bid: N]` (or `[bid: pass]`) and `[budget: B]`.