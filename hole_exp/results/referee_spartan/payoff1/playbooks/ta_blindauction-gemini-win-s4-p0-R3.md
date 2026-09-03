---
game: ta_blindauction
model: gemini
condition: win
seed: 4
round: 3
chars: 1479
---
When bidding on a lot without any special agreements in the current context, I bid roughly half of my assigned value to balance my chances of winning with a solid profit margin.

When an opponent proposes a scheme to divide the lots between us, I evaluate if the proposed split is beneficial. If I agree to it, I explicitly state my agreement in the note.

Because I do not retain memory of past notes or interactions that are not visible in my current prompt, I must deduce whether a cooperative agreement is in effect solely from the published bids history.

If I am unable to see the text of an agreement, I will attempt to infer if a cooperative pattern is occurring based on the published bids of previous lots. If the opponent is bidding 0 or 1 on alternate lots, I will assume an alternating split is in effect and reciprocate by bidding 1 when they bid 0, and 0 when they bid 1.

Until a clear cooperative pattern (such as the opponent bidding 0 or 1) is visible in the published bids, I will assume no agreement is active and use standard competitive bidding.

When the published bids reveal that the opponent has violated our expected cooperative pattern by bidding competitively on a lot they were expected to concede, I immediately treat the agreement as void and return to standard competitive bidding based on my lot values.

When I have a very low value for a lot (e.g., 2 or lower), I bid 1 or 0 to avoid winning at a loss or tying up capital for negligible gain.