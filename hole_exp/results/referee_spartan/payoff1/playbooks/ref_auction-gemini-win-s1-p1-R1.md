---
game: ref_auction
model: gemini
condition: win
seed: 1
round: 1
chars: 1294
---
When I start a new game, I read the exact starting budget provided in the very first prompt. I do not assume a default starting budget of 100. 

When calculating my remaining budget, I subtract the exact prices of the lots I have already won (as shown in the "Results so far" section) from my true starting budget. 

When prompted for my budget, I output this accurately tracked remaining budget in the `[budget: N]` token.

When deciding whether to bid, I verify that the minimum required bid (standing high bid + minimum raise) is less than or equal to my remaining budget. If I do not have enough funds, I pass.

When deciding my bid amount, I ensure the required bid is lower than the lot's value to me to guarantee a profit. If the required bid is higher than my valuation, I pass.

When placing a bid in the first round of a lot, I bid exactly the minimum raise to keep the final purchase price as low as possible.

When placing a bid in the second and final round of a lot, I bid exactly the minimum required to take the lead, provided it is profitable and within my budget.

What did not work: Hallucinating a starting budget of 100 instead of reading the provided budget of 30. This caused me to place bids that vastly exceeded my actual funds and completely ruined my budget tracking.