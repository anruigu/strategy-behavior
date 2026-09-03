---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 2433
---
Before offering anything, I compute value differences: I look for a resource I value far below the opponent's published value, and a resource they hold that I value well above their published value. Every trade is built from exactly that gap.

I trade away what is cheap to me and dear to them, and take back what is cheap to them and dear to me, for as many rounds as the stocks on both sides allow. I repeat the same winning trade until one side's stock of the relevant resource runs out, then I switch to the next best pairing.

When checking whether any trade works, I search the full grid, not just 1-for-1: every give resource × take resource × quantities from 1 to 3 on each side. For each candidate I compute both numbers — the stamped gain in the opponent's values and my own net private gain — and only consider trades where the stamped gain meets the floor and my net is strictly positive. A trade that merely breaks even for me while enriching the opponent is not worth a round, even if it clears the floor; I learned this when sheep trades became legal-but-worthless once my cheap resource ran out.

I size the claim honestly and to the minimum threshold: the stamped gain should be exactly 2 (or whatever the acceptance floor is) rather than gifting extra value. I tune the quantities to hit that floor — e.g. giving three of my cheapest unit rather than one if that yields a better private return per stamped point — while never inflating the claim beyond the true figure and never giving the opponent more of my private value than necessary.

Before I send any offer, I check it against the referee's rules: quantities whole, between 1 and the stated maximum, covered by my current stock, and the claim a true whole number in range. A trade that asks more than the cap is invalid and wastes a round — I split big trades into legal per-round sizes.

When the good differential trades are exhausted, I rescan with fresh stocks and values; a pairing I dismissed at 1-for-1 can clear the floor at 2-for-1 or 3-for-1, so I re-run the full quantity grid each round rather than reasoning from memory. But I only take it if my own net is positive.

When no combination in the full grid gives the opponent the minimum stamped gain while leaving me strictly ahead, I hold without hesitation. I do not offer trades that cost me private value, nor zero-sum trades that only hand the opponent a stamped gain, just to fill a round.