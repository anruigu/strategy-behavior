---
game: ref_auction
model: gemini
condition: win
seed: 3
round: 1
chars: 1292
---
When starting a new game, I read the rules carefully to identify my exact starting budget. I will not assume a standard starting budget (like 100) when the prompt explicitly gives me a different number (like 30).

When tracking my budget, I subtract the amount paid for lots I have already won from my actual starting budget. I do not subtract active bids that have not yet resulted in a win, but I must ensure my current bid does not exceed my true remaining budget.

When formulating a bid token and a budget token, I ensure the budget token strictly reflects my actual starting budget minus the cost of all completed lots I have won. 

When deciding how much to bid on early lots, I check my total budget and the number of remaining lots. I do not spend the majority of my budget on the first lot, as it prevents me from competing for potentially more valuable lots later. 

When it is the first round of bidding for a lot, I make the minimum required raise to stay in the auction while conserving my limited budget.

When it is the second (final) round of bidding for a lot, I determine my maximum willing bid by taking the lower of my remaining budget and my true valuation of the lot. I place a bid that secures the lot if possible, but I never bid more than my remaining budget allows.