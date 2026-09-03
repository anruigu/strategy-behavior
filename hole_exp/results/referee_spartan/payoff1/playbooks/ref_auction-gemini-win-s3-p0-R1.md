---
game: ref_auction
model: gemini
condition: win
seed: 3
round: 1
chars: 967
---
I must always read the first prompt carefully to find my exact starting budget, rather than assuming a standard budget of 100, which caused me to bid money I did not have.

When I start the game, I record my exact starting budget as stated in the instructions.

When the results state that I won a lot, I subtract the exact amount I paid from my actual remaining budget. 

When I output the `[budget: N]` token, I ensure `N` is my true remaining budget based on the initial value minus the sums paid for won lots, not a presumed amount.

When deciding to bid, I check that the required bid (standing high bid plus minimum raise) is strictly less than or equal to my actual remaining budget. If it is greater, I must pass.

When evaluating a lot, I bid only if the required bid is less than or equal to the lot's worth to me. 

When it is the final round of a lot, if the lot is profitable and within my real budget, I bid the minimum amount required to take the lead.