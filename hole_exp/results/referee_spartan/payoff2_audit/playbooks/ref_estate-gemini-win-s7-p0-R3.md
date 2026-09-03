---
game: ref_estate
model: gemini
condition: win
seed: 7
round: 3
chars: 1138
---
When settling a turn, I calculate my total available cash before making any decisions. I start with my last declared balance, add my salary if the prompt states I passed or landed on START, and add any funds the prompt says I received from other investors since my last turn.

When I land on a property owned by another investor, I output `[pay: N to P<k>]` using the specified rent and owner's number, and I subtract the rent from my cash. 

When I land on an unowned property, a property I already own, or START, I output `[pay: none]`.

When I land on an unowned property, I compare my available cash to the purchase price. If I can afford it, I output `[buy: yes]` and subtract the purchase price from my cash, as buying early maximizes future rent collection. If I do not have enough cash, I output `[buy: no]`.

When I land on an owned property or on START, I output `[buy: no]`.

When I have resolved all income, rent payments, and purchases for the turn, I output my final calculated cash as `[balance: N]`.

I always place the three required tokens—`[pay: ...]`, `[buy: ...]`, and `[balance: ...]`—at the very end of my response.