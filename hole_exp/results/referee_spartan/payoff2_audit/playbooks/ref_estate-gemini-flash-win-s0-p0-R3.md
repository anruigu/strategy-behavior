---
game: ref_estate
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1322
---
# Estate Playbook

- **Accounting Equation Every Turn:**
  - Start with `last declared balance`.
  - Add any incoming cash explicitly stated under "Since your last turn you received X from other investors" (if none stated, add 0).
  - Add salary (25) if the prompt explicitly states "You passed START" or "landed on START".
  - Subtract rent owed if landing on another player's property.
  - Subtract property price if purchasing the current property (`[buy: yes]`).
  - Output the resulting integer in `[balance: N]`.

- **Rent Obligations:**
  - When landing on a property owned by investor $k$, output `[pay: <rent> to P<k>]`.
  - When landing on an unowned property, my own property, or START, output `[pay: none]`.

- **Property Purchases:**
  - When landing on an unowned property:
    - If available cash (after adding received rent + salary, minus any rent due) is greater than or equal to the property price, output `[buy: yes]`.
    - If cash is strictly less than the purchase price, output `[buy: no]`.
  - When landing on an already owned tile or START, output `[buy: no]`.

- **Output Formatting:**
  - Keep reasoning brief or omit commentary.
  - Always provide the three required action tags in order:
    1. `[pay: <rent> to P<k>]` or `[pay: none]`
    2. `[buy: yes]` or `[buy: no]`
    3. `[balance: N]`