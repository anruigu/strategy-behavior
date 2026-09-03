---
game: ref_estate
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 1298
---
**Playbook for ref_estate**

- When an unowned property is offered and I can afford it without going below a small cash buffer (say 15–20), I buy it. Rent-to-price ratio matters less than total rent captured over remaining laps; early in the game almost any purchase beats holding cash.
- When buying would drop me to near zero, I still buy if the price is modest (50–80) and there are many laps left, because salary on passing START will restore liquidity and owned deeds count toward the final score at full purchase price.
- I always add any "received since last turn" money to my declared balance before deciding affordability and before stating the new balance.
- When I land on my own property or START with nothing due, I simply declare pay: none, buy: no, and the correct updated balance including salary or receipts.
- When rent is due, I pay it promptly and subtract it from the correct balance (last declared + receipts).
- Final score counts cash + purchase price of deeds held, so a property bought for X is worth X even if it never collects rent — buying is almost never a loss. Skipped purchases are the main risk, not overextending.
- Keep bookkeeping exact: balance = last declared + receipts since last turn − payments this turn. A single arithmetic slip corrupts all later turns.