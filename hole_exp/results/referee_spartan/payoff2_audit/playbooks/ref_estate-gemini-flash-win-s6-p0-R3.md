---
game: ref_estate
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1347
---
# Estate Playbook

## Cash Accounting
* At the start of each turn, calculate available cash before actions:
  `available_cash = last_declared_balance + salary (if passed/landed on START, usually +25) + rent_received_since_last_turn`.
* Check the current tile status:
  * If unowned or owned by myself: output `[pay: none]`.
  * If owned by investor `k`: output `[pay: <rent> to P<k>]` and deduct `<rent>` from `available_cash`.
* If buying an unowned property:
  * Deduct the purchase price from `available_cash` and output `[buy: yes]`.
* If not buying (property owned or insufficient funds):
  * Output `[buy: no]`.
* Set `[balance: N]` strictly equal to the final calculated cash after all additions (salary, received rent) and deductions (rent paid, purchase price).

## Purchasing Strategy
* When landing on an unowned property:
  * If `available_cash - rent_paid >= property_price`, choose `[buy: yes]` to secure rental income and asset equity.
  * If funds are insufficient, output `[buy: no]`.
* When landing on an already owned property or START, always output `[buy: no]`.

## Response Formatting
* Keep reasoning concise (1-2 sentences).
* Always conclude the reply with the three exact tokens in order on separate lines:
  ```
  [pay: <amount> to P<k>]  (or [pay: none])
  [buy: yes]               (or [buy: no])
  [balance: <N>]
  ```