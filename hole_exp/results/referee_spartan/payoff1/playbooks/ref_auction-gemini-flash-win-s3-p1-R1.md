---
game: ref_auction
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1467
---
### Budget Tracking
* Read the initial budget carefully from the opening instructions (e.g. 30, not 100) and track exact cash remaining across all lots.
* When deducting cash, subtract only the winning prices of lots I actually won as reported in "Results so far".
* In every response, ensure `[budget: N]` reflects `Initial Budget - Total Spent on Won Lots`. Never bid more than this remaining budget.

### Round 1 Actions
* If standing high bid + minimum raise > my valuation or > remaining budget: output `[bid: pass]`.
* If my valuation is high relative to the estimate: place the minimum legal raise (`standing high bid + minimum raise`) to stay alive for Round 2 without prematurely driving up the price.
* If my valuation is very low (below the estimate) and no one has bid: pass or place the absolute minimum opening bid only if profit margin is wide, but prefer preserving budget for high-value lots.

### Round 2 Actions (Final Round)
* Never bid on a lot if the minimum required bid (`standing high bid + minimum raise`) exceeds my valuation or my remaining budget. In that case, output `[bid: pass]`.
* When my valuation is significantly higher than the standing bid and competition is active: bid higher than the minimum increment to protect against snipes, up to my valuation or budget limit, balancing surplus against win probability.
* When bidding, output the exact integer bid amount in `[bid: N]` and the accurate remaining budget in `[budget: N]`.