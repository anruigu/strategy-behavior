---
game: ref_estate
model: gemini-flash
condition: win
seed: 9
round: 1
chars: 1267
---
# Estate Strategy Playbook

## Cash Flow & Accounting
- Start with the previous turn's declared balance.
- Add any salary collected if passing or landing on START (+25 or specified salary).
- Add all incoming rent payments listed in the prompt as received from other investors since the last turn.
- Subtract any rent due to an opponent for landing on their property: declare `[pay: N to P<k>]`. If landing on an unowned tile, START, or my own property, declare `[pay: none]`.
- Subtract the property purchase price if deciding to buy: declare `[buy: yes]`, otherwise `[buy: no]`.
- Set `[balance: N]` strictly equal to: `Previous Balance + Salary + Incoming Rent - Rent Paid - Property Cost`.

## Property Purchasing
- Buy unowned properties whenever affordable while maintaining a safe cash buffer for expected rent payments on the circuit.
- Prioritize acquiring deeds early; buying properties converts cash into equal deed value for final scoring while generating recurring rental income.
- When cash is strictly lower than the purchase price of the landed property, choose `[buy: no]`.

## Response Format
- Always output all three tokens at the end of the settlement:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]`