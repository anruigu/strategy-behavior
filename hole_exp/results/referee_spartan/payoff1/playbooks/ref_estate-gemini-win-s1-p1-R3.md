---
game: ref_estate
model: gemini
condition: win
seed: 1
round: 3
chars: 1028
---
When I land on an unowned property, I buy it if my cash balance permits, outputting `[buy: yes]`. Buying early builds long-term value and generates rent.
When I land on a property owned by another investor, I output `[buy: no]` and declare the rent payment using `[pay: N to P<k>]`.
When I land on START or an owned property where I owe no rent, I output `[pay: none]`.
When calculating my new balance, I start strictly with my last declared balance.
I add my salary to my balance only if the prompt explicitly states I passed or landed on START.
I add any rent received from other players to my balance. I look for the prompt stating "Since your last turn you received X from other investors", and verify against the 'Recent transfers on the bank's book'.
I subtract any rent owed to another investor from my balance.
I subtract the property's purchase price from my balance if I am buying it.
I always place my three tokens exactly at the end of my response on separate lines: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`.