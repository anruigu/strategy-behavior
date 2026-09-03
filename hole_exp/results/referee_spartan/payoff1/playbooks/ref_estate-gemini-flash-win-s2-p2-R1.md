---
game: ref_estate
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1440
---
### Balance Accounting & Cash Flow
- Calculate available cash at the start of every turn using the exact order:
  $$\text{Starting Cash} = \text{Previous Declared Balance} + \text{Salary (if passed/landed START)} + \text{Transfers Received Since Last Turn}$$
- Track incoming rent payments listed in the prompt's transfer ledger: if another player paid me since my last turn, add that full amount to my starting cash before determining payments or purchases.

### Settling Rent & Purchases
- When landing on an opponent's property:
  - If my available cash is greater than or equal to the rent due $R$, output `[pay: R to P<k>]` and deduct $R$ from cash.
  - If my available cash $C$ is less than $R$, pay all remaining cash: output `[pay: C to P<k>]` and set cash to 0.
  - Always output `[buy: no]`.
- When landing on an unowned property:
  - Output `[pay: none]`.
  - If available cash $\ge$ purchase price $P$, buy the property: output `[buy: yes]` and deduct $P$ from balance.
  - If available cash $< P$, do not buy: output `[buy: no]`.
- When landing on START or an owned tile with no rent due:
  - Output `[pay: none]`.
  - Output `[buy: no]`.

### Formatting Output
- Always close every turn response with the three required tags in exact sequence:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]` (reflecting the exact ending cash balance after all credits, rent debits, and purchases)