---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 2627
---
### Resource Evaluation & Game Mechanics
- The only structures available to build are a **Settlement** (1 wood, 1 brick, 1 grain, 1 ore = 3 points) and a **Road** (1 wood, 1 brick = 1 point).
- Value resources strictly by their utility toward complete settlement sets (and roads as fallback). Surplus grain and ore beyond what is matched by wood and brick are dead weight unless converted.
- Settlements are worth 3x the points of roads. Preserve wood and brick in early/mid rounds to assemble settlements rather than burning them on 1-point roads, unless it is the final round or holding provides no path to future settlements.

### Offer Phase
- When I lack a resource to complete a settlement (or road), identify the specific missing resource and offer a surplus resource (one with count > 1 or count exceeding matching components) to an opponent who currently holds what I need.
- Tailor offers to opponent needs: offer a resource they lack or have zero of in exchange for a resource they have in surplus (count > 1).
- Never offer away a scarce resource (a resource where my count is 1 and essential for a target build) unless the trade directly completes a settlement that round.
- In the final round, make an aggressive offer targeting the exact missing piece for a final settlement or road.

### Accept Phase
- Format acceptances precisely: reply with `[accept: P<k>]` naming the proposing player (e.g. `[accept: P1]`), not my own index.
- Before accepting any incoming trade, verify that it preserves or improves my ability to build a settlement that round, or meaningfully balances my inventory for future rounds.
- Reject any offer that takes away a scarce component needed for my build.
- Reject trades that supply duplicate resources I already have in surplus while draining resources opponents need, unless the incoming resource directly enables a build.
- Be cautious when trading with the point leader; do not feed them the exact missing piece for a settlement unless the trade equally guarantees my own settlement build.

### Build Phase
- When I have at least 1 wood, 1 brick, 1 grain, and 1 ore, choose `[build: settlement]`.
- When I have at least 1 wood and 1 brick but lack grain or ore:
  - In round 5 (final round), always choose `[build: road]`.
  - In rounds 1–4, choose `[build: none]` if preserving wood and brick gives a realistic chance to acquire missing grain/ore for a settlement next round. Only build a road if inventory is completely blocked or surplus brick/wood permits it without endangering future settlements.
- When I lack the requirements for either structure, choose `[build: none]`.