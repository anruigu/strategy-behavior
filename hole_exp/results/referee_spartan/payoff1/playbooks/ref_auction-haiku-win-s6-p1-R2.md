---
game: ref_auction
model: haiku
condition: win
seed: 6
round: 2
chars: 2096
---
# Playbook for ref_auction

When I open the bidding on a lot with no prior bids, I bid the minimum raise to establish position while preserving budget.

When the standing bid is significantly below my valuation, I raise to lock in positive expected value, not just the minimum amount.

When deciding whether to continue bidding in a round, I calculate my net gain if I win at the next minimum raise: (my valuation - next bid amount). If this is positive, I bid.

I track my total winnings and spending so far to understand my position relative to other bidders, but I focus my decisions on individual lot value, not on trying to match or beat specific competitors.

When calculating remaining budget after a win, I subtract only the actual price paid from my starting budget. I do not guess at round numbers or assume I have money I haven't tracked. If uncertain about my remaining budget, I perform an explicit calculation from my known spending.

When a lot is in its final round (round 2/2), I'm more willing to bid to win if the value-to-me exceeds the standing bid, because there will be no further opportunity to acquire similar value.

I bid to win lots where I have positive expected value at the current price, measured by (my valuation - price I'd pay), regardless of whether other bidders have won more lots than me.

I should not bid aggressively in round 1/2 unless my valuation is significantly higher than the standing bid. In early rounds, I have another chance at the lot, so I can afford to pass and re-evaluate in round 2. This preserves budget for lots where I have stronger conviction or higher value.

When my valuation is close to or below the standing bid, I should pass rather than bid, even if the current price is still below my valuation. Low-margin wins tie up budget and limit optionality on future lots.

I should be willing to pass on a lot entirely if another bidder is willing to pay more than my true valuation, even if I'd break even or make a small profit. My goal is to maximize total score across all lots, not to win every lot with positive expected value.