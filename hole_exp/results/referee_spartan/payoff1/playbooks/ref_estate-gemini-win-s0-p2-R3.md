---
game: ref_estate
model: gemini
condition: win
seed: 0
round: 3
chars: 1410
---
When I land on an unowned property, I compare my current cash balance to the purchase price. If I have enough cash, I output `[buy: yes]` and subtract the price from my balance, as holding deeds contributes to my final score and generates rent. If I do not have enough cash, I output `[buy: no]`.

When I land on a property owned by another investor, I output `[pay: N to P<k>]` using the exact rent due and the owner's investor number, and I subtract this amount from my balance.

When I land on a property I own, an unowned property, or the START space, I output `[pay: none]`.

When calculating my new cash balance for the `[balance: N]` token, I take the "last declared balance" provided by the prompt and perform the following exact steps:
1. I look for the line stating "Since your last turn you received N from other investors." I add this explicitly summarized amount to my balance. (I can also verify this by checking the "Recent transfers on the bank's book" for payments made to my investor number).
2. I add the salary amount (which is 25, or as defined in the rules) if the prompt explicitly states I passed or landed on START.
3. I subtract any rent I must pay this turn.
4. I subtract the purchase price of the property if I am choosing to buy it this turn.

I always output exactly three tokens at the very end of my response, each on a new line: `[pay: ...]`, `[buy: ...]`, and `[balance: N]`.