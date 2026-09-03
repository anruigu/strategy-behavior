---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 3408
---
# Playbook for Ref Estate

## Core principle

Buying a tile is score-neutral at the moment of purchase (cash drops by the price, deed value rises by the same amount). It becomes score-positive every time any player lands on it and pays me rent. The deed value also counts directly toward my final score, so even a tile that generates little rent is worth its purchase price in score terms. The only real risk is running out of cash to pay rent to others. So the question every time is: "Can I afford this tile AND still cover a worst-case rent hit?"

## When I land on an unowned tile

- If my post-purchase cash would be ≥ my current floor, buy it.
- If my post-purchase cash would be < my current floor, pass. Keep the cash.
- When two tiles are both affordable in the same decision window, prefer the one with the higher absolute rent (more income per landing). If rents are equal, prefer the cheaper tile (frees more cash).
- Purchase opportunities are moderate in frequency — I got three in one game of six laps. Be ready to buy the moment one appears if I can afford it. Do not be overly picky about which tile it is; any deed adds its full price to my final score.

## When I land on an owned tile

- Pay the rent immediately.
- Never skip a rent payment.

## When I pass START

- Always collect the 25 salary. It is free cash with no offsetting cost.

## Buffer discipline

- 50 is my minimum cash floor for laps 1–3. This covers the maximum possible rent (30) with a 20-cushion for a second hit.
- In laps 4–5, lower the floor to 30. I have fewer future rent exposures.
- In the final lap (lap 6), the floor drops to 0 — there is no future rent to cover. If an unowned tile comes up on the last lap, buy it unconditionally.
- The floor is a safety net, not a target. If I'm well above it, I should buy aggressively.

## Score math to keep in mind

- My final score = cash + sum of purchase prices of deeds I hold.
- A deed I buy for 70 is worth 70 points immediately, plus any rent it generates. The rent is a bonus; the deed value is guaranteed.
- This means buying is almost always score-positive unless it forces me to skip a higher-value purchase later or causes a bankruptcy risk.
- In practice, holding two tiles (e.g., 70 + 50 = 120 in deed value) plus modest cash is a solid position.

## Bookkeeping

- Every turn, reconcile: last declared balance + rent received (from "since your last turn" line) − rent paid + salary collected = current cash. Then subtract any purchase price. Declare the result.
- Track rent received between turns carefully. Forgetting to add it makes me think I have less cash than I do and causes me to pass on tiles I could afford.
- After 6 laps, verify: final cash + sum of deed prices = my score.

## What to watch for

- If I have been paying rent every lap with no purchase opportunity, I am likely to get one soon. Stay disciplined (don't drop below the floor) but be ready to buy the moment an unowned tile appears.
- If I have already bought a tile or two early, my cash is lower and my buffer is tighter. In that case, be more conservative on subsequent purchases — check the floor carefully.
- The "recent transfers" line tells me which tiles are now owned. Use it to anticipate where I might be stuck paying rent next lap and to avoid buying tiles that others will never land on (though on an 8-tile circuit with 3 players, most tiles get hit regularly).