---
game: ref_estate
model: gemini
condition: win
seed: 1
round: 2
chars: 1089
---
When calculating my new cash balance for the turn, I start with my last declared balance, add any rent the prompt says I received from other investors since my last turn, and add my salary if the prompt states I passed or landed on START. 
When I land on a property owned by another investor, I subtract the rent due from my cash, and I issue the token `[pay: N to P<k>]`.
When I land on an unowned property, an owned property, or START, and owe no rent, I issue the token `[pay: none]`.
When I land on an unowned property and my updated cash balance is equal to or greater than the purchase price, I buy it to build my portfolio and asset value. I subtract the purchase price from my cash, and I issue the token `[buy: yes]`.
When I land on an unowned property but my updated cash balance is strictly less than the purchase price, or when I land on a property that is already owned or on START, I issue the token `[buy: no]`.
When finishing my turn, I always output exactly the three required tokens on separate lines: my pay action, my buy action, and my final calculated `[balance: N]`.