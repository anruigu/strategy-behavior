---
game: ref_auction
model: gemini
condition: win
seed: 4
round: 3
chars: 1230
---
I must read the specific starting budget provided in the very first prompt (LOT 1, round 1). I must never assume a default starting budget of 100.

To track my budget correctly across rounds, I must always look back at the `[budget: N]` token from my own most recent reply. If the "Results so far" section shows that I won a lot since my last reply, I subtract the exact winning price of that lot from my previous budget to calculate my current budget. Otherwise, my budget remains exactly the same as the number I output in my previous reply.

When considering a raise, I cap my absolute maximum bid at the lower of two numbers: my private valuation of the lot, or my currently available budget. 

When the required minimum bid (standing high bid plus minimum raise) exceeds either my remaining budget or my private valuation, I strictly output `[bid: pass]`. 

When outputting my budget token alongside a bid or pass, I write the budget I currently have left based on past resolved wins, not subtracting the bid I am currently proposing. 

When I decide to compete for a lot, I place a bid equal to the standing high bid plus the minimum raise, ensuring this amount leaves me with a positive profit margin (valuation minus bid).