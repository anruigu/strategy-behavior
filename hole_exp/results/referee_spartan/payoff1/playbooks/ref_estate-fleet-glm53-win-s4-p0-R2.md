---
game: ref_estate
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2643
---
My playbook for ref_estate:

- When I land on an unowned property early, I buy it if the rent-to-price ratio is decent (roughly 20%+) and I have the cash. Early buys compound rent income over the whole game. Buying Mill at lap 3 for 90 leaving only 6 cash worked out fine — the salary plus incoming rent rescued the balance within one lap.
- Track my true balance carefully: last declared balance plus any rents received since ("since your last turn you received N"). I must add that before deciding affordability — a property that looks unaffordable against the stale balance may actually be buyable.
- Do not skip a purchase just because it leaves me thin on cash mid-game; passing START gives a guaranteed 25 salary, and owning more tiles both generates rent and denies opponents income. With multiple opponents circling an 8-tile board, owned tiles get hit often, so a near-zero buffer is riskier only when I face high-rent tiles I don't own — but rent paid to opponents is a one-lap cash-flow issue, not score destruction, since my deeds still count at full price.
- Salary and rent in the same turn combine arithmetically: balance + 25 - rent. Never forget the salary when I pass START — that's free money toward the final score. (Confirmed: 6 + 40 rent + 25 salary = 71.)
- Landing on my own property means nothing due and nothing to buy; declare pay none, buy no, and carry the balance forward plus any rents received since the last turn.
- Keep purchases biased toward mid-to-high rent tiles; the cheapest tiles (low absolute rent) matter less than blocking opponents from completing broad ownership coverage.
- The final score is cash plus purchase price of deeds held, so a property bought is never "lost" money — it converts to score at full price while paying rent along the way. This makes buying strictly better than hoarding cash whenever I can afford it.
- Aggressive early buying paid off: ending with two deeds (80 + 90 = 170 in deed value) plus 65 cash gave +253. Buy nearly everything I land on that I can afford, even late (lap 4-5), since deed price is score-neutral and rent flow is pure gain.
- Watch the bank's transfer log to see which opponents own which tiles — it tells me where my rent exposure is and how much ownership coverage opponents are building. An opponent buying multiple tiles (investor 1 took Foundry, Terrace, Depot) is the main threat; deny them tiles when I can.
- Rent payments to opponents reduce my cash but not my score relative to what I'd have without the deed — pay them promptly and correctly, and keep the arithmetic exact (balance minus rent only; salary added only when I passed START).