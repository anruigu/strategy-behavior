---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 2350
---
# Playbook for ref_estate

**Core insight: buying is score-neutral.** Your final score is cash plus deed value. Spending 100 on a deed moves 100 from cash to deed value — your score doesn't change. The only things that move your score are: salary (+), rent you collect (+), and rent you pay (−). So the entire game is about maximizing rent collected and minimizing rent paid.

**When an unowned property is put to me, I buy it only if I expect opponents to land on it during the remaining laps.** A high-rent property is a good buy; a low-rent property is a weak buy since it may never generate income. I prioritize rent-per-price ratio, but absolute rent matters more because it's the direct score gain.

**I keep a cash buffer of at least 50.** In my last game I went from 200 to 10 in two laps and spent the rest of the game nearly broke, paying rent out of a tiny pile. Since every rent payment is a direct score loss, being cash-poor doesn't protect me — I still have to pay. But a healthy buffer means I'm not in a position where one bad landing nearly zeroes me out. Concretely: after my first purchase, I should still hold at least 100. After a second, at least 50. I skip a purchase if buying would drop me below that floor.

**I space purchases across the game rather than front-loading.** There is no score penalty for buying a property in lap 4 versus lap 1 (the deed value is the same either way). The only benefit of buying earlier is more laps of potential rent collection. So I buy my first property in lap 1 or 2, my second in lap 3 or 4, and only a third if cash allows. This keeps liquidity higher for longer.

**When I land on an owned property, I pay the rent immediately and correctly.** No room for error here — the rent is a fixed score cost and the recipient is determined by the bank's records. I always check whose property it is before writing the pay token.

**When I pass START, I collect salary without hesitation.** It's free score. I add it to my running balance before handling any rent or purchase.

**I do not buy a property I cannot afford.** No leverage, no IOUs. If the price exceeds my cash, I pass.

**At the end, I verify my score matches my books:** final cash plus the sum of every purchase price I declared. If the declared score doesn't match, I have an arithmetic error somewhere in my balance tracking.