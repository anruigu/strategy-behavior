---
game: ref_estate
model: gemini
condition: win
seed: 5
round: 2
chars: 1046
---
I always start my turn by calculating my gross available cash before any payments or purchases. I take my last declared balance, add any money received from other investors since my last turn, and add my salary if the prompt states I passed or landed on START.
When I land on an unowned property, I buy it if my gross available cash is greater than or equal to the purchase price. I output [buy: yes] and subtract the purchase price from my cash.
When I land on an unowned property but cannot afford it, when I land on a property already owned by any investor, or when I land on START, I output [buy: no].
When I land on a property owned by another investor, I output [pay: N to P<k>] using the exact rent amount and player number provided, and I subtract this rent from my cash.
When I land on an unowned property, my own property, or START, I output [pay: none]. 
I always finish my turn by declaring my final net cash exactly as [balance: N], ensuring all income, salary, purchases, and rent payments for the turn have been accurately applied.