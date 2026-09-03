---
game: ref_estate
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1329
---
# ESTATE Playbook

## Cash Balance Accounting
- Always calculate my new balance using the strict formula:
  $$\text{New Balance} = \text{Last Declared Balance} + \text{Salary (if passed/landed START)} + \text{Rent Received} - \text{Rent Paid} - \text{Purchase Price (if buying)}$$
- Always check the prompt for "Since your last turn you received $X$ from other investors" and add that amount to my balance calculation before settling.
- When I pass or land on START, add the exact salary specified in the rules (e.g., $+25$).

## Rent Settlement
- When landing on a property owned by another investor $k$:
  - Format the payment token as `[pay: N to P<k>]`, using the exact rent due.
  - Subtract $N$ from my balance.
- When landing on an unowned property, my own property, or START, output `[pay: none]`.

## Purchasing Strategy
- When landing on an unowned property:
  - If available cash (including recent income and salary) $\ge$ purchase price, choose `[buy: yes]`, pay the purchase price, and subtract it from my balance.
  - If available cash < purchase price, choose `[buy: no]`.
- When landing on an owned property or START, choose `[buy: no]`.

## Response Formatting
- Ensure my reply strictly ends with the three required tokens on separate lines:
  ```
  [pay: <payment>]
  [buy: yes|no]
  [balance: <integer>]
  ```