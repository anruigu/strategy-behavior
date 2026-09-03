---
game: ref_auction
model: gemini
condition: win
seed: 2
round: 3
chars: 1362
---
I check the very first message in the conversation history carefully for my exact starting budget, as it is only stated there. I will never assume a standard default like 100 without checking the first prompt.

Because the starting budget is only shown in the first prompt, I will explicitly state my original starting budget in my text reasoning on *every single turn* by looking back at the beginning of the conversation. 

I calculate my remaining budget before every bid by subtracting the total amounts of any lots I have already won (as shown in the "Results so far" for my bidder number) from my actual starting budget. I do not subtract bids for lots that are still ongoing or lots I did not win.

I output my remaining budget accurately in the `[budget: N]` token based on this exact calculation.

When it is round 1 of a lot, I bid the minimum raise to enter the auction while keeping the price as low as possible, provided the standing bid is below my valuation.

When it is round 2 of a lot, I recognize this is my final chance to win the item. I do not just make a minimum raise. I bid my maximum comfortable price—which is the item's value to me minus a small profit margin, strictly capped by my actual remaining budget.

I pass if the standing high bid plus the minimum raise exceeds my valuation of the lot, or if it exceeds my remaining budget.