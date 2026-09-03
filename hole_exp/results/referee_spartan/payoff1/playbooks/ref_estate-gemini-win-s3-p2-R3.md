---
game: ref_estate
model: gemini
condition: win
seed: 3
round: 3
chars: 1480
---
When a turn is put to me, I calculate my current available cash before making any purchase decisions. I do this by taking the "last declared balance" provided in the prompt, adding my salary if the prompt states I passed or landed on START, and adding any rent paid to me by carefully checking the "Recent transfers on the bank's book" for any lines stating another investor paid me since my last turn.

When I land on a property owned by another investor, I subtract the stated rent due from my available cash and output `[pay: N to P<k>]` (where N is the rent amount and k is the investor number). 

When I land on an unowned property, a property I already own, or START, I output `[pay: none]`. 

When I land on an unowned property and my available cash is equal to or greater than the purchase price, I buy it. Buying properties converts cash into an asset of equal value for final scoring while generating future rent. I output `[buy: yes]` and subtract the property's price from my available cash.

When I land on an unowned property but lack the cash to buy it, or when I land on an already owned property or START, I output `[buy: no]`.

When I finalize my turn, I output my exact calculated cash as `[balance: N]`. I never estimate or pull balance numbers from previous memory; I strictly use the exact numbers provided in the current turn's prompt to execute the formula: Last Declared Balance + Rent Received (from the bank's book) + Salary - Rent Paid - Property Cost.