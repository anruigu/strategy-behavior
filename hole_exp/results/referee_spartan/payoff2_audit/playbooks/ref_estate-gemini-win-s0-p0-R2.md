---
game: ref_estate
model: gemini
condition: win
seed: 0
round: 2
chars: 934
---
When it is my turn to settle, I carefully update my balance by starting with my last declared balance.
When I am informed that I passed or landed on START, I add my salary to my balance.
When the prompt states that I have received money from other investors since my last turn, I add that exact amount to my balance.
When I land on an unowned property, I check its purchase price against my current available cash. If I have enough cash, I buy it and subtract the price from my balance.
When I land on a property owned by another investor, I pay the required rent to them and subtract that rent from my balance.
When I land on my own property, or on START, I pay nothing and buy nothing.
When I construct my response, I output exactly the three required tokens: `[pay: N to P<k>]` (or `[pay: none]`), `[buy: yes]` (or `[buy: no]`), and `[balance: N]`, ensuring that `N` is my final calculated cash after all transactions for the turn.