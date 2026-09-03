---
game: ref_estate
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 2041
---
**Playbook for ESTATE**

- The win metric is cash plus *purchase price* of deeds. That means buying a property is net-worth-neutral the moment I do it (cash drops by price, deed value rises by the same amount), and every rent I collect after that is pure profit. So when an unowned property is put to me, my default is to buy, even late in the game. My earlier instinct to "keep cash for flexibility" was wrong — cash has no upside, deeds do.

- I buy any unowned property whenever my post-purchase cash stays comfortably above the largest single rent on the board (here, ~30), so one bad landing can't cripple me. If two properties are offered on consecutive turns, I buy both in price-ascending order if I can, cheap ones first.

- Exception: if the game is one turn from ending and I cannot collect rent or pass START again, a purchase is exactly neutral — buy or not based on nothing else. It's never a loss to buy, so when in doubt, buy.

- Rent on an owned tile: I pay promptly, keep reasoning to one line, and always recompute the balance from the last declared figure plus any income noted since ("you received N from other investors", salary, etc.) — not from memory. Most of my arithmetic errors came from forgetting the side income lines.

- When I collect salary, I add it before deciding on a purchase, not after.

- Track which opponents are buying which tiles from the bank's transfer log. If a rich opponent is hoarding the high-rent tiles, I want to grab any remaining unowned tile before they land on it, since denying them rent income is worth as much as collecting my own.

- At settlement, my net worth calculation: cash + sum of purchase prices of my deeds. I keep the deeds' prices in the running total mentally from the moment I buy, so the endgame is just cash counting.

- Never decline a buy purely to "keep flexibility" — in this game flexibility buys nothing. The only reasons to decline are (a) it would take my cash below one big rent payment, or (b) the game is over and no further rent or salary is possible.