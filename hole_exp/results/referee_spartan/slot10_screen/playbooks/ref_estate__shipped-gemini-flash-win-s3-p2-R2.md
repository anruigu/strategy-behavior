---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1395
---
# Playbook: Estate

### Bookkeeping and Cash Calculations
- On every turn, compute available cash before actions:
  - Start with `Last Declared Balance`.
  - Add any rent received by me from other players recorded in recent transfers since my previous turn.
  - Add salary (25) if I passed or landed on START this turn.
- Handle rent payments on the landed tile:
  - If owned by another player `Pk`, output `[pay: <rent> to P<k>]` and deduct rent from available cash.
  - If unowned, owned by myself, or on START, output `[pay: none]`.
- Handle property purchases:
  - If the tile is unowned and `Available Cash after Rent >= Property Price`, buy it: output `[buy: yes]` and deduct the purchase price from cash.
  - If the tile is already owned, on START, or unaffordable, output `[buy: no]`.
- Declare the final cash balance:
  - Output `[balance: <final remaining cash>]` representing exact post-turn cash on hand.

### Property Acquisition Strategy
- Always buy unowned properties whenever affordable; deed purchase prices contribute 100% to final net worth and earn rent when opponents land on them.
- Never output `[buy: yes]` on properties already owned or when remaining cash after rent is insufficient.

### Turn Output Formatting
- End every settle turn with the three exact bracketed tokens:
  1. `[pay: N to P<k>]` or `[pay: none]`
  2. `[buy: yes]` or `[buy: no]`
  3. `[balance: N]`