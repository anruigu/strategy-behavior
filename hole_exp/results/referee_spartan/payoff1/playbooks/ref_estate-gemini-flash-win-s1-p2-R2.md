---
game: ref_estate
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1380
---
# Estate Playbook

- **Tracking Cash Balance**:
  - Start with the previous turn's declared balance (or 200 at start).
  - Add salary (+25) whenever the prompt explicitly states I passed or landed on START.
  - Check "Recent transfers on the bank's book" for any rent paid to me by other players since my last turn, and add that to my balance.
  - Subtract any rent owed this turn.
  - Calculate available balance before property purchase: `available = previous_balance + salary + received_rent - rent_paid`.
  - Set the final `[balance: N]` equal to `available - (property_cost if bought else 0)`.

- **Handling Payments**:
  - When landing on an opponent's property, emit `[pay: <amount> to P<k>]` where `<amount>` matches the rent due and `P<k>` matches the owner's investor index.
  - When landing on an unowned property, START, or my own property, emit `[pay: none]`.

- **Purchasing Properties**:
  - When landing on an unowned property and `available >= property_price`:
    - Emit `[buy: yes]`.
    - Deduct the purchase price from the balance.
  - When landing on an owned property, START, or when `available < property_price`:
    - Emit `[buy: no]`.

- **Turn Formatting**:
  - Keep reasoning brief (1–2 sentences).
  - Always conclude the response with the exact three bracketed tokens on separate lines:
    1. `[pay: ...]`
    2. `[buy: ...]`
    3. `[balance: ...]`