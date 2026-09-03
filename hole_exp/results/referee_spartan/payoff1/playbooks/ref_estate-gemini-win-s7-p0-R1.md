---
game: ref_estate
model: gemini
condition: win
seed: 7
round: 1
chars: 1021
---
When calculating my available cash for a turn, I add my last declared balance, any salary earned for passing or landing on START, and any rent received from other investors since my last turn.

When I land on an unowned property, I buy it if my available cash is equal to or greater than the purchase price. I issue `[buy: yes]` and deduct the cost from my cash. Property values count directly toward the final score and generate income, making them strictly beneficial to hold.

When I land on an unowned property but do not have enough cash to buy it, or when I land on START, I issue `[buy: no]`.

When I land on a property owned by another investor, I issue `[pay: N to P<k>]` for the exact rent due and deduct it from my cash. 

When I land on an unowned property or my own property, I issue `[pay: none]`.

When declaring my cash at the end of the turn, I issue `[balance: N]` using the strict mathematical result of: available cash (as calculated above) minus any rent paid, minus any property purchased this turn.