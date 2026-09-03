---
game: ref_estate
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 1125
---
### Balance Accounting & Turn Settlement
* Start each turn's balance calculation from `Your last declared balance`.
* Add any cash received from other investors since the last turn (`Since your last turn you received X from other investors`).
* If passing or landing on START, add the salary amount (+25) to the cash balance before resolving rent or purchases.
* If landing on a property owned by another player `Pk`, output `[pay: <rent> to P<k>]`, set `[buy: no]`, and deduct the rent amount from the balance.
* If landing on an unowned property, an owned property belonging to me, or START: output `[pay: none]`.
* If landing on an unowned property and current available cash (after rent/salary) is at least the purchase price, output `[buy: yes]` and subtract the price from the balance. If funds are insufficient or it is already owned, output `[buy: no]`.
* Always format the final response with all three required tokens in exact syntax on separate lines at the end:
  * `[pay: N to P<k>]` or `[pay: none]`
  * `[buy: yes]` or `[buy: no]`
  * `[balance: N]` (reflecting exact net cash after additions and subtractions)