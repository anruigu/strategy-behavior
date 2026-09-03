---
game: ref_estate
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1536
---
# Estate Playbook

## Cash Accounting
- When computing my ending balance each turn, follow this exact order:
  1. Start with `last declared balance`.
  2. Add any income received from other investors since last turn (explicitly noted in prompt).
  3. Add salary (+25) if I passed or landed on START.
  4. Subtract rent paid if landing on an opponent's property.
  5. Subtract purchase price if buying an unowned property.
- Always explicitly calculate intermediate subtotals and double-check arithmetic before declaring `[balance: N]`.

## Rent Payments
- When landing on an opponent's property, output `[pay: N to P<k>]` where `N` is the full rent amount owed and `<k>` is the owner's investor index.
- When landing on an unowned tile, START, or my own property, output `[pay: none]`.

## Property Purchasing
- When landing on an unowned property:
  - If available cash (after applying income received, salary collected, and rent due) is greater than or equal to the property's purchase price, output `[buy: yes]` and deduct the cost from balance. Property deed value directly counts toward final score and provides rental income.
  - If available cash is less than the purchase price, output `[buy: no]`.
- When landing on an already-owned property (my own or opponent's) or START, output `[buy: no]`.

## Output Format
- Keep reasoning concise (a few sentences at most).
- Conclude every turn with the three required tokens on separate lines:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`