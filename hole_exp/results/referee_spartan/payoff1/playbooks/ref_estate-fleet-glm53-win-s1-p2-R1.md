---
game: ref_estate
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2152
---
**Playbook for ESTATE**

Final wealth is declared cash plus purchase prices of deeds, so buying a property is a zero-sum cash conversion — money spent on purchase returns to my score immediately. Rent paid is pure loss; rent collected is pure gain. This means I should buy aggressively and early, as long as I keep enough cash to survive rent hits.

- When an unowned property is put to me and my post-purchase balance stays above roughly 20, I buy it. If buying would drop me near zero, I still buy unless I expect a large rent bill before my next salary — a cash cushion of 15–25 is only worth keeping if I'm likely to land on an owned high-rent tile before passing START.
- Prioritize purchases by rent-to-price ratio: Wharf (80/18), Foundry (100/24), Exchange (120/30), Mill (90/20) are the strong tiles; Depot (50/10) and Terrace (70/14) are middling. Given equal cash, take the better ratio first, since rental income compounds over the remaining laps.
- Buy in the early laps even at the cost of a thin balance — purchases made after roughly lap 4 of 6 rarely pay back in rent, so late-game I should hoard cash instead and skip unaffordable or low-value buys.
- Track other players' purchases from the bank's book: rent I owe depends on who owns what, and opponents who spent heavily early will be cash-poor — I can afford to spend down to a small cushion when they can't extract it.
- Always add any "received since last turn" rent to my last declared balance before computing payment and the new balance; forgetting inbound rent made me understate my position.
- The [pay] token on a purchase goes to the bank, not another player; rent goes to the owner. Include the salary of 25 in the balance whenever I pass START.

What did not work: skipping a strong early buy to hold cash was a mistake — by the last lap I sat on 29 with no chance to convert it, and my final score was dominated by the three deeds I'd bought cheap. Conversely, spending down to 20 left me nearly broke after two rent hits; with three opponents holding properties, I should keep a floor of about 25–30 after buying, or size my purchase to the rent exposure on the board.