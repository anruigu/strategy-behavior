---
game: ref_estate
model: gemini-flash
condition: win
seed: 6
round: 2
chars: 1165
---
### Playbook for ESTATE

- **Balance Tracking Formula:**
  - Start with `last declared balance`.
  - Add salary (+25) if I passed or landed on START.
  - Add rent received since last turn (if explicitly stated: `Since your last turn you received X from other investors`).
  - Subtract rent owed if landing on an opponent's property (`[pay: N to P<k>]`). If landing on an unowned tile, START, or my own property, output `[pay: none]`.
  - Subtract property price if purchasing (`[buy: yes]`).
  - Set `[balance: N]` to the final computed cash amount.

- **Property Purchase Decisions:**
  - When landing on an unowned property, buy it (`[buy: yes]`) if cash after accounting for salary, incoming rent, and owed rent is greater than or equal to the purchase price. Property value counts 1:1 toward final net worth and generates rental income.
  - Set `[buy: no]` if funds are insufficient, or if the tile is already owned (by me or another player) or is START.

- **Response Formatting:**
  - Always end the reply with the three required bracketed tokens in exact order:
    - `[pay: N to P<k>]` or `[pay: none]`
    - `[buy: yes]` or `[buy: no]`
    - `[balance: N]`