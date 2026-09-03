---
game: ref_estate
model: gemini
condition: win
seed: 9
round: 1
chars: 1025
---
When calculating my new balance, I start with my last declared balance, add any rent received from other investors since my last turn, add my salary if the prompt states I passed or landed on START, subtract any rent I must pay this turn, and subtract the property price if I am buying it.

When I land on an unowned property, I buy it if my updated cash balance is greater than or equal to the purchase price. Buying properties increases my total asset value for the final score and generates passive rent. 

When I land on a property owned by another investor, I pay the required rent and record it using the format `[pay: N to P<k>]`.

When I do not owe rent to anyone, I output `[pay: none]`.

When a property is already owned, or if my available cash is strictly less than the purchase price of an unowned property, I output `[buy: no]`.

I always conclude my turn by outputting exactly three bracketed tokens in this exact order: `[pay: N to P<k>]` (or `[pay: none]`), `[buy: yes]` (or `[buy: no]`), and `[balance: N]`.