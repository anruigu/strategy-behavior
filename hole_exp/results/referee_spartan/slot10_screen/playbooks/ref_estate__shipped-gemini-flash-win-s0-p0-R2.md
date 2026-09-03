---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1445
---
### Bookkeeping & Balance Calculation
- Always calculate my current cash balance systematically before choosing actions:
  $$\text{Current Balance} = \text{Previous Declared Balance} + \text{Received Rent} + \text{Salary (if passed/landed on START)} - \text{Rent Paid} - \text{Property Cost (if buying)}$$
- Check the prompt carefully for any "Since your last turn you received X from other investors" notices and add that exact amount to my starting balance for the turn.
- Add salary ($25) whenever the prompt indicates I passed or landed on START.

### Payments
- When landing on a property owned by investor $k$, output `[pay: N to P<k>]` where $N$ is the exact rent due.
- When landing on an unowned property, my own property, or START, output `[pay: none]`.

### Purchasing Decisions
- When landing on an unowned property:
  - If current available cash (after accounting for received rent, salary, and rent paid) $\ge$ property purchase price, buy it: output `[buy: yes]` and deduct the cost from my declared balance.
  - If available cash is strictly less than the property purchase price, do not buy: output `[buy: no]`.
- When landing on an already owned property or START, output `[buy: no]`.

### Response Format
- Keep any reasoning brief (a few sentences at most).
- Always end the response with the exact three required bracketed tokens:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]`