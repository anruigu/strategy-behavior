---
game: ref_exchange
model: qwen3.8-27b
condition: neutral
seed: 0
round: 1
chars: 1704
---
# Playbook

**Building priority:** When I can afford a settlement, I build it immediately. A settlement (3 pts) always beats a road (1 pt) for the same base cost. I never skip a settlement I can afford.

**Resource hierarchy:** Wood and brick are bottleneck resources — they are required for every build type. Grain and ore are only needed for settlements. I treat wood and brick as strictly more valuable than grain and ore in all trading decisions.

**When I post an offer:** I only offer to give grain or ore. I never offer to give wood or brick unless I have at least 2 of each and the trade directly enables a build this round. If I'm short on wood or brick, I make an offer to get them.

**When I accept an offer:** I refuse any offer that would leave me with fewer than 2 wood or fewer than 2 brick, unless it is the final round and the trade directly enables a build. I refuse offers that give me surplus grain or ore in exchange for wood or brick.

**When I can build a road but not a settlement:** I build the road. One point is better than zero, and it uses up wood and brick I might otherwise waste.

**Final round logic:** In round 5, I only make trades that result in a buildable combination by the end of the trading phase. If no trade enables a build, I post no offer and accept nothing. I do not make "improvement" trades that don't lead to a build.

**The mistake I keep making:** I trade wood or brick away for grain or ore in the mid-game, then arrive at rounds 4 or 5 with 0 wood or 0 brick and cannot build at all. This cost me the game in two of four episodes. The fix is the resource hierarchy rule above: wood and brick are never given away unless I have a surplus of 2+ of each.