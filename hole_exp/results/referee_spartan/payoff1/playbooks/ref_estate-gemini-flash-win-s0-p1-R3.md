---
game: ref_estate
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1350
---
# Estate Playbook

## Balance Tracking & Cash Accounting
- Calculate current turn balance starting strictly from `last declared balance`:
  - Add salary (+25) if I passed or landed on START this turn.
  - Add any income explicitly stated under "Since your last turn you received X from other investors".
  - Subtract rent due to another player if landing on an owned property.
  - Subtract purchase price if buying an unowned property this turn.
- Formula: `final_balance = last_declared_balance + salary_collected + rent_received - rent_paid - purchase_price`.

## Action Tokens & Formatting
- **Rent / Payments**:
  - If landing on an unowned tile, START, or my own property: output `[pay: none]`.
  - If landing on a property owned by investor $k$ with rent $R$: output `[pay: R to Pk]`.
- **Purchases**:
  - If landing on an unowned property and cash after collecting salary/rents is sufficient to cover the purchase price: output `[buy: yes]`.
  - If landing on an owned property, START, or an unowned property I cannot afford: output `[buy: no]`.
- **Declared Balance**:
  - Output `[balance: final_balance]` matching the exact net balance after all additions and deductions for the turn.
- Always output all three tokens exactly at the end of each turn in the required order: `[pay: ...]`, `[buy: ...]`, `[balance: ...]`. Keep reasoning brief.