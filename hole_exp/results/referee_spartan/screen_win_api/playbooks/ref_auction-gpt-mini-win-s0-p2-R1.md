---
game: ref_auction
model: gpt-mini
condition: win
seed: 0
round: 1
chars: 1812
---
When the standing high bid is below my private value and I can win by raising by the minimum raise without paying more than my value, I raise by exactly the minimum raise (or to the smallest bid ≤ my value that outbids the standing high bid).

When the standing high bid is greater than or equal to my private value, I pass.

When the minimum raise would force me above my private value, I pass.

When there are no bids on a lot, I open with a bid no higher than my private value and preferably at the minimum reasonable starting level (e.g., the lot estimate or a small increment below my value) rather than immediately bidding my full value.

When I place a bid, I immediately subtract the full bid amount from my remaining budget and report that remaining budget accurately in the bid token.

When outbid in the first round, I re-evaluate using only my remaining budget and my private value; I will only raise in the second round if raising to the minimum (or the smallest profitable increment) still leaves the price ≤ my private value.

When winning a previous lot, I update my budget and use that updated budget for all subsequent decisions; I do not assume any outside replenishment.

When another bidder’s current standing bid already exceeds my private value by more than the minimum raise, I do not chase the lot—even for strategic reasons—if it would produce a negative payoff.

If a lot’s private value is close to the current high bid (within one minimum raise), I prefer to either make the minimal profitable raise or pass; avoid escalating bidding wars that require multiple raises unless I still profit at the expected final price.

If I notice any inconsistency in my reported budget or a bookkeeping error, I correct it immediately and base all future actions on the corrected remaining budget.