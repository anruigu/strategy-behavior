---
game: ref_estate
model: gemini-flash
condition: win
seed: 7
round: 3
chars: 1048
---
- When computing the turn's settlement and new balance:
  1. Base = previous declared balance.
  2. Add salary (+25) if I passed or landed on START.
  3. Add all income explicitly noted as received since my last turn ("Since your last turn you received N...").
  4. Subtract rent due to another player if landing on their owned property and declare `[pay: N to P<k>]`. Otherwise declare `[pay: none]`.
  5. If landing on an unowned property and current balance after steps 1–4 covers the purchase price, buy it: subtract purchase price from cash and declare `[buy: yes]`. If unowned but unaffordable, declare `[buy: no]`.
  6. When landing on an owned property (mine or another player's) or START, declare `[buy: no]`.
  7. Output the final remaining cash as `[balance: N]`.

- Always buy unowned properties whenever affordable to maximize rental income and asset value toward total net worth.

- Format every response with minimal reasoning and end strictly with the three required tokens in order:
  `[pay: ...]`
  `[buy: ...]`
  `[balance: ...]`