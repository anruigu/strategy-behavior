---
game: ref_estate
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 2399
---
**Playbook for ESTATE**

- When an unowned tile is put to me and I can afford it, I buy. Buying converts cash into an asset counted at full price in the final tally, so a purchase costs nothing in net worth while earning rent on top. This episode confirmed it: my final score was exactly cash (61) plus the two deed prices (100 + 90), so every purchase was pure gain. Keep buying whenever my balance covers the price.

- But don't buy down to near-zero. Spending to a 10-cash balance left me unable to buy Depot (50) on lap 3 even after adding rent received. Keep at least 30–50 in reserve when choosing between purchases, so I can still buy mid-priced tiles that come up later. If two buys are in view, prefer the one that leaves more cash.

- Before declaring a purchase, check total available cash including rent received since my last turn — this episode I had 34 (10 declared + 24 rent) but that still didn't cover Depot at 50, so the [buy: no] was correct. Never forget the rent-received add-on when checking affordability.

- When I can't afford a tile, declare [pay: none] [buy: no] with the correct updated balance. Either omit reasoning entirely or keep it to one clean sentence before the tokens.

- Always reconcile my balance before declaring: start from last declared balance, add salary if I passed START, add any rent received from other investors since my last turn, then subtract rent owed. The prompt tells me when I received money; I must not forget to add it (this worked cleanly on laps 3, 4, and 6).

- Rent owed to another investor: pay it, declare [pay: N to P<k>], [buy: no]. Payments to players use P<k>, payments for purchases go to "bank" — don't mix the formats.

- Landing on my own tile: [pay: none] [buy: no], balance unchanged.

- Output format: exactly the three bracketed tokens on their own lines. Never leave stray or garbled text before the tokens, which risks rejection.

- The endgame is total declared cash plus deed prices. Final score check: my two deeds at purchase price plus final declared cash — so purchases are never "lost" money, and passing START on the final lap is free money; collect and declare it.

- Six laps is short: expect roughly 3–4 of my own turns plus START passes. Prioritize high-price/high-rent tiles (Exchange, Foundry, Wharf) early, since rent income over remaining laps adds up and deed price counts fully at the end either way.