---
game: ref_estate
model: gemini-flash
condition: win
seed: 6
round: 1
chars: 1183
---
### Playbook for ESTATE

- **Balance Tracking Formula:**
  - Start with `last declared balance`.
  - Add `salary` (+25) if I passed or landed on START.
  - Add all rent received since last turn (stated as `Since your last turn you received X from other investors`).
  - Subtract rent owed if landing on an opponent's property (`[pay: N to P<k>]`). If landing on an unowned tile, START, or my own property, set `[pay: none]`.
  - Subtract property cost if I choose to buy (`[buy: yes]`).
  - Declare the exact resulting amount in `[balance: N]`.

- **Property Purchase Decisions:**
  - Always buy unowned properties whenever available funds (`current balance before purchase`) are strictly greater than or equal to the property price, especially in early/mid game laps, since property values count 1:1 toward final net worth and generate recurring rent.
  - Choose `[buy: no]` only when funds are insufficient to cover the property price or when landing on already-owned/START tiles.

- **Response Formatting:**
  - Always provide the required tokens in order at the end of the response:
    - `[pay: N to P<k>]` or `[pay: none]`
    - `[buy: yes]` or `[buy: no]`
    - `[balance: N]`