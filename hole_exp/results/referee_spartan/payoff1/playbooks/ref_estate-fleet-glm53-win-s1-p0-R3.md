---
game: ref_estate
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 3090
---
**Playbook for ESTATE**

Buying is how I win. Final score is cash plus purchase price of deeds, so every dollar spent on a property converts 1:1 into score while also generating rent income. There is no penalty for being cash-poor except the inability to buy. When a property is unowned and I can afford it, I buy it — with one refinement below about pacing.

Buy aggressively early — but this game exposed the real cost of draining cash too fast. I bought Wharf (80) on lap 1 and Terrace (70) on lap 2, leaving myself at 68. Then I landed on Exchange (120) with 86 and Mill (90) with 86, and could buy neither. Those two misses cost me more than the early buys earned me: I finished with only two deeds while opponents picked up Foundry, Mill, and Depot behind me. So: buying to low cash is fine only if the remaining unowned tiles are cheap enough to buy out of salary and rent. When the board still holds expensive unowned tiles (Exchange at 120 especially), keep a buffer that can cover the next most expensive tile, or at least don't assume I can skip a mid-priced tile now and buy a big one later — the dice rarely cooperate.

Rough rule: if buying now leaves me with less than the price of the priciest remaining unowned tile, and that tile is one I could plausibly land on within two laps, consider holding one lap for salary + rent to accumulate. Cash shortage, not price selection, is the binding constraint. Rent owed to other investors drains me too — budget for landing on their tiles.

Prioritize by rent yield per price, but in a short game (6 laps) pure acquisition matters more than selection. Exchange (120/30) and Foundry (100/24) are the best tiles; missing Exchange was the biggest single loss this game. An expensive high-rent tile is worth taking if I can afford it — and worth saving up for.

I must track my true balance every turn. The prompt's "last declared balance" excludes receipts noted since my last turn ("you received N from other investors") and salary when passing START. Before declaring, I compute: last balance + rent received since last turn + salary if I passed START − rent I owe this turn − purchase price if buying. I did this correctly every turn this game; keep doing it explicitly each turn.

Also read the bank's transfer log: it tells me who owns what (via purchases) and whether rent was paid to me. Rent due to me may appear in the log before my turn — always include it. When rent is due to another investor, I pay it and subtract exactly that amount; nothing else changes hands.

Endgame: on the final lap, buying at face value is score-neutral in cash-plus-deed terms. Take the last-turn buy if affordable — at worst it's a wash. This game I had no buy available on lap 6 (Foundry owned, rent 24 paid) and finished at +255 = 105 cash + 150 in deeds.

Key failure to avoid: running my balance below the price of tiles still on the board. The lap-3/lap-4 lockout (86 vs 120 and 90) came directly from buying Terrace to near-zero on lap 2. Buy early and often, but keep enough cash that the next expensive unowned tile is still reachable.