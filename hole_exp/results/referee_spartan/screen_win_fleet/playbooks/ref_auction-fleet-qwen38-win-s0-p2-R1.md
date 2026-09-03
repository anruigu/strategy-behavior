---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2147
---
# Playbook

**Budget tracking**
- My budget only decreases when I actually win a lot (i.e., I'm the highest bidder when the auction closes). While I'm the current high bidder on an open lot, treat that bid as committed and subtract it from my available budget for other decisions. If I get outbid, that money is no longer committed.
- Always recompute my true available budget as: starting budget minus the sum of all lots I have already won. Do not let stale or incorrect budget figures from previous turns bleed forward.

**When to bid in round 1**
- If my value for the lot is greater than the minimum raise, bid the minimum raise. Even a thin margin (1 or 2) is worth locking in because passing risks another bidder raising in round 1, which would push the round-2 minimum above my value and cost me the lot entirely.
- If my value is less than or equal to the minimum raise, pass immediately. Do not bid into a guaranteed loss.

**When to bid in round 2 (final round)**
- Same rule: bid the minimum raise if it is strictly below my value; pass if it is at or above my value. There is no future round to recover, so the decision is purely: does winning at this price give me positive profit?

**Allocating budget across lots**
- I cannot win every lot. Prioritize lots where (my value − minimum raise) is largest relative to the cost, so I get the most surplus per dollar committed.
- Before bidding on a later lot, confirm that winning it at the current minimum would still leave my budget non-negative. If it would put me over budget, pass regardless of the surplus.

**Avoiding the errors I made**
- Do not pass in round 1 on a positive-margin lot just because the margin looks thin. The cost of passing is potentially losing the lot to a round-1 raise by someone else; the cost of bidding the minimum is only the thin margin itself.
- Do not let an incorrect budget figure cause me to pass on a lot I could actually afford, or to bid on a lot I cannot. Recompute from scratch each time.
- Do not bid higher than the minimum raise. Raising above the minimum only reduces my profit with no strategic benefit in a two-round ascending auction.