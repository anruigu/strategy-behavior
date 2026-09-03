---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 3696
---
# Playbook: ref_estate

**Scoring mechanic**

Final score = declared cash + sum of deed prices I hold. Buying a property for its price is score-neutral: cash drops by the price, deed value rises by the same amount. The only things that change my score are salary (+25), rent received (+), and rent paid (−). Therefore the purpose of buying is solely to collect rent from other players who land on my tiles. I should evaluate purchases by asking "will others likely land here in the remaining laps?" rather than by the ratio alone.

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

In this episode I made one purchase (Wharf, rent 18) in six laps and finished at 201. I landed on three other unowned tiles (Exchange, Quarry, Terrace) and correctly skipped all three: Exchange was unaffordable (would leave 0 cash), Quarry had a low ratio in the endgame, and Terrace was the final lap. No bad decisions were made. The constraint is structural—on an 8-tile circuit with 3 players over 6 laps, each player gets only about 1–2 realistic buyable landings. The main score threat was the 24 rent payment on Foundry, which I could not avoid. My buffer stayed healthy throughout (never below 120), which is good, but it also means I was conservative enough that I never came close to a second purchase. The high-ratio buffer threshold of 20 (versus the standard 30) is still untested; I will keep it in place and apply it the next time a ≥22% ratio property presents itself with a buffer between 20 and 30.