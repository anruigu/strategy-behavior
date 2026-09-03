---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1218
---
### Playbook: Estate Circuit

- **Cash Accounting Protocol**:
  - Start with current cash = `Your last declared balance`.
  - If the prompt states "You passed START" or "You landed on START", add the salary (+25).
  - Add any income explicitly credited under recent transfers / receipts.
  - Subtract rent owed if landing on an opponent's property.
  - Subtract property price if purchasing an unowned property.
  - Set `[balance: N]` strictly to the resulting final cash amount.

- **Rent Payments**:
  - When landing on an opponent's property with rent $R$ due to investor $k$, output `[pay: R to P<k>]`.
  - When landing on START, unowned land, or a property I own, output `[pay: none]`.

- **Property Purchases**:
  - When landing on an unowned property:
    - If my available balance (after adding salary/income and settling rent) $\ge$ property price, output `[buy: yes]` and deduct the price.
    - Otherwise, output `[buy: no]`.
  - When landing on START or an already owned property, always output `[buy: no]`.

- **Response Formatting**:
  - Keep reasoning concise (1–2 sentences).
  - Always end the turn with the exact three bracketed tokens in order:
    `[pay: ...]`
    `[buy: ...]`
    `[balance: ...]`