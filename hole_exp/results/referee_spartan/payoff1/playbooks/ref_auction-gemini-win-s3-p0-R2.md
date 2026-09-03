---
game: ref_auction
model: gemini
condition: win
seed: 3
round: 2
chars: 864
---
I must always look back at the very first message in the conversation history to find my exact starting budget. I will never assume a standard budget of 100.

I calculate my current budget by taking my exact starting budget (found in the first prompt) and subtracting the amounts of any lots the "Results so far" state I have won. 

When I output the `[budget: N]` token, I ensure `N` is my true remaining budget calculated this way.

When deciding to bid, I check that the required bid (standing high bid plus minimum raise) is strictly less than or equal to my actual remaining budget. If it is greater, I must pass.

When evaluating a lot, I bid only if the required bid is less than or equal to the lot's worth to me. 

When it is the final round of a lot, if the lot is profitable and within my real budget, I bid the minimum amount required to take the lead.