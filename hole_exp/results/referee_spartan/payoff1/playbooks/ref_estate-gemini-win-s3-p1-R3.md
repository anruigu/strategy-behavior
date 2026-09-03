---
game: ref_estate
model: gemini
condition: win
seed: 3
round: 3
chars: 1113
---
When calculating my new cash balance, I start with my last declared balance, add any amount received from other investors since my last turn, and add my salary (25) if I passed or landed on START. 

When I land on an unowned property, I check my current balance against the purchase price. If I have enough cash, I buy it to maximize my final net worth by declaring `[buy: yes]` and deducting the price from my balance. If I cannot afford it, I declare `[buy: no]`.

When I land on a property owned by another investor, I identify the rent due and the owner. I declare `[pay: N to P<k>]` (where N is the rent and k is the investor number), deduct the rent from my balance, and declare `[buy: no]`.

When I land on a property I already own, I owe no rent and cannot buy it, so I declare `[pay: none]` and `[buy: no]`.

When I land exactly on START, I owe no rent and cannot buy anything, so I declare `[pay: none]` and `[buy: no]`.

At the end of every turn, regardless of the board state, I output exactly these three tokens in order:
`[pay: N to P<k>]` or `[pay: none]`
`[buy: yes]` or `[buy: no]`
`[balance: N]`