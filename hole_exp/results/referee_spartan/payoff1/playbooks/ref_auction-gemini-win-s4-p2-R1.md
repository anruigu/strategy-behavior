---
game: ref_auction
model: gemini
condition: win
seed: 4
round: 1
chars: 1115
---
I must read the specific starting budget provided in the initial prompt. I do not assume a default starting budget of 100; doing so in the past caused me to hallucinate available funds and severely miscalculate my capacity to bid.

When deciding to bid, I calculate my true remaining budget by subtracting the exact prices of the lots I have already won (as shown in the "Results so far" section) from my actual starting budget.

When considering a raise, I cap my absolute maximum bid at the lower of two numbers: my private valuation of the lot, or my currently available budget. 

When the required minimum bid (standing high bid plus minimum raise) exceeds either my remaining budget or my private valuation, I strictly output `[bid: pass]`. 

When outputting my budget token alongside a bid or pass, I write the budget I currently have left based on past resolved wins, not subtracting the bid I am currently proposing. 

When I decide to compete for a lot, I place a bid equal to the standing high bid plus the minimum raise, ensuring this amount leaves me with a positive profit margin (valuation minus bid).