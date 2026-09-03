---
game: ref_estate
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 3360
---
My playbook for ref_estate:

- When I land on an unowned property early, I buy it if the rent-to-price ratio is decent (roughly 20%+) and I have the cash. Early buys compound rent income over the whole game. Buying Wharf (18/80) lap 1 and Exchange (30/120) lap 2 left me at 0 cash mid-game and still worked out — salary and incoming rent rescued the balance.
- Track my true balance carefully: last declared balance plus any rents received since ("since your last turn you received N"). I must add that before deciding affordability — a property that looks unaffordable against the stale balance may actually be buyable.
- Going to zero (or even briefly negative) is survivable: with two deeds and a final rent inflow I ended +235. Rent paid to opponents is a cash-flow issue, not score destruction, since my deeds still count at full price. Don't panic if a rent payment pushes the declared balance below zero — just report the arithmetic exactly and keep playing.
- However, note that a zero buffer meant I couldn't buy anything on laps 3-5 even if I'd landed on something unowned, and I took two rent hits back-to-back with no cushion. When two opponents split the board, going all-in on purchases early is still right (deeds are score-neutral and rent is pure gain), but accept that the mid-game will be lean and my cash floor may dip negative before rents and salary flow back.
- Salary and rent in the same turn combine arithmetically: balance + 25 - rent. Never forget the salary when I pass START — that's free money toward the final score.
- Landing on my own property means nothing due and nothing to buy; declare pay none, buy no, and carry the balance forward plus any rents received since the last turn.
- Keep purchases biased toward mid-to-high rent tiles; Exchange (120, rent 30) was my best earner. The cheapest tiles (low absolute rent) matter less than blocking opponents from completing broad ownership coverage.
- The final score is cash plus purchase price of deeds held, so a property bought is never "lost" money — it converts to score at full price while paying rent along the way. This makes buying strictly better than hoarding cash whenever I can afford it.
- In this run I only landed on two buyable tiles all game (Wharf, Exchange) and still finished +235 with two deeds (200 deed value) plus 5 cash. The lesson: buying opportunity is scarce on an 8-tile board — never decline a buyable tile I can afford, at any lap, because laps 3-5 mostly landed me on opponents' tiles paying rent with no purchase chances.
- Watch the bank's transfer log to see which opponents own which tiles — it tells me where my rent exposure is and how much ownership coverage opponents are building. Investor 1 assembled Foundry, Mill, Quarry and collected 36 rent from me across two laps; an opponent buying multiple tiles is the main threat, so deny them tiles whenever I land on an unowned one.
- Rent payments to opponents reduce my cash but not my score relative to what I'd have without the deed — pay them promptly and correctly, and keep the arithmetic exact (balance minus rent only; salary added only when I passed START; plus rents received since last turn).
- If opponents rent-strike me into negative balance, later rent receipts ("you received N since your last turn") restore me — fold those into the next turn's balance exactly as shown.