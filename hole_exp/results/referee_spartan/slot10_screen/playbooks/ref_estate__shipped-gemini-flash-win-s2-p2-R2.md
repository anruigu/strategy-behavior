---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1460
---
# Playbook for ESTATE

## Balance Tracking and Accounting
- When calculating my starting cash for the turn, start with my last declared balance, add the salary (25) if the turn states "You passed START" or "landed on START", and add any incoming payments explicitly recorded to me on the bank's ledger since my last turn.
- When calculating my final balance for the turn:
  - Subtract rent paid to another player.
  - Subtract property purchase price if buying (`[buy: yes]`).
  - Ensure the resulting balance cannot drop below 0.
- Note that property purchase price converts cash directly into property deed value 1:1, so buying unowned properties does not decrease total score net worth.

## Payments and Obligations
- When I land on a property owned by another player $Pk$, set `[pay: <rent> to P<k>]` where `<rent>` is the exact rent amount due stated in the prompt, capped at my available cash if insufficient.
- When I land on START, an unowned property, or a property I already own, set `[pay: none]`.

## Property Purchases
- When I land on an unowned property and have sufficient funds after collecting salary and paying obligations, set `[buy: yes]`.
- When I land on an already owned property, START, or lack sufficient funds to purchase, set `[buy: no]`.

## Response Format
- Always output the three required tokens in order, matching exact bracket syntax:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`