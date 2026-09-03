---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1365
---
When I land on an unowned property in the early laps, I buy it even if it nearly empties my cash, as long as I can still cover a likely rent payment before my next salary — deeds count at full price in my final total, and they collect rent meanwhile.

Before declaring my balance, I recompute it from my last declared balance: add salary if I passed START, add any rent the bank's book shows other investors paid me since my last turn, subtract my own purchases and rents paid. I never skip the "received from other investors" line.

When I land on an owned tile, I pay exactly the listed rent and nothing else, and I name the owner correctly from the bank's book.

In the final lap or two, I stop buying cheap leftover deeds if the price would leave me unable to pay a plausible rent, but otherwise I still convert spare cash into deeds since deeds score at purchase price and cash in hand does nothing extra.

I keep my declared balance honest and consistent turn to turn — the book is auditable, and clean arithmetic is what converts a good position into a good final score.

I double-check whether I passed START each turn by comparing positions around the circuit, and I add the salary before subtracting any payments due that turn.

I always reply with all three tokens, with the balance token last, and I avoid trailing whitespace that could confuse parsing.