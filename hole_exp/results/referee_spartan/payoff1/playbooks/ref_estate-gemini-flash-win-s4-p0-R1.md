---
game: ref_estate
model: gemini-flash
condition: win
seed: 4
round: 1
chars: 1368
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
- Always output the final cash total as `[balance: N]`.

### Purchasing Strategy
- Prioritize buying unowned properties whenever affordable, especially during early and middle laps:
  - Property acquisition converts liquid cash into deed value at 1:1 while opening rental income streams.
  - Buy unowned properties if the purchase price is less than or equal to available cash after rent, provided it does not cause an immediate bankruptcy risk.
- Decline purchase (`[buy: no]`) if the property cost exceeds the cash available after accounting for salary and any rent obligations on that turn.