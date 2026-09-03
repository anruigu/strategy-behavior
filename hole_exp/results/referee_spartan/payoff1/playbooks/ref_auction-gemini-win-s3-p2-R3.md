---
game: ref_auction
model: gemini
condition: win
seed: 3
round: 3
chars: 1688
---
When starting a new game, I read the very first prompt carefully to identify my exact starting budget (e.g., "You start with a budget of X"). I must never assume a default starting budget like 100.

In every single turn, I will explicitly state my starting budget in my reasoning to ensure I do not forget it. 

When calculating my remaining budget, I subtract the exact amount paid for lots I have already won (as shown in the "Results so far" section) from my true starting budget. I do not subtract active bids that have not yet resulted in a win.

When formulating a bid, I must ensure my bid never exceeds my true remaining budget. If my valuation for a lot is higher than my remaining budget, I am strictly capped at bidding my remaining budget. Bidding more than my remaining budget will invalidate my bids and ruin my score.

When formulating the `[budget: N]` token, I ensure it strictly reflects this mathematically correct remaining budget based on my true starting budget minus the cost of all completed lots I have won. 

When deciding how much to bid on early lots, I check my total budget and the number of remaining lots. I do not spend the majority of my budget on the first lot, as it prevents me from competing for potentially more valuable lots later. 

When it is the first round of bidding for a lot, I make the minimum required raise to stay in the auction while conserving my limited budget.

When it is the second (final) round of bidding for a lot, I determine my maximum willing bid by taking the lower of my remaining budget and my true valuation of the lot. I place a bid that secures the lot if possible, but I never bid more than my remaining budget allows.