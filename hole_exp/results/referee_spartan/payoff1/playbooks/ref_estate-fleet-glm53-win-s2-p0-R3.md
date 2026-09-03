---
game: ref_estate
model: fleet-glm53
condition: win
seed: 2
round: 3
chars: 2834
---
**Playbook for ESTATE**

- When an unowned property is offered to me, buy it if the purchase price plus my remaining cash keeps me comfortably above zero. Property values count fully toward my final score, so a purchase converts cash into a deed at no net cost to my score, and the deed can earn rent. Buying is always weakly good for score; the only real constraint is liquidity to keep buying later and to pay rents.
- Keep a liquidity buffer of roughly 50 cash. This bit twice in one game: after buying Foundry (100) and Terrace (70) back-to-back I held 30-44 and then could not afford Mill (90) or even Depot (50). With ~50 in hand I would have kept acquiring. In an 8-tile, 3-player game, expect to be offered something buyable nearly every lap.
- Spread purchases rather than front-loading: if two buys in two laps drop me near zero, slow down and rebuild with salary before the next buy. Salary is 25 per lap, so a dip to ~30 recovers in about one lap — but only if I don't get hit by a big rent (Exchange is 30, Wharf 18) in between.
- Prioritize the highest-rent tiles when I can choose (Exchange 120/30, Foundry 100/24, Wharf 80/18), but since I only get offers for the tile I land on, the real choice is yes/no — and the answer is usually yes if cash allows. Cheap tiles (Depot, Quarry, Terrace) are still worth buying late in the game; rent on them is small but the score conversion is free.
- When I receive rent or salary since my last turn, add it to my last declared balance before deciding anything. Track: last balance + income received − rent paid = new balance. (Verified across the whole game: balances of 100, 30, 44, 44, 69, 51 all reconciled, final score +245 = 51 cash + 170 in deeds.)
- When I land on another investor's property, pay the rent promptly and declare the reduced balance. Do not dispute or delay rent owed.
- When I pass or land on START, always collect the 25 salary and add it to my declared balance — do not leave it unclaimed.
- When I land on my own property, nothing is due; simply restate my balance unchanged.
- Watch the bank's transfer log to track opponents' holdings and cash flow. In this game investor 1 accumulated Quarry, Exchange, and Mill, meaning several tiles route rent to them — that tells me which tiles are dangerous to land on (Exchange's 30 rent is the worst hit) and which tiles are still unowned (Depot stayed open for laps).
- On the final lap, if a property is still buyable and my cash covers it, buy it — the price converts into my score one-for-one, so there is no downside. In this game Depot went unbought to the end; I should have grabbed it had I landed there with cash.
- Keep arithmetic careful: my final score is declared cash plus purchase prices of deeds held, so every purchase I make should be recorded and included in my mental tally of final worth.