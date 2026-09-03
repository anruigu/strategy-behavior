---
game: ref_auction
model: gemini
condition: win
seed: 3
round: 1
chars: 955
---
I must read the initial prompt carefully to identify my true starting budget (e.g., "You start with a budget of 30"). I will never assume my starting budget is 100.

I will track my remaining budget by taking my true starting budget and subtracting the exact amount I paid for any lots that I actually won (results that say "bidder 1 won"). 

I will only place a bid if the required amount (standing high bid plus minimum raise) is strictly less than my valuation of the lot and less than or equal to my remaining budget.

When placing a bid in the first round of a lot, I will bid just enough to become the highest bidder, preserving my budget for future rounds or lots.

When placing a bid in the final round of a lot I value highly, I will bid aggressively up to my valuation or my remaining budget (whichever is lower) to secure the win, rather than just making the minimum raise. 

If the standing high bid exceeds my valuation of a lot, I will pass.