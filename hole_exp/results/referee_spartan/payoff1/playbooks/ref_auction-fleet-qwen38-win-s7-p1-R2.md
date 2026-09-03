---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 2950
---
# Playbook

**Budget tracking (CRITICAL):**
- My budget starts at 30 and ONLY decreases when I win a lot. Placing a bid does NOT cost money.
- When I report [budget: N], it must reflect 30 minus the sum of my winning bids on prior lots. Never subtract a current bid from my budget.
- Before bidding in the final round, confirm: remaining budget = 30 − (sum of prices I paid for lots already won). My bid must not exceed this.

**Opening bids (round 1 of 2):**
- Bid roughly 50% of my value to test the field. This signals interest without revealing my ceiling.
- If my value is low (below the estimate by a wide margin) and the minimum raise would leave me with negligible surplus even in round 2, consider passing.
- Never bid more than my value in round 1.

**Final round (round 2 of 2):**
- This is the only round where the lot is decided. I must commit.
- If (my value) > (standing high bid + minimum raise), I should win this lot. Bid the minimum of (my value − 1) and (my remaining budget). This ensures I win whenever it's profitable and I can afford it.
- The reason for bidding near my full value: if the competition is also aggressive, a conservative bid (like 80% of value) will lose to a competitor who bids 90% or 100%. I have no way to know their value, so I should assume they'll bid up to theirs.
- Only pass if the minimum acceptable winning bid exceeds my value, or if I can't afford it.
- Bid as a whole number. If my value is 33, bid 32 (not 33) to keep a 1-point surplus.

**Reading the competition:**
- Track which bidders are winning lots and at what prices. If a bidder consistently wins at or near estimate, they likely value lots high and will bid aggressively. Against them, I need to be willing to bid near my full value.
- If a bidder passed a lot, they may be budget-constrained or valuing it low. I can sometimes win those cheaper.
- If two bidders seem to be in a war (both raising), I should be cautious about entering unless my value is significantly above the current standing bid.

**When to pass:**
- Round 1: Pass if my value is so low that even winning at the minimum raise gives me ≤ 1 surplus, or if I've spent nearly all my budget on prior lots.
- Round 2: Pass only if (standing high + minimum raise) ≥ my value, or if my remaining budget is less than (standing high + minimum raise).

**Overall priority:**
- My score is total surplus across all lots. I should try to win every lot where my value exceeds what I'd pay.
- Since I can't see future lots, the safe rule is: win every profitable lot. The only reason to skip a profitable lot is if I can't afford it without going negative.
- The biggest risk is underbidding in round 2 and losing a lot I could have won profitably. Always bid up to my value (capped by budget) in the final round.

**Tie-breaking:**
- If I bid the same amount as another bidder, I may lose the tie. When possible, bid 1 above the expected competitor bid rather than matching it.