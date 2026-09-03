---
game: ref_estate
model: gemini-flash
condition: win
seed: 1
round: 3
chars: 1532
---
### Accounting & Balance Updates
- When starting a turn, compute the available balance before any decisions:
  `Available Cash = Last Declared Balance + (Rent Received since last turn) + (Salary if passed/landed on START)`.
- Always check the prompt text for lines explicitly stating "Since your last turn you received X from other investors" and "You passed START, so you may collect your salary of Y" to include them in the available balance.
- When rent is owed on a landed property owned by another player `Pk`:
  - Output `[pay: <rent> to P<k>]`.
  - Deduct the rent from available cash.
- When no rent is owed (unowned tile, START, or own property), output `[pay: none]`.

### Purchasing Decisions
- When landing on an unowned property:
  - If `Available Cash - Rent Owed >= Property Price`, choose `[buy: yes]` and deduct the purchase price: `Final Balance = Available Cash - Rent Owed - Property Price`.
  - If funds are insufficient, choose `[buy: no]` and `Final Balance = Available Cash - Rent Owed`.
- Always prioritize buying unowned properties whenever affordable, as property value counts 1:1 toward final net worth and generates recurring rent.
- On non-purchasable tiles (e.g., START or properties already owned by anyone), always output `[buy: no]`.

### Output Formatting
- End every turn with the exact three tokens in order:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]` (reflecting the exact final cash balance after all additions and subtractions for the turn).