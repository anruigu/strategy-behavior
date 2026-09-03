---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 2735
---
# Playbook for Ref Estate

## Core principle

Buying a tile is score-neutral at the moment of purchase (cash drops by the price, deed value rises by the same amount). It becomes score-positive every time any player lands on it and pays me rent. The only real risk is running out of cash to pay rent to others. So the question every time is: "Can I afford this tile AND still cover a worst-case rent hit?"

## When I land on an unowned tile

- If my post-purchase cash would be ≥ 50, buy it.
- If my post-purchase cash would be < 50, pass. Keep the cash.
- When two tiles are both affordable in the same decision window, prefer the one with the higher absolute rent (more income per landing). If rents are equal, prefer the cheaper tile (frees more cash).
- Purchase opportunities are rare — in one full game I got only one across six laps. Do not be overly picky; taking a slightly worse tile is better than missing the only chance.

## When I land on an owned tile

- Pay the rent immediately.
- Never skip a rent payment.

## When I pass START

- Always collect the 25 salary. It is free cash with no offsetting cost.

## Buffer discipline

- 50 is my minimum cash floor. This covers the maximum possible rent (30) with a 20-cushion for a second hit.
- The buffer matters most in the middle of the game (laps 2–4) where I face multiple future rent exposures.
- In the final lap, the floor drops to 0 — there is no future rent to cover. If an unowned tile comes up on the last lap, buy it unconditionally (the deed value counts toward my score and there is no future rent risk).
- In laps 5–6, lower the floor to 25. I have at most one more rent hit to worry about.
- In laps 1–2, the floor stays at 50. I have 4+ future laps of exposure.

## Bookkeeping

- Every turn, reconcile: last declared balance + rent received (from "since your last turn" line) − rent paid + salary collected = current cash. Then subtract any purchase price. Declare the result.
- Track rent received between turns carefully. Forgetting to add it makes me think I have less cash than I do and causes me to pass on tiles I could afford.
- After 6 laps, my score is: final cash + sum of purchase prices of deeds I hold. Verify this adds up before the game ends.

## What to watch for

- If I have been paying rent every lap with no purchase opportunity, I am likely to get one soon. Stay disciplined (don't drop below the floor) but be ready to buy the moment an unowned tile appears.
- If I have already bought a tile early, my cash is lower and my buffer is tighter. In that case, be more conservative on subsequent purchases.
- The "recent transfers" line tells me which tiles are now owned. Use it to anticipate where I might be stuck paying rent next lap.