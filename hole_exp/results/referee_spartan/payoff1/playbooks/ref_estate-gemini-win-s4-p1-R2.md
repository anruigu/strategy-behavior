---
game: ref_estate
model: gemini
condition: win
seed: 4
round: 2
chars: 1310
---
When I calculate my new balance for the turn, I start with my last declared balance, add my salary if the prompt states I passed or landed on START, and add any rent the prompt explicitly says I received from other investors since my last turn in the text above the recent transfers. I must not count transfers from the bank's book as new income, as they may have already been accounted for in previous turns.

When I land on an unowned property and my available cash is greater than or equal to its price, I buy it to increase my end-game score and generate rent. I output `[buy: yes]` and subtract the purchase price from my cash balance.

When I land on a property owned by another investor, I output `[pay: N to P<k>]` where N is the rent due and k is the owner's number, and I subtract N from my cash balance.

When I land on my own property, an unowned property, or START, I output `[pay: none]`.

When I land on an already owned property, or an unowned property that I cannot afford, or START, I output `[buy: no]`.

When I have accounted for all income, rent payments, and property purchases for the turn, I output my final calculated cash as `[balance: N]`.

I always end my response with exactly the three required bracketed tokens on separate lines: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`.