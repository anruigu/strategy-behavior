---
game: ref_exchange
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 2841
---
# Playbook

**Building priority:** When I can afford a settlement, I always build it. A road is only a fallback when I cannot complete a settlement. Never build a road if a settlement is available.

**Bottleneck identification:** At the start of each round, I identify which resource I am shortest on (relative to what I need for a settlement: 1 of each). That is the resource I should be trying to acquire through trade.

**When to post an offer:** I post an offer when I have a surplus of one resource (2 or more) and a deficit of another (0 or 1). I target the player who has the resource I want and appears to have a surplus of what I'm offering. In round 1 especially, I should be trading to fix my weakest resource so I can build a settlement.

**When to decline an offer:** I decline an incoming offer if accepting it would remove a resource I need to complete a settlement this round. Specifically: if after accepting, I would have 0 of any resource, and I currently have exactly 1 of that resource, I decline unless the incoming resource is one I have 2+ of (making the trade a true surplus swap). In the final round this is especially critical — I check whether declining keeps me at settlement-able before I accept anything.

**Never trade away the last copy of a resource I need to build this round.** Before accepting any offer, I simulate my post-trade holdings and verify I can still build what I intend. If the trade drops me below the build threshold, I decline.

**Avoiding negative holdings:** I never post an offer that gives away a resource I have only 1 of, unless I am confident I will receive something back that same round (e.g., I have a pending incoming offer for that resource). Going negative on a resource locks me out of building for the rest of the round.

**Brick is the most contested resource.** I prioritize acquiring brick early (rounds 1–2) because multiple players need it and it tends to get absorbed quickly. If I start with only 1 brick, I should trade for a second one in round 1.

**Final round strategy:** In round 5, my only goal is to maximize points from the build phase. I check: do I have 1 of each resource? If yes, I decline any trade that would break that. If I'm one resource short, I trade specifically for that resource and decline everything else. I do not trade for "better" resources if it costs me the ability to build.

**When I'm in last place and far behind:** I become more aggressive with trades, accepting offers that are roughly fair (1-for-1) to get the specific resource I need to build, rather than holding out for a better deal.

**Holding resources:** If I already have a full settlement's worth (1 of each) and no trade would let me build *more* than one settlement this round, I decline incoming offers and post no offer. I just build and save surplus for next round.