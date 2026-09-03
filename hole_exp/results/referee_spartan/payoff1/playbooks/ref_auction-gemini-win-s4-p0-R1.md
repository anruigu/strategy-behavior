---
game: ref_auction
model: gemini
condition: win
seed: 4
round: 1
chars: 896
---
I verify my starting budget in the initial prompt and use that exact number to track my finances; I never assume a default starting budget like 100.

I calculate my remaining budget before every move by subtracting the closing prices of only the lots I have explicitly won (as listed in "Results so far") from my true starting budget. 

When I am in the first round of bidding for a lot that is profitable to me, I bid the minimum required amount to participate while keeping my potential cost as low as possible.

When I am in the second and final round of bidding for a lot, I do not just bid the minimum valid raise. Because I will not get another chance to counter, I bid a strong, competitive amount up to my actual valuation or my remaining budget limit to ensure I secure the lot.

When the minimum required bid for a lot exceeds my private valuation or my actual remaining budget, I pass.