---
game: ref_auction
model: gemini
condition: win
seed: 0
round: 2
chars: 1316
---
I find my current remaining budget by looking at the `[budget: N]` token from my own immediately preceding reply. If this is the very first turn of the game, I look at the initial prompt for my starting budget. I never assume a default budget (such as 100).

When calculating my remaining budget to output in the `[budget: N]` token, I subtract the final purchase prices of any lots I have definitively won in the most recent round from my previous remaining budget. I do not subtract active bids for lots that have not yet concluded.

My bid must never exceed my actual remaining budget. If my desired bid is higher than my remaining budget, I bid my remaining budget instead, unless my remaining budget is less than the minimum required bid, in which case I pass.

When I am in the first round of bidding for a lot, I bid the minimum required raise to stay in the auction while keeping the price as low as possible, provided I can afford it.

When I am in the final round of bidding for a lot, I bid the highest amount I am willing to pay to secure the win, ensuring this bid does not exceed my true value for the lot or my actual remaining budget. 

When the minimum required bid (standing high bid plus the minimum raise) exceeds the lot's value to me, or exceeds my remaining budget, I reply with `[bid: pass]`.