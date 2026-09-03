---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1571
---
# ESTATE Playbook

## Cash Accounting Formula
Whenever a turn is presented, compute the new cash balance step-by-step before deciding to buy:
1. Start with `last declared balance`.
2. Add any incoming rent explicitly credited on the bank's books / prompt.
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
- When landing on an unowned property during early-to-mid laps (laps 1–5), choose `[buy: yes]` whenever cash permits, as property prices convert 1:1 into final score (cash + property purchase price) while generating passive rental income.
- When cash is strictly less than the property price after accounting for rent/salary, output `[buy: no]`.
- On owned properties, always output `[buy: no]` and pay the specified owner.

## Output Formatting
- Keep any accompanying explanation brief (1–2 sentences).
- Always conclude with the three exact bracketed tokens in this order:
  - `[pay: <amount> to P<owner_id>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: <exact_calculated_amount>]`