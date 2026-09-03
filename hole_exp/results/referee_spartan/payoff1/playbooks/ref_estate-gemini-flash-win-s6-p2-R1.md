---
game: ref_estate
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1283
---
# Estate Playbook

## Cash Balance Tracking
- Start with base cash of 200.
- At the start of every turn, calculate available cash before actions:
  - Take the last declared balance.
  - Add salary (+25) if the turn prompt explicitly states I passed or landed on START.
  - Add all incoming rent received since my last turn as reported in the prompt.
- Deduct rent owed if landing on an opponent's property.
- Deduct property purchase price if buying the tile.
- Declare the exact resulting amount in `[balance: N]`.

## Rent Payments
- When landing on a tile owned by investor $k$ with rent $R$:
  - Declare `[pay: R to Pk]`.
- When landing on START, an unowned tile, or a property I already own:
  - Declare `[pay: none]`.

## Property Purchases
- When landing on an unowned tile:
  - If available cash (after collecting salary/incoming rent and paying any due rent) is greater than or equal to the property price, declare `[buy: yes]`.
  - If available cash is strictly less than the property price, declare `[buy: no]`.
- When landing on START or any tile that is already owned:
  - Declare `[buy: no]`.

## Formatting
- Always output the exact three bracketed tokens in every turn response:
  - `[pay: N to Pk]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`