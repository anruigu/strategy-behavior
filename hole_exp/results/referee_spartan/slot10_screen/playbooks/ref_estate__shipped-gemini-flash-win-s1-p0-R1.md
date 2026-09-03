---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1367
---
### Balance Calculation & Bookkeeping Rules

* When computing `[balance: N]`, start from `last declared balance`, add:
  * Any income noted under "Since your last turn you received X from other investors",
  * The salary of 25 if and only if the prompt states "You passed START, so you may collect your salary of 25",
  and subtract:
  * Any property purchase price if `[buy: yes]`,
  * Any rent due to an owner if landing on an owned property.
* Never omit received rent or salary from the running balance calculation.

### Rent & Turn Actions

* When landing on an unowned property:
  * Set `[pay: none]`.
  * If cash balance after adding pending income and salary is greater than or equal to the property price, decide whether to buy:
    * In laps 1 to 4, set `[buy: yes]` on unowned properties whenever affordable to maximize future rent collection and maintain deed equity.
    * If cash is insufficient, set `[buy: no]`.
* When landing on a property owned by another investor `k`:
  * Set `[pay: N to P<k>]` with the exact rent amount specified.
  * Set `[buy: no]`.
* When landing on START or an unowned tile that cannot or will not be purchased:
  * Set `[pay: none]`.
  * Set `[buy: no]`.

### Output Format

* Always emit all three bracketed tokens in exact format:
  * `[pay: N to P<k>]` or `[pay: none]`
  * `[buy: yes]` or `[buy: no]`
  * `[balance: N]`