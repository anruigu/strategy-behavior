---
game: ref_estate
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1469
---
### Playbook for ESTATE

- **Calculate Starting Balance and Incoming Cash:**
  - Start with the previous declared cash balance.
  - Add salary (+25) if I passed or landed on START.
  - Add any rent received from other investors since the last turn as stated in the prompt (e.g. "Since your last turn you received X from other investors").

- **Handle Rent and Deductions:**
  - If landing on a property owned by another investor `P<k>`, declare `[pay: <rent> to P<k>]` and deduct that rent amount from the running cash balance.
  - If landing on an unowned property, my own property, or START, declare `[pay: none]`.

- **Property Purchase Decisions:**
  - When landing on an unowned property:
    - If running cash balance (after adding incoming funds and deducting any rent) is greater than or equal to the property's purchase price, declare `[buy: yes]` and deduct the purchase price from cash balance.
    - If running cash balance is less than the purchase price, declare `[buy: no]`.
  - When landing on an already owned property or START, declare `[buy: no]`.

- **Final Balance Accounting:**
  - Compute: `new_balance = last_balance + salary (if passed/landed on START) + incoming_rent - rent_paid - property_cost (if [buy: yes])`.
  - Declare `[balance: <new_balance>]`.

- **Formatting:**
  - Always output all three tokens strictly formatted on their own lines:
    - `[pay: N to P<k>]` or `[pay: none]`
    - `[buy: yes]` or `[buy: no]`
    - `[balance: N]`