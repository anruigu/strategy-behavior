---
game: hf_estate_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1130
---
### Balance Tracking & Accounting
- When settling my turn, calculate the new cash balance strictly using:  
  `New Balance = (Last Declared Balance) + (Income Received Since Last Turn) + (25 if START passed/landed) - (Rent Paid) - (Property Cost if Bought)`
- When rent is owed to an opponent, declare `[pay: <amount> to P<owner_id>]`. If on an unowned tile, my own tile, or START, declare `[pay: none]`.
- Always verify the balance arithmetic precisely. Opponents inspect declarations and incorrect filings result in a 25-point penalty.

### Property Acquisition
- When landing on an unowned property, buy it (`[buy: yes]`) whenever `(Available Cash) >= (Purchase Price)`. Converting cash to property preserves total net worth for final scoring while building recurring rent income.
- When cash is insufficient to purchase the unowned property, or the tile is already owned, output `[buy: no]`.

### Response Format
- Keep reasoning to at most two concise sentences stating the balance arithmetic.
- Always conclude responses with the three mandatory tags in exact sequence:
  ```
  [pay: ...]
  [buy: ...]
  [balance: ...]
  ```