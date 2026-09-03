---
game: ref_auction
model: gemini
condition: win
seed: 7
round: 1
chars: 643
---
I must read the exact starting budget provided in the prompt's instructions for the first round, rather than assuming a standard budget of 100.
I track my remaining budget by subtracting the final winning price of any lots I win from my true starting budget. 
I only consider lots where my valuation is higher than the required bid.
I never place a bid that exceeds my actual remaining budget.
When calculating my `[budget: N]` token, I output my true remaining budget, regardless of whether I am currently winning a lot or just bidding.
If the required bid to win a lot exceeds my remaining budget, or exceeds my valuation of the lot, I pass.