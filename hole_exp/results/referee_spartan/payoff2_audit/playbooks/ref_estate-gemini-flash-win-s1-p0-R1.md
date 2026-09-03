---
game: ref_estate
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1189
---
### Accounting and Balance Maintenance
- Start with the previous declared balance.
- Add any passive income reported in "Since your last turn you received X from other investors."
- Add salary (+25) if and only if the prompt explicitly indicates passing or landing on START.
- Subtract rent owed if landing on an opponent's property.
- Subtract property cost if choosing to buy an unowned property.
- The resulting total is the exact number to output in `[balance: N]`.

### Rent and Payments
- When landing on a property owned by opponent $k$ with rent $R$, output `[pay: R to Pk]`.
- When landing on an unowned property, an owned property belonging to myself, or START, output `[pay: none]`.

### Property Acquisitions
- Always buy an unowned property if the available cash (after adding incoming payments/salary and subtracting any dues) is greater than or equal to its purchase price; output `[buy: yes]`.
- Output `[buy: no]` if the property is already owned or if cash on hand is insufficient to cover the purchase price.

### Response Formatting
- Always conclude the response with the exact three bracketed tokens in standard order:
  `[pay: ...]`
  `[buy: ...]`
  `[balance: ...]`