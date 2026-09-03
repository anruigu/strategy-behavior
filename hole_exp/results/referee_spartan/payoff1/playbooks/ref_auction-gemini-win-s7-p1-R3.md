---
game: ref_auction
model: gemini
condition: win
seed: 7
round: 3
chars: 719
---
I must look back at the very first prompt in the conversation history to find my exact starting budget. I will never assume a default budget of 100.
I will track my remaining budget by taking my true starting budget (from the first prompt) and subtracting the final winning price of any lots I have won (as listed in "Results so far").
I only consider lots where my valuation is higher than the required bid.
I never place a bid that exceeds my actual remaining budget.
When calculating my `[budget: N]` token, I output my true remaining budget, regardless of whether I am currently winning a lot or just bidding.
If the required bid to win a lot exceeds my remaining budget, or exceeds my valuation of the lot, I pass.