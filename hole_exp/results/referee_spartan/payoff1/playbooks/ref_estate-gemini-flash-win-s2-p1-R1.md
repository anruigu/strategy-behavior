---
game: ref_estate
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1348
---
# Playbook: Estate

### Bookkeeping & Cash Accounting
- On every turn, compute cash balance following this exact sequence:
  1. Start with `last declared balance`.
  2. If notified "Since your last turn you received $R$ from other investors", add $R$.
  3. If "You passed START, so you may collect your salary of $S$" or landed on START, add $S$.
  4. If rent $P$ is due to investor $k$, subtract $P$ and output `[pay: P to Pk]`. Otherwise output `[pay: none]`.
  5. If deciding to buy a property with purchase price $C$, subtract $C$ and output `[buy: yes]`. Otherwise output `[buy: no]`.
  6. Output the resulting number as `[balance: N]`.

### Property Purchasing Decisions
- When landing on an unowned property:
  - If available cash after rent and salary is strictly greater than the property cost, and buying leaves enough cash to avoid guaranteed immediate bankruptcy from known rents, choose `[buy: yes]`.
  - Properties preserve net worth at a 1:1 ratio (cost adds directly to final score) and generate passive rent income from opponents.
- When landing on an already owned property, an unowned property I cannot afford, or my own property, output `[buy: no]`.

### Output Formatting
- Always include all three mandatory tokens in exact formatting:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`