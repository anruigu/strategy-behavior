---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 0
round: 1
chars: 1742
---
### Trading & Offering Phase

- When evaluating my hand during the offer phase, prioritize acquiring missing resources needed to build a settlement (1 wood, 1 brick, 1 grain, 1 ore) over building roads, since settlements provide the highest point-to-cost ratio (3 points vs 1 point).
- When making an offer, identify a resource where I have a surplus (2 or more) and propose a 1-for-1 trade for a resource I currently have 0 of. Target a player whose holdings show they actually possess the requested resource.
- If I already possess the full resource set for a settlement (at least 1 wood, 1 brick, 1 grain, 1 ore) and am in the lead, post `[offer: none]` to prevent opponents from balancing their hands.
- When evaluating incoming offers in the accept phase, accept only if the trade directly provides a missing resource needed for a settlement without breaking an existing settlement set, or if it converts an unusable surplus into a needed resource. Otherwise, reply `[accept: none]`.
- Do not accept trades based on nonexistent mechanics (such as development cards or cities); base all trade values strictly on the cost of settlements and roads.

### Building Phase

- When holding at least 1 wood, 1 brick, 1 grain, and 1 ore, always choose `[build: settlement]`.
- When lacking resources for a settlement but holding at least 1 wood and 1 brick:
  - If it is round 5 (the final round), build a road (`[build: road]`) to secure immediate points from leftover resources.
  - In rounds 1–4, choose `[build: road]` only if holding on to the wood and brick will not help complete a settlement in subsequent rounds via expected yields and trading.
- When lacking sufficient resources for either a settlement or a road, reply `[build: none]`.