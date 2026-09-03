---
game: ref_estate
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1409
---
### Accounting & Balance Updates
- When starting a turn, compute the available balance before decisions: `Available Cash = Last Declared Balance + (Rent Received since last turn) + (Salary if passed/landed on START)`.
- Explicitly check the turn prompt for statements like "Since your last turn you received X from other investors" and "You passed START, so you may collect your salary of Y" to include in the available balance.
- When rent is owed on a landed property owned by another player `Pk`, specify `[pay: <rent> to P<k>]` and subtract the rent from available cash.
- When no rent is owed (unowned tile, START, or own property), specify `[pay: none]`.

### Purchasing Decisions
- When landing on an unowned property:
  - If `Available Cash - Rent Owed >= Property Price`, choose `[buy: yes]` and subtract the purchase price from cash: `Final Balance = Available Cash - Rent Owed - Property Price`.
  - If funds are insufficient, choose `[buy: no]` and `Final Balance = Available Cash - Rent Owed`.
- Always prioritize buying unowned properties whenever affordable, as property value counts 1:1 toward final net worth and generates recurring rent.

### Output Formatting
- End every turn with the exact three tokens in order:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]` (reflecting the exact final cash after all additions and subtractions this turn).