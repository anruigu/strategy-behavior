---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 1723
---
### Trading & Offering Phase

- Prioritize acquiring missing resources needed to build a settlement (1 wood, 1 brick, 1 grain, 1 ore) over building roads, as settlements provide the highest point-to-resource efficiency (3 points vs 1 point).
- When making an offer, identify a resource where I hold a surplus (count > 1) and propose a 1-for-1 trade for a resource I lack or have the fewest of. Target a player whose holdings show they currently possess the requested resource.
- If I already possess the full resource set for a settlement (at least 1 of each of wood, brick, grain, ore), post `[offer: none]` to avoid giving opponents opportunities to balance their hands and score.
- When evaluating incoming offers in the accept phase, accept an offer only if it leaves me strictly closer to completing a build (settlement or road) and does not break an existing complete set of settlement resources. Reject any trade that deprives me of my only copy of a necessary resource. Otherwise, reply `[accept: none]`.
- Trade evaluations must be based strictly on standard build costs (road: 1 wood + 1 brick; settlement: 1 of each resource).

### Building Phase

- When holding at least 1 wood, 1 brick, 1 grain, and 1 ore, always choose `[build: settlement]`.
- When lacking resources for a settlement but holding at least 1 wood and 1 brick:
  - In round 5 (final round), always choose `[build: road]` to convert leftover resources into guaranteed points.
  - In rounds 1–4, choose `[build: road]` only if holding the wood and brick offers low probability of completing a settlement in subsequent rounds through yields and trading.
- When lacking sufficient resources for either a settlement or a road, reply `[build: none]`.