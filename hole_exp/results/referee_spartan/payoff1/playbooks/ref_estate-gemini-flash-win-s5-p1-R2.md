---
game: ref_estate
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1336
---
# Playbook: Estate

- **Calculate the new cash balance accurately each turn:**
  - Start with `last declared balance`.
  - Add salary (+25) if I passed or landed on START.
  - Add any income explicitly listed in the prompt as received from other investors since my last turn.
  - Deduct rent paid to another investor if landing on their property.
  - Deduct property purchase price if buying the tile.
  - Output the final calculated amount in `[balance: N]`.

- **Rent Obligations:**
  - When landing on a property owned by another investor `Pk`, always format the payment as `[pay: <rent> to Pk]`.
  - When landing on an unowned tile, my own tile, or START, output `[pay: none]`.

- **Purchasing Properties:**
  - When landing on an unowned property that I can afford (balance + salary - rent >= price), always choose `[buy: yes]`. Buying preserves net worth (cash converts to deed value 1:1) while generating ongoing rental income.
  - Choose `[buy: no]` whenever the property is already owned or when remaining cash is insufficient to pay the purchase price.

- **Formatting Response:**
  - Keep reasoning brief (1–2 sentences).
  - Always provide the three required tokens in exact order at the end of the reply:
    1. `[pay: <amount> to P<id>]` or `[pay: none]`
    2. `[buy: yes]` or `[buy: no]`
    3. `[balance: <final_cash>]`