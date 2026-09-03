---
game: ref_estate
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1452
---
# Playbook for ESTATE

## Accounting Rules
- Calculate turn starting cash: `Cash = [Last Declared Balance] + [Received from other investors] + [25 Salary if passed/landed on START]`.
- Always check if the prompt states: "Since your last turn you received X from other investors" and add `X` to cash immediately.
- Always check if the prompt states: "You passed START, so you may collect your salary of 25" and add `25` to cash immediately.
- Rent payment:
  - If landing on an opponent's property: output `[pay: N to Pk]` where `N` is rent due and `k` is the owner's index (e.g. `[pay: 12 to P2]`), then subtract `N` from cash.
  - If landing on unowned property, self-owned property, or START: output `[pay: none]`.
- Property purchase:
  - If landing on an unowned property and cash covers the price: output `[buy: yes]` and subtract the price from cash.
  - If not purchasing, unaffordable, already owned, or landing on START: output `[buy: no]`.
- Output `[balance: Final Cash]` with the final calculated cash balance.

## Buying Strategy
- Acquire unowned properties aggressively when affordable to maximize total deed value and generate ongoing rent income.
- Never make a purchase that would drive cash below 0.

## Output Format
- Keep any reasoning concise (or omit to avoid formatting errors).
- End every turn with exactly the three required tokens:
  1. `[pay: N to Pk]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]`