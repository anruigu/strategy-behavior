---
game: ref_estate
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1346
---
# Estate Playbook

## Cash Accounting
* At the start of each turn, calculate available cash before actions: `available_cash = last_declared_balance + salary_collected (if passed/landed on START) + rent_received_from_others`.
* If landing on an unowned property or a property I own, format payment as `[pay: none]`.
* If landing on a property owned by another investor `Pk`, deduct the rent due: `[pay: <rent> to P<k>]` and subtract `<rent>` from `available_cash`.
* If buying an unowned property, subtract its purchase price from remaining cash and format as `[buy: yes]`.
* If not buying, format as `[buy: no]`.
* Set `[balance: N]` strictly equal to the final calculated cash after all additions (salary, received rent) and deductions (rent paid, purchase price).

## Purchasing Strategy
* When landing on any unowned property:
  * Check if `available_cash - rent_paid >= property_price`.
  * If affordable, always choose `[buy: yes]` to secure rental income and asset equity.
  * If funds are insufficient, output `[buy: no]`.
* When landing on an already owned property (by myself or another player), always output `[buy: no]`.

## Response Formatting
* Always conclude the reply with the three exact tokens on their own lines:
  ```
  [pay: <amount> to P<k>]  (or [pay: none])
  [buy: yes]               (or [buy: no])
  [balance: <N>]
  ```