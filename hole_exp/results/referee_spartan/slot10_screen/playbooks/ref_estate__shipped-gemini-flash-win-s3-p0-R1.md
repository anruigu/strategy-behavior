---
game: ref_estate__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 901
---
- Calculate starting cash each turn: take `Your last declared balance`, add any cash explicitly received from other players since last turn, and add the salary of 25 if the prompt indicates I passed or landed on START.
- If landing on a property owned by another investor $k$, set `[pay: <rent> to P<k>]` and subtract that rent from cash; otherwise, set `[pay: none]`.
- If landing on an unowned property:
  - If available cash (after rent/salary adjustments) is greater than or equal to the purchase price, choose `[buy: yes]` and subtract the purchase price from final cash.
  - If available cash is strictly less than the purchase price or the property is already owned, choose `[buy: no]`.
- Output `[balance: N]` with the exact final calculated cash balance.
- Keep the response strictly formatted with the three required bracketed tokens at the end: `[pay: ...]`, `[buy: ...]`, `[balance: ...]`.