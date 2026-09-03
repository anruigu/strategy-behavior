---
game: ref_auction
model: gemini
condition: win
seed: 3
round: 3
chars: 1456
---
I will read the very first message of the episode (LOT 1, round 1) carefully to extract my exact starting budget. 

In every single turn's reasoning, I will explicitly state that true starting budget before doing any math. I will never assume my starting budget is 100 or any other default number.

I will accurately track my remaining budget by taking that exact starting budget and subtracting the amounts I paid for any lots that I actually won (which are explicitly listed in the "Results so far" section as "bidder [my number] won at X").

I will output my accurately calculated remaining budget in the `[budget: N]` token on every single turn. 

If my remaining budget is 0, or if it is lower than the standing high bid plus the minimum raise, I must output `[bid: pass]`.

I will only place a bid if the required amount (standing high bid plus minimum raise) is strictly less than or equal to my valuation of the lot, AND less than or equal to my remaining budget. 

If the standing high bid plus minimum raise exceeds my valuation of a lot, or exceeds my remaining budget, I will pass.

When placing a bid in the first round of a lot, I will bid just enough to become the highest bidder, preserving my budget for future rounds or lots.

When placing a bid in the final round of a lot I value highly, I will bid aggressively up to my valuation or my remaining budget (whichever is lower) to secure the win, rather than just making the minimum raise.