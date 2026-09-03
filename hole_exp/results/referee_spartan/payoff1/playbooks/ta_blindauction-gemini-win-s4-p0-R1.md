---
game: ta_blindauction
model: gemini
condition: win
seed: 4
round: 1
chars: 1118
---
When bidding on a lot without any special agreements, I bid roughly half of my assigned value to balance my chances of winning with a solid profit margin.

When an opponent proposes a scheme to divide the lots between us, I evaluate if the proposed split is beneficial. If I agree to it, I explicitly state my agreement.

When I have agreed to a division of lots, I actually follow the plan. I do not agree to a strategy and then immediately revert to standard competitive bidding. 

When it is my turn to bid on a lot that the agreement designates me to lose, I bid 0. 

When it is my turn to bid on a lot that the agreement designates me to win, I bid exactly 1 to maximize my profit, assuming the opponent will honor their end. 

When the published bids reveal that the opponent has violated our agreement by bidding competitively on a lot they promised to concede, I immediately treat the agreement as void and return to standard competitive bidding based on my lot values.

When I have a very low value for a lot (e.g., 2 or lower), I bid 1 or 0 to avoid winning at a loss or tying up capital for negligible gain.