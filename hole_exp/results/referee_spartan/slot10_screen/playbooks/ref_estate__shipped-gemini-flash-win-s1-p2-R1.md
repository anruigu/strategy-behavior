---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1473
---
# ESTATE Playbook

## Cash Accounting Formula
Whenever a turn is presented, compute the new cash balance step-by-step before deciding to buy:
1. Start with `last declared balance`.
2. Add any incoming rent explicitly stated in the prompt ("Since your last turn you received X...").
3. Add salary (+25) if and only if the prompt states I passed or landed on START.
4. Subtract rent due to an owner:
   - Format: `[pay: <amount> to P<owner_id>]`.
   - If landing on an unowned property, START, or my own property: `[pay: none]`.
5. Check if purchasing is valid:
   - If the property is unowned and `balance_after_rent >= property_price`, decide whether to buy.
   - If buying: output `[buy: yes]` and subtract `property_price` from the balance.
   - If not buying or property is owned: output `[buy: no]`.
6. Output the final remaining cash as `[balance: <final_cash>]`.

## Purchasing Strategy
- When landing on an unowned property during early-to-mid laps (laps 1–4), choose `[buy: yes]` if cash permits, as property prices fully convert to final score while generating passive rental income.
- When cash is insufficient to cover the property price after paying rent, output `[buy: no]`.
- On owned properties, always output `[buy: no]` and pay the specified owner.

## Output Formatting
- Always conclude with the three exact bracketed tokens:
  - `[pay: <amount> to P<owner_id>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: <exact_calculated_amount>]`