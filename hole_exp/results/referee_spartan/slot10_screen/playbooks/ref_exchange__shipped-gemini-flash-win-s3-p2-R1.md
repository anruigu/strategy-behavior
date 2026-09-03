---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1769
---
### Build Phase Strategy
- Remember that only settlements (1 wood, 1 brick, 1 grain, 1 ore for 3 points) and roads (1 wood, 1 brick for 1 point) exist in this ruleset; do not hoard grain/ore expecting "cities".
- When I have at least 1 wood, 1 brick, 1 grain, and 1 ore, reply `[build: settlement]`.
- When I have at least 1 wood and 1 brick, but lack grain or ore and cannot make a settlement, reply `[build: road]`.
- If neither cost is met, reply `[build: none]`.

### Trade Offer Strategy
- Track my exact missing resources for a settlement (and secondarily for a road).
- When creating an offer, give away my surplus resources (resources of which I have more than 1, or resources I do not need if building a road) in exchange for the exact resource(s) I lack to complete a settlement. Target the player who holds the resource I need and has a deficit of what I am offering.
- Do not trade away a resource if it drops my count of that resource below 1 unless it directly completes a buildable combination that yields higher net points this round.
- If I already hold the exact set to build a settlement, reply `[offer: none]` unless I have surplus resources to convert into materials for future rounds.

### Accept Phase Strategy
- When evaluating incoming offers, simulate the resulting inventory from accepting each offer or combination of offers.
- Accept an offer if and only if it enables an immediate settlement build this round, or moves me strictly closer to a settlement/road without destroying an existing build opportunity.
- Reject offers that ask for resources I need to build this turn unless what I receive in return still allows the build.
- If no incoming offer improves my ability to build immediately or in the next round, reply `[accept: none]`.