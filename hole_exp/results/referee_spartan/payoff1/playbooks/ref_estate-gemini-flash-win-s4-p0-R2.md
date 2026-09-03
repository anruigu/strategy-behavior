---
game: ref_estate
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1472
---
# Playbook: Estate

### Bookkeeping and Accounting Rules
- Calculate the starting available balance before current-turn decisions as:
  $$\text{Current Balance} = \text{Last Declared Balance} + \text{Inter-turn Receipts} + (\text{Salary if passed/landed START else } 0)$$
- When landing on an opponent's property, deduct the rent:
  $$\text{Balance after rent} = \text{Current Balance} - \text{Rent}$$
  Format the payment token as `[pay: <Rent> to P<OwnerID>]`.
- When landing on unowned property, START, or my own property, format the payment token as `[pay: none]`.
- When deciding to buy an unowned property:
  - If buying: deduct purchase price from the balance after rent and declare `[buy: yes]`.
  - If not buying: declare `[buy: no]` and keep the balance unchanged.
- Always output all three tokens strictly formatted:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]` (final cash held at the end of the turn)

### Purchasing Strategy
- Prioritize buying unowned properties whenever affordable during early and middle laps:
  - Property acquisition preserves 1:1 net worth value (cash converted to deed purchase price) while generating passive rental income from other players.
  - Buy unowned properties whenever $\text{Purchase Price} \le \text{Current Balance} - \text{Rent}$.
- Declare `[buy: no]` automatically when landing on owned properties, START, or when cash on hand is insufficient to cover the purchase price.