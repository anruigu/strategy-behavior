---
game: ref_estate
model: fleet-glm53
condition: win
seed: 1
round: 2
chars: 2816
---
**Playbook for ESTATE**

Buying is how I win. Final score is cash plus purchase price of deeds, so every dollar spent on a property converts 1:1 into score while also generating rent income. There is no penalty for being cash-poor except the inability to buy. When a property is unowned and I can afford it, I buy it — the only exception is if I expect to pass START very soon and need a buffer, and even then I should usually buy.

I should buy aggressively early, even to near-zero cash. Salary and rent will replenish me. This game I bought Foundry for 100 on lap 1, dropping from 200 to 100, and it paid off: Foundry's 24 rent came in from both opponents while I waited. Running down to zero is fine when the alternative is missing a purchase.

Cash shortage is the real constraint, not price selection. If my balance is below a property's price, I simply can't buy — I lost Exchange on lap 2 that way (100 cash vs 120 price). So buy early when cash is high; don't assume I'll be able to buy later after other drains on my cash. Rent owed to other investors drains me too — budget for the possibility of landing on their tiles.

Prioritize by rent yield per price, but in a short game (6 laps) pure acquisition matters more than selection. The Foundry (100/24) was my best buy: high rent per cost, bought lap 1, collected rent multiple times. An expensive high-rent tile is still worth taking if I can afford it.

I must track my true balance every turn. The prompt's "last declared balance" excludes receipts noted since my last turn ("you received N from other investors") and salary when passing START. Before declaring, I compute: last balance + rent received since last turn + salary if I passed START − rent I owe this turn − purchase price if buying. I did this correctly in this game; the calculation lines matched every time. Keep doing it explicitly each turn.

Also read the bank's transfer log: it tells me who owns what (via purchases) and whether rent was paid to me. Rent due to me from opponents may appear in the log before my turn — always include it.

When rent is due to another investor, I pay it and subtract exactly that amount; nothing else changes hands.

Endgame: on the final lap, buying at face value is score-neutral in cash-plus-deed terms, and a final score of +351 with three deeds bought suggests aggressive buying to the end worked. Take the last-turn buy if affordable — at worst it's a wash, at best there's rent income or the scoring rewards ownership. Don't skip out of miscalculation fear; just do the arithmetic cleanly.

Key failure to avoid: being cash-shy on mid-priced properties, and forgetting that a low cash balance can lock me out of a buy entirely (the lap-2 Exchange miss). Keep buying down to low balances in the first half of the game; the board pays me back.