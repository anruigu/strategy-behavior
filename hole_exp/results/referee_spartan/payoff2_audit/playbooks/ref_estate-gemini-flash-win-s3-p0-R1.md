---
game: ref_estate
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1342
---
### Playbook for ESTATE

- **Calculate Starting Balance and Incoming Cash:**
  - Start with the previous declared cash balance.
  - Add salary (+25) if I passed or landed on START.
  - Add any rent received from other investors since the last turn as stated in the prompt.

- **Handle Rent and Deductions:**
  - If landing on a property owned by another investor `P<k>`, declare `[pay: <rent> to P<k>]` and deduct that amount from my running cash balance.
  - If landing on an unowned property, my own property, or START, declare `[pay: none]`.

- **Property Purchase Decisions:**
  - When landing on an unowned property:
    - If my running cash balance after rent exceeds or equals the purchase price, evaluate purchase: declare `[buy: yes]` to secure rent income and asset value, then deduct the purchase price from my balance.
    - If running cash is strictly less than the purchase price, declare `[buy: no]`.
  - When landing on an already owned property or START, declare `[buy: no]`.

- **Final Balance Accounting:**
  - Compute `new_balance = last_balance + salary (if applicable) + incoming_rent - rent_paid - property_cost (if bought)`.
  - Declare `[balance: <new_balance>]`.

- **Formatting:**
  - Always output all three tokens strictly formatted on their own lines:
    - `[pay: ...]`
    - `[buy: ...]`
    - `[balance: ...]`