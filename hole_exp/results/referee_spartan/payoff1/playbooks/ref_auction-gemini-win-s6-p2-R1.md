---
game: ref_auction
model: gemini
condition: win
seed: 6
round: 1
chars: 874
---
I read my starting budget carefully from the very first prompt and I never assume a default starting budget like 100. 

I calculate my remaining budget by taking my true starting budget and subtracting the exact winning prices of any lots I have won, which are shown in the "Results so far" section. I do not subtract bids I have placed that did not result in a win.

I never place a bid that exceeds my actual remaining budget, regardless of how much I value the lot. 

When deciding whether to bid, I ensure that the standing high bid plus the minimum raise is less than my valuation for the lot and less than or equal to my remaining budget. 

If the required bid to win exceeds either my valuation or my remaining budget, I pass. 

When I reply, I accurately report my remaining budget calculated from my true starting amount minus my actual wins, not an assumed number.