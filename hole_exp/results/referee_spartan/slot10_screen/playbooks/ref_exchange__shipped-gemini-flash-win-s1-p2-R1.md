---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1889
---
# Settlement & Trade Playbook

### Trading Strategy: Offers
* When I have an excess of a resource (2+ copies) and need a specific missing resource to complete a settlement (1 wood, 1 brick, 1 grain, 1 ore) or a road (1 wood, 1 brick), I post an offer targeting a player who holds a surplus of the resource I need: `[offer: to P<k>, give 1 <excess>, get 1 <needed>]`.
* When posting an offer, never offer my last copy of wood, brick, grain, or ore if I already have a balanced hand or if doing so drops me below the threshold for an immediate build.
* When I am unable to reach a build target this round, or when trading would directly enable the current points leader to build a settlement, I post `[offer: none]`.
* In the final round, if I cannot reach a build threshold regardless of trade, I post `[offer: none]` to prevent feeding opponents.

### Trading Strategy: Accepting
* When an incoming offer gives me a missing resource needed to complete a settlement or road without breaking my existing build requirements, I accept: `[accept: P<k>]`.
* When an incoming offer trades away my only copy of a resource needed for a settlement, or aids an opponent without advancing my own immediate build goal, I decline: `[accept: none]`.
* When multiple trade offers arrive, I evaluate them against my starting inventory for the round and accept only the combinations that leave me with the resources to build.

### Building Strategy
* When I hold at least 1 wood, 1 brick, 1 grain, and 1 ore during the building phase, I always prioritize building a settlement: `[build: settlement]`.
* When I hold at least 1 wood and 1 brick but lack the grain or ore for a settlement—and it is the final round or I have surplus wood/brick that won't compromise future settlements—I build a road: `[build: road]`.
* When I lack the resources to build either a settlement or a road, I reply `[build: none]`.