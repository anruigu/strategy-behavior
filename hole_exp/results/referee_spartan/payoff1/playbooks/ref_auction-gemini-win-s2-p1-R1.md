---
game: ref_auction
model: gemini
condition: win
seed: 2
round: 1
chars: 1277
---
I must read my starting budget carefully from the very first prompt. I will not assume my starting budget is 100, as it can be a different number (e.g., 30).

To determine my current budget, I subtract the final winning prices of any lots I have already won (which are listed in the "Results so far") from my true starting budget. I do not subtract bids for lots I did not win, and I do not subtract my current bid from the budget token unless explicitly required to do so by the prompt format. 

When formatting my response, I ensure the `[budget: N]` token accurately reflects this remaining available budget. 

When deciding how much to bid in the first round of a lot, I place a minimal bid or one slightly above the minimum to take the lead without driving the price up unnecessarily.

When bidding in the second and final round of a lot, I check the standing high bid. If the standing bid plus the minimum raise is less than or equal to my valuation of the lot, I bid exactly the standing bid plus the minimum raise to maximize my profit margin.

I will never bid more than my specific valuation for a lot, as doing so would result in a negative score for that item. I will pass if the standing high bid plus the minimum raise exceeds my valuation or my available budget.