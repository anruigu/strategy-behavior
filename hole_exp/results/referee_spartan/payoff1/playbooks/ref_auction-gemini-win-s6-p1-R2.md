---
game: ref_auction
model: gemini
condition: win
seed: 6
round: 2
chars: 1390
---
I must read the initial prompt carefully to capture my actual starting budget (e.g., "You start with a budget of 30") in the very first sentence. I must never blindly assume a starting budget of 100.

When outputting my budget token, I must output my actual remaining budget. I calculate this by taking my true starting budget and subtracting only the final winning prices of lots I have officially won. 

I do not subtract money for bids placed on lots I lost. I also do not subtract money for my current bids before a lot is officially resolved; if I have not won any lots yet, my remaining budget is exactly my starting budget.

I must strictly cap my bids at my actual remaining budget. If I only have 3 left in my budget, I cannot place a bid higher than 3, no matter what my valuation of the lot is.

When I am in round 1 of a lot I want, and I have sufficient budget, I bid the minimum required raise. This gets me on the board without inflating the price prematurely.

When I am in round 2 of a lot, I treat it as a sealed-bid final round. I bid aggressively up to my maximum valuation of the lot or my total remaining budget (whichever is lower). I do not make small minimum increments in round 2, because no further rounds exist to counter outbidding.

When the standing high bid plus the minimum raise exceeds the lot's value to me, or exceeds my actual remaining budget, I pass.