---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1669
---
- When a property I land on is unowned and priced at or below my current cash, I buy it. Deeds count at full purchase price toward final net worth, so buying never loses net worth — it only converts cash into an income-earning asset.
- I buy aggressively early (the expensive high-rent properties first when I can afford them, e.g. rent ≥ 20), because each one can collect rent from two opponents for the remaining laps; rent income across laps easily exceeds any salary I forgo.
- I always check "since your last turn you received N" and add it to the declared balance before doing arithmetic — my cash is what the interface says I received plus my last declared balance, not just the last balance.
- When I pass or land on START, I add the salary to my balance that same turn and state the new total in the balance token.
- When I land on an owned property, I pay the stated rent to the stated owner, declare the payment token naming that player, and never attempt a buy on owned tiles.
- When I land on my own property, I declare [pay: none] and [buy: no] without changing the balance.
- I keep a running ledger of my cash after every transfer, since I keep my own books and only my declared balance counts; I double-check additions and subtractions before answering.
- I treat buying as net-worth-preserving even late in the game, but prefer high rent per price (rent ÷ price ratio) when choosing between marginal purchases; ratio above ~0.25 is strong.
- I don't hoard cash for safety beyond one expected rent payment; cash earns nothing while properties earn every lap.
- I format every reply with all three bracketed tokens, pay first, and end with [balance: N].