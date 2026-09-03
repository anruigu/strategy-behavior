---
game: ref_estate
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 2223
---
**Playbook for ref_estate**

- When an unowned property is offered and I can afford it without going below a small cash buffer (say 15–20), I buy it. Rent-to-price ratio matters less than total rent captured over remaining laps; early in the game almost any purchase beats holding cash.
- When buying would drop me to near zero, I still buy if there are laps left, because salary on passing START and rent receipts will restore liquidity and owned deeds count toward the final score at full purchase price. I bought Wharf on lap 5 leaving only 11 cash and it still paid off — the deed's face value makes even a late purchase score-neutral at worst, and rent is pure upside.
- I always add any "received since last turn" money to my declared balance before deciding affordability and before stating the new balance. My declared balance must include receipts (rent from others, salary) and exclude payments made this turn.
- When I land on my own property or START with nothing due, I declare pay: none, buy: no, and the correct updated balance including salary or receipts.
- When rent is due, I pay it promptly and subtract it from the correct balance (last declared + receipts − rent). Paying rent does not change my net worth relative to the final score — cash leaves but I already counted it — but paying on time keeps the bank's book consistent.
- Final score counts cash + purchase price of deeds held, so a property bought for X is worth X even if it never collects rent — buying is almost never a loss. Skipped purchases are the main risk, not overextending. The only exception would be the very last turn with no chance of future rent, and even then buying is score-neutral, so buy anyway unless cash is needed for rent this same turn.
- Keep bookkeeping exact: balance = last declared + receipts since last turn − payments this turn. A single arithmetic slip corrupts all later turns. This run's score (+291 on 21 cash + 270 in deeds) came from clean bookkeeping and aggressive buying — keep both.
- Watch the bank's transfer log for what opponents own; rent expectations on my landings depend on it, and I can estimate whether keeping a cash buffer matters (opponents holding many deeds means more rent exposure).