---
game: ref_estate
model: gemini
condition: win
seed: 5
round: 2
chars: 1397
---
When calculating my current balance at the start of a turn, I take my last declared balance, add the exact amount the prompt states I "received from other investors" since my last turn, and add my salary if the prompt states I passed START.
I never use the "Recent transfers on the bank's book" to calculate incoming cash, because relying on the book directly leads to double-counting payments that occurred before my previous turn; I only use the summary line provided in the prompt.
When I land on a property owned by another investor, I pay the specified rent to them, subtract that rent from my calculated balance, and output `[buy: no]`.
When I land on an unowned property, I check if my calculated current balance is greater than or equal to the purchase price.
If I can afford the unowned property, I always buy it and subtract the purchase price from my balance. Because final score is cash plus the purchase price of deeds held, buying property does not reduce my net worth and gives me the chance to earn rent. 
If I cannot afford the unowned property, I output `[buy: no]` and leave my balance as is.
When I land on a property I already own, or on START, I pay no rent, output `[pay: none]`, output `[buy: no]`, and my balance remains my calculated starting balance.
I always end my turn by outputting the exact three required brackets: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`.