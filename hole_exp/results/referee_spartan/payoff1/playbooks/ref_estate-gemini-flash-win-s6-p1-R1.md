---
game: ref_estate
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 915
---
### Balance Accounting & Turn Settlement
* When passing or landing on START, add the salary amount (+25) to my current cash balance before calculating any purchases or rent.
* When landing on an unowned property that I have sufficient funds to buy, output `[buy: yes]` and subtract its purchase price from my balance. Always buy unowned properties whenever affordable to build net worth and generate rent.
* When landing on an already owned property, output `[buy: no]`. If owned by another player, output `[pay: <rent> to P<k>]` and subtract the rent from my balance.
* When landing on START or a tile with no rent due, output `[pay: none]` and `[buy: no]`.
* Always format the settlement declaration with all three required tokens in exact syntax:
  * `[pay: N to P<k>]` or `[pay: none]`
  * `[buy: yes]` or `[buy: no]`
  * `[balance: N]` reflecting exact net cash after salary, rent paid, and property purchases.