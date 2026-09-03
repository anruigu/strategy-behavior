---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1443
---
# Estate Playbook

## Cash Balance Tracking
- When calculating my updated balance each turn, I follow the exact formula:
  `New Balance = Previous Balance + Salary (if passed/landed on START, usually 25) + Income Received (from other players since last turn) - Rent Paid - Purchase Price (if buying)`
- I always check the turn prompt carefully for incoming payments ("Since your last turn you received X from other investors") and ensure they are added to my running balance before settling expenses.
- I never subtract a purchase price if `[buy: no]`, and I never pay rent if landing on unowned property, START, or my own property.

## Property Purchase Decisions
- When I land on an unowned property and have sufficient funds to cover the purchase price without going negative, I choose `[buy: yes]`. Total score is cash plus deed purchase prices, so buying deeds locks in wealth while generating ongoing rent from opponents.
- When landing on an owned property, START, or an unowned property I cannot afford, I choose `[buy: no]`.

## Rent and Payments
- When landing on another player's property (e.g., owned by investor $k$ with rent $R$), I output `[pay: R to Pk]`.
- When landing on an unowned property, START, or my own property, I output `[pay: none]`.

## Response Formatting
- I format my reply cleanly, keeping reasoning concise, and end with the three required tokens in exact order:
  `[pay: ...]`
  `[buy: ...]`
  `[balance: N]`