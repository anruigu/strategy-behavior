---
game: ref_estate
model: gemini-flash
condition: win
seed: 11
round: 1
chars: 1250
---
# Playbook: Estate

### Bookkeeping & Balance Calculation
When settling each turn, calculate my new cash balance strictly in this order:
1. Start with `last declared balance`.
2. Add `received from other investors` if explicitly stated since my last turn.
3. Add `salary of 25` if I landed on or passed START this turn.
4. Subtract rent `due` to the property owner if landing on an opponent's property.
5. Subtract property `price` if buying an unowned property.
6. The resulting total is the value for `[balance: N]`.

### Turn Actions
- **Rent / Payments:**
  - If landing on an unowned property, START, or my own property: output `[pay: none]`.
  - If landing on an opponent's property: output `[pay: <rent> to P<owner_id>]`.

- **Property Purchases:**
  - If landing on an unowned property and my available cash (after accounting for received income and salary) is greater than or equal to the property price: output `[buy: yes]`.
  - If landing on an unowned property but my cash is insufficient: output `[buy: no]`.
  - If landing on an owned property or START: output `[buy: no]`.

- **Output Format:**
  - Always respond with all three tokens:
    ```
    [pay: <amount> to P<k> | none]
    [buy: yes | no]
    [balance: <final_cash>]
    ```