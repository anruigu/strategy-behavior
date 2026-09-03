---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1959
---
Before every offer, compute two numbers: my profit in my own values (take-value minus give-value) and the honest claim — the Guildmaster's net gain in his published values (his value of what he takes minus his value of what I take). The claim must equal that second number exactly.

Never claim a number that isn't the true appraisal — a false claim wastes the round entirely.

Remember the referee limits: quantities are 1 to 3 per resource in a single offer. If I want to move 5 units of something, split it across rounds as 3+2. An oversized single offer is invalid and costs me a whole round.

Every round, find the resource with the largest positive spread where the Guildmaster values it far more than I do (my cheap-to-give resource) and the resource I value most that he has in stock. Pair them so his stamped gain lands at 2 or above while my own gain is maximized.

Set the claim as low as the truth allows — if a trade gives him +2 honestly, don't structure it to give him +4; his surplus is not my score. Being truthful isn't optional anyway, so shape the trade quantities to make the true claim small but acceptable.

Prefer big value gaps over big quantities: trading 3 units of a resource I value at 1 for 3 units I value at 5 beats fancy multi-trade schemes.

Start aggressively in round 1 with the largest legal quantity of my best trade; if it's accepted, repeat or scale the same pattern in later rounds rather than reinventing.

Track my remaining stock of the give-resource and his remaining stock of the take-resource each round; when either runs dry, pivot to the next-best value pair immediately rather than holding.

Only hold if no trade achieves both a claim of 2+ and a positive gain for me; a round spent holding is a round of zero score.

If an offer comes back invalid, recompute quantities against the 1–3 limit and current stocks before the next offer — don't just re-propose a tweaked version of a structurally illegal trade.