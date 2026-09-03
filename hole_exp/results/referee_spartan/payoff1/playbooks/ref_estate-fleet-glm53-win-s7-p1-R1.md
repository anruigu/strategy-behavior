---
game: ref_estate
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 2095
---
**Playbook for ESTATE**

**Buying decisions:**
- When an unowned tile is offered and my cash after purchase stays comfortably above roughly 40, I buy. Deeds count fully toward the final score at purchase price, so a tile is never "wasted" cash — it converts liquid cash into score while also generating rent.
- When my post-purchase cash would drop below ~40 mid-game, I still buy if it's lap 1–4 (there are salaries still coming and few rent liabilities left), but I skip marginal buys on the last lap unless rent income is very likely.
- Cheap tiles (price ≤ 60, rent ≥ 10) are the best value — rent equal to about 20–25% of price. Always take these when offered. Expensive tiles (price ≥ 120) are fine too since the full purchase price returns to my score; my cash buffer is the only real constraint.

**Cash accounting:**
- I always recompute my balance from the full event list: prior balance + salary (if START passed) + all rent received since my last turn − rent paid − purchase price. The bank tells me rent received, so I must not forget it — I dropped received rent once and my declared balance lagged behind my true holdings. That error must be corrected at the next turn's declaration, never silently carried forward.
- Purchase price goes to "bank" and shows only in the balance token dropping — the buy token covers the transfer. Don't double-declare the payment.

**Rent:**
- When I land on an owned tile, I pay promptly and don't agonize — it's a fixed cost. When I land on my own tile, nothing is due; just collect and update the balance.

**Endgame:**
- Score = declared cash + deed purchase prices, so end-of-game strategy is: hold deeds, and make sure my final declared balance is accurate and includes all rent owed to me. Over the last lap, buying is still score-neutral-to-positive (cash → deed at par), so I buy even late if the ledger allows; the only real risk is running short of cash for rent, which reduces my score one-for-one.

**Overall rule:** maximize deeds held subject to keeping enough cash to cover expected rent (~40 buffer), and never miscount a receipt.