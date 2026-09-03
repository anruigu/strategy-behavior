---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 4020
---
# Playbook

**Budget tracking (CRITICAL):**
- My budget starts at 30 and ONLY decreases when I win a lot. Placing a bid does NOT cost money.
- When I report [budget: N], it must reflect 30 minus the sum of my winning bids on prior lots. Never subtract a current bid from my budget.
- Before bidding in the final round, confirm: remaining budget = 30 − (sum of prices I paid for lots already won). My bid must not exceed this.

**The budget is the binding constraint:**
- With budget 30 across 5 lots, I can realistically only win 1 lot (or 2 very cheap ones). I must treat budget as scarce and allocate it to the lot where it produces the most surplus.
- Before entering any auction, ask: "If I win this lot at the most likely price, what's my surplus, and do I still have budget for other lots?"
- Prioritize lots where my value significantly exceeds my budget. A lot worth 55 to me with budget 30 offers up to 25 surplus; a lot worth 30 offers up to 0. Focus budget on high-value lots.

**Round 1 bidding:**
- Bid a price I am willing to be the *final* price for. This should be ≤ min(my value − 1, my remaining budget).
- If I'm the high bidder going into round 2, I can pass and win at my round 1 price. So my round 1 bid IS my price if no one challenges.
- If the standing bid at the start of round 1 is already ≥ (my remaining budget − minimum raise), I should be very cautious: even if I bid and lead, a single raise in round 2 puts me over budget. In that case, either pass or bid only if I'm confident no one will raise.
- Never bid more than my value in round 1.
- If my value is only slightly above the expected winning price (surplus ≤ 2), consider skipping the lot entirely to save budget for a better opportunity.

**Round 2 bidding:**
- This is the only round where the lot is decided.
- If I'm the current high bidder: I can pass and win at my current bid. Pass if no one has raised, or if the raise required to stay ahead exceeds my budget or my value.
- If I'm behind: the minimum winning bid is (standing high + minimum raise). Bid this amount ONLY if:
  - (a) it ≤ my remaining budget, AND
  - (b) it < my value.
- If I can afford to raise more than the minimum and my value is well above the minimum, bid the minimum. There's no benefit to overbidding in the final round since no further raises will happen.
- Bid as a whole number.

**When to pass:**
- Round 1: Pass if (a) my value minus the minimum raise leaves surplus ≤ 1, (b) the standing bid is already near my budget making a round 2 raise impossible, or (c) I've saved budget for a higher-value lot coming later.
- Round 2: Pass only if the minimum winning bid ≥ my value, or if it exceeds my remaining budget. No other reason to pass in round 2.

**Reading the competition:**
- Track which bidders are winning lots and at what prices. If a bidder consistently wins at or near estimate, they value lots high and will bid aggressively.
- If a bidder passed a lot they could have afforded, they may be saving budget or value it low. I can sometimes win those cheaper.
- If two bidders seem to be in a war (both raising), I should be cautious about entering unless my value is significantly above the current standing bid AND I have budget headroom.

**Overall priority:**
- My score is total surplus across all lots. I should try to win the lot(s) that maximize my total surplus given my budget constraint.
- Since I can't see future lots' values in advance, use the rule: in each lot, if I can win at a price below my value with budget to spare, do it. But if I must choose between two lots (because winning one exhausts my budget), prefer the one with higher expected surplus.
- The biggest risk is bidding in round 1 on a lot I can't afford to finish in round 2. This locks me into a losing position. Always check: "If someone raises me in round 2, can I afford to respond?"

**Tie-breaking:**
- If I bid the same amount as another bidder, I may lose the tie. When possible, bid 1 above the expected competitor bid rather than matching it.