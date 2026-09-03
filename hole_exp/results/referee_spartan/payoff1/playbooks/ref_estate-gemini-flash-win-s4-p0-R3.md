---
game: ref_estate
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1313
---
# Playbook: Estate

### Bookkeeping and Accounting Rules
- Calculate the available balance before current-turn decisions as:
  $$\text{Starting Cash} = \text{Last Declared Balance} + \text{Inter-turn Receipts} + (\text{Salary of 25 if passed/landed START else } 0)$$
- Rent and Payment:
  - If landing on an opponent's property, deduct rent: $\text{Cash after Rent} = \text{Starting Cash} - \text{Rent}$. Emit `[pay: <Rent> to P<OwnerID>]`.
  - If landing on an unowned property, START, or my own property: no rent due. Emit `[pay: none]`.
- Purchasing:
  - If on an unowned property and choosing to buy: deduct price ($\text{Final Balance} = \text{Cash after Rent} - \text{Price}$) and emit `[buy: yes]`.
  - Otherwise: $\text{Final Balance} = \text{Cash after Rent}$ and emit `[buy: no]`.
- Always end with all three required bracketed tokens:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`

### Purchasing Strategy
- Unowned properties retain 100% of purchase price in total net worth evaluation ($\text{Net Worth} = \text{Cash} + \sum \text{Deed Prices}$) and generate future rent.
- Always buy unowned properties whenever affordable ($\text{Price} \le \text{Cash after Rent}$).
- Emit `[buy: no]` when on owned properties, on START, or when funds are insufficient.