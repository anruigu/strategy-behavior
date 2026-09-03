---
game: ref_auction
model: haiku
condition: win
seed: 3
round: 3
chars: 4339
---
# Playbook for ref_auction

## Budget Management
When I consider any bid, I must track my remaining budget accurately throughout the game. After each winning bid, I recalculate what I have left. My budget only decreases when I win a lot and pay the bid I made. If I lose a bid, my budget does not change. I will verify my budget statement against my actual spending history before each reply and correct errors immediately if I notice them. In the last episode, I corrupted my budget tracking by showing 199991 after lot 1 round 2 (a clear error), which cascaded through all remaining decisions. This was a critical failure and must not happen again.

## Valuation vs. Price Discipline
When a lot's value to me is below the estimate, I pass in round 1. Only in round 2, if the standing bid has dropped significantly below my valuation, do I reconsider entering.

When a lot's value to me is well above the standing bid, I enter the bidding immediately, even in round 1. The sooner I establish my interest, the better I can control escalation.

When the value to me is only marginally above the estimate (within 10%), I am cautious and pass unless the standing bid is very low. Lot 5 (34 vs. 32 estimate) should have been passed in round 1; the margin is too thin to justify spending budget.

## Strategic Raising
When I decide to bid, I raise by the minimum required amount, not more. This preserves my budget for subsequent lots and keeps the price as low as possible while maintaining my position.

## Lot Prioritization
Before round 1 of lot 1, I will mentally rank all five lots by the gap between my valuation and the estimate. I prioritize competing hardest on lots where my private valuation is highest relative to the estimate. I ration my limited budget toward the highest-value lots and pass readily on marginal ones. Lot 5 (34 vs. 32) and lots 2–4 (all marginal or negative margins) should receive lower priority than lot 1 (44 vs. 32, a +12 margin).

## End-Game Awareness
As I approach the final lot, I remember that this is my last chance to win value. If the final lot has high personal value to me relative to the estimate, I should be aggressive within the constraint of my remaining budget. If the final lot is marginal, I should pass and preserve my budget unspent. In the last episode, I spent my entire budget on lot 5 (a marginal lot worth only 34 vs. estimate 32). The standing bid was 15, and I paid 18. This was a poor use of capital.

## Aggression on Strong Value
When my valuation exceeds the estimate by a wide margin (e.g., lot 1: 44 vs. 32), I should bid in round 1 to establish control. Waiting risks losing to other bidders. I should also be willing to raise more aggressively in round 2 if the standing bid is still low. In the last episode, I bid only 3 in round 1 on lot 1 (the minimum), then only 9 in round 2 when the standing bid was 6. Bidder 2 took it at 12. I should have bid at least 12 in round 2 to push harder for this high-value lot.

## Correcting Past Errors
My budget tracking failure after lot 1 round 2 created a false sense of unlimited capital (showing 199991 when I had 27). This led me to bid on marginal lots 2, 3, and 5 at prices close to or above my valuations, which were not optimal uses of a limited budget of 30. In future, I will maintain accurate budget tracking and use it to ration my capital. I will also note when the system shows an implausible budget (e.g., 199991 when I started with 30) and immediately correct it.

## What Worked
Bidding on high-value, low-standing-bid scenarios with small minimum raises preserved budget and kept me competitive. My final score of +37 came from winning lot 2 at 16 (winning +37 on that lot) and lot 5 at 24 (breaking even). The strategy of raising the minimum amount when I did bid was sound.

## What Did Not Work
Passing on lot 1 round 2 when my valuation was 44 and the standing bid was 9 was too passive. I bid 9 instead of raising more aggressively (12 or higher). Bidding on marginal lots (2, 3, 5) at prices close to my valuations was wasteful when my budget was limited to 30. I should have concentrated my bids on lot 1, the highest-value opportunity. Spending any budget at all on lot 5 (34 vs. 32) in round 2 when the bid was already 15 was unjustified; the value margin did not warrant it, and I had already won lot 2.