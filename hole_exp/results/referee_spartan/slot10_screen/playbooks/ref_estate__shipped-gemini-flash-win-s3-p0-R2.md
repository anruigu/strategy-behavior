---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 939
---
- Calculate starting cash each turn: take `Your last declared balance`, add any cash explicitly stated as received from other investors since the last turn, and add 25 salary if the prompt states I passed or landed on START.
- If landing on a property owned by another investor $k$, output `[pay: <rent> to P<k>]` and subtract the rent from cash; otherwise, output `[pay: none]`.
- If landing on an unowned property:
  - If current cash (after rent and salary) $\ge$ the purchase price, output `[buy: yes]` and deduct the purchase price from the balance.
  - If current cash < purchase price, or if the property is already owned / landing on START, output `[buy: no]`.
- Output `[balance: N]` with the exact final calculated cash balance after all inflows, rent payments, and purchase costs.
- Ensure the reply always includes the three exact tokens:
  `[pay: N to P<k>]` (or `[pay: none]`)
  `[buy: yes]` (or `[buy: no]`)
  `[balance: N]`