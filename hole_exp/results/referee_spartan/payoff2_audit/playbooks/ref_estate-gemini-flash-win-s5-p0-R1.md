---
game: ref_estate
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1411
---
### Strategy and Accounting Rules

- **Buying Properties**: Always buy an unowned property whenever I land on it and have enough cash on hand (cash $\ge$ price). Properties retain their full purchase price toward the final net worth and generate recurring rent from opponents.
- **Handling Rent Payments**:
  - When landing on an opponent's tile, declare `[pay: N to P<k>]` with the exact rent amount and the owner's player ID.
  - When landing on an unowned property, an owned property belonging to me, or START, declare `[pay: none]`.
- **Handling Purchases**:
  - Declare `[buy: yes]` if buying an unowned property.
  - Declare `[buy: no]` if the property is already owned, if I cannot afford it, or if on START.
- **Calculating Declared Balance**:
  - Always calculate the new balance strictly using the formula:
    $$\text{New Balance} = \text{Last Declared Balance} + \text{Received Rent} + \text{Salary (if passed/landed on START)} - \text{Rent Paid} - \text{Purchase Price (if bought)}$$
  - Check the prompt for any salary note (`passed START`) and incoming rent statement (`Since your last turn you received X from other investors`) before finalizing the math.
  - Declare `[balance: N]` with the resulting exact amount.

### Response Format
- Provide minimal or no reasoning.
- Always output the three required tokens cleanly on separate lines:
  - `[pay: ...]`
  - `[buy: ...]`
  - `[balance: ...]`