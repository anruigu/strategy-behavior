---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1824
---
### Resource Evaluation & Game Mechanics
- Always remember that the only structures available to build are a **Settlement** (1 wood, 1 brick, 1 grain, 1 ore = 3 points) and a **Road** (1 wood, 1 brick = 1 point). There are no cities or other structures.
- Value resources strictly by their utility toward complete settlement sets (and roads as fallback). Surplus grain and ore beyond what is matched by wood and brick are dead weight unless converted.

### Offer Phase
- When I hold unbalanced resources (e.g., surplus grain/ore but lacking wood/brick), identify the missing component needed to complete a settlement and send an offer giving my surplus resource to a player who actually possesses what I need.
- Never trade away a scarce resource (especially wood or brick if I have only 1) unless doing so directly enables a settlement in the current round.
- In the final round, check which single resource is missing for a final build (wood or brick for road/settlement) and target the player holding it with an offer of whatever surplus I have.

### Accept Phase
- Before accepting any incoming trade, verify that it preserves or improves my ability to build a settlement that round.
- Reject any offer that takes away a scarce component (reducing wood or brick below 1 when I need it for a build).
- Reject trades proposed by the current point leader if accepting would allow them to build a settlement, unless it also immediately guarantees my own settlement build.

### Build Phase
- When I have at least 1 wood, 1 brick, 1 grain, and 1 ore, choose `[build: settlement]`.
- When I have 1 wood and 1 brick but lack grain or ore, and it is the final round (or holding resources provides no path to future settlements), choose `[build: road]`.
- When I lack the requirements for either structure, choose `[build: none]`.