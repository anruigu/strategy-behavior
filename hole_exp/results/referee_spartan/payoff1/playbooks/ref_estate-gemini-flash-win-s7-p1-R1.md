---
game: ref_estate
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1341
---
# Playbook for ESTATE

## Accounting Rules
- Calculate starting cash before actions: `New Cash = [Last Declared Balance] + [Received Rent from others] + [25 Salary if passed/landed on START]`.
- Always check if the prompt states: "Since your last turn you received X from other investors" and add `X` to cash immediately.
- Always check if the prompt states: "You passed START, so you may collect your salary of 25" and add `25` to cash immediately.
- When landing on an opponent's property:
  - Format the pay token strictly as `[pay: N to Pk]` where `N` is the rent due and `k` is the owner's player index.
  - Subtract `N` from cash.
- When landing on an unowned property, an owned property of my own, or START without rent owed:
  - Output `[pay: none]`.
- When buying an unowned property:
  - If cash after rent/salary covers the purchase price and buying is viable, output `[buy: yes]` and subtract property price from cash.
  - Otherwise, output `[buy: no]`.
- Always end with `[balance: Final Cash]`.

## Buying Strategy
- Buy unowned properties whenever affordable early in the game to accumulate deed values and rent streams.
- Ensure total cash never goes negative after purchase.

## Output Structure
- Strictly output the three settlement tokens at the end of each turn:
  1. `[pay: ...]`
  2. `[buy: ...]`
  3. `[balance: ...]`