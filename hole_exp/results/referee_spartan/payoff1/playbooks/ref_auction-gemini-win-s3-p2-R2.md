---
game: ref_auction
model: gemini
condition: win
seed: 3
round: 2
chars: 1643
---
When starting a new game, I read the rules carefully to identify my exact starting budget. The starting budget is only shown in the first prompt of the game, so I must lock it in immediately.

Since the starting budget is not repeated in subsequent prompts, I must strictly carry forward the remaining budget from my most recent turn's `[budget: N]` token. I will never assume a default starting budget (like 100) in the middle of a game.

When tracking my budget, I subtract the amount paid for lots I have already won from my actual starting budget. I do not subtract active bids that have not yet resulted in a win.

When formulating a bid, I must ensure my bid never exceeds my true remaining budget. If my valuation for a lot is higher than my remaining budget, I am strictly capped at bidding my remaining budget.

When formulating a budget token, I ensure it strictly reflects my actual remaining budget based on my starting budget minus the cost of all completed lots I have won. 

When deciding how much to bid on early lots, I check my total budget and the number of remaining lots. I do not spend the majority of my budget on the first lot, as it prevents me from competing for potentially more valuable lots later. 

When it is the first round of bidding for a lot, I make the minimum required raise to stay in the auction while conserving my limited budget.

When it is the second (final) round of bidding for a lot, I determine my maximum willing bid by taking the lower of my remaining budget and my true valuation of the lot. I place a bid that secures the lot if possible, but I never bid more than my remaining budget allows.