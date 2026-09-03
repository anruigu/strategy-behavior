---
game: ref_auction
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 2120
---
When the standing high bid is below my private value and I can win by raising by the minimum raise without paying more than my value, I raise by exactly the minimum raise (i.e., bid the smallest legal amount that outbids the standing high bid and is ≤ my private value).

When the standing high bid is greater than or equal to my private value, I pass.

When the minimum raise would force me above my private value, I pass.

When there are no bids on a lot, I open with a bid no higher than my private value and preferably at the minimum reasonable starting level (for example, the lot estimate or the smallest legal opening bid) rather than immediately bidding my full value.

I always ensure my bid does not exceed my remaining budget. I subtract the full bid amount from my remaining budget immediately when I place the bid and report that remaining budget accurately; I will not report or act with an impossible budget.

When outbid in the first round, I re-evaluate using only my remaining budget and my private value; I will only raise in the second round if raising to the minimum (or the smallest profitable increment) still leaves the price ≤ my private value and ≤ my remaining budget.

When winning a previous lot, I update my budget and use that updated budget for all subsequent decisions; I do not assume any outside replenishment.

When another bidder’s current standing bid already exceeds my private value by more than the minimum raise, I do not chase the lot—even for strategic reasons—if it would produce a negative payoff.

If a lot’s private value is close to the current high bid (within one minimum raise), I prefer to either make the minimal profitable raise or pass; avoid escalating bidding wars that require multiple raises unless I still profit at the expected final price.

If I notice any inconsistency in my reported budget or a bookkeeping error, I correct it immediately and base all future actions on the corrected remaining budget.

I prefer conservative, incremental bidding: make the minimum legal raises that secure profitable wins rather than large jumps that risk wasting budget.