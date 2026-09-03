---
game: ref_auction
model: gemini
condition: win
seed: 6
round: 3
chars: 1603
---
Because my starting budget is only stated in the very first prompt of the episode (Lot 1, Round 1), I must always look back at the very beginning of the conversation history to find my true starting budget. I must never blindly assume a starting budget of 100 or rely on assumptions when the number is missing from the current turn's prompt.

When outputting my budget token, I must output my actual remaining budget. I calculate this by taking my true starting budget (found in the first message) and subtracting only the final winning prices of lots I have officially won (found in the "Results so far" section). 

I do not subtract money for bids placed on lots I lost. I also do not subtract money for my current bids before a lot is officially resolved; if I have not won any lots yet, my remaining budget is exactly my starting budget.

I must strictly cap my bids at my actual remaining budget. If I only have 30 left in my budget, I cannot place a bid higher than 30, no matter what my valuation of the lot is.

When I am in round 1 of a lot I want, and I have sufficient budget, I bid the minimum required raise. This gets me on the board without inflating the price prematurely.

When I am in round 2 of a lot, I treat it as a sealed-bid final round. I bid aggressively up to my maximum valuation of the lot or my total remaining budget (whichever is lower). I do not make small minimum increments in round 2, because no further rounds exist to counter outbidding.

When the standing high bid plus the minimum raise exceeds the lot's value to me, or exceeds my actual remaining budget, I pass.