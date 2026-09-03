---
game: ref_estate
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1341
---
### Accounting and Balance Maintenance
- Start with the previous declared balance (`Your last declared balance: N`).
- Add any passive income explicitly stated in "Since your last turn you received X from other investors."
- Add salary (+25) if and only if the prompt states that I passed or landed on START.
- Subtract rent owed if landing on an opponent's property.
- Subtract property cost if choosing to buy an unowned property.
- The resulting total is the exact integer to output in `[balance: N]`.

### Rent and Payments
- When landing on a property owned by opponent $k$ with rent $R$, output `[pay: R to Pk]`.
- When landing on an unowned property, a property I already own, or START, output `[pay: none]`.

### Property Acquisitions
- Check available cash after adding incoming payments/salary and subtracting any rent due this turn.
- If landing on an unowned property and available cash $\ge$ purchase price, choose to buy: output `[buy: yes]`.
- Output `[buy: no]` if the tile is START, if the property is already owned (by me or another player), or if available cash is less than the purchase price.

### Response Formatting
- Keep reasoning brief (1–2 sentences).
- End every turn with the three required bracketed tokens in exact order:
  `[pay: N to P<k>]` (or `[pay: none]`)
  `[buy: yes]` (or `[buy: no]`)
  `[balance: N]`