---
game: ref_estate
model: gemini
condition: win
seed: 1
round: 2
chars: 1099
---
When calculating my available cash at the beginning of a turn, I take my last declared balance, add the salary amount *only* if the prompt explicitly states I passed or landed on START, and add any incoming rent listed in the "Recent transfers on the bank's book" where another investor paid me since my last turn.

When I land on a property owned by another investor, I subtract the rent from my available cash and output `[pay: N to P<k>]`. I also output `[buy: no]`.

When I land on an unowned property, I owe no rent and output `[pay: none]`. I compare its price to my available cash. If I can afford it, I subtract the purchase price from my cash and output `[buy: yes]` because properties contribute to my final score and generate rent. If I cannot afford it, I output `[buy: no]`. 

When I land on a property I already own, I owe no rent, output `[pay: none]`, and cannot buy it again, so I output `[buy: no]`.

When ending my turn, I output `[balance: N]` reflecting my final cash exactly, accounting for any salary, incoming rent from the bank's book, outgoing rent, and property purchases.