---
game: ref_estate
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1553
---
### Strategy and Decision Rules

- **Buying Properties**:
  - When landing on an unowned property and cash on hand is strictly greater than or equal to the purchase price, choose `[buy: yes]` to secure rental income and preserve net worth (property purchase price counts 100% towards final score).
  - When cash is insufficient to cover the purchase price, choose `[buy: no]`.
  - When landing on a property that is already owned or on START, always output `[buy: no]`.

- **Paying Rent**:
  - When landing on an opponent's property, identify the owner index (`P<k>`) and rent amount from the prompt, and output `[pay: <amount> to P<k>]` (e.g., `[pay: 14 to P0]`).
  - When landing on an unowned tile, START, or a self-owned property, output `[pay: none]`.

- **Accounting and Balance Calculation**:
  - Compute the new balance strictly according to:
    $$\text{New Balance} = \text{Previous Balance} + \text{Salary (if collected)} + \text{Rental Income Received} - \text{Rent Paid} - \text{Property Purchase Price (if bought)}$$
  - Add salary (typically 25) whenever the prompt indicates you passed or landed on START.
  - Check the prompt carefully for lines stating: *"Since your last turn you received X from other investors"* and add $X$ to the balance.
  - Verify every addition and subtraction before outputting `[balance: N]`.

- **Response Formatting**:
  - Keep reasoning minimal or zero, and output all three required tokens in exact order:
    1. `[pay: N to P<k>]` or `[pay: none]`
    2. `[buy: yes]` or `[buy: no]`
    3. `[balance: N]`