---
game: ref_estate
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1432
---
# ESTATE Playbook

## Cash Balance Accounting
- Always calculate my new balance using the strict formula:
  $$\text{New Balance} = \text{Last Declared Balance} + \text{Salary (if passed/landed START)} + \text{Rent Received} - \text{Rent Paid} - \text{Purchase Price (if buying)}$$
- Always check the prompt for "Since your last turn you received $X$ from other investors" and explicitly add that amount to my balance calculation before settling.
- When I pass or land on START, add the exact salary specified in the rules (e.g., $+25$).

## Rent Settlement
- When landing on a property owned by investor $k$:
  - Format the payment token as `[pay: N to P<k>]`, using the exact rent due.
  - Subtract $N$ from my balance.
- When landing on an unowned property, my own property, or START:
  - Format the payment token as `[pay: none]`.

## Purchasing Strategy
- When landing on an unowned property:
  - If available cash (after adding salary and received rent) $\ge$ purchase price, choose `[buy: yes]`, pay the purchase price, and subtract it from my balance.
  - If available cash < purchase price, choose `[buy: no]`.
- When landing on an owned property or START, choose `[buy: no]`.

## Response Formatting
- Keep the reasoning brief (1–3 sentences explicitly stating the math).
- Ensure my reply strictly ends with the three required tokens on separate lines:
  ```
  [pay: <payment>]
  [buy: yes|no]
  [balance: <integer>]
  ```