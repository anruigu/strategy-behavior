---
game: ref_estate
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1596
---
### Strategy and Decision Rules

- **Buying Properties**:
  - When landing on an unowned property during early-to-mid laps (laps 1–4) and cash allows, choose `[buy: yes]` to secure ongoing rental income and add property value to the final net worth score.
  - When cash is insufficient to cover the purchase price or when buying would leave cash at zero with dangerous upcoming rent hazards, choose `[buy: no]`.
  - When landing on a property that is already owned or on START, always output `[buy: no]`.

- **Paying Rent**:
  - When landing on an opponent's property, identify the owner index (`P<k>`) and rent amount from the prompt, and output `[pay: <amount> to P<k>]`.
  - When landing on an unowned tile, START, or a self-owned property, output `[pay: none]`.

- **Accounting and Balance Calculation**:
  - Compute the new balance strictly according to:
    $$\text{New Balance} = \text{Previous Balance} + \text{Salary (if passed/landed on START)} + \text{Rental Income Received} - \text{Rent Paid} - \text{Property Purchase Price (if bought)}$$
  - Standard salary is 25 whenever the prompt states you passed or landed on START.
  - Check the prompt carefully for lines stating rent received from other investors since the last turn and ensure this amount is added to the balance.
  - Always output the exact updated cash total in `[balance: N]`.

- **Response Formatting**:
  - Keep reasoning brief (or omit extra text) and format the reply with all three required tokens in exact order:
    1. `[pay: N to P<k>]` or `[pay: none]`
    2. `[buy: yes]` or `[buy: no]`
    3. `[balance: N]`