---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2487
---
# Playbook: ref_estate

**Buying properties**

When I land on an unowned property and can afford it, I buy it if the rent-to-price ratio is at least 18% and the purchase leaves me with a cash buffer of at least 40. High-ratio properties (≥22%) get priority: I buy them even if the buffer drops to around 30, because the compounding rent income over remaining laps usually pays for the risk.

When I land on an unowned property but buying would leave me below 30 cash, I skip it unless it's the last lap or the ratio is exceptional (≥25%). A cash shortage on a future rent payment is far worse than a missed purchase.

**When I cannot afford the property I landed on**

I simply note the balance and move on. I do not speculate about whether I could have planned differently on earlier turns—just execute the current turn cleanly.

**Rent and salary**

When I pass START, I collect my salary and add it to my running cash total before settling any rent due on the tile I landed on. The order is: salary in, rent out, then declare the net balance.

When I land on my own property, nothing is due. I confirm this explicitly rather than assuming a zero payment might be ambiguous.

**Cash tracking**

I maintain a running total from turn to turn: previous balance + salary (if any) + rent received from others (if any) − rent paid to others − purchase price (if any) = new declared balance. I always verify this arithmetic before declaring.

**Endgame (last 1–2 laps)**

With few laps remaining, I weight the decision toward liquidity. A cheap property with low absolute rent (e.g., rent 10–14) is unlikely to generate enough income to justify depleting my buffer, because there aren't enough remaining passes for others to collect it. I only buy in the endgame if the property is high-rent (≥24) and I can still afford any single rent payment on other players' tiles after the purchase.

**What did not work**

I was too passive in the mid-game. After my second purchase dropped me to 54 cash, I had no opportunity to buy again for two laps, and I never recovered enough to make a third purchase. Lesson: when I have a choice between two affordable properties on consecutive turns, I should favor the higher-rent one even if it leaves a thinner buffer, because the income gap compounds. I should also resist the urge to "save up" for a property I haven't landed on yet—the only properties I can buy are the ones I land on, so hoarding cash for a hypothetical future tile is a dead strategy.