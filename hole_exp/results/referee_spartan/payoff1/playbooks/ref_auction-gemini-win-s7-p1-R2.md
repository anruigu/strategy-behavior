---
game: ref_auction
model: gemini
condition: win
seed: 7
round: 2
chars: 771
---
I must read the exact starting budget provided in the prompt's instructions for the first round.
I will explicitly state my true starting budget in my reasoning during every single round, so I do not forget it and wrongly assume a default budget of 100 later in the game.
I track my remaining budget by subtracting the final winning price of any lots I win from my true starting budget. 
I only consider lots where my valuation is higher than the required bid.
I never place a bid that exceeds my actual remaining budget.
When calculating my `[budget: N]` token, I output my true remaining budget, regardless of whether I am currently winning a lot or just bidding.
If the required bid to win a lot exceeds my remaining budget, or exceeds my valuation of the lot, I pass.