---
game: ref_auction
model: gemini
condition: win
seed: 3
round: 3
chars: 1090
---
I must carefully read the very first prompt of the game to find the exact text "You start with a budget of X". This number "X" is my absolute starting budget. I will never assume a default budget of 100; I must extract the specific number provided in that first message and remember it for the entire game.

I calculate my current budget by taking my exact starting budget (found in the first prompt) and subtracting the amounts of any lots the "Results so far" state I have won. 

When I output the `[budget: N]` token, I ensure `N` is my true remaining budget calculated this way.

When deciding to bid, I check that the required bid (standing high bid plus minimum raise) is strictly less than or equal to my actual remaining budget. If it is greater than my remaining budget, I cannot afford it and must pass, regardless of the lot's value.

When evaluating a lot, I bid only if the required bid is less than or equal to the lot's worth to me. 

When it is the final round of a lot, if the lot is profitable and within my real budget, I bid the minimum amount required to take the lead.