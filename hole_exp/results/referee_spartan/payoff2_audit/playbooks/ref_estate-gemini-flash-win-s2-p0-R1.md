---
game: ref_estate
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1297
---
# Estate Strategy Playbook

- **Tracking Cash Balance**: Calculate new balance strictly in this order:
  1. Start with `Your last declared balance`.
  2. Add any incoming cash explicitly noted in `Since your last turn you received X from other investors`.
  3. Add salary (+25) if `You passed START` or landed on START.
  4. Subtract rent due to another player if landing on their owned property (`[pay: N to P<k>]`).
  5. Subtract the purchase price if buying an unowned property (`[buy: yes]`).
  6. The resulting number is the exact value for `[balance: N]`.

- **Property Purchases**:
  - Always choose `[buy: yes]` on an unowned property if current available cash (after salary and rent) is greater than or equal to the property price.
  - Choose `[buy: no]` if the property is already owned (by myself or another investor) or if funds are insufficient.

- **Rent Payments**:
  - If landing on an opponent's property, reply with `[pay: N to P<k>]` specifying the exact rent amount and owner identifier.
  - If landing on START, unowned property, or my own property, reply with `[pay: none]`.

- **Response Formatting**:
  - Output all three required tokens on every turn: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`. Keep brief reasoning preceding the tokens to avoid calculation errors.