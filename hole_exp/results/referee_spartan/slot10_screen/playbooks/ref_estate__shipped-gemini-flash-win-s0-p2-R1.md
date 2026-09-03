---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1167
---
# Playbook: ESTATE

- **Rent Calculation & Payment**:
  - When landing on a tile owned by another investor `Pk`, emit `[pay: <rent> to P<k>]`.
  - When landing on an unowned tile, START, or a property I own, emit `[pay: none]`.

- **Purchasing Decisions**:
  - When landing on an unowned property that I can afford (current balance + salary + incoming rent - outgoing rent $\ge$ property price), emit `[buy: yes]`.
  - When landing on an owned property, START, or an unowned property I cannot afford, emit `[buy: no]`.

- **Balance Accounting**:
  - Calculate `balance` strictly as:
    $$\text{New Balance} = \text{Previous Balance} + \text{Salary (if passed/landed on START)} + \text{Incoming Rent Received} - \text{Outgoing Rent Paid} - \text{Purchase Price (if buying)}$$
  - Check the bank transfer report and prompt text carefully for any salary bonuses or incoming rent payments received between turns and add them in before subtracting purchase costs.
  - Always output `[balance: <New Balance>]`.

- **Formatting**:
  - Ensure every turn output concludes with the three exact bracketed tokens:
    ```
    [pay: ...]
    [buy: ...]
    [balance: ...]
    ```