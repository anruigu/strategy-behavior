---
game: ref_estate
model: gemini
condition: win
seed: 4
round: 3
chars: 1128
---
I calculate my available cash at the start of each turn by taking my last declared balance, adding any rent received from other investors since the last turn, and adding my salary if the prompt states I passed or landed on START.

When I land on an unowned property, I check my available cash. If I have enough to cover the purchase price, I buy it to maximize my investment score by outputting `[buy: yes]` and subtracting the price from my balance. 

When I land on an unowned property but my available cash is lower than the purchase price, I output `[buy: no]` and do not subtract the price from my balance.

When I land on a property owned by another investor, I output `[pay: N to P<k>]` with the required rent and subtract that amount from my balance. I also output `[buy: no]`.

When I land on an unowned property, a property I already own, or START, I output `[pay: none]`. If the property is owned by me or it is START, I also output `[buy: no]`.

When I finish my calculations, I always output exactly the three required tokens in order: the pay token, the buy token, and the balance token with my final updated cash.