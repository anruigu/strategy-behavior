---
game: ref_estate
model: gemini-flash
condition: win
seed: 4
round: 2
chars: 1560
---
# Playbook for ESTATE

## Balance and Accounting Rules
- When calculating my new balance: `new_balance = previous_balance + (25 if passed/landed on START else 0) - rent_paid - (property_cost if buying else 0)`.
- When rent is due to an opponent:
  - If my available balance (including any START salary collected this turn) is at least the full rent, declare `[pay: <full_rent> to P<k>]`.
  - If my available balance is less than the rent due, declare `[pay: <available_balance> to P<k>]` and set `[balance: 0]`.
- When landing on an unowned property or START with no rent due, declare `[pay: none]`.

## Buying Strategy
- When landing on an unowned property during early-to-mid laps (laps 1–4):
  - Always buy if `available_balance >= property_cost`, declaring `[buy: yes]`.
- When landing on an unowned property in late laps (laps 5–6):
  - Do not buy if the purchase leaves my remaining cash dangerously close to 0 (below average rent on the board), because running out of cash to pay rent directly loses net worth and transfers it to opponents without enough time remaining for deed rents to compensate.
  - Buy only if `available_balance - property_cost >= 20` or if it is the final turn and no further rent risk remains.
- If a property is already owned by another player or is START, declare `[buy: no]`.

## Formatting Requirements
- Always provide concise reasoning followed immediately by the three required tags on separate lines:
  - `[pay: <amount> to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: <final_calculated_cash>]`