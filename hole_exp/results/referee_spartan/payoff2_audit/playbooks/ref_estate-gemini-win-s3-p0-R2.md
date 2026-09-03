---
game: ref_estate
model: gemini
condition: win
seed: 3
round: 2
chars: 910
---
When my turn begins, I calculate my gross balance by taking my last declared balance, adding any rent received from other investors since my last turn, and adding my salary if the prompt states I passed or landed on START.

When I land on an opponent's property, I subtract the rent due from my gross balance. I output `[pay: N to P<k>]` where N is the rent amount and k is the opponent's number. 

When I land on my own property, an unowned property, or START, I output `[pay: none]`.

When I land on an unowned property, I check if my gross balance is greater than or equal to the purchase price. If it is, I purchase it by outputting `[buy: yes]` and subtracting the purchase price from my balance. If I cannot afford it, or if the property is already owned, or if I landed on START, I output `[buy: no]`.

At the end of my turn, I declare my final calculated cash for the turn by outputting `[balance: N]`.