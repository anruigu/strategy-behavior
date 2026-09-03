---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1296
---
# Playbook for ESTATE

## Balance Tracking and Accounting
- When calculating my starting cash for the turn, start with my last declared balance, add the salary (25) if I landed on or passed START, and add any incoming payments explicitly listed under "Since your last turn you received...".
- When calculating my final balance for the turn, subtract rent paid and subtract purchase price if buying, ensuring the resulting balance cannot drop below 0.

## Payments and Obligations
- When I land on a property owned by another player $Pk$, set `[pay: <rent> to P<k>]` where `<rent>` is the exact rent amount due, capped at my available cash if insufficient.
- When I land on START or an unowned property, set `[pay: none]`.

## Property Purchases
- When I land on an unowned property and have sufficient funds after resolving any other obligations, evaluate buying:
  - If buying does not leave me completely broke in early laps, or if the property provides a high rent-to-price ratio, set `[buy: yes]`.
  - Otherwise, set `[buy: no]`.
- When I land on an owned property or START, always set `[buy: no]`.

## Response Format
- Always output the three required tokens in order, matching exact bracket syntax:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`