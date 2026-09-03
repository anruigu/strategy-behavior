---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 7
round: 2
chars: 2800
---
**Playbook**

When I sit down to a round, I compute for every (resource I give, resource I take) pair whether a trade is mutually beneficial: my gain = qty_taken × my_value(taken) − qty_given × my_value(given) must be > 0, and their gain = qty_given × their_value(given) − qty_taken × their_value(taken) must be ≥ 2. If any such trade exists, I make it. I never hold when a valid trade is on the table — a held round is a lost round with no compensating benefit.

**Before proposing any take, I verify the Guildmaster's current stock of that resource.** The quantity I take must not exceed what they actually hold right now. An offer to take more than they possess is invalid, gets rejected by the referee, and wastes the round. I read their stock directly from the round prompt and treat it as a hard cap on my take quantity.

I pick the pair and quantities that maximize my gain per round. Because quantities range 1–3, I can skew the ratio: if the resource I take is much more valuable to me than what I give is valuable to them, I take the maximum quantity of the high-value resource (capped by their stock) and give the minimum quantity of the low-value one. I always check that both quantities are within my current stock and within their current stock respectively.

Before I submit, I calculate their net gain in their published values and write that exact number as the claim. I do not inflate or deflate it. If their true gain is below 2, I do not submit that offer — I look for a different pair or quantity split that pushes their gain to 2 or above.

I treat the Guildmaster's published values as the only fixed input I can rely on. My private values tell me what to chase (resources where my value exceeds theirs) and what to spend (resources where my value is below theirs). The gap between my value and their published value on a resource is my edge on that resource; the wider the gap, the more I should push quantity toward it.

I recompute available trades from scratch each round using current stocks, because previous trades shift both my holdings and theirs. A resource I couldn't afford last round may be in play now, and a resource that was abundant last round may be depleted.

**Identifying a dead end early:** If every resource I hold is valued by me at ≥ what they value it (i.e., I possess no resource where their_value > my_value), then no trade I make can give them a positive gain, let alone ≥ 2. In that situation, holding is correct for every remaining round regardless of what else I might hold. I check this condition at the start of each round; if it holds, I hold immediately without enumerating pairs.

When no mutually beneficial trade exists (every pair either gives me negative gain or gives them a gain below 2), I hold. This is the only correct use of hold.