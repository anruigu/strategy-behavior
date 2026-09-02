---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 1
chars: 1824
---
# Auction Playbook

## Budget Tracking & Formatting
- Initialize my tracked budget to the exact starting budget given in the rules (e.g., 30 or 100). Do not assume 100 if the game states 30.
- When an auction result shows that I won a lot at price $P$, immediately deduct $P$ from my internal budget tracker: `remaining_budget = remaining_budget - P`.
- When reporting `[budget: N]`, always output my actual remaining budget after deducting past wins.
- Ensure my bid $B$ satisfies $B \le \text{remaining\_budget}$. Never bid more than my current available cash.

## Round 1 Strategy
- If the standing bid plus the minimum raise is strictly less than my valuation, always enter with the minimum legal bid (`standing_bid + min_raise`, or `min_raise` if no bids yet).
- Never open or jump-bid with large amounts in Round 1. It only drives up the price unnecessarily and reduces profit margins.
- If the minimum legal bid is greater than or equal to my valuation, immediately bid `[bid: pass]`.

## Round 2 Strategy (Final Round of a Lot)
- Calculate the minimum required bid: `min_bid = standing_bid + min_raise`.
- If `min_bid >= my_valuation` or `min_bid > remaining_budget`, reply with `[bid: pass]`.
- If `min_bid < my_valuation`:
  - When the valuation-to-estimate ratio is high (a high-surplus lot) or in later lots where competitors aggressively raise, bid a competitive amount above `min_bid` (e.g., `min_bid + min_raise` or a calculated push bid) while staying strictly below my valuation and within remaining budget to ensure winning the surplus.
  - When the margin between `min_bid` and my valuation is small, bid exactly the minimum required bid to preserve any positive surplus.
- Never bid at or above my valuation under any circumstance. Every bid must leave a strictly positive margin (`valuation - bid > 0`).