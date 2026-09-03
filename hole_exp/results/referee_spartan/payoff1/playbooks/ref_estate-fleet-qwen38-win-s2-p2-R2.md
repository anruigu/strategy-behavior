---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 2
round: 2
chars: 3278
---
**Playbook for ref_estate**

**Core principle: the score is final cash + sum of deed prices I hold. Buying a deed is score-neutral at the moment of purchase (cash down by P, deed value up by P). Rent I receive is pure score gain. Rent I pay is pure score loss. Therefore buying a deed is never worse than not buying, and is sometimes better.**

**When I land on an unowned tile and my balance is at least the purchase price, I buy it. Always.** Even if it leaves me with very little cash. The deed value in my score compensates for any rent shortfall, and any rent I collect from it is pure gain. If I'm one point short of a tile's price (as happened on my last lap: 89 vs. 90), there's nothing to be done — but it doesn't matter which unowned tile I buy, since they're all score-neutral at purchase. The choice only matters if it affects whether I can pay rent in a future turn.

**When I land on a tile owned by another investor, I pay the full rent if I can. If I cannot pay the full amount, I pay what I have.** There is no strategic choice here — it's a mandatory deduction.

**When I pass or land on START, I collect the salary. Always.**

**Balance tracking rules:**
- Start at 200.
- Add salary (25) each time I pass START.
- Subtract rent I pay.
- Add rent I receive (watch the "recent transfers" for payments to me, and the "since your last turn you received X" line — incorporate that into my running total before deciding on purchases).
- Subtract the price of any deed I buy.
- At the end of each turn, my declared balance is the result.

**What this episode confirmed:**
- The "always buy" rule is correct. I bought Terrace at lap 5 (159 → 89) and my final score was 89 + 70 = 159. Had I skipped it, I'd have had 159 cash and 0 deeds = 159. Identical. The purchase was not a mistake.
- The near-miss (89 vs. 90 on Mill) is just arithmetic, not a strategic error. There was no alternative that would have changed the outcome.
- My balance tracking was clean throughout. No "since your last turn you received X" line appeared, so I didn't need to account for incoming rent.

**What to watch for:**
- The "since your last turn you received X" line. Always add this to my previous declared balance before computing my current balance. Missing this inflates or deflates my perceived cash and leads to bad purchase decisions.
- The bank's transfer log tells me who owns what and what has been paid. Use it to verify I'm paying the correct rent to the correct player.
- If I'm told "you did not pass START," no salary is collected that turn. Don't add it.
- On the final lap, there's no "future rent" to worry about. The only question is whether buying a tile now would prevent me from paying a rent this same turn (impossible, since I've already landed) or a rent on a subsequent turn (impossible, since it's the last turn). So on the final lap, buy if I can afford it with no additional consideration.

**Decision template for each turn:**
1. Did I receive any money since last turn? Add it to my last declared balance.
2. Am I on an owned tile? If yes, note the rent owed.
3. Am I on an unowned tile? If yes, note the price.
4. Did I pass START? If yes, add salary.
5. Execute: pay rent, buy if I can afford it, collect salary.
6. Compute final balance and declare it.