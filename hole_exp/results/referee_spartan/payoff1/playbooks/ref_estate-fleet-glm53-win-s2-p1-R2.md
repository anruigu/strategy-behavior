---
game: ref_estate
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2589
---
**Playbook for ESTATE**

- The win metric is cash plus *purchase price* of deeds. Buying is net-worth-neutral the moment I do it (cash drops by price, deed value rises by the same), and every rent collected after that is pure profit. So my default on an unowned property is to buy.

- This episode showed my cash-buffer rule was too strict. I declined Depot at 8 remaining cash and Wharf at 3 remaining — both net-neutral buys — purely to stay above the largest rent (~30). That safety buys nothing unless unpaid rent has a penalty worse than the debt itself. Revised rule: buy unless post-purchase cash would go *negative*; if cash goes to near zero, I'm still solvent because the deed counts as worth its full price, and any rent I can't cover in cash I can presumably settle against the deed or declare as debt — but the buy itself never loses me net worth. When in doubt, buy.

- On the final turn, with no further rent or salary possible, a purchase is exactly neutral — buy or decline on nothing else. I bought Depot on lap 6 with the game ending; that was fine either way.

- Rent on an owned tile: pay promptly, one line of reasoning, and always recompute the balance from the last declared figure plus any income noted since ("you received N from other investors", salary, etc.) — not from memory. Most arithmetic errors come from forgetting the side income lines.

- When I pass START, add salary *before* deciding on a purchase, not after.

- Track which opponents are buying which tiles from the bank's transfer log. If an opponent is hoarding high-rent tiles, grab remaining unowned tiles before they land on them — denying them rent income is worth as much as collecting my own. In this game I got lucky that my two early buys (Foundry, Exchange) were also the two highest-rent tiles I landed on; the two I declined (Depot, Wharf) were also landed on, so declining them was pure lost rent opportunity had the game run longer.

- Endgame buying when cash is thin is safe: the worst case mid-game is landing on a big rent with low cash, which only matters if there's an actual bankruptcy rule. Absent one, buying with cash nearly to zero is still correct, particularly for high-rent tiles or when few laps remain.

- Never decline a buy to "keep flexibility" — flexibility buys nothing here. The only hard reason to decline is if post-purchase cash would be negative and I can't fund the shortfall.

- At settlement: cash + sum of purchase prices of my deeds. Keep the deed prices in the running total mentally from the moment of purchase, so the endgame is just cash counting.