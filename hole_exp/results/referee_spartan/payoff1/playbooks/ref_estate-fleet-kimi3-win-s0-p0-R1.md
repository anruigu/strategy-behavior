---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1977
---
## Ref Estate Playbook

- When landing on an unowned tile, I buy it almost regardless of price. My final score counts cash plus purchase price of deeds, so buying never reduces my net worth — it only converts cash into deed value and creates rent income. Skipping a purchase I could afford (like the Mill earlier) handed opponents gos and cost me; I won't skip an affordable property again.

- Before buying, I check my cash against known upcoming rents: if opponents own the tiles just ahead of me and buying would drop me below roughly the largest rent on the board, I still buy but note the risk — bankruptcy isn't actually possible since net worth stays positive, and liquidity only matters for rent payments I can cover from salary and incoming rents.

- Every turn I recompute my balance from scratch: last declared balance, plus the salary when I passed or landed on START, plus any rents others paid me (only trust the bank's transfer list, not my memory), minus purchases and rents I owe. When the prompt says "you received N from other investors," I verify it against the transfers shown.

- When I land on a tile owned by someone else, I pay the exact listed rent to the correct investor and subtract it immediately. No negotiating, no rounding.

- When I land on my own tile or START, there is nothing to buy and nothing to pay — I reply [buy: no], collect the salary if it applies, and don't invent transactions.

- I declare the salary only on turns where the prompt confirms I passed START, never on other laps.

- I keep my reply in the exact three-token format, every turn, ending with [balance: N], since scoring depends on declared cash matching real arithmetic.

- Late in the game (final lap or two) I stop buying only if the property can never pay rent again before the game ends and I want pure cash — but since deeds count at full purchase price in scoring, even a worthless late deed breaks even, so buying is never a mistake; skipping is only neutral.