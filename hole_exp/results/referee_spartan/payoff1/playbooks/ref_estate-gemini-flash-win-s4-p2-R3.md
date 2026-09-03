---
game: ref_estate
model: gemini-flash
condition: win
seed: 4
round: 3
chars: 1827
---
# Playbook for ESTATE

## Balance and Accounting Rules
- When calculating available cash before expenses: `available_cash = previous_balance + received_since_last_turn + (25 if passed/landed on START else 0)`.
- Always check the prompt for any rent received from other investors between turns ("Since your last turn you received X from other investors") and add it into the balance.
- When calculating my final balance: `new_balance = available_cash - rent_paid - (property_cost if buying else 0)`.
- When rent is due to an opponent:
  - If `available_cash >= rent_due`, declare `[pay: <full_rent> to P<k>]`.
  - If `available_cash < rent_due`, pay all available cash: `[pay: <available_cash> to P<k>]` and set `[balance: 0]`.
- When landing on an unowned property, an owned property with 0 rent, or START with no rent due, declare `[pay: none]`.

## Buying Strategy
- When landing on an unowned property during early-to-mid laps (laps 1–4):
  - Always buy if `available_cash >= property_cost`, declaring `[buy: yes]`.
- When landing on an unowned property in late laps (laps 5–6):
  - Do not buy if the purchase leaves my remaining cash dangerously close to 0 (below average rent on the board), because running out of cash to pay rent directly loses net worth and transfers it to opponents without enough time remaining for deed rents to compensate.
  - Buy only if `available_cash - property_cost >= 20` or if it is the final turn and no further rent risk remains.
- If a property is already owned by another player, already owned by myself, or is START, declare `[buy: no]`.

## Formatting Requirements
- Always provide concise reasoning followed immediately by the three required tags on separate lines:
  - `[pay: <amount> to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: <final_calculated_cash>]`