---
game: ref_estate
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1282
---
# Estate Playbook

- **Tracking Cash Balance Step-by-Step:**
  - Start with `Your last declared balance`.
  - Add income: `Since your last turn you received N from other investors` (if explicitly stated).
  - Add salary (+25) if the turn prompt explicitly states I passed or landed on START.
  - Deduct rent paid if landing on an opponent's property.
  - Deduct purchase price if buying an unowned property (`[buy: yes]`).
  - Set `[balance: N]` strictly equal to this final calculated cash amount.

- **Purchasing Decisions:**
  - When landing on an unowned property, if my post-income available cash $\ge$ purchase price, emit `[buy: yes]`.
  - When landing on an owned property, START, or if cash is insufficient to cover the purchase price, emit `[buy: no]`.

- **Rent Payments:**
  - When landing on an opponent's property owned by investor $k$, emit `[pay: R to Pk]`, where $R$ is the rent due and $k$ is their player index (e.g., `P0`, `P1`).
  - When landing on START, an unowned property, or my own property, emit `[pay: none]`.

- **Output Format:**
  - Keep reasoning brief (1–2 sentences).
  - Always end the response with the exact three bracketed tokens in this order:
    1. `[pay: N to P<k>]` or `[pay: none]`
    2. `[buy: yes]` or `[buy: no]`
    3. `[balance: N]`