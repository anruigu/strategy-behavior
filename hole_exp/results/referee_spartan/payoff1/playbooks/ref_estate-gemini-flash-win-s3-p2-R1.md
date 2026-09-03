---
game: ref_estate
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1369
---
# Estate Playbook

- **Accounting & Balance Calculation:**
  - Start with `last declared balance`.
  - Add `salary` (25) if I passed or landed on START this turn.
  - Add any income listed under "Since your last turn you received X from other investors."
  - Subtract rent owed if landing on an opponent-owned property (`[pay: N to P<k>]`), otherwise use `[pay: none]`.
  - Subtract property price if buying (`[buy: yes]`), otherwise `[buy: no]`.
  - Compute and declare the final exact cash balance as `[balance: N]`.

- **Rent Obligations:**
  - When landing on an opponent's property, pay the full rent specified via `[pay: N to P<k>]`.
  - When landing on an unowned property, START, or my own property, output `[pay: none]`.

- **Property Acquisition:**
  - Whenever landing on an unowned property, evaluate affordability after accounting for any incoming cash (salary + received rent) and rent owed.
  - If current available cash $\ge$ purchase price, choose `[buy: yes]` unless it leaves insufficient cash for unavoidable upcoming liabilities. Properties add their full purchase value to final score while generating rental income.
  - If available cash < purchase price, choose `[buy: no]`.

- **Formatting:**
  - Always end every turn response with the exact three required tokens on separate lines:
    - `[pay: ...]`
    - `[buy: ...]`
    - `[balance: ...]`