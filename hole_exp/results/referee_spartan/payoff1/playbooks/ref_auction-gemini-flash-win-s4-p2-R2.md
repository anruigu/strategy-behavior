---
game: ref_auction
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1314
---
# Auction Playbook

## Budget Tracking
* Read the initial budget carefully from the opening instructions and do not assume a default value like 100.
* Explicitly maintain the remaining budget after each lot:
  $$\text{Current Budget} = \text{Initial Budget} - \sum \text{Winning Bids on Completed Lots I Won}$$
* Always report `[budget: B]` matching my true remaining budget across all rounds and lots, even when passing.
* Never place a bid $N > \text{Current Budget}$.

## Bidding Strategy
* Calculate the minimum valid bid: $\text{min\_bid} = \text{standing high bid} + \text{minimum raise}$.
* Pass (`[bid: pass]`) whenever:
  * $\text{min\_bid} \ge \text{my valuation}$ (avoids zero or negative surplus).
  * $\text{min\_bid} > \text{Current Budget}$ (exceeds available funds).
* When $\text{min\_bid} < \text{my valuation}$ and $\text{min\_bid} \le \text{Current Budget}$:
  * Round 1: Place a bid of exactly $\text{min\_bid}$ to stay in contention cheaply.
  * Round 2: Bid $\text{min\_bid}$ if it locks in positive surplus ($\text{valuation} - \text{min\_bid} > 0$), provided winning at this price leaves enough budget for upcoming lots with potentially higher expected surplus.
* Never bid above my valuation on any lot. Always output both required tokens: `[bid: N]` (or `[bid: pass]`) and `[budget: B]`.