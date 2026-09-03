---
game: ref_auction
model: haiku
condition: win
seed: 6
round: 1
chars: 1479
---
# Playbook for ref_auction

When I open the bidding on a lot with no prior bids, I bid the minimum raise to establish position while preserving budget.

When the standing bid is significantly below my valuation, I raise to lock in positive expected value, not just the minimum amount.

When deciding whether to continue bidding in a round, I calculate my net gain if I win at the next minimum raise: (my valuation - next bid amount). If this is positive, I bid.

I track my total winnings and spending so far to understand my position relative to other bidders, but I focus my decisions on individual lot value, not on trying to match or beat specific competitors.

When I have remaining rounds after winning a lot, I don't assume my budget is depleted—I calculate what I actually spent and what I have left, then use that for future bidding decisions.

I avoid making bids when my budget calculation is uncertain. If I don't have reliable information about my remaining budget, I should not guess at a large round number like 200000—this signals I've lost track of my actual position.

When a lot is in its final round (round 2/2), I'm more willing to bid to win if the value-to-me significantly exceeds the standing bid, because there will be no further opportunity to acquire similar value.

I bid to win lots where I have positive expected value at the current price, measured by (my valuation - price I'd pay), regardless of whether other bidders have won more lots than me.