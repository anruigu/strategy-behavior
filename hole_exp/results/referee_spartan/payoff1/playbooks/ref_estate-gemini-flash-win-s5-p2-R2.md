---
game: ref_estate
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1279
---
# Playbook for Estate

- When it is my turn to settle, calculate available cash before actions:
  - Start with `last declared balance`.
  - Add salary (+25 or specified amount) if the prompt states I passed or landed on START this turn.
  - Add any income explicitly stated as received from other investors since my last turn.

- When I land on a property owned by another investor:
  - Format the payment token as `[pay: <rent> to P<k>]` where `k` is the owner's investor index (e.g., `[pay: 24 to P0]`).
  - Subtract that rent amount from my balance.
  - Set `[buy: no]`.

- When I land on an unowned property:
  - Set `[pay: none]`.
  - If available balance is greater than or equal to the property price, choose `[buy: yes]` and subtract the purchase price from my balance.
  - If available balance is less than the purchase price, choose `[buy: no]` and leave the balance unchanged.

- When I land on START or a property I own (or nothing is due):
  - Set `[pay: none]`.
  - Set `[buy: no]`.

- Reply formatting:
  - Keep reasoning brief (1-2 sentences).
  - Always end the reply with the three required bracketed tokens on their own lines:
    - `[pay: <amount> to P<k>]` or `[pay: none]`
    - `[buy: yes]` or `[buy: no]`
    - `[balance: <final calculated cash balance>]`