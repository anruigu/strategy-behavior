---
game: ref_estate
model: gemini
condition: win
seed: 6
round: 1
chars: 715
---
When I land on a property owned by another investor, I output `[pay: N to P<k>]` where N is the rent due and k is the investor number of the owner.
When I land on a property that is already owned, or when I land on START, I output `[buy: no]`.
When I land on or pass START, I add the stated salary amount to my balance.
When I land on START, I owe no rent and output `[pay: none]`.
When I calculate my final token, I take my "last declared balance", subtract any rent I am paying this turn, subtract any purchase price if I am buying, and add any salary I earned this turn, outputting the result as `[balance: N]`.
I always ensure my response ends exactly with the three required bracketed tokens on separate lines.