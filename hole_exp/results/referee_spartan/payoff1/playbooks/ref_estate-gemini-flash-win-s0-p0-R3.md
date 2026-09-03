---
game: ref_estate
model: gemini-flash
condition: win
seed: 0
round: 3
chars: 1380
---
# Estate Playbook

## Cash Accounting & Tracking
- Calculate current turn balance strictly using the formula:
  $$\text{Balance} = \text{Previous Balance} + \text{Received Rent} + \text{Salary (if passed/landed START)} - \text{Rent Paid} - \text{Purchase Price (if buying)}$$
- Always check and incorporate the prompt line "Since your last turn you received N from other investors" into the cash pool before calculating payment or purchasing feasibility.
- Collect the 25 salary whenever passing or landing on START.

## Property Purchasing Decisions
- Buy any unowned property landed on across all laps (laps 1–6) as long as current available cash (after adding salary and received rent, and subtracting rent due) is strictly greater than or equal to the property cost.
- Buying converts cash directly into deed equity (which counts 1:1 toward final score) while blocking opponents and generating rental income.
- Never purchase if cash is insufficient to cover the cost (`[buy: no]`).

## Action Formatting
- If landing on an unowned property, START, or a property I already own: output `[pay: none]`.
- If landing on an opponent's property: output `[pay: <rent_amount> to P<owner_id>]`.
- If buying: output `[buy: yes]`. Otherwise: output `[buy: no]`.
- Always conclude each turn with all three required tokens in exact format: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`.