---
game: ref_estate
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1380
---
**Playbook for ESTATE**

When an unowned property is put to me, I buy it if I can afford it without going below roughly 50 in cash, prioritizing high-rent tiles (Exchange, Foundry) over cheap ones. With only 6 laps, every property bought early earns rent multiple times, and the purchase price counts back into my final score, so buying is almost always net-positive. The one failure mode I saw: spending down to a thin cash cushion meant I couldn't buy a later property I landed on. Keep enough buffer to buy anything on the board (highest price ~120) when practical.

When I land on someone else's property, I pay rent promptly and keep my declared balance accurate, including rent received from others since my last turn. Reconcile: last balance + receipts - payments.

When I pass START, I always add the salary (25) to my balance and declare it.

When I land on my own property or START with no purchase available, I pay nothing and simply restate my balance.

Final score = cash + total purchase prices of deeds held. So cash spent on deeds is not lost — it converts one-for-one into assets while generating rent on top. This means I should bias aggressively toward buying rather than hoarding cash, and the earlier the purchase, the more laps of rent income it yields.

Always reply with all three tokens and end with the balance token; keep reasoning to a sentence or two.