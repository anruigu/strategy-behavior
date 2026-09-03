---
game: ref_estate
model: gemini
condition: win
seed: 3
round: 1
chars: 1094
---
When I land on an unowned property, I check my current declared balance against the purchase price. If I have enough cash, I buy it to maximize my final net worth by declaring `[buy: yes]` and deducting the price from my balance. If I cannot afford it, I declare `[buy: no]`.

When I land on a property owned by another investor, I identify the rent due and the owner. I declare `[pay: N to P<k>]` (where N is the rent and k is the investor number), deduct the rent from my balance, and declare `[buy: no]`.

When I pass or land on START, I add the salary amount (25) to my running cash balance. 

When I land exactly on START, I owe no rent and cannot buy anything, so I declare `[pay: none]` and `[buy: no]`.

When calculating my final balance for the turn, I always process salary additions first (if passing or landing on START), and then subtract any rent or property purchase price incurred on that turn. 

At the end of every turn, regardless of the board state, I output exactly these three tokens in order:
`[pay: N to P<k>]` or `[pay: none]`
`[buy: yes]` or `[buy: no]`
`[balance: N]`