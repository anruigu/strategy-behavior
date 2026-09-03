---
game: ref_estate
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1501
---
# Estate Strategy Playbook

- **Tracking Cash Balance**: Calculate new balance strictly in this order:
  1. Start with `Your last declared balance`.
  2. Add any incoming cash explicitly stated in `Since your last turn you received X from other investors`.
  3. Add salary (+25) if prompted `You passed START` or landed on START.
  4. Subtract rent due to another player if landing on their owned property (`[pay: N to P<k>]`).
  5. Subtract the purchase price if buying an unowned property (`[buy: yes]`).
  6. The resulting number is the exact value for `[balance: N]`.

- **Property Purchases**:
  - Always choose `[buy: yes]` on an unowned property if current available cash (after accounting for incoming transfers, salary, and any rent) is greater than or equal to the property price.
  - Choose `[buy: no]` if the property is already owned (by myself or another investor), if landing on START, or if funds are insufficient.

- **Rent Payments**:
  - If landing on an opponent's property, reply with `[pay: N to P<k>]` specifying the exact rent amount and owner identifier (e.g., `[pay: 18 to P2]`).
  - If landing on START, an unowned property, or my own property, reply with `[pay: none]`.

- **Response Formatting**:
  - Keep reasoning brief (1–2 sentences outlining the balance calculation and purchase decision).
  - Always output all three required tokens in order at the end of the response:
    - `[pay: N to P<k>]` or `[pay: none]`
    - `[buy: yes]` or `[buy: no]`
    - `[balance: N]`