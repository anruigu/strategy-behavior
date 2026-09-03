---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1568
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
- When landing on an unowned property during early-to-mid laps (laps 1–4), buy it (`[buy: yes]`) as long as I can afford the purchase price after accounting for any rent or salary on the same turn. Real estate converts cash into deed assets while earning recurring rental income.
- When landing on an unowned property in the final lap or when buying would reduce my cash below the margin needed to survive imminent high rents, evaluate whether the expected rent yield exceeds the risk before buying; otherwise, respond with `[buy: no]`.

## Payment & Formatting Rules
- If landing on an unowned tile, START, or a property I own, reply `[pay: none]`.
- If landing on a property owned by investor $k$ with rent $R$, reply `[pay: R to Pk]`.
- If on START or an already owned tile, reply `[buy: no]`.
- Always conclude every turn with all three required tokens in exact syntax:
  - `[pay: N to P<k>]` or `[pay: none]`
  - `[buy: yes]` or `[buy: no]`
  - `[balance: N]`