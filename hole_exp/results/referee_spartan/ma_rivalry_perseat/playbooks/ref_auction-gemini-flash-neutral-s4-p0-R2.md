---
game: ref_auction
model: gemini-flash
condition: neutral
seed: 4
round: 2
chars: 1793
---
# Auction Playbook

## Budget Tracking & Formatting
- Read the starting budget strictly from the introductory text (e.g., 30 or 100). Do not hallucinate or switch starting budget across rounds.
- When an auction result shows that I won a lot at price $P$, immediately deduct $P$ from my internal budget tracker: `remaining_budget = remaining_budget - P`.
- When reporting `[budget: N]`, always output my exact remaining budget.
- Ensure every bid $B$ satisfies $B \le \text{remaining\_budget}$. Never bid more than my current available cash.

## Round 1 Strategy
- If the standing bid plus the minimum raise is strictly less than my valuation, enter with the minimum legal bid (`standing_bid + min_raise`, or `min_raise` if standing bid is 0).
- Never jump-bid or bid above the minimum legal amount in Round 1; keeping the standing price minimal preserves surplus and room for Round 2.
- If the minimum legal bid is greater than or equal to my valuation or exceeds remaining budget, bid `[bid: pass]`.

## Round 2 Strategy (Final Round of a Lot)
- Calculate the minimum required bid: `min_bid = standing_bid + min_raise`.
- If `min_bid >= my_valuation` or `min_bid > remaining_budget`, reply with `[bid: pass]`.
- If `min_bid < my_valuation`:
  - Competitors frequently bid `min_bid + min_raise` (e.g., standing bid + 2 increments) in Round 2.
  - If my valuation allows a strong profit margin, place a competitive bid above the minimum (typically `min_bid + min_raise` / standing bid + 2 raises, or up to ~65–75% of valuation) to outbid opponents while guaranteeing positive surplus.
  - If the valuation margin is tight (e.g., `min_bid` is close to valuation), bid exactly `min_bid`.
  - Always strictly cap bids at `min(remaining_budget, my_valuation - 1)`. Never bid at or above valuation.