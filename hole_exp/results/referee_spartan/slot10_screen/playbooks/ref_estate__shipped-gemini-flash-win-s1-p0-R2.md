---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1530
---
### Balance Calculation & Bookkeeping Rules

* When computing `[balance: N]`, start from `last declared balance`, add:
  * Any income noted under "Since your last turn you received X from other investors",
  * The salary of 25 if and only if the prompt states "You passed START, so you may collect your salary of 25" (or landed on START),
  and subtract:
  * Any property purchase price if `[buy: yes]`,
  * Any rent due to an owner if landing on an owned property.
* Always explicitly verify arithmetic: `new_balance = last_balance + received_rent + salary - rent_paid - purchase_price`.

### Rent & Turn Actions

* When landing on an unowned property:
  * Set `[pay: none]`.
  * If cash balance (after adding pending income and salary) is greater than or equal to the property price:
    * Always set `[buy: yes]` on affordable unowned properties, even in late laps, since purchase price is preserved 1:1 as deed equity in final scoring and eliminates future risk of opponents buying it.
  * If cash balance is strictly less than the property price, set `[buy: no]`.
* When landing on a property owned by another investor `k`:
  * Set `[pay: N to P<k>]` with the exact rent amount specified in the prompt.
  * Set `[buy: no]`.
* When landing on START, your own property, or an unowned tile that cannot be purchased:
  * Set `[pay: none]`.
  * Set `[buy: no]`.

### Output Format

* Always emit all three bracketed tokens in exact format:
  * `[pay: N to P<k>]` or `[pay: none]`
  * `[buy: yes]` or `[buy: no]`
  * `[balance: N]`