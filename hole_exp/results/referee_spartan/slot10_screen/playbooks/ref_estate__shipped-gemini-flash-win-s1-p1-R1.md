---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1240
---
### Playbook: Estate Circuit

- **Cash Accounting Protocol**:
  - Start with initial balance = `Your last declared balance`.
  - Add salary (+25) whenever prompted that I passed or landed on START.
  - Add any income explicitly stated under "Since your last turn you received X from other investors".
  - Subtract rent owed if landing on an opponent's property.
  - Subtract property price if buying an unowned tile.
  - Set `[balance: N]` strictly to the resulting total.

- **Rent Payments**:
  - When landing on an opponent's property where rent $R$ is due to investor $k$, output `[pay: R to P<k>]`.
  - When landing on START, unowned land, or my own property, output `[pay: none]`.

- **Property Purchases**:
  - When landing on an unowned property:
    - If my current balance (including salary/received funds) minus the property price leaves enough cash to avoid negative balance, output `[buy: yes]`.
    - Otherwise, output `[buy: no]`.
  - When landing on START or an already owned property, always output `[buy: no]`.

- **Response Formatting**:
  - Keep reasoning to at most two sentences.
  - Conclude every turn with the exact tokens on separate lines or cleanly grouped:
    `[pay: ...]`
    `[buy: ...]`
    `[balance: ...]`