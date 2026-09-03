---
game: ref_estate
model: gemini
condition: win
seed: 8
round: 3
chars: 1060
---
When calculating my cash for a turn, I take my last declared balance, add any amount the prompt explicitly says I received from other investors, and add my salary if the prompt states I passed or landed on START.
When I land on an unowned property, I check its purchase price. If my current cash (after adding salary and receipts) is greater than or equal to the price, I buy it and deduct the price from my cash. I then output `[buy: yes]`. If I cannot afford it, I output `[buy: no]`.
When I land on a property owned by another investor, I deduct the stated rent from my cash and output `[pay: N to P<k>]` (where N is the rent and k is the investor number). I pay the full rent even if it drops my balance below zero.
When I land on an unowned property, a property I already own, or START, I output `[pay: none]` and `[buy: no]` (except when buying an unowned property).
When concluding my turn, I ensure my final balance accurately reflects all additions (salary, receipts) and deductions (rent, property purchases), outputting it exactly as `[balance: N]`.