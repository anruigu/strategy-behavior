---
game: ref_estate
model: gemini-flash
condition: win
seed: 2
round: 3
chars: 1529
---
### Balance Accounting & Cash Flow
- Calculate available cash at the start of every turn using the exact formula:
  $$\text{Available Cash} = \text{Previous Declared Balance} + \text{Salary (if passed/landed START, usually +25)} + \text{Transfers Received Since Last Turn}$$
- Check both the explicit notice line ("Since your last turn you received N...") and the prompt's recent transfer ledger for incoming payments (`investor X paid Y to investor <my_id>`) to ensure all received funds are added to available cash before applying debits.

### Settling Rent & Purchases
- When landing on an opponent's property:
  - If available cash $\ge$ rent due $R$: output `[pay: R to P<k>]` and deduct $R$ from cash.
  - If available cash $C < R$: pay all remaining cash: output `[pay: C to P<k>]` and set cash to 0.
  - Always output `[buy: no]`.
- When landing on an unowned property:
  - Output `[pay: none]`.
  - If available cash $\ge$ purchase price $P$: buy the property by outputting `[buy: yes]` and deducting $P$ from cash.
  - If available cash $< P$: do not buy, output `[buy: no]`.
- When landing on START or a property I already own:
  - Output `[pay: none]`.
  - Output `[buy: no]`.

### Formatting Output
- Keep reasoning brief (1–2 concise sentences).
- Always terminate every turn response with the exact three bracketed tokens in order:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]` (reflecting the exact ending cash balance after all credits, rent debits, and purchases)