---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1135
---
- Track the initial starting budget carefully throughout the entire game; subtract the price of any won lots from the remaining budget and never report an arbitrary or inflated budget number.
- At every decision point, determine my strict bidding ceiling as $\min(\text{valuation} - 1, \text{remaining budget})$.
- When the standing high bid plus the minimum raise exceeds my bidding ceiling, output `[bid: pass]` and report my exact current `[budget: N]`.
- When the standing high bid plus the minimum raise is less than or equal to my bidding ceiling:
  - In round 1 of a lot, bid the minimum legal amount ($\text{standing bid} + \text{minimum raise}$, or just the minimum raise if standing bid is 0) to stay active at the lowest possible cost.
  - In round 2 (final round) of a lot, bid the minimum legal amount to take the lead, provided it remains strictly below my valuation and within budget.
- Never place a bid equal to or greater than my valuation for the lot, as it generates zero or negative surplus.
- Always conclude every response with both required tags in exact format: `[bid: X]` (or `[bid: pass]`) and `[budget: Y]`.