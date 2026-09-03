---
game: ref_estate
model: gemini
condition: win
seed: 6
round: 1
chars: 1043
---
When I am prompted to settle a turn, I first calculate my true available cash before making any decisions: I take my last declared balance, add any salary from passing or landing on START this turn, and add any money the prompt states I received from other investors since my last turn.

When I land on a property owned by another investor, I output `[pay: N to P<k>]` for the exact rent due and subtract that amount from my available cash.

When I land on an unowned property, a property I already own, or START, I output `[pay: none]`.

When I land on an unowned property, I compare its purchase price to my available cash. If my cash is equal to or greater than the price, I output `[buy: yes]` and subtract the price from my available cash to maximize my total asset value. If I do not have enough cash, I output `[buy: no]`.

When I land on an owned property or START, I output `[buy: no]`.

When I have resolved all income, rent payments, and property purchases for the turn, I output `[balance: N]` with the exact resulting cash amount.