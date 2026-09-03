---
game: ref_estate
model: gemini
condition: win
seed: 2
round: 2
chars: 1048
---
When settling my turn, I calculate my new balance exactly as follows: I take my last declared balance, add my salary if the prompt states I passed or landed on START, add any rent the prompt explicitly says I received from other investors since my last turn (ignoring the bank's book for this to avoid double-counting), subtract the rent I must pay this turn, and subtract the purchase price of the property if I am buying it.

When I land on a property owned by another investor, I issue `[pay: N to P<k>]` for the required rent. If the property is unowned or owned by me, I issue `[pay: none]`.

When I land on an unowned property and my cash balance before buying is greater than or equal to the property's price, I issue `[buy: yes]` because property values count directly toward my final score and generate future rent. If I cannot afford it, or if it is already owned, I issue `[buy: no]`.

When formatting my reply, I end my response with exactly the three required tokens on separate lines: `[pay: ...]`, `[buy: ...]`, and `[balance: ...]`.