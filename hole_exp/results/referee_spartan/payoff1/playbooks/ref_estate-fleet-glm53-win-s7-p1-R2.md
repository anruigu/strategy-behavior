---
game: ref_estate
model: fleet-glm53
condition: win
seed: 7
round: 2
chars: 3002
---
**Playbook for ESTATE**

**Buying decisions:**
- When an unowned tile is offered and my cash after purchase stays comfortably above roughly 40, I buy. Deeds count fully toward the final score at purchase price, so a tile is never "wasted" cash — it converts liquid cash into score while also generating rent.
- When my post-purchase cash would drop below ~40 mid-game, I still buy if it's lap 1–4 (salaries still coming, few rent liabilities left), but I skip marginal buys on the last lap unless rent income is very likely. Buying down to 0 on lap 3 worked out fine — rents received (32) plus salary restored me to 57 immediately, so the buffer rule can bend early for a solid tile.
- Cheap tiles (price ≤ 60, rent ≥ 10) are the best value — rent equal to about 20–25% of price. Always take these when offered. Expensive tiles (price ≥ 120) are fine too since the full purchase price returns to my score; my cash buffer is the only real constraint.
- Owning a cheap tile means every opponent landing on it pays me — Depot and Terrace both paid out within two laps. Deeds that opponents will actually cross are worth more than their par value.

**Cash accounting — the critical part:**
- I recompute my balance from the full event list: prior balance + salary (if START passed) + all rent received *since my last declaration* − rent paid − purchase price.
- The ledger state shown to me each turn already folds in everything I declared last turn, and the "since your last turn you received N" line covers receipts in between. On the final lap I mistakenly re-added rent I had already booked (declared 65 when the true figure was 45) by re-scanning the whole transfer list. Rule: only count events that occurred AFTER my last declared balance — never re-add anything already reflected in the prior declared figure. The transfer log shows several laps of history; most of it is already in my books.
- Purchase price shows only in the balance token dropping — the buy token covers the transfer. Don't double-declare the payment.

**Rent:**
- When I land on an owned tile, I pay promptly and don't agonize — it's a fixed cost. When I land on my own tile, nothing is due; just collect and update the balance.

**Endgame:**
- Score = declared cash + deed purchase prices, so end-of-game strategy is: hold deeds, and make sure my final declared balance is accurate and includes all rent owed to me but nothing double-counted. Buying on the last lap is still score-neutral (cash → deed at par); the only real risk is running short of cash for rent, which reduces my score one-for-one.
- Before submitting the final balance, check it against the immediately prior declaration plus only the events since: rent received since, rent paid since, salary since, purchase since. If the number moves by more than that, I've double-counted.

**Overall rule:** maximize deeds held subject to keeping enough cash to cover expected rent (~40 buffer mid-game, less early), and never miscount a receipt — in either direction.