---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 1597
---
# Playbook for ESTATE

## Bookkeeping & Accounting Formula
When calculating my cash balance each turn, I will strictly follow this order of operations:
1. Start with **Last Declared Balance**.
2. Add **Salary** (+25) if I passed or landed on START.
3. Add **Received Cash** from other investors noted in the prompt ("Since your last turn you received X").
4. Deduct **Rent Paid** to another player if landing on an opponent's property.
5. Deduct **Property Purchase Cost** if deciding to buy the current unowned property.
6. Set `[balance: N]` strictly equal to the resulting amount.

## Buying Strategy
- When landing on an unowned property during early-to-mid laps (laps 1–5), buy it (`[buy: yes]`) whenever I have sufficient funds after accounting for any turn adjustments. Real estate locks in net worth at 100% deed value while generating passive rental income.
- On late laps (lap 6), buying remains net-worth neutral (cash converts to deed value at 1:1), so buy if funds allow unless preserving liquid cash is required.
- If cash is insufficient to cover the property price after accounting for any turn debits/credits, respond `[buy: no]`.

## Payment & Formatting Rules
- If landing on an unowned tile, START, or a property I own, reply `[pay: none]`.
- If landing on a property owned by investor $k$ with rent $R$, reply `[pay: R to Pk]`.
- If on START or an already owned tile (by self or opponent), reply `[buy: no]`.
- Always conclude every turn with all three required tokens in exact syntax:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`