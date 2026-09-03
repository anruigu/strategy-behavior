---
game: ref_estate
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1587
---
# Playbook for ESTATE

## Turn Accounting Rules
- Calculate the updated balance systematically each turn before outputting tokens:
  1. Start with `last declared balance`.
  2. Add any income explicitly stated under "Since your last turn you received X from other investors".
  3. Add 25 salary if the prompt states "You passed START, so you may collect your salary of 25" or if landing on/passing START.
  4. Subtract rent due if landing on another player's property.
  5. Subtract purchase price if buying an unowned property (`[buy: yes]`).
- Verify the math so that `[balance: N]` strictly equals: `last_declared + rent_received + salary - rent_paid - purchase_cost`.

## Property Purchases
- When landing on an unowned property during early/mid game (Laps 1–4) and balance covers the purchase price, choose `[buy: yes]` to secure deeds and rental income.
- When landing on an unowned property where buying would leave insufficient cash or during late game when ROI is negligible, evaluate and choose `[buy: no]`.
- When landing on an already owned property, START, or any non-purchasable tile, always choose `[buy: no]`.

## Rent Payments
- When landing on an opponent's property with rent due of $N$ to investor $k$, output `[pay: N to P<k>]` (e.g., `[pay: 24 to P1]`).
- When landing on START, unowned property, or my own property, output `[pay: none]`.

## Response Format
- Keep brief reasoning at the start of the reply.
- Always output all three tokens clearly at the end of the reply:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`