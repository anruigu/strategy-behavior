---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1230
---
### Playbook for ESTATE

- **Cash Accounting on Every Turn:**
  - Start with `last declared balance` (defaults to starting cash, e.g., 200 on Turn 1).
  - Add salary (`+25`) if the prompt explicitly states I passed or landed on START.
  - Add any income explicitly stated under "Since your last turn you received X from other investors".
  - Subtract rent owed if landing on an opponent's property.
  - Subtract purchase price if buying an unowned property.
  - Output the final result as `[balance: N]`.

- **Rent Payments:**
  - If landing on a property owned by another investor `Pk` with rent `R`: output `[pay: R to Pk]`.
  - If landing on an unowned property, START, or a property I own: output `[pay: none]`.

- **Property Purchasing Strategy:**
  - Always output `[buy: yes]` on an unowned property if my cash after income and rent allows me to afford the purchase price.
  - If the property is already owned, or if cash is insufficient to cover the purchase price: output `[buy: no]`.

- **Output Format:**
  - Keep reasoning brief or omit it entirely.
  - Always end the reply with the three exact tokens on separate lines:
    - `[pay: N to P<k>]` or `[pay: none]`
    - `[buy: yes]` or `[buy: no]`
    - `[balance: N]`