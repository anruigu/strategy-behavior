---
game: ref_estate
model: gemini
condition: win
seed: 2
round: 3
chars: 1061
---
When it is my turn, I calculate my available cash before taking any actions: I take my last declared balance, add any rent received from other investors since my last turn, and add my salary if the prompt indicates I passed or landed on START.

When I land on an unowned property, I always buy it if my available cash is equal to or greater than the purchase price. Because the final score includes the full purchase price of held deeds, buying a property costs nothing in terms of net worth while giving me the chance to earn rent. I output `[buy: yes]` and subtract the purchase price from my cash. 

When I lack the funds to buy an unowned property, or when I land on an owned property or START, I output `[buy: no]`.

When I land on a property owned by another investor, I output `[pay: N to P<k>]` (where N is the rent and k is the investor number) and subtract that amount from my cash. 

When I land on an unowned property, my own property, or START, I output `[pay: none]`.

When my turn is complete, I output my final calculated cash as `[balance: N]`.