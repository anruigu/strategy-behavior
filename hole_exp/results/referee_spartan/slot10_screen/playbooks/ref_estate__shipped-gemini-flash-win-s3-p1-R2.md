---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1418
---
### Playbook: Estate

- **Step 1: Calculate Starting Cash for the Turn**
  - Start with my last declared balance.
  - If the prompt states "Since your last turn you received X from other investors", add `X` to the balance.
  - If the prompt indicates I passed or landed on START, add the salary amount (+25) to the balance.

- **Step 2: Settle Rent**
  - When landing on a property owned by another investor, deduct the specified rent from my balance and emit `[pay: <rent> to P<owner_id>]`.
  - When landing on START, my own property, or an unowned property, emit `[pay: none]`.

- **Step 3: Buying Decisions**
  - When landing on an unowned property and my available balance (after accounting for received transfers, salary, and any rent) is greater than or equal to the purchase price, choose `[buy: yes]` and deduct the purchase price from my balance. Property adds directly to final score value and generates rent income.
  - When landing on an already owned property, START, or when balance is strictly less than the purchase price, choose `[buy: no]`.

- **Step 4: Format Response**
  - Compute the final balance strictly as:
    `Final Balance = Last Declared Balance + Incoming Transfers + Salary (if passed/landed START) - Rent Paid - Property Cost (if bought)`.
  - Always conclude the response with the three exact tokens in order:
    `[pay: ...]`
    `[buy: ...]`
    `[balance: <final_calculated_cash>]`