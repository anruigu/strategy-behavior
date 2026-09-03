---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 2
round: 1
chars: 1313
---
When I land on an unowned property and I can afford it without dropping my cash below 30, I buy it.

When I land on an unowned property that costs more than 40% of my current cash, I pause and only buy if it has notably higher rent (rent/price ratio significantly above board average) or completes a set/strategic advantage.

When I pass START, I collect the salary immediately and add it to my declared balance.

When I land on another investor's property, I pay the exact rent immediately and update my balance.

When I receive payments from other investors, I add them to my cash before making buying decisions on my next turn.

When I own the property I land on, I do nothing and declare no purchase.

When asked to settle a turn, I always declare three tokens: [pay: ...] (or [pay: none]), [buy: yes] or [buy: no], and [balance: N] showing my updated cash.

When cash is low (below 30), I avoid purchasing more properties until I recover via rent or passing START; buying when cash is extremely low proved risky.

When deciding between two purchases, I prefer the one with the higher absolute rent and the better rent-to-price ratio.

When an opponent offers a trade or deal, I only accept if it increases my declared net worth (cash + purchase prices of deeds) immediately or clearly improves future income.