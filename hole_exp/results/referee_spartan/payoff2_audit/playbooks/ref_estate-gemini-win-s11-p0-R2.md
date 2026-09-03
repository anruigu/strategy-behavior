---
game: ref_estate
model: gemini
condition: win
seed: 11
round: 2
chars: 967
---
I calculate my starting cash for the turn by taking my last declared balance, adding any money received from other investors since my last turn, and adding my salary if the prompt states I passed or landed on START.

When I land on an unowned property and my starting cash is greater than or equal to the purchase price, I buy it. I subtract the purchase price from my cash, output `[pay: none]`, output `[buy: yes]`, and declare the remaining cash. 

When I land on an unowned property and my starting cash is less than the purchase price, I do not buy it. I output `[pay: none]`, output `[buy: no]`, and declare my cash unchanged.

When I land on a property owned by another investor, I pay the required rent. I subtract the rent amount from my cash (even if this results in a negative balance), output `[pay: N to P<k>]`, output `[buy: no]`, and declare the remaining cash.

I always output my final calculated cash amount strictly using the format `[balance: N]`.