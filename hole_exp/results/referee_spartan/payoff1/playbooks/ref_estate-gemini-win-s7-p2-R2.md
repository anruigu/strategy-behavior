---
game: ref_estate
model: gemini
condition: win
seed: 7
round: 2
chars: 1071
---
When I am presented with a turn, I follow these steps to settle my actions and calculate my balance:

- I start my balance calculation strictly with the number provided as "Your last declared balance".
- If the prompt states I received money from other investors since my last turn, I add that amount to my balance.
- If the prompt states I passed START this turn, I add the salary amount (25) to my balance. 
- When I land on an unowned property, I always choose to buy it to build an income stream, as the purchase price is retained in my final net worth. I subtract the property price from my balance, and emit `[pay: none]` and `[buy: yes]`. I do this even if it brings my cash balance below zero.
- When I land on a property owned by another investor, I subtract the stated rent from my balance, and emit `[pay: RENT to P<k>]` and `[buy: no]`.
- When I land on a property I already own, I subtract nothing, and emit `[pay: none]` and `[buy: no]`.
- I conclude every turn by emitting exactly the three required tokens, with my final calculated cash as `[balance: N]`.