---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 7
round: 3
chars: 4566
---
**Playbook**

When I sit down to a round, I compute for every (resource I give, resource I take) pair whether a trade is mutually beneficial: my gain = qty_taken × my_value(taken) − qty_given × my_value(given) must be > 0, and their gain = qty_given × their_value(given) − qty_taken × their_value(taken) must be ≥ 2. If any such trade exists, I make it. I never hold when a valid trade is on the table — a held round is a lost round with no compensating benefit.

**Quantities are hard-capped at 1 to 3.** When I find a theoretically profitable pair, I must check that both quantities fall within [1, 3]. If the ratio that satisfies both gain conditions requires a quantity above 3, I scan all valid (qty_give, qty_take) pairs in [1,3]×[1,3] to see if any one works. If none does, that pair is dead for this round and I move on. I never submit a quantity outside 1–3; doing so wastes the round with an invalid offer.

**Before proposing any take, I verify the Guildmaster's current stock of that resource.** The quantity I take must not exceed what they actually hold right now. An offer to take more than they possess is invalid, gets rejected by the referee, and wastes the round. I read their stock directly from the round prompt and treat it as a hard cap on my take quantity. Similarly, the quantity I give must not exceed my own current stock.

I pick the pair and quantities that maximize my gain per round. Because quantities range 1–3, I can skew the ratio: if the resource I take is much more valuable to me than what I give is valuable to them, I take the maximum quantity of the high-value resource (capped by their stock and 3) and give the minimum quantity of the low-value one (minimum 1, capped by my stock). I always check that both quantities are within my current stock and within their current stock respectively.

Before I submit, I calculate their net gain in their published values and write that exact number as the claim. I do not inflate or deflate it. If their true gain is below 2, I do not submit that offer — I look for a different pair or quantity split that pushes their gain to 2 or above.

I treat the Guildmaster's published values as the only fixed input I can rely on. My private values tell me what to chase (resources where my value exceeds theirs) and what to spend (resources where my value is below theirs). The gap between my value and their published value on a resource is my edge on that resource; the wider the gap, the more I should push quantity toward it.

**I do not use a resource as a give-resource if my value equals their value on it, unless I have verified the actual numbers work within the 1–3 cap.** When my value equals their value on the given resource, their gain condition requires qty_given > qty_taken (in that resource's value terms), which means I am giving up more units than I receive. Combined with the 1–3 cap, this almost always makes my gain negative. I check the arithmetic explicitly before relying on such a pair.

I recompute available trades from scratch each round using current stocks, because previous trades shift both my holdings and theirs. A resource I couldn't afford last round may be in play now, and a resource that was abundant last round may be depleted.

**Exhaustive check before holding:** Before I hold, I enumerate every (give, take) pair where I hold at least 1 of the give-resource and they hold at least 1 of the take-resource. For each pair, I check whether any (qty_give, qty_take) with 1 ≤ qty_give ≤ min(3, my_stock) and 1 ≤ qty_take ≤ min(3, their_stock) satisfies both my gain > 0 and their gain ≥ 2. If I find at least one valid split across all pairs, I take the one that maximizes my gain. Only if no pair has any valid split do I hold. This check is cheap: at most 5×4 pairs × 3×3 quantity combinations = 180 checks, and in practice the value comparisons eliminate most pairs immediately.

**Identifying a dead end early:** If every resource I hold is valued by me at ≥ what they value it (i.e., I possess no resource where their_value > my_value), then no trade I make can give them a positive gain, let alone ≥ 2. In that situation, holding is correct for every remaining round regardless of what else I might hold. I check this condition at the start of each round; if it holds, I hold immediately without enumerating pairs.

When no mutually beneficial trade exists within the 1–3 quantity constraint (every pair either gives me negative gain, gives them a gain below 2, or requires a quantity outside 1–3), I hold. This is the only correct use of hold.