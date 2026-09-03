---
game: ref_estate
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 3062
---
**Playbook for ESTATE**

- Buy any unowned property I land on whenever my balance after purchase stays comfortably positive — deeds count toward the final score at full purchase price and collect rent, so buying is score-neutral at worst and profitable over laps. This episode: bought Terrace (70) on lap 2 and Depot (50) on lap 3, finished with 61 cash + 120 deed value = 181. The buys carried my score.
- Exception: don't spend down to near-zero if a rent-heavy tile ahead of me is owned by someone else and I'm likely to land on it before my next salary. Buying Depot left me at 62; that was low but acceptable since I collected salary before the next rent hit. Rough rule: keep at least one expected rent payment (call it 25–30) in reserve after any buy.
- Compute my balance from the ledger each turn, not just my last declaration: add salary when I pass START, add any rent received since ("you received N from other investors" lines), subtract rent due this turn and the purchase price of anything bought. Declare that exact number — the score is declared cash plus deed value, so accurate books matter. My lap-4 arithmetic (62 + 10 rent received + 25 salary − 12 rent = 85) worked; keep doing exactly that.
- Rent-to-price ranking from this board: Depot (10/50) and Wharf (18/80) and Quarry (12/60) are the best ratio; Terrace (14/70) is fine; Foundry (24/100) and Exchange (30/120) are the worst ratio but biggest absolute rent — good to own, expensive to land on. Mill (90 for 20) is middle. When constrained, prefer the high-ratio tiles; when flush, take whatever is there.
- Expect the hot tiles to be bought fast: Wharf, Exchange, Foundry were gone by lap 2, Quarry by lap 4. If I land on an unowned tile in the first three laps, buy it — waiting means someone else takes it, and my only ownership all game came from those early buys.
- Be aggressive early, cash-hungry late: rent bleeds cash steadily (I paid 18+12+24 = 54 in rent across six laps with only two properties owned). Early buys both build deed value and stop that bleed; late buys of what's left rarely rescue a position.
- Passing START: always collect the salary even if nothing is purchasable — it's pure score.
- When rent is due, pay it promptly and fold it into the declared balance in the same turn — never carry an unpaid debt into the next declaration.
- Own tiles in the path of the dice I actually roll: my small die rolls (1, 2, 3 mostly) meant short hops. Landing on my own Terrace on the final lap cost nothing and confirmed ownership has a defensive value even when rent income is thin.
- With only 6 laps and modest rent levels, don't bankrupt myself for a buy: one or two solid mid-priced properties plus preserved cash scored competitively. Aiming for three properties bought by lap 3 is the target if the landings allow it.
- The real risk isn't overpaying for deeds, it's dying by a thousand rent cuts while holding no property. If two laps pass with no purchase, treat every subsequent unowned tile as a must-buy unless it would put me below roughly 25 in reserve.