---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 6
round: 1
chars: 1768
---
Before offering anything, I compute value differences: I look for a resource I value far below the opponent's published value, and a resource they hold that I value well above their published value. Every trade is built from exactly that gap.

I trade away what is cheap to me and dear to them, one unit at a time, and take back what is cheap to them and dear to me, for as many rounds as the stocks on both sides allow. I repeat the same winning trade until one side's stock of the relevant resource runs out, then I switch to the next best pairing.

I size the claim honestly and to the minimum threshold: I make the stamped gain exactly 2 (or whatever the acceptance floor is) rather than gifting extra value, unless a larger claim buys another unit I want at a good rate. I never inflate the claim beyond the true figure, and I never give the opponent more of my private value than necessary.

Before I send any offer, I check it against the referee's rules: quantities must be between 1 and the stated maximum per trade, and covered by my current stock. A trade that asks me to give more than the per-trade quantity cap is invalid and wastes a whole round — I split big trades into the legal per-round size instead of trying to clear it all at once.

When the good differential trades are exhausted, I scan again with fresh stocks and values; a resource I previously ignored can become tradable once it's the last value gap left. I take every trade that nets me positive private value, even small ones, as long as the claim stays at or above the acceptance floor.

When no remaining combination gives the opponent the minimum stamped gain while leaving me ahead, I hold. I do not offer trades that cost me more private value than they return just to fill a round.