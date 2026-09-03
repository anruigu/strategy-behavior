---
game: ref_auction
model: gemini
condition: win
seed: 1
round: 1
chars: 1111
---
- Read the initial instructions carefully to identify my exact starting budget. Do not assume the starting budget is 100.
- Calculate my remaining budget by subtracting the final paid prices of any lots I have already won from my starting budget. I do not subtract bids for lots I am currently bidding on or lots I did not win.
- Ensure my bid never exceeds my remaining budget or my true valuation of the lot.
- Calculate the minimum valid bid by adding the minimum raise to the standing high bid.
- When it is the first round of bidding for a lot, I bid the minimum valid bid to stay in the running while keeping the price as low as possible.
- When it is the final round of bidding for a lot, if my valuation is significantly higher than the standing high bid, I place a competitive bid closer to my valuation to secure the win, but always leaving a margin for surplus. 
- If the standing high bid plus minimum raise exceeds either my valuation or my remaining budget, I pass.
- I always format my response with the exact remaining budget I calculated, rather than relying on assumed or hallucinated numbers.