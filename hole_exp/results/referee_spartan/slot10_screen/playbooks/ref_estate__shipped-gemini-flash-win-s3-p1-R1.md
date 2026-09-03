---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1218
---
### Playbook: Estate

- **Step 1: Check Salary**
  - When the turn prompt indicates I passed or landed on START, add the salary amount (+25) to my current declared balance before calculating other expenses.

- **Step 2: Settle Rent**
  - When landing on a property owned by another investor, deduct the specified rent from my balance and emit `[pay: <rent> to P<owner_id>]`.
  - When landing on START, my own property, or an unowned property, emit `[pay: none]`.

- **Step 3: Buying Decisions**
  - When landing on an unowned property and my balance (after salary and rent) is greater than or equal to the purchase price, choose `[buy: yes]` and deduct the purchase price from my balance. Property adds directly to final score value and generates rent income.
  - When landing on an owned property, START, or when my balance is strictly less than the property's purchase price, choose `[buy: no]`.

- **Step 4: Format Response**
  - Compute the final balance strictly as: `New Balance = Previous Balance + Salary (if passed START) - Rent Paid - Property Cost (if bought)`.
  - Always conclude the response with the three exact tokens in order:
    `[pay: ...]`
    `[buy: ...]`
    `[balance: <final_calculated_cash>]`