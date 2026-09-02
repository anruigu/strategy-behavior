---
game: ref_exchange
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 4791
---
# Playbook

**Building priority:** When I can afford a settlement, I always build it. A road is a fallback when I cannot complete a settlement but can afford 1 wood + 1 brick. Never build a road if a settlement is available. If neither is possible, build nothing.

**Bottleneck identification:** At the start of each round, I identify which resource(s) I am at 0 of (relative to what I need for a settlement: 1 of each). Those are the resources I should be trying to acquire through trade.

**When to post an offer:** I post an offer whenever I am missing at least one resource needed for a settlement and have at least one resource I can spare (i.e., I have 2+ of it, or I have 1 of it but am missing a different resource and the trade would move me closer to building). I target the player who has the resource I want and who has 2+ of what I'm offering (surplus for them). A 1-for-1 trade where both sides fix a deficit is the strongest trade, but I should not require the target to have 0 of what I'm offering — a player with 2+ of my offered resource is still likely to accept since they don't need all copies.

**Be aggressive when I can't build:** If I'm missing resources and can't build this round, I should always post an offer for the resource I need. Even if the trade is imperfect or may not be accepted, posting costs nothing and may unlock a build. I should not sit idle with "no offer" when I have any resource I can trade away for one I'm missing.

**Simulating combined settlement effects (critical):** Both my posted offer and any accepted incoming offer settle against my holdings at the start of the trading phase. Before accepting an incoming offer, I must simulate my holdings after BOTH my posted offer and the accepted offer resolve simultaneously. If the combined result leaves me unable to build a settlement (0 of any resource), I decline the incoming offer unless the combined result still lets me build at least as much as I could by declining. This is the single most common way I lose points.

**When to decline an offer:** I decline an incoming offer if, after simulating the combined effect (my posted offer + this accepted offer), I would be unable to build a settlement. In the final round this is especially critical. However, if I already cannot build a settlement even without accepting, I should accept any offer that moves me toward having a full set — the downside is zero since I can't build anyway.

**Never trade away the last copy of a resource I need to build this round.** Before accepting any offer, I simulate my post-trade holdings (including my own posted offer) and verify I can still build what I intend. If the trade drops me below the build threshold, I decline.

**Avoiding negative holdings:** I never post an offer that gives away a resource I have only 1 of, unless I am confident I will receive that same resource back in the same round from an incoming offer I plan to accept. Going negative on a resource locks me out of building.

**Maintaining a full set is the top priority.** The resource I'm "most contested on" matters less than simply keeping 1 of each resource in hand. If I have a full set, I hold and build. If I'm missing one resource, I trade specifically for that one. I do not trade for "better" resources if it costs me the ability to build.

**Final round strategy:** In round 5, my only goal is to maximize points from the build phase. I check: do I have 1 of each resource? If yes, I decline any trade that would break that and post no offer. If I'm one resource short, I trade specifically for that resource, offering something the target player has surplus of. I decline incoming offers only if they would break my ability to build; if I can't build regardless, I accept any offer that gets me closer to a full set.

**When I'm in last place and far behind:** I become more aggressive with trades, accepting offers that are roughly fair (1-for-1) to get the specific resource I need to build, rather than holding out for a better deal.

**Holding resources:** If I already have a full settlement's worth (1 of each) and no trade would let me build more than one settlement this round, I decline incoming offers and post no offer. I just build and save surplus for next round.

**When stuck with two missing resources:** If I'm missing two different resources and can only make one trade, I prioritize the resource that is harder to get later (the one fewer other players have in surplus). I accept that I won't build this round and focus on fixing my position for the next round.

**Road as fallback:** If I cannot build a settlement but have 1 wood + 1 brick, I build a road for 1 point. This is better than building nothing and keeps me competitive, especially in the final round where every point matters.