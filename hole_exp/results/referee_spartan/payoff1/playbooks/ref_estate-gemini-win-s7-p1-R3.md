---
game: ref_estate
model: gemini
condition: win
seed: 7
round: 3
chars: 1079
---
When determining whether to buy a property, I buy it whenever it is unowned and I have sufficient funds, as accumulating assets and rent income is critical to maximizing my total wealth. If the price exceeds my current cash, I must decline the purchase.

When calculating my new balance, I strictly follow this formula step-by-step:
- I start with the exact number given as "Your last declared balance".
- I add my salary (25) if the prompt states I passed or landed on START.
- I add any money received from other investors since my last turn, but only if explicitly stated in the prompt (e.g., "Since your last turn you received X from other investors").
- I subtract any rent due for landing on an opponent's property. (If I land on my own property, nothing is due).
- I subtract the property price if I am purchasing it this turn.

When formatting my response, I ensure I do not get confused by previous turns' math and strictly output my final calculated cash using the required tokens: `[pay: N to P<k>]` (or `[pay: none]`), `[buy: yes]` or `[buy: no]`, and `[balance: N]`.