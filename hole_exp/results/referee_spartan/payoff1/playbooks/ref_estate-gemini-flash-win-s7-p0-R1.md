---
game: ref_estate
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1197
---
- When starting balance and transactions occur, compute new balance systematically:
  1. Base = previous declared balance.
  2. Add salary (+25) if I passed or landed on START.
  3. Add all rental income explicitly noted as received since my last turn.
  4. Subtract rent due to another player if landing on their owned property: declare `[pay: N to P<k>]`. Otherwise declare `[pay: none]`.
  5. If landing on an unowned property and current balance after steps 1–4 covers the purchase price, evaluate purchase: subtract purchase price if buying and declare `[buy: yes]`; otherwise declare `[buy: no]`.
  6. Output the final remaining cash as `[balance: N]`.

- Prioritize buying unowned properties whenever affordable, especially in early laps, to maximize rental yield and asset valuation toward the final score (declared cash + deed purchase prices).

- If an unowned property cost exceeds available cash after rent and salary adjustments, declare `[buy: no]` and keep cash intact.

- When landing on an owned property or START, always set `[buy: no]`.

- Format all responses with brief or no commentary and end strictly with the three tokens:
  `[pay: ...]`
  `[buy: ...]`
  `[balance: ...]`.