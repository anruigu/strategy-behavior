---
game: ref_estate
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1297
---
# Estate Playbook

- **Tracking Cash Balance**:
  - Start with the previous turn's declared balance.
  - Add salary (+25) whenever the prompt explicitly states I passed or landed on START.
  - Add any income received from other players since the last turn as stated in the prompt.
  - Subtract any rent owed before calculating available purchasing power.
  - Set the final `[balance: N]` equal to `previous_balance + salary + received_rent - rent_paid - (property_cost if bought else 0)`.

- **Handling Payments**:
  - When landing on an opponent's property, emit `[pay: <amount> to P<k>]` where `<amount>` matches the rent due and `P<k>` matches the owner's investor index.
  - When landing on an unowned property, START, or my own property, emit `[pay: none]`.

- **Purchasing Properties**:
  - When landing on an unowned property and my cash after salary, incoming rent, and owed rent is greater than or equal to the property price:
    - Emit `[buy: yes]`.
    - Deduct the purchase price from my balance.
  - When landing on an owned property or when I cannot afford an unowned property:
    - Emit `[buy: no]`.

- **Turn Formatting**:
  - Always end every turn response with the exact three bracketed tokens on their own lines:
    1. `[pay: ...]`
    2. `[buy: ...]`
    3. `[balance: ...]`