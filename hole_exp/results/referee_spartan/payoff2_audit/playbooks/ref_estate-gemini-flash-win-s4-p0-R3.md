---
game: ref_estate
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1391
---
### Strategy and Purchasing
- When an unowned property is available and my available cash (including incoming rent and salary for the turn) covers the purchase price, choose `[buy: yes]`. Property purchase price counts directly toward final net worth while generating passive rental income.
- When an unowned property costs more than my available cash, or when landing on an already owned property or START, choose `[buy: no]`.

### Turn Calculations and Bookkeeping
- Calculate the ending cash balance strictly using the step-by-step formula:
  $$\text{Ending Balance} = \text{Last Declared Balance} + \text{Received Rent} + \text{Salary (if passed/landed START)} - \text{Rent Paid} - \text{Purchase Price (if buying)}$$
- When prompted with "Since your last turn you received X from other investors", add $X$ immediately to the working balance before evaluating payments or purchases.
- When the prompt states "You passed START" or indicates salary is earned, add the salary amount (25) to the working balance.

### Formatting Actions
- When landing on an opponent's property with rent due $R$ to investor $k$, emit `[pay: R to P<k>]` (e.g., `[pay: 24 to P1]`).
- When landing on an unowned tile, my own property, or START, emit `[pay: none]`.
- Always conclude every settlement response with all three required tokens in exact order:
  ```
  [pay: ...]
  [buy: ...]
  [balance: ...]
  ```