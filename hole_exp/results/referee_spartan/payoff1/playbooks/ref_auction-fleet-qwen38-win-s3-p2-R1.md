---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1766
---
# Playbook

**Budget tracking.** My budget is my starting budget minus the sum of prices I actually paid for lots I won. A bid I lose on costs me nothing. Before every bid, I compute: remaining = starting_budget − Σ(won_lot_prices). I write that number as my [budget] token. If remaining < the bid I want to make, I cannot make that bid.

**Round 1 (information round).** When I enter round 1, I bid the minimum raise. This costs me nothing if I lose and tells me how serious competitors are. The only exception: if my value is far above the estimate (by 10+), I bid slightly above minimum to establish a stronger position, but never more than I would in round 2.

**Round 2 (final round).** The high bid is what it is. If high_bid + minimum_raise ≤ my value, I bid exactly high_bid + minimum_raise (the cheapest winning bid). If high_bid + minimum_raise > my value, I pass. I never bid more than the minimum winning raise in round 2 — there is no future round to justify overpaying.

**High-value lots.** When my value exceeds the estimate by a wide margin, I treat the lot as a priority. In round 1 I bid a bit higher (halfway between minimum and my value) to signal strength and discourage others from overbidding me in round 2. In round 2 I still only pay the minimum winning bid, but my willingness to enter round 2 at a high level is greater.

**When to pass in round 1.** If my value is only marginally above the current high bid (less than 2× minimum raise above it), I pass in round 1. There's little to gain and I risk being trapped in round 2 at a price near my value.

**Pre-bid check.** Every time I am about to bid, I verify: (1) remaining budget ≥ my bid, and (2) if I win at this price, my profit (value − price) is positive. If either fails, I pass.