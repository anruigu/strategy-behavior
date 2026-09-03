---
game: ref_estate
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1362
---
# Playbook: Estate

- **Calculate the new cash balance accurately each turn:**
  - Start with `last declared balance`.
  - Add salary (+25) if I passed or landed on START.
  - Add any income explicitly listed as received from other investors since my last turn.
  - Deduct rent paid to another investor if landing on their property.
  - Deduct property purchase price if buying the tile.
  - Output the final calculated amount in `[balance: N]`.

- **Rent Obligations:**
  - When landing on a property owned by another investor `Pk`, always format the payment as `[pay: <rent> to Pk]`.
  - When landing on an unowned tile, my own tile, or START, output `[pay: none]`.

- **Purchasing Properties:**
  - When landing on an unowned property that I can afford without going negative, always choose `[buy: yes]`. Buying adds the full purchase price to my final score in property equity while generating potential rental income, making it strictly neutral on total asset value immediately and strictly positive over time.
  - Only choose `[buy: no]` when the property is already owned or when cash is insufficient to cover the purchase price.

- **Formatting Response:**
  - Always provide the three required tokens in order at the end of the reply:
    1. `[pay: <amount> to P<id>]` or `[pay: none]`
    2. `[buy: yes]` or `[buy: no]`
    3. `[balance: <final_cash>]`