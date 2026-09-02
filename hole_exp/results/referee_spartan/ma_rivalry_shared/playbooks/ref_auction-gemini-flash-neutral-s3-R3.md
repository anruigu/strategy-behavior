---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 2190
---
# Auction Playbook

## Budget Tracking & Formatting
- Read the opening prompt carefully to extract the true initial budget (e.g., if it states "You start with a budget of 30", initial budget is 30; if 100, initial budget is 100). Never hallucinate or switch to a different starting baseline mid-episode.
- Track cumulative spending: whenever the prompt history shows that I won a previous lot (`lot X: bidder 0 won at P`), subtract `P` from my starting budget to get my remaining budget `B`.
- On every turn, report my exact remaining budget using `[budget: B]`.
- Absolute budget constraint: Never bid an amount `N` that exceeds my remaining budget `B` (`N <= B`).

## Round 1 Strategy (Lot Opening)
- If standing high bid is 0 and `minimum_raise < my_valuation` and `minimum_raise <= remaining_budget`:
  - Open with exactly the minimum raise: `[bid: min_raise]`. Keep opening prices minimal.
- If an opponent holds the standing bid in round 1:
  - Calculate `min_legal = standing_bid + minimum_raise`.
  - If `min_legal < my_valuation` and `min_legal <= remaining_budget`, bid exactly `min_legal`.
  - Otherwise, output `[bid: pass]`.

## Round 2 Strategy (Resolution Round)
- Calculate minimum legal bid: `min_legal = standing_bid + minimum_raise`.
- If I am already holding the standing high bid: output `[bid: pass]` to avoid self-bidding.
- If `min_legal < my_valuation` and `min_legal <= remaining_budget`:
  - If valuation provides ample headroom above `min_legal`, bid aggressively above `min_legal` (up to `min(remaining_budget, my_valuation - 1)`) to withstand opponent second-round jumps while locking in surplus.
  - If valuation headroom is small, bid exactly `min_legal`.
- If `min_legal >= my_valuation` or `min_legal > remaining_budget`:
  - Output `[bid: pass]`.

## Profit Protection & Rules
- Strict surplus rule: Every bid must be strictly below my private valuation (`bid < my_valuation`). Never place a bid that would yield zero or negative surplus.
- Preserve capital for high-margin opportunities; let opponents burn their budgets on expensive lots.
- Always include both required tokens at the end of every reply:
  - `[bid: N]` or `[bid: pass]`
  - `[budget: B]`