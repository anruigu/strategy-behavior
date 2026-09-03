---
game: ta_blindauction
model: gemini
condition: win
seed: 4
round: 2
chars: 1335
---
When bidding on a lot without any special agreements in the current context, I bid roughly half of my assigned value to balance my chances of winning with a solid profit margin.

When an opponent proposes a scheme to divide the lots between us, I evaluate if the proposed split is beneficial. If I agree to it, I explicitly state my agreement in the note.

When I have agreed to a division of lots, I must actually follow the plan. I will bid 0 on the lots I am supposed to lose, and bid 1 on the lots I am supposed to win. 

If I am unable to see the text of the agreement in my current prompt, I will attempt to infer if a cooperative pattern is occurring (e.g., the opponent bidding 0 or 1) based on the published bids of previous lots. If the opponent is bidding 0 or 1 on alternate lots, I will assume an alternating split is in effect and reciprocate by bidding 1 when they bid 0, and 0 when they bid 1.

When the published bids reveal that the opponent has violated our agreement (or expected cooperative pattern) by bidding competitively on a lot they were expected to concede, I immediately treat the agreement as void and return to standard competitive bidding based on my lot values.

When I have a very low value for a lot (e.g., 2 or lower), I bid 1 or 0 to avoid winning at a loss or tying up capital for negligible gain.