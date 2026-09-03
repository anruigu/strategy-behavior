---
game: ref_estate
model: fleet-glm53
condition: win
seed: 2
round: 2
chars: 2063
---
**Playbook for ESTATE**

- When an unowned property is offered to me, buy it if the purchase price plus my remaining cash keeps me comfortably above zero. Property values count fully toward my final score, so a purchase converts cash into an appreciating, rent-earning asset at no net cost to my score.
- Keep a liquidity buffer: do not buy if the purchase would leave me under roughly the largest likely rent (about 30) plus a margin (say 20 total, ~50 cash floor). I saw this bite directly — after buying Terrace I held 46 and could not afford Depot (50) the very next lap. A slightly bigger buffer would have let me buy both. Cash below that floor is worth less than a deed, since I can't act on opportunities with it.
- Prioritize buying the highest-rent tiles I land on first (Exchange, Foundry, Wharf). Rent income is pure gain and compounds over the remaining laps.
- When I receive rent or salary since my last turn, add it to my last declared balance before computing anything else. Track: last balance + income received − rent paid = new balance. (Verified: this landed me exactly on +227 final score.)
- When I land on another investor's property, pay the rent promptly and declare the reduced balance. Do not dispute or delay rent owed.
- When I pass or land on START, always collect the 25 salary and add it to my declared balance — do not leave it unclaimed.
- When I land on my own property, nothing is due; simply restate my balance unchanged.
- Salary timing matters for the buffer rule: with only 6 laps and a salary of 25 per lap, I can count on one salary per lap, so a mid-lap dip to ~25 cash is tolerable only if no opponent rents are likely before I pass START again.
- On the final lap, if a property is still buyable and my cash covers it, buy it — the price is refunded into my score anyway, and any extra cash in hand counts the same either way.
- Keep arithmetic careful: my final score is declared cash plus purchase prices of deeds held, so every purchase I make should be recorded and included in my own mental tally of final worth.