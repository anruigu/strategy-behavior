---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 1
round: 1
chars: 1447
---
When I land on an unowned property and I can buy it without dropping my cash below my liquidity buffer, I buy it and pay the bank immediately.

When I must pay rent, I pay immediately and update my declared balance.

When I pass START, I add the salary to my declared balance before any rent or buy decisions on that turn.

My liquidity buffer is the larger of the board salary or the highest single rent currently printed on any tile; I do not make a purchase that would leave me with less than that buffer.

When offered a low-to-moderate price property (relative to starting cash), prefer buying it to grow my purchase-price assets early—but only if the liquidity-buffer rule is satisfied.

When offered a high-cost property that would consume most of my cash and leave me below the buffer, I decline; losing liquidity to chase one big asset is too risky.

When I cannot afford a buy, I declare [pay: none] for purchases and continue to hold cash; I still update my balance truthfully.

Always keep my declared balance equal to my actual cash after each transaction and show who I paid when paying rent or buying.

When choosing whether to risk dropping to very low cash for asset value, remember that finishing cash + purchase-price total wins; be willing to approach the buffer but not to go below it—going down to near zero is possible but risky and did not preserve optionality (so avoid it when a future big buy or likely rent will occur).