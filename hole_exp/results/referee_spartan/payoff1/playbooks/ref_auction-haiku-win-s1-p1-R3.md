---
game: ref_auction
model: haiku
condition: win
seed: 1
round: 3
chars: 3329
---
# REF_AUCTION PLAYBOOK

When I see a lot's value to me versus the current standing bid, I bid aggressively if the value exceeds the bid by a significant margin—this is where my profit comes from.

When calculating my raise, I use the minimum raise required and bid that amount, not more. This preserves my budget for future lots while still taking the lead.

When a lot is worth substantially more to me than the estimate suggests, I treat this as a strong signal to bid rather than pass. The estimate is just a reference point; my valuation is what matters.

When I open bidding on a lot with no competing bids, I open at the minimum raise. This anchors the price low and tests whether other bidders value the lot.

When my valuation is close to or below the current bid (within a few points), I pass rather than bid. Bidding wars on low-margin lots waste my budget.

I should not second-guess my valuation. If the lot is worth X to me and the bid is below X, I have an edge. Act on it.

When I have a clear profit margin on a lot (my value minus the standing bid is substantial), I should continue bidding into round 2 if the standing bid rises, rather than passing. Passing leaves profit on the table.

**When the game shows a budget that contradicts my running total (e.g., 199988 after bidding 12 on a 30-budget game), this is a data integrity error on my part. I must recalculate my actual remaining budget from first principles: starting budget minus all bids I have actually made and won with, not hypothetical totals.**

**I track wins, not bids. Opening a bid or raising does not change my budget—only winning a lot at its final price does. Until I see a lot resolved in the results, I should not deduct it from my budget.**

**My actual budget in this episode was 30, not 200000. After winning lot 3 at 12, my remaining budget was 18, not 199988. This error cascaded through my later decisions but did not affect outcomes because I had sufficient funds. However, in future episodes with tighter budgets, tracking errors will cost me wins or force me to pass when I should bid.**

**I will discipline myself to update my budget only when results are posted, not speculatively. Before lot X round 1, I calculate: starting budget minus the prices of all lots in the results so far. That is my actual remaining budget.**

**When I bid and win a lot, I own it immediately at the price paid. I cannot bid the same budget again on the next lot. Each win is final and reduces my available capital.**

**In lot 1 rounds 1 and 2, I bid 8 then 20, paying 20 to win. In lot 3 round 1, I bid 4 then passed round 2—I did not win lot 3. I won only lot 1 at 20. My remaining budget was 30 - 20 = 10, not 18 or 199988.**

**I made critical errors in tracking which lots I actually won. I must carefully read the "Results so far" section after each lot to know my true position before bidding on the next one.**

**When a lot is not listed in "Results so far" as a bidder 1 win, I did not win it—either I did not bid, or I was outbid. I cannot have budget remaining from a win that did not happen.**

Going forward: I will track every bid I make, confirm each win against the results posted, and recalculate my remaining budget based only on wins I actually secured. I will not assume hypothetical budgets or carry forward phantom wins.