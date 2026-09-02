---
game: ref_exchange
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 2672
---
# Playbook

**Building:**
- When I can afford a settlement (at least 1 of each resource), I build it immediately. It is always the highest-value action available.
- When I cannot afford a settlement but can afford a road (1 wood + 1 brick), I build the road. A road is always better than passing.
- I never pass on a build if I can afford anything.

**Trading — what to offer:**
- I trade to complete a build, not to "balance" or "stockpile." If I'm missing exactly one resource for a settlement, I trade specifically for that resource. If I'm missing two or more, I trade for the one that gets me closest to a build (prioritize the resource that appears in both settlement and road costs: wood or brick).
- Before posting an offer, I check three conditions. All must be met:
  1. I have 2+ of the resource I'm offering (so the trade doesn't reduce my own buildability).
  2. The counterparty has at least 1 of the resource I want.
  3. After the trade, the counterparty can still build at least as much as they could before. Specifically: if the counterparty has exactly 1 of the resource I'm asking for, and that resource is part of a build they could otherwise complete this round, they will reject. I only ask for a resource when the counterparty has 2+ of it, OR when the resource I'm giving them is one they have 0 of (making the trade attractive enough to accept even at cost of 1).
- I target the counterparty for whom the trade is most attractive: they have the resource I want in surplus (2+), AND they have 0 of the resource I'm offering (so the trade gives them something new).
- If no counterparty passes all three conditions, I do not waste my offer. I skip and rely on land yield or incoming offers.
- In the final round, if I'm one resource short of a settlement or road, I relax condition 3 slightly: I will offer even if the counterparty goes from "can build" to "can't build," because the game is over and they have no future rounds to lose. But I still require condition 1 (I offer a surplus).
- Brick is the most commonly scarce resource in this game. If I have 0 brick, I treat acquiring it as the top trading priority every round, above ore or grain.

**Trading — what to accept:**
- I accept an offer if, after the trade, I can build at least as much as I could before. This is the single test. If accepting keeps me buildable (or makes me buildable when I wasn't), I accept.
- I decline an offer if, after the trade, I lose the ability to build something I could build before. This is a hard rule: if I have 1 of each and someone wants my only grain, I decline, even if they're giving me ore. I would go from "can build settlement" to "can't build