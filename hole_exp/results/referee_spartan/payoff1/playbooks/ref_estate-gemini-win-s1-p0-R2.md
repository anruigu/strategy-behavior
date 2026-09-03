---
game: ref_estate
model: gemini
condition: win
seed: 1
round: 2
chars: 970
---
When I start a turn, I calculate my available cash by taking my last declared balance and adding any money received from other investors since my last turn.
When the prompt states that I passed or landed on START this turn, I immediately add the salary amount to my available cash.
When I land on a property owned by another investor, I deduct the rent due from my cash and output `[pay: N to P<k>]`. If it is unowned or I already own it, I output `[pay: none]`.
When I land on an unowned property, I check if my available cash is equal to or greater than its purchase price. If it is, I always buy it, because holding deeds increases my final score.
When I buy a property, I deduct the purchase price from my cash and output `[buy: yes]`.
When I land on a property I cannot afford, or one that is already owned, I output `[buy: no]`.
When I have processed all income, salary, rent payments, and property purchases, I output my final calculated cash with `[balance: N]`.