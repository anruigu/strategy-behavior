---
game: ref_estate
model: gemini
condition: win
seed: 4
round: 3
chars: 1211
---
When I land on an unowned property and have enough cash, I buy it. 
When I buy a property, I declare `[buy: yes]` and subtract the purchase price from my cash balance.
When I land on a property owned by another investor, I pay the rent due by declaring `[pay: N to Pk]` (using the investor's number without angle brackets) and subtract that amount from my cash balance.
When the rent due exceeds my available cash, I pay my entire remaining cash balance, leaving me with zero.
When I pass or land on START, I add the salary amount to my cash balance before calculating any other transactions for the turn.
When I receive cash from other investors between turns, I add it to my starting balance before making any deductions.
I calculate my final balance for the turn precisely by taking my previous balance, adding any salary or cash received from other investors, and subtracting any purchases or rent payments, then declaring it as `[balance: N]`.
I do not hoard cash. Holding large cash balances does not work because it leaves my wealth exposed to rent payments; converting cash into properties secures that value for my final score and reduces the amount of rent I can be forced to pay if I run low on cash.