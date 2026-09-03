---
game: ref_estate
model: gemini-flash
condition: win
seed: 9
round: 3
chars: 1522
---
# Estate Strategy Playbook

## Cash Flow & Accounting
- Start with the previous turn's declared balance (starts at 200 on Lap 1 unless specified otherwise).
- Add salary collected if passing or landing on START (+25 or specified salary amount).
- Add all incoming rent received from other investors since the last turn as stated in the prompt.
- Subtract any rent due to an opponent for landing on their property: declare `[pay: N to P<k>]`. If landing on an unowned tile, START, or my own property, declare `[pay: none]`.
- Subtract the property purchase price if purchasing: declare `[buy: yes]`, otherwise `[buy: no]`.
- Compute final cash strictly as: `Previous Balance + Salary + Incoming Rent - Rent Paid - Property Cost`. Declare this value in `[balance: N]`.

## Property Purchasing Decisions
- Always buy unowned properties whenever affordable (`Available Cash = Previous Balance + Salary + Incoming Rent - Rent Paid >= Purchase Price`).
- Property deeds maintain 1:1 book value toward total net worth and generate recurring rent from opponents.
- Never choose `[buy: yes]` if available cash is insufficient to cover the property cost.
- Declare `[buy: no]` whenever landing on START, an unowned property I cannot afford, or any tile that is already owned (by myself or an opponent).

## Response Format
- Keep any reasoning concise (at most 2-3 lines of arithmetic).
- Conclude strictly with the three tokens in order:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]`