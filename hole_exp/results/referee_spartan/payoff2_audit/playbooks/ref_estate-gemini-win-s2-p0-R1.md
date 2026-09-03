---
game: ref_estate
model: gemini
condition: win
seed: 2
round: 1
chars: 817
---
When I am prompted to settle a turn, I calculate my new balance step-by-step starting from my last declared balance.
I check the prompt for money received from other investors since my last turn and add this to my balance.
When the prompt states that I passed or landed on START, I add my salary to my balance.
When I land on a property owned by another investor, I subtract the rent from my balance and output `[pay: N to P<k>]`.
When I land on an unowned property and have sufficient funds, I buy it to increase my long-term rent collection and net worth, subtract the purchase price from my balance, and output `[buy: yes]`.
When I land on a property I already own, or on START, I output `[pay: none]` and `[buy: no]`.
After all additions and deductions, I output my final calculated cash amount as `[balance: N]`.