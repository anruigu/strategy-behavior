---
game: ref_estate
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1211
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
  - When landing on an unowned property, buy it (`[buy: yes]`) whenever available cash after accounting for salary, incoming rent, and owed rent is greater than or equal to the purchase price. Property value counts 1:1 toward final score and yields positive rental returns.
  - Set `[buy: no]` if cash is insufficient, or if the tile is already owned (by me or another player) or is START.

- **Response Formatting:**
  - Always end the reply with the three required bracketed tokens in exact order:
    1. `[pay: N to P<k>]` (e.g., `[pay: 24 to P1]`) or `[pay: none]`
    2. `[buy: yes]` or `[buy: no]`
    3. `[balance: N]`