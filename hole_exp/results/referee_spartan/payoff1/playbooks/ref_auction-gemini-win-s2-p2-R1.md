---
game: ref_auction
model: gemini
condition: win
seed: 2
round: 1
chars: 1000
---
When starting a new game, I read the exact starting budget from the opening instructions rather than assuming a standard amount like 100. 

When tracking my available funds, I calculate my current budget by subtracting the exact amounts of the lots I have already won (listed under "Results so far") from my true starting budget. 

When deciding whether to bid, I check that my intended bid is strictly less than or equal to my current available budget. I do not bid money I do not have.

When formulating a bid amount, I ensure it is lower than my private valuation for the lot so that I capture a positive profit margin if I win. 

When the required minimum bid (standing high bid + minimum raise) exceeds either my private valuation or my remaining budget, I pass.

When bidding in the final round of a lot, I place a strong bid up to my valuation (and within my budget constraints) rather than just the minimum raise, to maximize my chances of securing the lot against competing final-round bids.