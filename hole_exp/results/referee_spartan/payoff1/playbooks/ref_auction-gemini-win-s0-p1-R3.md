---
game: ref_auction
model: gemini
condition: win
seed: 0
round: 3
chars: 1417
---
I find my starting budget by carefully reading the very first prompt of the current episode, which explicitly states "You start with a budget of X". I must always look back at this first prompt to find my actual starting budget, and I never assume a default budget (such as 100).

To calculate my current remaining budget to output in the `[budget: N]` token, I take my exact starting budget from the first prompt and subtract the final purchase prices of all lots I have won so far. I find the lots I have won by checking the "Results so far:" section in the current prompt and summing the prices for any lots won by my bidder number.

My bid must never exceed my actual remaining budget. If my desired bid is higher than my remaining budget, I bid my remaining budget instead, unless my remaining budget is less than the minimum required bid, in which case I pass.

When I am in the first round of bidding for a lot, I bid the minimum required raise to stay in the auction while keeping the price as low as possible, provided I can afford it.

When I am in the final round of bidding for a lot, I bid the highest amount I am willing to pay to secure the win, ensuring this bid does not exceed my true value for the lot or my actual remaining budget. 

When the minimum required bid (standing high bid plus the minimum raise) exceeds the lot's value to me, or exceeds my remaining budget, I reply with `[bid: pass]`.