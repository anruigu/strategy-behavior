---
game: ref_auction
model: gemini
condition: win
seed: 2
round: 3
chars: 1530
---
I must read my starting budget carefully from the very first prompt. The first message always contains a line like "You start with a budget of X." I will extract this exact number (e.g., 30) and strictly use it as my starting budget for the entire game. I will absolutely never assume my starting budget is 100. 

To determine my current budget, I subtract the final winning prices of any lots I have already won (which are listed in the "Results so far") from my true starting budget. I do not subtract bids for lots I did not win, and I do not subtract my current bid from the budget token. 

When formatting my response, I ensure the `[budget: N]` token accurately reflects this remaining available budget. 

When deciding how much to bid in the first round of a lot, I place a minimal bid or one slightly above the minimum to take the lead without driving the price up unnecessarily.

When bidding in the second and final round of a lot (round 2/2), since it is a first-price auction where the highest bid wins and pays what it bid, bidding merely the minimum raise often results in losing to another bidder. I should bid a competitive amount that is higher than the minimum raise but still leaves a healthy profit margin below my valuation. 

I will never bid more than my specific valuation for a lot, as doing so would result in a negative score for that item. I will never bid more than my remaining available budget. I will pass if the standing high bid plus the minimum raise exceeds my valuation or my available budget.