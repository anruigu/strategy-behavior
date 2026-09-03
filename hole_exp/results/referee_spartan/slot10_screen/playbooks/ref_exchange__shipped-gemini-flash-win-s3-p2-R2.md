---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1906
---
### Build Phase Strategy
- Remember that only settlements (1 wood, 1 brick, 1 grain, 1 ore for 3 points) and roads (1 wood, 1 brick for 1 point) exist in this ruleset; do not hoard grain/ore expecting cities.
- When I have at least 1 wood, 1 brick, 1 grain, and 1 ore, reply `[build: settlement]`.
- When I have at least 1 wood and 1 brick, but lack grain or ore and cannot make a settlement, reply `[build: road]`.
- If neither cost is met, reply `[build: none]`.

### Trade Offer Strategy
- Track my exact missing resources for a settlement (and secondarily for a road).
- When creating an offer, offer my surplus resources (count >= 2, or resources not required for my target build) in exchange for the exact resource I lack.
- Target the counterparty who actually holds the resource I want and has a deficit/need for the resource I am giving away.
- Do not offer a resource if giving it away prevents me from building a settlement unless the incoming trade enables the settlement.
- If I already hold all necessary resources to build a settlement this round and have no clear surplus to prep for future rounds, reply `[offer: none]`.

### Accept Phase Strategy
- Simulate the resulting inventory for each combination of incoming offers before accepting.
- Reject offers that ask for non-surplus resources (count = 1) needed for an immediate build if giving them up just shifts the missing resource to another category without solving the build requirement.
- Accept an offer if it gives me a missing piece for an immediate settlement build while only taking true surplus (count >= 2).
- If multiple offers arrive from different players asking for the same scarce resource, verify that accepting one does not compromise my build; reject both if neither is beneficial.
- If no incoming offer enables an immediate build or improves my inventory without compromising current builds, reply `[accept: none]`.