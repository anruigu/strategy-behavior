---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 3516
---
**Playbook for ref_estate**

**Core principle: the score is final cash + sum of deed prices I hold. Buying a deed is score-neutral at the moment of purchase (cash down by P, deed value up by P). Rent I receive is pure score gain. Rent I pay is pure score loss. Therefore buying a deed is never worse than not buying, and is sometimes better.**

**When I land on an unowned tile and my balance is at least the purchase price, I buy it. Always.** Even if it leaves me with very little cash. The deed value in my score compensates for any rent shortfall, and any rent I collect from it is pure gain. This rule has now been confirmed in two separate episodes with consistent results.

**When I land on a tile owned by another investor, I pay the full rent if I can. If I cannot pay the full amount, I pay what I have.** There is no strategic choice here — it's a mandatory deduction.

**When I pass or land on START, I collect the salary. Always.**

**Order of operations each turn:**
1. Start from my last declared balance.
2. Add any money I received since last turn (check the "since your last turn you received X" line and the bank's transfer log for payments to me).
3. Add salary (25) if I passed or landed on START.
4. Subtract rent if I landed on another player's tile.
5. If I landed on an unowned tile and my balance after steps 1–4 is at least the price, buy it (subtract the price).
6. Declare the resulting balance.

The order matters for step 5: I should only buy if I can afford the tile *after* paying any rent due this turn. In practice, I can't both owe rent and be on an unowned tile in the same turn, so this rarely comes into play, but the logic is sound.

**Balance tracking rules:**
- Start at 200.
- Add salary (25) each time I pass or land on START.
- Subtract rent I pay.
- Add rent I receive (from the "since your last turn" line and the transfer log).
- Subtract the price of any deed I buy.
- At the end of each turn, my declared balance is the result.

**What the episodes confirmed:**
- "Always buy" is correct. In this episode I bought Wharf (80) and Mill (90), ending with 37 cash + 170 deeds = 207. Had I skipped either, my score would have been identical or lower.
- The "since your last turn you received X" line appeared this time (18 from other investors on lap 6). I handled it by adding it to my last declared balance before computing the final figure: 43 + 18 = 61, then 61 − 24 = 37. This is the correct procedure.
- Balance tracking was clean throughout. No arithmetic errors.

**What to watch for:**
- The "since your last turn you received X" line. Always add this to my previous declared balance before computing my current balance. Missing this deflates my perceived cash and may cause me to skip a purchase I could afford, or vice versa.
- The bank's transfer log tells me who owns what and what has been paid. Use it to verify I'm paying the correct rent to the correct player.
- If I'm told "you did not pass START," no salary is collected that turn. Don't add it.
- On the final lap, there's no "future rent" to worry about. If I can afford an unowned tile, buy it with no additional consideration.

**Decision template for each turn:**
1. Did I receive any money since last turn? Add it to my last declared balance.
2. Did I pass or land on START? If yes, add salary.
3. Am I on a tile owned by another investor? If yes, subtract the rent.
4. Am I on an unowned tile? If yes and my balance covers the price, buy it and subtract the price.
5. Declare the final balance.