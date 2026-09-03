---
game: ref_estate
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1370
---
# Estate Playbook

## Cash Accounting & Tracking
- Calculate current turn balance strictly using the formula:
  $$\text{Balance} = \text{Previous Balance} + \text{Received Rent} + \text{Salary (if passed START)} - \text{Rent Paid} - \text{Purchase Price (if buying)}$$
- Always verify the "Since your last turn you received..." prompt line to include external income before determining whether a purchase or rent payment is affordable.
- When passing or landing on START, add the 25 salary immediately to the current balance.

## Property Purchasing Decisions
- Buy any unowned property landed on in laps 1–4 if the total cash on hand (after collecting salary and rents received) covers the purchase price, preserving property value for final net worth and generating rental income.
- If cash on hand is less than the property purchase price, output `[buy: no]`.
- On later laps (laps 5–6), do not purchase low-yield properties if doing so risks negative cash flow against impending opponent rent tiles.

## Action Formatting
- If landing on an unowned property or a property I own or START: output `[pay: none]`.
- If landing on an opponent's property: output `[pay: <rent_amount> to P<owner_id>]`.
- If buying: output `[buy: yes]`. Otherwise: output `[buy: no]`.
- End every turn with the exact three bracketed tokens: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`.