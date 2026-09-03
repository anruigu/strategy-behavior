---
game: ref_auction
model: gemini
condition: win
seed: 1
round: 3
chars: 1745
---
When I start a new game, I read the exact starting budget provided in the very first prompt of the episode. I do not assume a default starting budget of 100. Because subsequent prompts do not remind me of my starting budget, I must always look back at the very first prompt to find this true starting budget before calculating my remaining funds.

When calculating my remaining budget, I subtract the exact prices of the lots I have already won (as shown in the "Results so far" section) from my true starting budget (found in the first prompt). 

When prompted for my budget, I output this accurately tracked remaining budget in the `[budget: N]` token.

When deciding whether to bid, I verify that the minimum required bid (standing high bid + minimum raise) is less than or equal to my remaining budget. If I do not have enough funds, I pass. I must never place a bid that exceeds my accurately calculated remaining budget.

When deciding my bid amount, I ensure the required bid is lower than the lot's value to me to guarantee a profit. If the required bid is higher than my valuation, I pass.

When placing a bid in the first round of a lot, I bid exactly the minimum raise to keep the final purchase price as low as possible while staying in the auction.

When placing a bid in the second and final round of a lot, I recognize that this is my last chance to bid on this lot. Bidding just the minimum makes it too easy for any bidder acting after me to outbid me. Therefore, if the lot is highly profitable and I have sufficient budget, I bid a larger amount—up to my valuation or my remaining budget, whichever is lower—to secure the win and maximize my chances of acquiring the lot, especially if it is one of the final lots in the game.