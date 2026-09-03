---
game: ref_estate
model: gemini
condition: win
seed: 4
round: 1
chars: 943
---
When calculating my new balance, I start with my last declared balance, add any rent received from other investors since my last turn, add my salary if I passed START, subtract any rent I must pay this turn, and subtract the property purchase price if I am buying one. 

When I land on an unowned property and my current available cash is equal to or greater than the purchase price, I buy it. Purchasing properties is the primary way to build net worth and generate passive income for future laps. 

When I land on an unowned property but lack the funds to buy it after accounting for incoming rent and salary, I decline the purchase and use the `[buy: no]` token.

When I land on a property owned by another investor, I deduct the rent from my available cash and format my payment exactly as `[pay: N to P<k>]`.

When I land on my own property, I pay nothing, buy nothing, and simply update my balance with any new income received this turn.