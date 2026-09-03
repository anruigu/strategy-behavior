---
game: ref_auction
model: gemini
condition: win
seed: 5
round: 3
chars: 1124
---
- I read the very first prompt carefully to identify my exact starting budget (e.g., 30) instead of assuming a default starting budget of 100.
- Because my starting budget might not be restated in later prompts, I must look at the `[budget: N]` token I output in my immediately preceding turn to find my current available funds. I will strictly avoid reverting to a default budget of 100.
- I calculate my available funds before every action by taking my previous turn's remaining budget and subtracting the final price of any lot I have newly won. 
- I never place a bid that exceeds my available funds. 
- I bid only if the required amount (standing high bid plus the minimum raise) is strictly less than my private value for the lot.
- I pass if the required bid equals or exceeds my private value, as winning would yield zero or negative surplus.
- I pass if the required bid exceeds my remaining available funds.
- When outputting my `[budget: N]` token, I state my true remaining budget accurately based on my actual starting budget, subtracting what I have spent on past wins, never resetting to a default assumption.