---
game: ref_auction
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 1943
---
When a lot is presented, compute my private value minus the current standing high bid; if that difference is <= 0, I pass.

When the standing high bid is below my value, raise only if I can still afford a final winning price that leaves nonnegative surplus (value − price ≥ 0) and leaves budget for future lots I might value more.

When making an opening bid, bid a meaningful amount but never more than my private value; prefer a bid that signals interest but preserves at least one competitive raise buffer (keep > minimum raise available).

When facing a rival's bid in the final round, raise only by the minimum allowed if that final price still leaves positive surplus for me; do not escalate beyond the point where value − price becomes negative.

When I would have to pay more than my private value to win, pass. Do not chase to deny others if it costs me positive expected loss.

When multiple lots remain, prioritize lots by (private value − estimate) and preserve budget for higher-priority lots rather than spending all-in on a single lot unless the surplus is large enough to justify it.

When considering an all-in or near-all-in bid, require that the expected net gain (value − price) is clearly larger than the opportunity cost of being unable to bid on remaining lots.

Always compute and update my budget accurately: budget_new = budget_old − any bid amount I am currently winning. Never increase my budget or report incorrect totals.

When the minimum raise is small relative to my surplus, use minimum raises to win cheaply; when the minimum raise is large and would push the price above my value, pass.

If I have already won items whose total spend consumes most of my budget, stop opening new bids unless the new item has very high surplus; conserve funds for items with strictly higher surplus.

When tempted to outbid for signaling or spite, stop and recalculate objective surplus — do not bid for non-economic reasons.