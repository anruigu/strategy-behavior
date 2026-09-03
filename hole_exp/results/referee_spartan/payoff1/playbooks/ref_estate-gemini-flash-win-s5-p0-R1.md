---
game: ref_estate
model: gemini-flash
condition: win
seed: 5
round: 1
chars: 1335
---
# Playbook: Estate

### Bookkeeping and Balance Calculations
- When calculating my new balance each turn, I will strictly follow this order of operations:
  $$\text{New Balance} = \text{Last Declared Balance} + \text{Cash Received from Others} + \text{Salary (if passed/landed on START)} - \text{Rent Paid} - \text{Property Purchase Price}$$
- When parsing incoming cash, I will check the prompt explicitly for "Since your last turn you received $X$ from other investors" and add $X$ before settling rent or purchases.
- If I passed or landed on START during the turn, I will add the salary ($25$) to my balance.

### Paying Rent
- When I land on a property owned by another investor, I will declare `[pay: <rent> to P<owner_id>]`.
- When I land on an unowned property, a property I own, or START, I will declare `[pay: none]`.

### Purchasing Property
- When I land on an unowned property and have sufficient funds after accounting for any rent and salary, I will buy it by declaring `[buy: yes]`, prioritizing early asset accumulation to collect rental income throughout the 6 laps.
- When I land on an owned tile, START, or an unowned property I cannot afford, I will declare `[buy: no]`.

### Output Format
- I will always conclude every turn with the exact three-line format:
  ```
  [pay: ...]
  [buy: ...]
  [balance: ...]
  ```