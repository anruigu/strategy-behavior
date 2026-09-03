---
game: ref_estate
model: gemini-flash
condition: win
seed: 5
round: 2
chars: 1436
---
# Playbook: Estate

### Bookkeeping and Balance Calculations
- When calculating my new balance each turn, I will strictly follow this arithmetic:
  $$\text{New Balance} = \text{Last Declared Balance} + \text{Cash Received from Others} + \text{Salary (if passed/landed on START)} - \text{Rent Paid} - \text{Property Purchase Price}$$
- When parsing incoming cash, I will check the prompt explicitly for "Since your last turn you received $X$ from other investors" and add $X$ into the starting cash pool for that turn.
- If the turn text states that I passed or landed on START, I will add the salary ($25$) to my balance.

### Paying Rent
- When I land on a property owned by another investor, I will declare `[pay: <rent> to P<owner_id>]`.
- When I land on an unowned property, a property I own, or START, I will declare `[pay: none]`.

### Purchasing Property
- When I land on an unowned property and have sufficient funds (after adding incoming cash/salary and subtracting any due rent), I will buy it by declaring `[buy: yes]`, prioritizing property acquisition to generate ongoing rental income and build total net worth.
- When I land on an owned tile, START, or an unowned property I cannot afford, I will declare `[buy: no]`.

### Output Format
- I will keep any reasoning to a minimum and always format the response to end with the required three tokens on separate lines:
  ```
  [pay: ...]
  [buy: ...]
  [balance: ...]
  ```