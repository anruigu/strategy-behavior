---
game: ref_estate
model: gemini-flash
condition: win
seed: 9
round: 2
chars: 1366
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
- Buy unowned properties whenever available and affordable (cash after salary, incoming rent, and rent owed is at least the purchase price).
- Property purchases convert cash to deed value 1:1 without lowering total net worth while generating recurring rental income from opponents.
- Never choose `[buy: yes]` if available cash before purchase is strictly less than the property cost.
- Output `[buy: no]` whenever landing on START or an already owned property.

## Response Format
- Keep reasoning concise and output all three tokens strictly in order:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]`