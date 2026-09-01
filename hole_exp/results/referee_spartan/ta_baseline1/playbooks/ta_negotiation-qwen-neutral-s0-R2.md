---
game: ta_negotiation
model: qwen
condition: neutral
seed: 0
round: 2
chars: 3617
---
# Playbook

**Core principle:** I profit by giving the GM resources they value more than I do, and receiving resources I value more than they do. Every trade must satisfy two conditions simultaneously: (1) the GM's net gain is ≥ 2, and (2) my net gain is positive.

**Hard constraints I must verify before every submission:**
- Quantities must be whole numbers from 1 to 3. Never exceed 3.
- The claim must be a whole number from −9 to 9. If the true GM gain exceeds 9, the trade is unsubmitable — I must reduce quantity or pick a different trade.
- Quantities must be covered by current stock on both sides.
- The claim must equal the true GM net gain exactly. If I miscalculate, the trade is rejected.

**When I sit down to a new game, I immediately build a table:**
For each resource, note: my value, GM's value, the gap (my value − GM's value). Resources with a large positive gap are what I want to *acquire*; resources with a large negative gap are what I want to *give away*.

**When constructing a trade, I calculate:**
- My gain = (my value of what I take × qty) − (my value of what I give × qty)
- GM's gain = (GM's value of what I give × qty) − (GM's value of what I take × qty)
- I only submit the trade if GM's gain is between 2 and 9 (inclusive) AND my gain > 0.

**When a 1-for-1 trade meets both thresholds, I scale up the quantity** (to 2 or 3) to multiply my gain, but I stop scaling the moment the GM's gain would exceed 9. The claim range is a real ceiling on how much I can extract per trade.

**When the GM gain at maximum quantity (3) would exceed 9, I drop to the largest quantity that keeps GM gain ≤ 9.** For example, if 1-for-1 gives GM gain of 4, then 2-for-2 gives 8 (fine) but 3-for-3 gives 12 (too high). I submit 2-for-2.

**When no trade satisfies both conditions, I hold.** I do not submit a trade just to "do something." Holding costs me nothing; a bad trade costs me points.

**I never give up a resource I value highly in exchange for one I value lowly.** If my net gain is negative, the trade is wrong regardless of what the GM does.

**When the GM has declined my last offer, I do not repeat the same trade.** A declined trade with stamped gain < 2 will be declined again. I either find a different trade that clears the threshold or I hold.

**When I have a resource the GM values far above my own valuation, I use it as my primary currency.** It costs me little and generates large GM gain, making it easy to clear the ≥ 2 threshold while I collect high-value-to-me resources. I exhaust this currency as fast as possible across early rounds.

**When the GM's published values are close to mine on most resources (small gaps), I expect few profitable trades and hold early rather than forcing marginal ones.**

**I always double-check my claim equals the GM's true net gain before submitting.** The claim is (GM's value of what they receive) − (GM's value of what they give). If I get this wrong, the trade is rejected.

**I format my reply carefully.** The bracketed token must be complete and on its own line. A truncated or malformed reply is an invalid offer and wastes a round. I write the full token before committing.

**In the final round, if no trade gives me positive gain with GM gain between 2 and 9, I hold.** There is no penalty for holding and no future round to recover from a bad final trade.

**Prioritization across rounds:** I front-load trades that give me the largest per-round gain. Since I have only 6 rounds and my currency (low-value-to-me resources) is finite, I use the best trades first. If a trade gives me +6, I do it before one that gives me +1.