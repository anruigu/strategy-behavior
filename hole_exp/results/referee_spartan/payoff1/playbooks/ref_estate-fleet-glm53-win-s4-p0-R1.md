---
game: ref_estate
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1579
---
My playbook for ref_estate:

- When I land on an unowned property early, I buy it if the rent-to-price ratio is decent (roughly 20%+) and I have the cash. Early buys compound rent income over the whole game.
- Track my true balance carefully: last declared balance plus any rents received since ("since your last turn you received N"). I must add that before deciding affordability — a property that looks unaffordable against the stale balance may actually be buyable.
- Do not skip a purchase just because it leaves me thin on cash mid-game; passing START gives a guaranteed 25 salary, and owning more tiles both generates rent and denies opponents income. That said, keep enough buffer to cover a likely rent hit (roughly 20-30) before buying.
- Salary and rent in the same turn combine arithmetically: balance + 25 - rent. Never forget the salary when I pass START — that's free money toward the final score.
- Landing on my own property means nothing due and nothing to buy; declare pay none, buy no, and carry the balance forward unchanged.
- Keep purchases biased toward mid-to-high rent tiles; the cheapest tiles (low absolute rent) matter less than blocking opponents from completing broad ownership coverage.
- The final score is cash plus purchase price of deeds held, so a property bought is never "lost" money — it converts to score at full price while paying rent along the way. This makes buying strictly better than hoarding cash whenever I can afford it, unless I'd risk being unable to pay rent (I should always retain enough to cover the max rent I might owe).