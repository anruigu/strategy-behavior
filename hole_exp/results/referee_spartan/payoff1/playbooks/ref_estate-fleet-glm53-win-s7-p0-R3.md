---
game: ref_estate
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 2950
---
**Playbook for ESTATE**

- When an unowned tile is put to me and I can afford it, I buy. Buying converts cash into an asset counted at full price in the final tally, so a purchase costs nothing in net worth while earning rent on top. This episode: bought Foundry (100) and Terrace (70) and both counted in the final score alongside my cash. Keep buying whenever my balance covers the price.

- But don't buy down to near-zero. After the second purchase I was at 54, which was fine — I could still absorb a 30-rent hit and stay solvent. Keep at least 30–50 in reserve when choosing between purchases, so a rent payment on the next turn doesn't zero me out and I can still buy mid-priced tiles (Depot 50, Quarry 60) if they come up. If two buys are in view, prefer the one that leaves more cash.

- Before declaring a purchase, check total available cash including rent received since my last turn — the prompt may tell me "you received N since your last turn," and I must add it before judging affordability. Never forget the rent-received add-on.

- Always reconcile my balance before declaring: start from last declared balance, add salary if I passed START, add any rent received from other investors since my last turn, then subtract rent owed. This worked cleanly on every lap this episode (lap 3: 54−30=24; lap 4: 24+25=49; lap 6: 49+14−30=33). Write the arithmetic in one short line when there's anything to compute.

- Rent owed to another investor: pay it, declare [pay: N to P<k>], [buy: no]. Payments to players use P<k>, payments for purchases go to "bank" — don't mix the formats. Paying rent is unavoidable and doesn't change the decision logic; just book it correctly.

- Landing on my own tile: [pay: none] [buy: no], balance unchanged.

- Output format: exactly the three bracketed tokens on their own lines. Keep reasoning to zero or one clean sentence before the tokens; no stray text after.

- The endgame is total declared cash plus deed prices of tiles held. Purchases are never "lost" money; passing START on the final lap is free money — collect and declare it. Note the final score this episode (+217) came out higher than my own arithmetic on cash+deeds (33+100+70=203), so the scorer may credit something extra (e.g. rent collected or a scoring subtlety). Don't agonize over predicting the exact score — just maximize cash kept plus deeds bought plus rent extracted.

- Watch the bank's transfer log for what opponents own and how their cash is moving — investor 1 assembled Wharf/Exchange/Depot and collected heavily from me (30 twice) and investor 2. Early high-price/high-rent tiles (Exchange, Foundry, Wharf) are worth contesting so the rent flows toward me instead of away.

- Six laps is short: expect roughly 6 own turns, 1–2 START passes, and 2–3 purchase opportunities. Prioritize high-price/high-rent tiles early, since rent income over remaining laps adds up and the deed price counts fully at the end either way.