---
game: ref_estate
model: fleet-glm53
condition: win
seed: 7
round: 3
chars: 3160
---
**Playbook for ESTATE**

**Buying decisions:**
- When an unowned tile is offered and my cash after purchase stays comfortably above roughly 40, I buy. Deeds count fully toward the final score at purchase price, so a tile is never "wasted" cash — it converts liquid cash into score while also generating rent.
- When my post-purchase cash would drop below ~40 mid-game, I still buy if it's lap 1–4 (salaries still coming, few rent liabilities left), but I skip marginal buys on the last lap unless rent income is very likely. Buying down to 0 on lap 2 (Exchange) and to 10 on lap 3 (Depot) both worked out — rents and salary restored me within one lap. The buffer rule can bend early for a solid tile.
- Cheap tiles (price ≤ 60, rent ≥ 10) are the best value — rent equal to about 20–25% of price. Always take these when offered. Expensive tiles (price ≥ 120) are fine too since the full purchase price returns to my score; my cash buffer is the only real constraint.
- Owning a cheap tile means every opponent landing on it pays me — Depot paid out within one lap of purchase. Deeds that opponents will actually cross are worth more than their par value.
- On the final lap, buying is score-neutral (cash → deed at par), so buy if I can afford it — but I can only spend cash actually on hand. Mill at 90 with 61 in cash was simply unaffordable; check the balance against price before even deliberating.

**Cash accounting — the critical part:**
- I recompute my balance from: prior declared balance + salary (if START passed) + the "since your last turn you received N" line − rent due this turn − purchase price this turn.
- The "since your last turn you received N" line is authoritative — this episode it caught the 60 in rent received on lap 3 and the 30 on lap 6 correctly. Only count events that occurred AFTER my last declared balance — never re-add anything already reflected in the prior declared figure. The transfer log shows several laps of history; most of it is already in my books.
- Purchase price shows only in the balance token dropping — the buy token covers the transfer. Don't double-declare the payment.
- Before submitting, sanity-check: new balance = old balance + only-this-turn's events. If the number moves by more than that, I've double-counted.

**Rent:**
- When I land on an owned tile, I pay promptly and don't agonize — it's a fixed cost. When I land on my own tile, nothing is due; just collect salary/rent and update the balance.

**Endgame:**
- Score = declared cash + deed purchase prices, so end-of-game strategy is: hold deeds, and make sure my final declared balance is accurate and includes all rent owed to me since my last declaration but nothing double-counted. On the last lap, rent received since my last turn still counts — add it in.
- The only real risk late is being short of cash for rent, which reduces my score one-for-one; buying on the last lap carries no such risk if I keep a small buffer for rent still due before the bell.

**Overall rule:** maximize deeds held subject to keeping enough cash to cover expected rent (~40 buffer mid-game, less early), and never miscount a receipt — in either direction.