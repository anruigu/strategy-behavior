---
game: ref_estate
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2826
---
**Playbook for ESTATE**

Buying decisions:
- Buy aggressively in the early laps whenever I can afford it. Rent-collecting potential compounds over the remaining laps, and a deed counts at full purchase price in the final score — so an early buy roughly pays for itself plus income. This worked: Quarry and Terrace both earned rent and counted at full price at the end.
- Good rule: buy any unowned tile in laps 1–3 if the purchase leaves me with a non-negative balance. Don't skip a buy just because the cash buffer gets small; income and endgame net worth beat a buffer.
- In the last lap or two, only buy if the price is fully recoverable (rent plus salary still to come) — otherwise cash in hand is worth just as much as the deed.

Cash management:
- Track my true balance carefully each turn: start from my last declared balance, add salary when passing START, add any rents received "since my last turn," then subtract purchases and rent paid. This arithmetic worked every lap — keep doing exactly this.
- NEW, the big lesson from this run: watch the high-value tiles. I spent down to 70 on lap 2 and then couldn't afford Exchange (120) on lap 3, and a rival bought it. The most expensive tile on the board is often the single biggest net-worth swing in the game. Before spending on a mid-priced tile, check whether the priciest unowned tile is still out there and whether buying now leaves me unable to reach it. If a 120 tile is unowned and I might land on it within two laps, hold back enough to buy it — even if that means skipping a 70 tile I can afford now.
- The fallback still holds: if I can only afford one tile and nothing expensive remains unowned, buy it rather than hoard.

Reading the board from the bank's ledger:
- Use the "recent transfers" log to track which tiles rivals own, so rent payments are never a surprise, and to see which big tiles they've locked up. It also shows their spending — an opponent who spends nearly everything is cash-poor and deed-rich, which matters for comparing final net worth.
- Note who pays rent to whom: investors landing on my tiles are my income stream; tiles I never get landed on earn nothing, so prefer high-traffic/high-rent tiles (like Exchange) when choosing between buys.

Endgame:
- Remember the scoring: final score = declared cash + purchase prices of deeds held. Every rent collected is pure gain; every rent paid is a small loss but unavoidable.
- Always pay rent promptly and declare the correct balance — the books are my own responsibility and errors compound.

General principle: income-generating assets beat idle cash over a multi-lap game, but liquidity has real option value too — an asset I can't buy because I spent my cash on a smaller one is a lost opportunity, not just a delay. Balance aggression with the ability to pounce on the big tiles.