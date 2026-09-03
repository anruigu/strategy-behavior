---
game: ref_auction
model: gemini
condition: win
seed: 3
round: 2
chars: 1191
---
I must read the very first message of the episode (LOT 1, round 1) carefully to identify my true starting budget (e.g., "You start with a budget of 30"). I will never assume my starting budget is 100.

I will track my remaining budget by taking that exact starting budget and subtracting the amounts I paid for any lots that I actually won (listed in the "Results so far" as "bidder [my number] won at X").

I will output my accurately calculated remaining budget in the `[budget: N]` token on every single turn. 

I will only place a bid if the required amount (standing high bid plus minimum raise) is strictly less than or equal to my valuation of the lot, AND less than or equal to my remaining budget. 

If the standing high bid plus minimum raise exceeds my valuation of a lot, or exceeds my remaining budget, I will pass.

When placing a bid in the first round of a lot, I will bid just enough to become the highest bidder, preserving my budget for future rounds or lots.

When placing a bid in the final round of a lot I value highly, I will bid aggressively up to my valuation or my remaining budget (whichever is lower) to secure the win, rather than just making the minimum raise.