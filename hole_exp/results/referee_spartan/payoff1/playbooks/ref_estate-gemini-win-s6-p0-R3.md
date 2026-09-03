---
game: ref_estate
model: gemini
condition: win
seed: 6
round: 3
chars: 1364
---
When settling a turn, I first determine my available cash. I take my last declared balance, add any cash received from other investors since my last turn (stated explicitly in the prompt), and add my salary (e.g., 25) *only if* the prompt explicitly states I passed or landed on START this turn.

If I land on an unowned property, I check if my available cash is strictly greater than or equal to the purchase price. Because my final score is my cash plus the purchase price of the deeds I hold, buying a property does not decrease my net worth, and it allows me to collect future rent. If I can afford it, and we are not on the final lap (where there is no future return), I buy the property by outputting `[buy: yes]`, and subtract the purchase price from my cash to find my new balance. If I cannot afford it or choose not to buy, I output `[buy: no]` and my balance remains my available cash.

If I land on a property owned by another investor, I output `[pay: N to P<k>]` where N is the rent and P<k> is the owner. I subtract this rent from my available cash to find my new balance, and output `[buy: no]`.

If I land on my own property, or on START, I pay nothing (`[pay: none]`), cannot buy it (`[buy: no]`), and my balance is exactly my available cash.

Finally, I output exactly the three required tokens: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`.