---
game: ref_auction
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 2232
---
When I bid, I always state my true remaining budget alongside the bid amount. True remaining funds means my starting budget minus amounts actually paid for lots I have already won — not minus my current bid, and never a small number. Writing [budget: 6] after bidding 6 on lot 4 was a mistake; the correct figure was 6 only because I'd already paid 24 for lot 2, and in general I must track it that way, not as 30-minus-the-bid.

I never bid above my value for the lot, no matter how the auction feels. If the standing high bid plus the minimum raise exceeds my value, I pass immediately.

In round 1 of a lot, I open at or near the minimum raise. Small increments keep the final price low; there is no benefit to jumping the price early with only two rounds of bidding.

Rivals jump the price aggressively between rounds: standing bids often doubled from round 1 to round 2 (8→20, 4→12, 8→16). So my round-1 min-raise routinely gets leapfrogged. With only two rounds per lot, round 1 may be my only chance to shape the price — if a lot is worth far more to me than the estimate, consider a larger round-1 raise (toward maybe 40–50% of my value) to set the base higher and make my round-2 raise decisive. My min-raise to 16 on lot 3 was still beaten by a jump to 20; a bigger round-1 bid might have won it.

In round 2 (the final round), I raise by exactly the minimum as long as the new price stays below my value, since this is my last chance to win. But I should also consider raising more than the minimum in round 2 when my surplus is huge — rivals can't respond, but a larger raise doesn't help me since round 2 is final anyway, so minimum raise is fine; the real fix is not losing round 1 by too little.

When a lot is worth much more to me than the estimate (e.g., value 49 vs estimate 37), I expect to win profitably and should press harder earlier — that's where the missed lot 3 (value 49, lost at 20) hurt.

When I am outbid at a price above my value, I fold without regret and save budget for later lots.

Track the running total of my payments as I win lots and deduct it from the stated budget from then on. The budget line is my actual remaining money; getting it wrong is the one catastrophic error to never repeat.