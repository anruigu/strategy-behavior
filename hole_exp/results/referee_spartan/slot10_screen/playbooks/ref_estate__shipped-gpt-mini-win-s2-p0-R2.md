---
game: ref_estate__shipped
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 2012
---
When I land on an unowned property I do not auto-buy; I first check affordability and prudence: I will buy if (a) the price is no more than 40% of my current cash AND the purchase would not drop me below 30 cash, or (b) the property has a notably higher rent/price ratio than board average or completes a set/strategic advantage that justifies exceeding the 40% threshold.

When I land on an unowned property and the price would leave me under 30 cash, I do not buy.

When I evaluate “notably higher rent/price ratio,” I prefer properties whose rent/price ratio meaningfully exceeds the board average or those that provide significant absolute rent; I also prefer a property that helps form a set even if its ratio is moderate.

When I pass or land on START I collect salary immediately and add it to my declared balance before making any buy decisions on that turn.

When I receive payments from other investors between my turns (rent or other transfers), I add them to my cash and count them toward my available funds for the next decision.

When I land on another investor’s property I pay the exact rent immediately and update my balance.

When I land on a property I already own I do nothing (no payment, no buy) and simply declare my unchanged holdings.

When my cash is low (below 30) I avoid purchasing additional properties until I recover via collected salary or incoming payments.

When deciding between multiple purchase opportunities I prefer the property with higher absolute rent and better rent-to-price ratio, with secondary preference for properties that complete sets or block opponents.

When an opponent offers a trade or deal, I accept only if it increases my declared net worth immediately (cash + purchase prices of deeds) or clearly improves my future income potential.

I always declare three tokens when settling a turn: [pay: N to P<k>] (or [pay: none]), [buy: yes] or [buy: no], and [balance: N] showing my updated cash, and I include any received payments or salary in that balance.