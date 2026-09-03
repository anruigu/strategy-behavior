---
game: ref_auction
model: gemini
condition: win
seed: 6
round: 2
chars: 1517
---
I must strictly read and adhere to my true starting budget given in the very first prompt. I will not invent a starting budget (such as 100). 

Because my starting budget is not repeated in later rounds, I must look at my own most recent reply's `[budget: N]` token to know what I have left. I will carry this exact number forward, subtracting only the final clearing prices of new lots listed as "won" by me in the "Results so far" section. I will never bid an amount that exceeds my actual remaining budget.

When I calculate my remaining budget, I subtract the final clearing price of only the lots I have actually won. Subtracting amounts for bids I have placed but not yet won completely breaks my budget tracking. 

When it is the first round of bidding for a lot, I bid the minimum raise or a low amount to stay in the running without driving up the price unnecessarily.

When it is the final round of bidding for a lot, and the lot is currently priced below my valuation, I bid my maximum acceptable price (my valuation minus a desired profit margin, capped by my true remaining budget). Making small incremental bids in the final round does not work, as it allows other bidders to win cheaply when I was willing to pay more.

When the standing high bid plus the minimum raise is equal to or greater than my private valuation for a lot, I immediately pass to avoid negative scores. 

When I output my budget token, I ensure it accurately reflects my remaining budget as carried forward from my previous turns.