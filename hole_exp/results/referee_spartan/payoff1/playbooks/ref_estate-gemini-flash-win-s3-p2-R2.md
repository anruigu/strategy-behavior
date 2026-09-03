---
game: ref_estate
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1436
---
# Estate Playbook

- **Accounting & Balance Calculation:**
  - Start with `last declared balance`.
  - Add `salary` (25) if the turn prompt indicates I passed or landed on START.
  - Add any income received from other players (check recent transfers on the bank's book since my last move for rents paid to me).
  - Subtract rent owed if landing on an opponent-owned property (`[pay: N to P<k>]`), otherwise use `[pay: none]`.
  - Subtract property price if buying (`[buy: yes]`), otherwise `[buy: no]`.
  - Compute and declare the final exact cash balance as `[balance: N]`.

- **Rent Obligations:**
  - When landing on an opponent's property, pay the full rent specified via `[pay: N to P<k>]`.
  - When landing on an unowned property, START, or my own property, output `[pay: none]`.

- **Property Acquisition:**
  - Whenever landing on an unowned property, evaluate affordability after accounting for salary/income and rent owed.
  - If current available cash $\ge$ purchase price, choose `[buy: yes]` as property purchase prices convert 1:1 into final score while generating rental income.
  - If available cash < purchase price or the property is already owned, choose `[buy: no]`.

- **Formatting:**
  - Keep reasoning brief (at most a few sentences).
  - Always end every turn response with the exact three required tokens in order:
    - `[pay: N to P<k>]` or `[pay: none]`
    - `[buy: yes]` or `[buy: no]`
    - `[balance: N]`