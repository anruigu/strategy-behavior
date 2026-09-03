---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1305
---
### Bookkeeping & Balance Calculation
- Always calculate my current cash balance systematically before choosing actions:
  $$\text{Current Balance} = \text{Previous Balance} + \text{Received Rent} + \text{Salary (if passed/landed on START)} - \text{Rent Paid} - \text{Property Cost (if buying)}$$
- Check the prompt carefully for any "Since your last turn you received $X$" notices and add them to my balance.
- Add salary ($25) whenever the prompt indicates I passed or landed on START.

### Payments
- When landing on a property owned by investor $k$, output `[pay: <rent> to P<k>]`.
- When landing on an unowned property, my own property, or START, output `[pay: none]`.

### Purchasing Decisions
- When landing on an unowned property:
  - If current available cash (after rent and salary) is greater than or equal to the property's purchase price, buy it: output `[buy: yes]` and deduct the cost from balance.
  - If current available cash is less than the property's purchase price, do not buy: output `[buy: no]`.
- When landing on an owned property, START, or an unaffordable property, output `[buy: no]`.

### Response Format
- Always output exactly the three required tokens at the end of the response:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]`