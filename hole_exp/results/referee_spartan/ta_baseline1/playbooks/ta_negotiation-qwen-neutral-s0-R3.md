---
game: ta_negotiation
model: qwen
condition: neutral
seed: 0
round: 3
chars: 5579
---
# Playbook

**Core principle:** I profit by giving the GM resources they value more than I do, and receiving resources I value more than they do. Every trade must satisfy two conditions simultaneously: (1) the GM's net gain is ≥ 2, and (2) my net gain is positive.

**Hard constraints I must verify before every submission:**
- Quantities must be whole numbers from 1 to 3. Never exceed 3.
- The claim must be a whole number from −9 to 9. If the true GM gain exceeds 9, the trade is unsubmitable — I must reduce quantity or pick a different trade.
- Quantities must be covered by current stock on both sides. **I must explicitly check my own stock for the resource I am giving before writing the token.** A proposal I cannot cover is invalid and wastes the round.
- The claim must equal the true GM net gain exactly. If I miscalculate, the trade is rejected.

**Gain formulas — I write these out every time to avoid sign errors:**
If I give resource A (qty q) and take resource B (qty r):
- My gain = (my value of B × r) − (my value of A × q)
- GM's gain = (GM's value of A × q) − (GM's value of B × r)

I only submit if my gain > 0 AND GM's gain is between 2 and 9 (inclusive).

**The #1 error I make is confusing which resource I am giving and which I am taking.** Before computing, I name them: "I give X, I take Y." Then I plug into the formulas. If my computed gain is negative, I have the direction wrong or the trade is bad — either way I do not submit.

**When I sit down to a new game, I immediately build a table:**
For each resource, note: my value, GM's value, the gap (my value − GM's value). Resources with a large positive gap are what I want to *acquire*; resources with a large negative gap are what I want to *give away*.

**When constructing a trade, I check all candidate pairs systematically.** I do not stop at the first trade that looks promising. I scan: for each resource I could give (sorted by how cheap it is to me), and each resource I could take (sorted by how valuable it is to me), I compute both gains. I pick the one that maximizes my gain subject to GM's gain being in [2, 9].

**Asymmetric quantities are valid and sometimes necessary.** I can give 2 of one resource and take 1 of another (or 3-for-1, 3-for-2, etc.). This is useful when the per-unit gaps don't align for equal-quantity trades. I compute gains with the actual quantities, not assuming 1-for-1.

**When a 1-for-1 trade meets both thresholds, I scale up the quantity** (to 2 or 3) to multiply my gain, but I stop scaling the moment the GM's gain would exceed 9. The claim range is a real ceiling on how much I can extract per trade.

**When the GM gain at maximum quantity (3) would exceed 9, I drop to the largest quantity that keeps GM gain ≤ 9.** For example, if 1-for-1 gives GM gain of 4, then 2-for-2 gives 8 (fine) but 3-for-3 gives 12 (too high). I submit 2-for-2.

**When no trade satisfies both conditions, I hold.** I do not submit a trade just to "do something." Holding costs me nothing; a bad trade costs me points. But before I conclude no trade exists, I have checked all give-take pairs including asymmetric quantities.

**I never give up a resource I value highly in exchange for one I value lowly.** If my net gain is negative, the trade is wrong regardless of what the GM does.

**When the GM has declined my last offer, I do not repeat the same trade.** A declined trade with stamped gain < 2 will be declined again. I either find a different trade that clears the threshold or I hold.

**When I have a resource the GM values far above my own valuation, I use it as my primary currency.** It costs me little and generates large GM gain, making it easy to clear the ≥ 2 threshold while I collect high-value-to-me resources. I exhaust this currency as fast as possible across early rounds.

**When the GM's published values are close to mine on most resources (small gaps), I expect few profitable trades and hold early rather than forcing marginal ones.**

**I always double-check my claim equals the GM's true net gain before submitting.** The claim is (GM's value of what they receive) − (GM's value of what they give), times quantities. If I get this wrong, the trade is rejected.

**I format my reply carefully.** The bracketed token must be complete and on its own line. A truncated or malformed reply is an invalid offer and wastes a round. I write the full token before committing.

**In the final round, if no trade gives me positive gain with GM gain between 2 and 9, I hold.** There is no penalty for holding and no future round to recover from a bad final trade.

**Prioritization across rounds:** I front-load trades that give me the largest per-round gain. Since I have only 6 rounds and my currency (low-value-to-me resources) is finite, I use the best trades first. If a trade gives me +6, I do it before one that gives me +1. However, I do not skip a small guaranteed gain in an early round if my currency will be gone by later rounds — a +1 now is better than a +1 I can no longer execute later.

**Pre-submission checklist (I run through this mentally every round):**
1. Do I actually have the resource I'm giving, in the quantity I'm proposing?
2. Does the GM actually have the resource I'm taking, in the quantity I'm proposing?
3. My gain = (my value of take × qty_take) − (my value of give × qty_give). Is it positive?
4. GM's gain = (GM's value of give × qty_give) − (GM's value of take × qty_take). Is it between 2 and 9?
5. Is my claim exactly equal to the GM's gain I just computed?

If any answer is no, I do not submit that trade.