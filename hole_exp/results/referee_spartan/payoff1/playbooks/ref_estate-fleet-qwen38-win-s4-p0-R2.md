---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 4
round: 2
chars: 3284
---
# Playbook: ref_estate

**Buying properties**

When I land on an unowned property and can afford it, I buy it if the rent-to-price ratio is at least 18% and the purchase leaves me with a cash buffer of at least 30. High-ratio properties (≥22%) get priority: I buy them even if the buffer drops to around 20, because the compounding rent income over remaining laps usually pays for the risk.

When I land on an unowned property but buying would leave me below 20 cash, I skip it unless the ratio is exceptional (≥25%) and there are at least 3 laps remaining. A cash shortage on a future rent payment is far worse than a missed purchase.

**When I cannot afford the property I landed on**

I simply note the balance and move on. I do not speculate about whether I could have planned differently on earlier turns—just execute the current turn cleanly.

**Rent and salary**

When I pass START, I collect my salary and add it to my running cash total before settling any rent due on the tile I landed on. The order is: salary in, rent out, then declare the net balance.

When I land on my own property, nothing is due. I confirm this explicitly rather than assuming a zero payment might be ambiguous.

**Cash tracking**

I maintain a running total from turn to turn: previous balance + salary (if any) + rent received from others (if any) − rent paid to others − purchase price (if any) = new declared balance. I always verify this arithmetic before declaring.

**Endgame (last 1–2 laps)**

With 1–2 laps remaining, I do not buy unowned properties. There are not enough future passes for the rent to compound, and depleting my cash buffer in the final laps risks an unaffordable rent payment. I only buy in the endgame if the property has rent ≥24 AND I can still cover a maximum rent payment (30) after the purchase.

**Aggression calibration**

I can only buy properties I land on, and I may not land on the same tile again for several laps. This makes each landing a rare opportunity. I should err toward buying when my ratio and buffer tests are met, rather than holding out for a better tile I may never reach. If I have 3+ laps remaining and the ratio is ≥20%, the expected rent income justifies the purchase even at a tighter buffer (down to 20).

**What did not work**

In this episode I made only one purchase in six laps. I landed on two unowned properties (Wharf and Mill) but could only afford the first. Mill (price 90, rent 20, ratio 22%) was unaffordable because a prior rent payment (24) had dropped me from 120 to 96, leaving only a 6-cash buffer after purchase. My buffer rule correctly prevented an unsafe purchase, but the root cause was that I was too exposed to rent payments from other players' properties while my own portfolio was still small. Lesson: the buffer rule protects me from going broke, but it also caps my portfolio growth. I should consider whether a slightly tighter buffer (20 instead of 30) on high-ratio properties (≥22%) would have let me build a second property without unacceptable risk. In practice, the difference is small—one property of rent 18–20 versus none—but over multiple episodes the compounding gap matters. I will lower the high-ratio buffer threshold to 20 and monitor whether it causes a liquidity crisis in a subsequent episode.