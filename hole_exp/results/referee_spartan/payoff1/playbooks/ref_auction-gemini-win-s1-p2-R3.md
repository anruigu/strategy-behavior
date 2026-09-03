---
game: ref_auction
model: gemini
condition: win
seed: 1
round: 3
chars: 1460
---
- I will find my exact starting budget by looking back at the text of the very first prompt in the transcript (LOT 1, round 1). The starting budget is ONLY stated there. I will never assume a "standard" starting budget of 100.
- I will explicitly state my true starting budget in my reasoning for every single turn.
- I will calculate my remaining budget by subtracting the final paid prices of any lots I have already won (as listed in "Results so far") from my true starting budget. I will not subtract bids for lots I am currently bidding on or lots I did not win.
- I will ensure my bid never exceeds my remaining budget or my true valuation of the lot. If the minimum valid bid exceeds my budget or valuation, I will pass.
- I will calculate the minimum valid bid by adding the minimum raise to the standing high bid.
- When it is the first round of bidding for a lot, I will bid the minimum valid bid to stay in the running while keeping the price as low as possible.
- When it is the final round of bidding for a lot, if my valuation is significantly higher than the standing high bid and I have the budget, I will place a competitive bid closer to my valuation to secure the win, but always leaving a margin for surplus. 
- I will always format my response with the exact remaining budget I calculated, rather than relying on assumed or hallucinated numbers, and use the exact required bracketed tokens: [bid: N] or [bid: pass] followed by [budget: N].