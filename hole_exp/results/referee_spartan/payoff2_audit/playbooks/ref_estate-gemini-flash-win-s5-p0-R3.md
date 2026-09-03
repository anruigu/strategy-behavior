---
game: ref_estate
model: gemini-flash
condition: win
seed: 5
round: 3
chars: 1585
---
### Strategy and Accounting Rules

- **Buying Properties**: Always buy an unowned property whenever I land on it and can afford it (available cash after salary and received rents $\ge$ price). Properties convert liquid cash 1:1 into asset value while generating ongoing rent income.
- **Handling Rent Payments**:
  - When landing on an opponent's tile, declare `[pay: N to P<k>]` with the exact rent specified in the prompt and the owner's player ID (e.g., `P1`, `P2`).
  - When landing on an unowned property, a property I own, or START, declare `[pay: none]`.
- **Handling Purchases**:
  - Declare `[buy: yes]` if purchasing an unowned property.
  - Declare `[buy: no]` if the tile is already owned, if I lack sufficient funds, or if on START.
- **Calculating Declared Balance**:
  - Carefully parse the prompt for all cash inflows and outflows:
    1. Start with `Last declared balance`.
    2. Add `Received from other investors` if explicitly stated in the prompt text.
    3. Add `Salary` (usually 25) if the prompt states I passed or landed on START.
    4. Subtract `Rent due` if landing on an opponent's property.
    5. Subtract `Purchase price` if buying the property.
  - Formula:
    $$\text{New Balance} = \text{Last Balance} + \text{Received Rent} + \text{Salary} - \text{Rent Paid} - \text{Purchase Price}$$
  - Declare `[balance: N]` with the exact resulting integer.

### Response Format
- Provide minimal or no reasoning.
- Output the three required tokens on separate lines:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`