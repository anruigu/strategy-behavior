---
game: ref_estate
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2055
---
**Playbook for ESTATE**

Buying is how I win. Final score is cash plus purchase price of deeds, so every dollar spent on a property converts 1:1 into score while also generating rent income. There is no penalty for being cash-poor except the inability to buy. When a property is unowned and I can afford it, I buy it — the only exception is if I expect to pass START very soon and need a buffer, and even then I should usually buy.

I should buy aggressively early, even to near-zero cash. Salary and rent will replenish me. In my last game I was left unable to buy later properties (a 50 and a 120) because I'd held back just enough cash to be repeatedly short. Running down to zero is fine when the alternative is missing a purchase.

Prioritize by rent yield per price, but in a short game (6 laps) pure acquisition matters more than selection — total ownership drives both rent collection and final score. High rent-per-cost tiles (like a 24-rent for 100) are the best buys, but an expensive high-rent tile is still worth taking if I can afford it.

I must track my true balance every turn, including rent received "since my last turn" and salary when passing START. A common error is forgetting to add those receipts — the prompt's "last declared balance" does not include them. Before declaring, I compute: last balance + receipts noted in the prompt + salary if I passed START − rent I owe this turn − purchase price if buying.

When rent is due to another investor, I pay it and subtract exactly that amount; nothing else changes hands.

Endgame: on the final lap, buying is still correct if affordable — it's a wash on score (cash − price + deed = 0) but only worth it if there's any chance of rent income before the end or if the scoring counts deeds at face value anyway. A face-value buy on the last turn is neutral, so I can take it or skip it; I skip if there's any risk of miscalculation.

Key failure to avoid: being cash-shy on mid-priced properties. Keep buying down to low balances in the first half of the game; the board pays me back.