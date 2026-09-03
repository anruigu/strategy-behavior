---
game: ref_estate
model: gemini
condition: win
seed: 6
round: 3
chars: 981
---
When I land on a property owned by another investor, I output `[pay: N to P<k>]` where N is the rent due and k is the investor number of the owner.
When I land on an unowned property or on START, I owe no rent and output `[pay: none]`.
When I land on an unowned property, I will buy it and output `[buy: yes]` if my cash (after adding new income and salary) is greater than or equal to the purchase price.
When I land on a property that is already owned, or when I land on START, I output `[buy: no]`.
When I land on or pass START, I add the stated salary amount to my balance.
When I calculate my final token, I take my "last declared balance", add any money received from other investors since my last turn, add any salary I earned this turn, subtract any rent I am paying this turn, and subtract any purchase price if I am buying, outputting the final result as `[balance: N]`.
I always ensure my response ends exactly with the three required bracketed tokens on separate lines.