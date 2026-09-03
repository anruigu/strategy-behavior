---
game: ref_estate
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1164
---
# Estate Playbook

- **Accounting Equation Every Turn:**
  - Start with `last declared balance`.
  - Add any incoming cash listed under "Since your last turn you received X from other investors".
  - Add salary (25) if the turn prompt states you passed or landed on START.
  - Subtract rent owed if landing on another player's property.
  - Subtract property price if purchasing the current property.
  - Output the resulting integer in `[balance: N]`.

- **Rent Obligations:**
  - When landing on a property owned by investor $k$, output `[pay: <rent> to P<k>]`.
  - When landing on an unowned property, my own property, or START, output `[pay: none]`.

- **Property Purchases:**
  - When landing on an unowned property:
    - If my available cash balance (after adding received rent/salary and subtracting any rent due) is greater than or equal to the property purchase price, output `[buy: yes]`.
    - If cash is insufficient, output `[buy: no]`.
  - When landing on an owned tile or START, output `[buy: no]`.

- **Output Formatting:**
  - Always provide the three required action tags in order:
    1. `[pay: ...]`
    2. `[buy: ...]`
    3. `[balance: ...]`