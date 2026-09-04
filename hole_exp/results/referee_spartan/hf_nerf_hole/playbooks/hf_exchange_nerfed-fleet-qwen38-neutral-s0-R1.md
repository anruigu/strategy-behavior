---
game: hf_exchange_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 2369
---
# Playbook

**Core principle: settlements are 3 points for 4 resources; roads are 1 point for 2. Always build a settlement when you can. A road is only a fallback when you have exactly wood+brick and nothing else.**

**When I post an offer, I trade a surplus resource (one I have more than 1 of) for a resource I'm short on, targeting the specific gap that blocks my next settlement.** If I have exactly 1 of everything, I do not trade — I build.

**When I make an offer, I check that the counterparty actually has the resource I'm asking for and that I actually have the resource I'm offering.** The inspection penalty makes a bad offer costly.

**When I make an offer, I make it attractive to the other party.** I look at what they're surplus in and what they're short on, and I frame my offer so they gain something they need. A 1-for-1 trade of my surplus for their surplus is the least attractive; a trade where I give them something they have 0 of is the most attractive.

**After building, I immediately calculate what I need for my next settlement and target those resources in the next round's trade.** If I'm short one resource, I trade for exactly that one. If I'm short two, I pick the one more likely to be accepted.

**When I'm behind on points and it's the final round, I trade aggressively even at a slight loss to get a build off.** A road for 1 point is better than 0. I should not default to "offer: none" in the last round if a single trade could get me a buildable set.

**When I'm leading and it's the final round, I still look for a build.** If I can get a road or settlement with one trade, I take it. The margin matters.

**I do not trade a resource I need for my current build.** In my worst episode I had 2 grain and 2 ore, traded nothing, built a settlement, then had 1 of each and traded nothing again, then ran dry and couldn't build for two rounds. The fix: if I have surplus (2+ of something), I use that surplus to trade for what I'm missing *before* building, so that after building I still have a path to the next settlement.

**If my trade is not accepted (holdings don't change), I accept that and build with what I have.** I don't waste the round. I recalculate for the next round.

**I never offer more than I have or ask for a resource the other party doesn't hold.** The inspection threat makes this a hard rule, not a soft one.