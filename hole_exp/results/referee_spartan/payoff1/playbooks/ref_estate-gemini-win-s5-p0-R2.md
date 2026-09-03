---
game: ref_estate
model: gemini
condition: win
seed: 5
round: 2
chars: 1233
---
When I start a turn, I calculate my total available cash before making any decisions. I take my last declared balance, add any money the prompt says I received from other investors since my last turn, and add the salary amount if the prompt states I passed or landed on START.

When I land on an unowned property, I check its purchase price. Because property values count fully towards my final score and generate rent, I always output `[buy: yes]` if my available cash is equal to or greater than the price. I then subtract that price from my cash. If I cannot afford it, I output `[buy: no]`.

When I land on a property owned by another investor, I output `[pay: N to P<k>]` where N is the rent due and k is the investor's number. I immediately subtract this rent amount from my cash. I also output `[buy: no]`.

When I land on my own property, an unpurchasable space like START, or an unowned property I am not buying, I output `[pay: none]`.

When completing my turn, I output `[balance: N]` using the final cash amount I calculated after applying all income, salaries, rent payments, and purchases for that specific turn. I must carry this exact balance forward mentally, as the game requires me to keep my own books accurately.