---
game: ref_auction
model: haiku
condition: win
seed: 3
round: 2
chars: 3362
---
# Playbook for ref_auction

## Budget Management
When I consider any bid, I must track my remaining budget accurately throughout the game. After each winning bid, I recalculate what I have left. I notice in this episode I made a critical error: after bidding 12 on lot 1 round 2 and losing, I somehow showed a budget of 200,000 instead of 27. This corrupted all subsequent budget tracking. In future, I will verify my budget statement against my actual spending history before each reply. If I lose a bid, my budget does not change; only winning bids reduce it.

## Valuation vs. Price Discipline
When a lot's value to me is below the estimate, I pass in round 1. Only in round 2, if the standing bid has dropped significantly below my valuation, do I reconsider entering.

When a lot's value to me is well above the standing bid, I enter the bidding immediately, even in round 1. The sooner I establish my interest, the better I can control escalation.

## Strategic Raising
When I decide to bid, I raise by the minimum required amount, not more. This preserves my budget for subsequent lots and keeps the price as low as possible while maintaining my position.

## Lot Prioritization
I assess all five lots mentally to identify which ones offer me the most value. I prioritize competing hardest on lots where my private valuation is highest relative to the estimate. In this episode, lot 5 (valuation 49) and lot 1 (valuation 38) were my strongest opportunities; lots 2, 3, and 4 were marginal. I should have been willing to spend more on the high-value lots and pass more readily on the marginal ones.

## End-Game Awareness
When I reach the final lot, I remember that this is my last chance to win value. If the final lot has high personal value to me, I should be aggressive within the constraint of my remaining budget. In this episode, I won lot 5 at a reasonable price (24) and secured +74 total, which suggests this strategy worked.

## Aggression on Strong Value
When my valuation exceeds the estimate by a wide margin (e.g., lot 1: 38 vs. 29), I should bid in round 1 to establish control. Waiting risks losing to other bidders. In this episode, I lost lot 1 to bidder 2 at 18—a bid I could have beaten if I had raised more aggressively in round 2 when the standing bid was only 9.

## What Did Not Work
My budget tracking failure on lot 2 onwards created a false sense of unlimited capital. This led me to bid on marginal lots (2 and 3) at prices close to my valuations (20 vs. 40 and 20 vs. 20), which were not optimal uses of a limited budget of 30. In future, I will maintain accurate budget tracking and use it to ration my capital toward the highest-value lots.

Passing on lot 1 round 2 when the bid was 9 and my valuation was 38 was too passive. The margin was enormous. I should have bid at least 12 to take control, which I did—but I need to track the outcome: bidder 2 won at 18. This suggests bidder 2 was willing to go higher. If I had raised more aggressively (to, say, 15 or higher in round 1), I might have won it.

## What Worked
Bidding aggressively on high-value, low-standing-bid scenarios (lots 1, 4, 5) was sound. My final score of +74 came from winning lots 2, 3, and 5, all at prices below or close to my valuation. The strategy of raising the minimum amount and only bidding when the value gap was clear kept me in contention.