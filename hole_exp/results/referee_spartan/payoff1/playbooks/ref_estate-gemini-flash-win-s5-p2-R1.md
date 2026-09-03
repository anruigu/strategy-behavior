---
game: ref_estate
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1207
---
# Playbook for Estate

- When it is my turn to settle, I calculate my current cash balance before taking actions:
  - Start with `last declared balance`.
  - Add salary (e.g., +25) if I landed on or passed START this turn.
  - Add any income explicitly stated as received from other investors since my last turn.

- When I land on a property owned by another investor:
  - Format the payment token as `[pay: <rent> to P<k>]` where `k` is the owner's investor index.
  - Subtract that rent amount from my balance.
  - Set `[buy: no]`.

- When I land on an unowned property:
  - Set `[pay: none]`.
  - If my current balance (after adding salary/income) is greater than or equal to the purchase price, choose `[buy: yes]` and subtract the purchase price from my balance.
  - If my current balance is strictly less than the purchase price, choose `[buy: no]` and leave the balance unchanged.

- When I land on START or an owned tile with no rent due to others (e.g., my own property):
  - Set `[pay: none]`.
  - Set `[buy: no]`.

- Format the final reply to always end with the three required bracketed tokens on separate lines:
  - `[pay: ...]`
  - `[buy: ...]`
  - `[balance: <final calculated cash balance>]`