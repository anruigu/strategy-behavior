---
game: ref_exchange
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 3710
---
# Playbook

**Building:**
- When I can afford a settlement (at least 1 of each resource), I build it immediately. It is always the highest-value action available.
- When I cannot afford a settlement but can afford a road (1 wood + 1 brick), I build the road. A road is always better than passing.
- I never pass on a build if I can afford anything.

**Trading — what to offer:**
- I trade to complete a settlement, not to "balance" or "stockpile" resources. If I'm missing exactly one resource for a settlement, I trade specifically for that resource.
- I only make an offer if I believe the counterparty will accept it. Before posting, I check: does the counterparty have 2 or more of the resource I want (so they can spare one), AND do they have 0 or 1 of the resource I'm offering (so they actually want it)? If neither condition is met, the offer will likely be rejected and I should skip it.
- I target the counterparty who has the resource I need in surplus (2+) and who is missing or low on what I'm offering.
- I never trade away my last copy of a resource I need for a settlement unless the trade gives me a resource I have 0 of AND I still have all other three (i.e., it completes the build).
- In the final round, if I'm one resource short of a settlement, I make that trade my top priority. If I'm two or more short, I try to get the most buildable combination (a road at minimum).
- If no counterparty has the resource I need in surplus, I do not waste my offer on a trade that will be rejected. I wait for land yield or accept incoming offers instead.

**Trading — what to accept:**
- I accept an offer if it completes a settlement or road I could otherwise not build this round.
- I accept an offer if it converts a resource I have in surplus (2+) into a resource I have 0 of, and I can still build this round after the trade.
- I decline an offer if it takes my last copy of any resource I need for a build I could otherwise complete this round. This is a hard rule: if I have 1 of each and someone offers to take my only grain, I decline, even if they're giving me something. I would go from "can build" to "cannot build."
- I decline an offer that takes my last copy of a resource I need for a settlement, unless the incoming resource is one I have 0 of AND I still have all other three after the trade.
- When I have multiple incoming offers, I evaluate each one against my current holdings independently and accept all that pass the criteria above.

**General principles:**
- The land yields resources every round, so I do not hoard. If I have 2 of a resource and need it for a build, I spend it. I'll get more next round.
- A settlement is 3 points for 4 resources (0.75 pts/resource). A road is 1 point for 2 resources (0.5 pts/resource). I always prefer settlements, but a road beats nothing.
- I avoid the trap of accumulating one resource type (e.g., ore) while neglecting the others. Ore alone is worthless. Every trade should move me closer to having at least 1 of each.
- If I find myself at the start of a trading phase with a resource distribution where I can't build anything (missing 2+ resources), I treat the round as urgent: I make my offer for the single most impactful missing resource and accept any incoming offer that fills a gap.
- I do not trade in a round where I already have 1 of each resource and can build a settlement. I build and let the land yield refill me.
- My offers get rejected when I ask someone to give up their only copy of a resource they need. I must always model the counterparty's position: after the trade, can they still build? If not, they will say no. I only make offers where the counterparty is strictly better off or at least not worse off.