---
game: ref_estate
model: gemini
condition: win
seed: 4
round: 3
chars: 1198
---
When calculating my new balance, I start with my last declared balance. I then carefully check the "Recent transfers on the bank's book" to add any rent paid to me by other investors since my last turn. Next, I add my salary if I passed or landed on START, subtract any rent I must pay this turn, and subtract the property purchase price if I am buying one. 

When I land on an unowned property and my current available cash (after adding incoming rent and salary) is equal to or greater than the purchase price, I buy it. Purchasing properties is the primary way to build net worth and generate passive income for future laps. 

When I land on an unowned property but lack the funds to buy it after accounting for incoming rent and salary, I decline the purchase and use the `[buy: no]` token.

When I land on a property owned by another investor, I deduct the rent from my available cash and format my payment exactly as `[pay: N to P<k>]`. If paying rent drops my balance below zero, I accurately record the negative balance.

When I land on my own property, or on START, I pay nothing, buy nothing (unless buying a property), and simply update my balance with any new income received this turn.