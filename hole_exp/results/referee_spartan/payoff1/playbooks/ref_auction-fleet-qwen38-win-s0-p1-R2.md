---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3105
---
# Playbook

**Read the starting budget.** The rules state my starting budget explicitly. I use exactly that number as my reference. I never assume a different starting amount. In this episode I used 100 when the stated budget was 30 — every subsequent report was wrong by the same offset.

**Budget tracking.** I only subtract from my budget when I win a lot (I am the high bidder at the end of the lot). I never subtract for bids I lose. Each time I report my budget, I compute: stated starting budget minus the sum of all lot prices I have won so far. I recount from the "Results so far" section shown to me. If I'm uncertain, I recompute from scratch.

**Budget as a constraint.** If the minimum raise on a lot would exceed my remaining budget, I pass. I do not bid into a position where my committed price exceeds what I can pay. This means on early lots with high prices relative to my budget, I may need to pass even if the lot is valuable to me, preserving budget for lots I can actually afford to win.

**Opening a lot when no one has bid.** I open at the minimum raise. This is the cheapest way to signal interest. If no one else bids, I win at the minimum. If someone does bid, I have a full second round to respond. Opening high just locks in a higher floor for no benefit.

**Round 1 of a contested lot.** If the current high bid is below my value, I bid the minimum raise to stay in. I do not bid above the minimum raise in round 1. Bidding high in round 1 only raises the floor for round 2 and costs me if the opponent calls.

**Round 2 (final round) when I want to win and can afford it.** I bid exactly the minimum raise. This is my last chance to commit, and I commit at the lowest legal price. If the minimum raise exceeds my value, I pass. If the minimum raise exceeds my remaining budget, I also pass — winning a lot I can't pay for is not a win.

**When to pass.** I pass when:
- The minimum raise would put my price at or above my value.
- The minimum raise would exceed my remaining budget.
- The lot's value to me is low relative to my remaining budget and I suspect better-value lots are still ahead.

**Budget allocation across lots.** Before bidding on a new lot, I estimate the likely final price (at minimum, the current high bid plus one minimum raise). If winning at that price would leave me with insufficient budget for remaining lots I expect to want, I bid more conservatively or pass. I prioritize lots with the highest surplus (value minus likely price) per dollar of budget consumed.

**What did not work in my last play:**
- I used a starting budget of 100 when the stated budget was 30. Every budget report was therefore wrong. The fix is mechanical: read the number the rules give me and start from there.
- I won lots at 37, 20, and 22 (total 79) with a budget of only 30. If the budget is a hard constraint, I was over from the first win. I need to check affordability before committing in round 2, not just check whether the price is below my value.
- The minimum-raise strategy itself worked well. I kept prices low and won 3 of 5 lots. I will keep doing this.