---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 1691
---
When an unowned property is offered and I can afford it, I buy it unless doing so leaves me unable to cover likely rent payments in the coming laps; deed value counts fully toward my final score, so cash sitting idle buys nothing.

When buying, I keep a minimum cash buffer sized to the highest rent on the board (or at least a couple of average rents), because going broke means I can't buy anything later and risk insolvency.

When I cannot afford a deed, I pass without hesitation and bank the incoming rent instead of stretching.

Before settling every turn, I recompute my cash from scratch: last declared balance, plus salary if I passed START, plus all rent received since my last turn, minus the deed price and any rent I owe. I declare that full recomputed figure, not just the change.

When I land on an opponent's deed, I pay the stated rent in full via the [pay: N to P<k>] token and subtract it from my balance immediately.

When I land on my own deed or opportunities not for sale, I declare [pay: none] and [buy: no] and confirm an unchanged balance.

When I pass START, I never forget to add the salary to my declared balance — it's free cash that compounds into buying power.

In the early laps I buy aggressively on high rent-to-price deeds (cheap deeds with decent rent pay back fast in opponents' fees); in the final lap I stop spending on anything that won't earn more than its price before the game ends.

I track the bank's transfer log each turn: it tells me which deeds opponents own (and thus what rents I might owe) and confirms my incoming rents were credited.

I always end my reply with the three required tokens, exactly formatted, with the balance token last.