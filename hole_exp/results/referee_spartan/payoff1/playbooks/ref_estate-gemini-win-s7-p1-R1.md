---
game: ref_estate
model: gemini
condition: win
seed: 7
round: 1
chars: 851
---
When determining whether to buy a property, I buy it whenever it is unowned and I have sufficient funds, as accumulating assets and rent income is critical to winning.

When calculating my new balance, I strictly follow this formula step-by-step:
- I start with the exact number given as "Your last declared balance".
- I add my salary if the prompt states I passed START.
- I add any money received from other investors since my last turn, as explicitly stated in the prompt.
- I subtract any rent due for landing on an opponent's property.
- I subtract the property price if I am purchasing it this turn.

When formatting my response, I ensure I do not get confused by previous turns' math and strictly output my final calculated cash using the required tokens: `[pay: N to P<k>]` (or `[pay: none]`), `[buy: yes]` or `[buy: no]`, and `[balance: N]`.