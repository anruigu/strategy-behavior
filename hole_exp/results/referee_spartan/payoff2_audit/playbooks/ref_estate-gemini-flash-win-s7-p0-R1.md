---
game: ref_estate
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1402
---
# Estate Playbook

## Cash Accounting
- When computing my ending balance each turn, I follow this exact order:
  1. Start with `last declared balance`.
  2. Add any income received from other investors since my last turn (noted in prompt).
  3. Add salary (+25) if I passed or landed on START.
  4. Subtract rent paid if landing on an opponent's property.
  5. Subtract purchase price if buying an unowned property.
- Always double-check that every line item (income received, salary, rent, purchase) is accounted for before outputting `[balance: N]`.

## Rent Payments
- When landing on an opponent's property, output `[pay: N to P<k>]` where `N` is the full rent owed and `<k>` is the owner's investor index.
- When landing on an unowned tile, START, or my own property, output `[pay: none]`.

## Property Purchasing
- When landing on an unowned property:
  - If my available cash after salary/rent covers the full purchase price, output `[buy: yes]` and deduct the cost from my declared balance. Prioritizing property acquisition yields deed value toward final score plus rental income.
  - If cash is insufficient to buy, output `[buy: no]`.
- When landing on an already-owned property or START, always output `[buy: no]`.

## Output Format
- End every turn with all three required tokens on separate lines:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`