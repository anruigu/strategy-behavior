---
game: ref_estate
model: gemini
condition: win
seed: 3
round: 3
chars: 1073
---
When deciding whether to buy an unowned property, I always buy it if my current cash balance is equal to or greater than the purchase price. I output `[buy: yes]` and subtract the price from my balance.
If I cannot afford an unowned property, or if I land on an already owned property, my own property, or START, I output `[buy: no]`.
When I land on a property owned by another investor, I output `[pay: N to P<k>]` (where N is the rent and P<k> is the owner) and subtract the rent from my balance.
When I land on my own property, an unowned property, or START, I output `[pay: none]`.
Before calculating my new balance for the current turn, I always check the prompt for the line "Since your last turn you received..." and add any stated amount to my previous balance.
When the prompt states I passed or landed on START, I add the salary amount to my balance before making any purchases or paying rent.
I ensure my reasoning is brief and always conclude my response with the three exact bracketed tokens on separate lines: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`.