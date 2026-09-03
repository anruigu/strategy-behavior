---
game: ref_estate
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1415
---
# Estate Playbook

- **Tracking Cash Balance**:
  - Start with the previous turn's declared balance (or 200 at start).
  - Add salary (+25) whenever the prompt explicitly states I passed or landed on START.
  - Add any income explicitly stated under "Since your last turn you received X from other investors" (or verify via recent transfers).
  - Subtract any rent owed this turn.
  - Calculate available balance before property purchase: `available = previous_balance + salary + received_income - rent_paid`.
  - Set the final `[balance: N]` equal to `available - (property_cost if bought else 0)`.

- **Handling Payments**:
  - When landing on an opponent's property, emit `[pay: <amount> to P<k>]` where `<amount>` matches the rent due and `P<k>` matches the owner's investor index (e.g., `[pay: 18 to P0]`).
  - When landing on an unowned property, START, or my own property, emit `[pay: none]`.

- **Purchasing Properties**:
  - When landing on an unowned property and `available >= property_price`:
    - Emit `[buy: yes]`.
    - Deduct the purchase price from the balance.
  - When landing on an already owned property, START, or when `available < property_price`:
    - Emit `[buy: no]`.

- **Turn Formatting**:
  - Keep reasoning brief (1–2 sentences).
  - Always conclude the response with the exact three bracketed tokens on separate lines:
    1. `[pay: ...]`
    2. `[buy: ...]`
    3. `[balance: ...]`