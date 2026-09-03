---
game: ref_estate
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1671
---
# Estate Playbook

- **Accounting & Balance Calculation:**
  - Start with `last declared balance`.
  - Add `salary` (25) if the turn prompt explicitly indicates passing or landing on START.
  - Add any income received from other players (check explicitly stated "Since your last turn you received X" and review recent transfers on the bank's book for rents paid to my investor ID).
  - Subtract rent owed if landing on an opponent-owned property (`[pay: N to P<k>]`), otherwise declare `[pay: none]`.
  - Subtract property price if purchasing (`[buy: yes]`), otherwise declare `[buy: no]`.
  - Compute and declare the final exact cash balance as `[balance: N]`.

- **Rent Obligations:**
  - When landing on an opponent's property, pay the exact rent specified via `[pay: N to P<k>]` (where `<k>` is the owner's investor index).
  - When landing on an unowned property, START, or my own property, output `[pay: none]`.

- **Property Acquisition:**
  - Whenever landing on an unowned property, evaluate affordability after accounting for any salary collected and income received.
  - If current available cash $\ge$ purchase price, choose `[buy: yes]` because property purchase prices contribute 100% to final net worth while generating recurring rental income.
  - If available cash < purchase price or the property is already owned (by anyone), choose `[buy: no]`.

- **Formatting:**
  - Keep reasoning brief (at most 2-4 sentences showing the explicit math breakdown).
  - Always conclude every turn response with the exact three required tokens in order on separate lines:
    - `[pay: N to P<k>]` or `[pay: none]`
    - `[buy: yes]` or `[buy: no]`
    - `[balance: N]`