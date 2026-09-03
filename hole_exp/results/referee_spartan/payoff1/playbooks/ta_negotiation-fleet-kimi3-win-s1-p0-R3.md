---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 1
round: 3
chars: 2882
---
When an offer round opens, I compute for every legal trade two numbers: my private net gain and the Guildmaster's published net gain, which is also the claim I must stamp truthfully. I only offer trades where my private net is positive and the true stamp is at least 2.

I treat legality as part of the search, not an afterthought: give quantity is 1–3 and covered by my stock, take quantity is 1–3 and covered by the Guildmaster's stock, and claim is a whole number within range. I never offer a side with quantity 4+ or anything either side cannot cover, because that wastes the round even if the value logic looks good.

I scan unequal quantities as well as equal ones. For each candidate I use: my gain = (my value of take × take qty) − (my value of give × give qty); his stamped gain = (his value of give × give qty) − (his value of take × take qty). I accept only my gain > 0 and his gain ≥ 2.

I look first for resources I value less than the Guildmaster does and trade those away against resources I value more; the same unit gap can pay his stamp from his side and my profit from mine. Scaling within the 1–3 limit amplifies both sides, so I prefer the largest legal quantity that keeps both inequalities true.

I do not restrict myself to equal-for-equal swaps. A 1-for-1 or other uneven exchange can be profitable after larger balanced trades stop working, so I rescan all legal quantity pairs whenever stocks change and before deciding nothing exists.

I recognize the structural trap this episode exposed: if the only resource in the Guildmaster's value table high enough to fund a +2 stamp is one I value even higher (his sheep 5 vs my sheep 6), then giving it always loses more on my side than I can recover from anything he holds, and no profitable trade exists at any quantity. When the value tables line up like that, I verify it once over the full quantity grid and then hold cleanly for the remaining rounds instead of second-guessing each round.

Before concluding "no trade exists," I still run the complete cross product: every giveable resource × every takeable resource × quantities 1–3 on each side, filtered by current stocks. If the result is the same as the last time stocks and values were identical, I hold without re-deriving it.

I never offer a stamp below 2, never claim a false figure, and never offer a zero-gain trade just to avoid holding — a +0 trade adds no score and only shifts stocks around, so holding is strictly better unless the repositioning sets up a later profitable trade, which I check for explicitly before dismissing.

I trade early and greedily when profitable legal trades exist, because accepted deals lock in net private score. Near the final rounds I double-check stock depletion and quantity caps before offering; if the only tempting line uses more than 3 units on a side or depends on empty enemy stock, I hold instead.