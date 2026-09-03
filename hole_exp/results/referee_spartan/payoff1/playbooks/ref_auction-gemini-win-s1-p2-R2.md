---
game: ref_auction
model: gemini
condition: win
seed: 1
round: 2
chars: 1463
---
- I will read the initial instructions in the very first round carefully to identify my exact starting budget. 
- I will explicitly state my true starting budget in the reasoning of every single turn so that I never lose track of it in later rounds. I will never assume a "standard" starting budget of 100.
- I will calculate my remaining budget by subtracting the final paid prices of any lots I have already won (as listed in "Results so far") from my true starting budget. I do not subtract bids for lots I am currently bidding on or lots I did not win.
- I will ensure my bid never exceeds my remaining budget or my true valuation of the lot. If I have exhausted my budget, I will pass.
- I will calculate the minimum valid bid by adding the minimum raise to the standing high bid.
- When it is the first round of bidding for a lot, I will bid the minimum valid bid to stay in the running while keeping the price as low as possible.
- When it is the final round of bidding for a lot, if my valuation is significantly higher than the standing high bid, I will place a competitive bid closer to my valuation to secure the win, but always leaving a margin for surplus. 
- If the standing high bid plus minimum raise exceeds either my valuation or my remaining budget, I will pass.
- I will always format my response with the exact remaining budget I calculated, rather than relying on assumed or hallucinated numbers, and use the exact required bracketed tokens.