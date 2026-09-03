---
game: ref_auction
model: gemini
condition: win
seed: 2
round: 1
chars: 1018
---
I check the prompt carefully for my exact starting budget rather than assuming a standard amount like 100. 

I calculate my remaining budget before every bid by subtracting the total amounts of any lots I have already won (as shown in the "Results so far") from my actual starting budget. I do not subtract bids for lots that are still ongoing or lots I did not win.

I output my remaining budget accurately in the `[budget: N]` token based on this calculation.

When it is round 1 of a lot, I bid the minimum raise to enter the auction while keeping the price as low as possible, provided the standing bid is below my valuation.

When it is round 2 of a lot, I recognize this is my final chance to win the item. I do not just make a minimum raise. I bid my maximum comfortable price—which is the item's value to me minus a small profit margin, strictly capped by my actual remaining budget.

I pass if the standing high bid plus the minimum raise exceeds my valuation of the lot, or if it exceeds my remaining budget.