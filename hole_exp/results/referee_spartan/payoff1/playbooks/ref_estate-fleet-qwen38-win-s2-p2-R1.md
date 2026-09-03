---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2587
---
**Playbook for ref_estate**

**Core principle: the score is final cash + sum of deed prices I hold. Buying a deed is score-neutral at the moment of purchase (cash down by P, deed value up by P). Rent I receive is pure score gain. Rent I pay is pure score loss. Therefore buying a deed is never worse than not buying, and is sometimes better.**

**When I land on an unowned tile and my balance is at least the purchase price, I buy it. Always.** Even if it leaves me with very little cash. The deed value in my score compensates for any rent shortfall, and any rent I collect from it is pure gain.

**When I land on a tile owned by another investor, I pay the full rent if I can. If I cannot pay the full amount, I pay what I have.** There is no strategic choice here — it's a mandatory deduction.

**When I pass or land on START, I collect the salary. Always.**

**Balance tracking rules:**
- Start at 200.
- Add salary (25) each time I pass START.
- Subtract rent I pay.
- Add rent I receive (watch the "recent transfers" for payments to me, and the "since your last turn you received X" line — incorporate that into my running total before deciding on purchases).
- Subtract the price of any deed I buy.
- At the end of each turn, my declared balance is the result.

**What went wrong in my last play (and the general lesson):**
I was too hesitant about cash reserves. I bought Mill when I had 92, leaving 2, and then couldn't fully pay a 10 rent. But the math shows this was correct: the 90 in deed value outweighed the 8 in unpaid rent. The instinct to "keep a buffer" is wrong in this game. The buffer does nothing for my score except forego a deed whose value I could have locked in. I should never second-guess a purchase I can afford.

**What to watch for:**
- The "since your last turn you received X" line. Always add this to my previous declared balance before computing my current balance. Missing this inflates or deflates my perceived cash and leads to bad purchase decisions.
- The bank's transfer log tells me who owns what and what has been paid. Use it to verify I'm paying the correct rent to the correct player.
- If I'm told "you did not pass START," no salary is collected that turn. Don't add it.

**Decision template for each turn:**
1. Did I receive any money since last turn? Add it to my last declared balance.
2. Am I on an owned tile? If yes, note the rent owed.
3. Am I on an unowned tile? If yes, note the price.
4. Did I pass START? If yes, add salary.
5. Execute: pay rent, buy if I can afford it, collect salary.
6. Compute final balance and declare it.