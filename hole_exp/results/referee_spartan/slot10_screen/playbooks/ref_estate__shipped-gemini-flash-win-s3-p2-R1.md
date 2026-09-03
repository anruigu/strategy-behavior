---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1264
---
# Playbook: Estate

### Bookkeeping and Cash Calculations
- On every turn, compute available cash before decisions: `Available Cash = Last Declared Balance + Rent Received Since Last Turn + (Passed START ? Salary : 0)`.
- When rent is owed on the landed tile:
  - If owned by another player `Pk`, output `[pay: <rent> to P<k>]` and subtract rent from available cash.
  - If unowned or owned by myself, output `[pay: none]`.
- When buying a property:
  - If the tile is unowned and `Available Cash after Rent >= Property Price`, prioritize buying: output `[buy: yes]` and subtract the price from remaining cash.
  - Otherwise, output `[buy: no]`.
- Output `[balance: <final remaining cash>]` representing exact post-turn cash on hand.

### Property Acquisition Strategy
- Always buy unowned properties whenever affordable, especially in early and middle laps; deed values fully count toward final net worth and generate passive rent income on opponent landings.
- Never declare `[buy: yes]` if available cash after rent is strictly less than the property purchase price.

### Turn Output Formatting
- End every settle turn with the three exact bracketed tokens in sequence:
  1. `[pay: N to Pk]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]`