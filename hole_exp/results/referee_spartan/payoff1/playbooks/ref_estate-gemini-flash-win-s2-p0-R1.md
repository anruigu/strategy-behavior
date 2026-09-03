---
game: ref_estate
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1336
---
# Playbook for ESTATE

## Turn Accounting Rules
- Calculate the updated balance systematically each turn before outputting tokens:
  1. Start with `last declared balance`.
  2. Add any income stated under "Since your last turn you received X from other investors".
  3. Add 25 if the prompt indicates I passed or landed on START.
  4. Subtract rent due if landing on another player's property.
  5. Subtract purchase price if buying an unowned property.
- Ensure the resulting number matches `[balance: N]`.

## Property Purchases
- When landing on an unowned property during early/mid game laps and my funds cover the cost while leaving enough buffer to pay immediate potential rents, choose `[buy: yes]`.
- When landing on an unowned property that I cannot afford or in the final lap where capital cannot yield positive rent return, choose `[buy: no]`.
- When landing on an owned property, START, or any non-purchasable tile, choose `[buy: no]`.

## Rent Payments
- When landing on an opponent's property with rent due of $N$ to investor $k$, output `[pay: N to P<k>]`.
- When landing on START, unowned property, or my own property, output `[pay: none]`.

## Response Format
- Always output all three tokens exactly at the end of the response:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`