---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 1
round: 2
chars: 2271
---
- When a property is unowned and I can afford it without leaving myself unable to pay a typical rent, I buy it — deeds count at full purchase price toward my final score, so buying is nearly free in net-worth terms as long as I keep a cash buffer.
- Before buying, I check the most expensive rent still in play and keep enough cash to survive one landing on an opponent's best property; I don't let a purchase drop me below roughly one expensive rent payment.
- When a purchase would drop me below zero or below that survival buffer, I skip it — this is what led me to pass on Depot at 46 cash, and it cost nothing in final score because I couldn't afford it regardless.
- On the last lap or two, pure affordability is the only test for buying: cash converts to deed value at par and liquidity no longer matters, so buy anything I can pay for outright.
- When cash gets thin after early buying, I stop buying mid-priced tiles and hold a reserve so I can still snap up top-value properties if I land on them late — I confirmed from the prior episode that over-buying early left me unable to take premium tiles.
- When I pass or land on START, I add the salary to my balance before anything else that turn, and I say so.
- When I land on an owned property, I immediately pay the rent to the correct owner with [pay: N to Pk] and subtract it — I never skip this or pay the bank by mistake.
- When I land on my own property, nothing is due: I declare [pay: none], [buy: no], and carry forward my balance (plus salary if I passed START).
- When I land on an unowned property I choose not to buy, I declare [pay: none] and [buy: no]; unowned tiles never cost rent.
- When the log shows "you received N from other investors," I add that amount to my last declared balance before settling; I never use the stale balance alone.
- I keep my running balance as: previous balance + salary (if passed START) + rents received since my last turn − my purchase − rent I owe, and I declare exactly that number.
- I always reply with all three tokens and end on the [balance: N] token.
- I track the bank's transfer log to see which properties are already owned and by whom, so I never attempt to buy an owned tile or misread my opponents' holdings when judging how much rent I might face.