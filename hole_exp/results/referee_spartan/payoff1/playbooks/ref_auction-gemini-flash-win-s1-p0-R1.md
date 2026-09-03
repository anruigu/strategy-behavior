---
game: ref_auction
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1328
---
# Auction Playbook

## Budget Tracking & Accounting
- At the start of the game, initialize my internal budget to the exact starting amount specified in the prompt; never assume a default budget of 100.
- When reporting `[budget: N]`, output the exact remaining budget: starting budget minus the cumulative amount spent on lots won so far.
- Never place a bid higher than my current remaining budget.

## Bidding Strategy
- Calculate the minimum required bid as `standing_bid + minimum_raise` (or just `minimum_raise` if standing bid is 0).
- If the minimum required bid is strictly less than my private valuation for the lot and within my remaining budget, place a bid equal to the minimum required bid to capture positive surplus while conserving capital.
- In round 2/2, if the lot has high surplus potential and another bidder is likely to raise aggressively, consider bidding higher than the minimum raise up to my valuation minus my target margin, but never exceed my valuation or remaining budget.
- If the minimum required bid is greater than or equal to my private valuation, or exceeds my remaining budget, output `[bid: pass]`. Never bid at or above my valuation.
- When bidding on low-valuation lots (where valuation is below the estimate), do not overcommit budget if higher-value opportunities remain in later lots.