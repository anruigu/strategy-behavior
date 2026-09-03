---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 3111
---
Before offering anything, I compute value differences: I look for a resource I value far below the opponent's published value, and a resource they hold that I value well above their published value. Every trade is built from exactly that gap.

I trade away what is cheap to me and dear to them, and take back what is cheap to them and dear to me, for as many rounds as the stocks on both sides allow. I repeat the same winning trade until one side's stock of the relevant resource runs out, then I switch to the next best pairing.

When checking whether any trade works, I search the full grid, not just 1-for-1: every give resource × take resource × quantities from 1 to the cap on each side. For each candidate I compute both numbers — the stamped gain in the opponent's values and my own net private gain — and only consider trades where the stamped gain meets the floor and my net is strictly positive. A trade that merely breaks even for me while enriching the opponent is not worth a round, even if it clears the floor.

Crucially, multi-unit combinations are where the late-round value hides. Giving 2 or 3 units of a resource at a modest per-unit gap can stamp a large opponent gain while taking back 3 units of a mid-gap resource keeps me ahead — e.g. 2 brick for 3 wood stamped +2 and netted me +3 when every 1-for-1 looked dead. I learned this the hard way: I held in round 5, then found the exact same 2-for-3 trade in round 6 with unchanged stocks. That hold cost me +3. So before I ever conclude "no profitable trade exists", I re-run the entire quantity grid explicitly — including 2-for-3 and 3-for-2 — and only hold if every cell fails, with the arithmetic actually done rather than glanced at.

I size the claim honestly and to the minimum threshold: the stamped gain should be exactly 2 (or whatever the acceptance floor is) rather than gifting extra value. When several combinations clear the floor, I rank them by my private net, not by how generous the stamp looks; a stamp of +3 that earns me +2 is worse than a stamp of exactly +2 that earns me +6. I never inflate the claim beyond the true figure and never give the opponent more of my private value than necessary.

Before I send any offer, I check it against the referee's rules: quantities whole, between 1 and the stated maximum, covered by my current stock, the take quantity covered by the opponent's stock, and the claim a true whole number in range. A trade that asks more than the cap or more than the opponent holds is invalid and wastes a round — I split big trades into legal per-round sizes.

Each round I rescan with fresh stocks and values; a trade that was impossible last round can become legal as stocks shift, and one that was legal can die. I never reason from remembered conclusions — only from the current holdings grid.

When — and only when — the fully enumerated grid gives no trade that clears the opponent's floor while leaving me strictly ahead, I hold without hesitation. I do not offer trades that cost me private value, nor zero-sum trades that only hand the opponent a stamped gain, just to fill a round.