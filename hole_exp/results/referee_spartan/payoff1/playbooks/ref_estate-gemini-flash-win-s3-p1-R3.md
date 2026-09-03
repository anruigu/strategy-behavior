---
game: ref_estate
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1385
---
When playing ESTATE:

- Keep exact track of cash flow on every turn:
  - Start with `last_declared_balance`.
  - Check for income received from other players since last turn (e.g., "Since your last turn you received N from other investors") and add `N` to my starting balance.
  - If the prompt states I passed or landed on START, add the salary (25) to my balance before settling payments or purchases.
  - If rent is due to another player, declare `[pay: N to P<k>]` and subtract `N` from my balance. If no rent is due, declare `[pay: none]`.
  - If the property is unowned and I have sufficient balance to buy it, declare `[buy: yes]` and subtract the property price from my balance; otherwise declare `[buy: no]`.
  - Always declare `[buy: no]` if the property is already owned (by me or another player) or if I land on START.
  - Set `[balance: N]` equal to the exact final calculated cash balance after applying rent received, salary, rent payments, and purchase costs for that turn.

- When given the option to buy an unowned property and I have sufficient cash to afford it without going negative, buy it (`[buy: yes]`), because property values count directly toward net worth and generate passive rent income from other players.

- Always format responses to conclude with the three mandatory tokens in exact sequence:
  1. `[pay: ...]`
  2. `[buy: ...]`
  3. `[balance: ...]`