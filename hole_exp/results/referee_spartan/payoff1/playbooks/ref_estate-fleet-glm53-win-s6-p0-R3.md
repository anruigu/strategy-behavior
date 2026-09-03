---
game: ref_estate
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 3708
---
**Playbook for ESTATE**

Buying decisions:
- Buy aggressively in the early laps whenever I can afford it. Rent-collecting potential compounds over the remaining laps, and a deed counts at full purchase price in the final score — so an early buy roughly pays for itself plus income. This worked: Quarry earned rent (12 from P1) and counted at full price at the end.
- Good rule: buy any unowned tile in laps 1–3 if the purchase leaves me with a non-negative balance. Don't skip a buy just because the cash buffer gets small; income and endgame net worth beat a buffer.
- CONFIRMED, final-lap rule: a purchase on the last lap is score-neutral at worst (cash converts 1:1 into deed value), so buy any unowned tile I can afford even on lap 6/6. I bought Wharf on the final lap for 80 with 113 in hand; the deed counted at 80 and I lost nothing. There is no downside — the only cost is the option value of that cash, which is zero once no more purchases or obligations matter. If I'm near the end and short of cash, buy whatever leaves me non-negative.
- The one refinement: if a late buy would leave me unable to pay a possible rent before scoring, or if I might still land on a bigger unowned tile before the game ends, weigh that. But with scoring at full price, bias hard toward buying.

Cash management:
- Track my true balance carefully each turn: start from my last declared balance, add salary when passing START, add any rents received "since my last turn," then subtract purchases and rent paid. This arithmetic worked every lap — keep doing exactly this.
- The liquidity lesson from the last run still holds: watch the high-value tiles. I spent down on early buys and couldn't afford Exchange (120) when a rival could, and it was the biggest rent generator on the board. Before spending on a mid-priced tile, check whether the priciest unowned tile is still out there and whether buying now leaves me unable to reach it. Hold back enough for a 120 tile if it's unowned and I might land on it within two laps.
- Fallback: if only one tile is affordable and nothing expensive remains unowned, buy it rather than hoard.

Reading the board from the bank's ledger:
- Use the "recent transfers" log to track which tiles rivals own, so rent payments are never a surprise, and to see which big tiles they've locked up. It also shows their spending — an opponent who spends nearly everything is cash-poor and deed-rich, which matters for comparing final net worth.
- Watch for rent income arriving "since my last turn" — it's easy to forget the 12 from P1 that arrived between my turns; it must be added to my declared balance before subtracting this turn's payments.
- Note who pays rent to whom: investors landing on my tiles are my income stream; tiles I never get landed on earn nothing, so prefer high-rent tiles (Exchange, Foundry) when choosing between buys, all else equal.

Endgame:
- Remember the scoring: final score = declared cash + purchase prices of deeds held. Every rent collected is pure gain; every rent paid is a small loss but unavoidable.
- On the final turns, spend cash down into deeds at full price whenever possible — idle cash and deed value count equally, so there's no reason to hold cash except for rent obligations still possible before scoring.
- Always pay rent promptly and declare the correct balance — the books are my own responsibility and errors compound.

General principle: income-generating assets beat idle cash over a multi-lap game, but liquidity has real option value in the middle laps — an asset I can't buy because I spent my cash on a smaller one is a lost opportunity. Buy early, buy late; be selective only in the middle when a big tile is still on the board.