---
game: ref_estate
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1792
---
- When a property is unowned and I can afford it without leaving myself unable to pay a typical rent, I buy it — deeds count at full purchase price toward my final score, so buying is nearly free in net-worth terms as long as I keep a cash buffer.
- Before buying, I check the cheapest rent still on the circuit and keep enough cash to survive one landing on an opponent's best property; I don't let a purchase drop me below roughly one expensive rent payment.
- When cash gets thin after early buying, I stop buying mid-priced tiles and only consider the top-value properties if I can truly afford them; late-game purchases of cheap tiles are still fine since price equals score.
- When I pass or land on START, I add the salary to my balance before computing anything else that turn, and I say so.
- When I land on an owned property, I immediately pay the rent to the correct owner with [pay: N to Pk] and subtract it from my balance — I never skip this or pay the bank by mistake.
- When I land on an unowned property I choose not to buy, I declare [pay: none] and [buy: no]; unowned tiles never cost rent.
- When the log shows "you received N from other investors," I add that amount to my last declared balance before settling; I never use the stale balance alone.
- I keep my running balance as: previous balance + salary (if passed START) + rents received since my last turn − my purchase − rent I owe, and I declare exactly that number.
- I always reply with all three tokens and end on the [balance: N] token.
- What did not work: spending down to nearly zero on consecutive early purchases left me unable to buy the highest-value property when it came up and forced me to scrape by on rent income; next time I pace purchases so I still have a reserve when premium tiles appear late.