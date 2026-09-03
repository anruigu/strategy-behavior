---
game: ref_auction
model: gpt-mini
condition: win
seed: 3
round: 2
chars: 3146
---
When a lot is presented, compute my private value and the current standing high bid; if value − standing_bid ≤ 0, I pass.

When the standing high bid is below my value, consider raising only if the final price I would have to pay (after the raise) still leaves nonnegative surplus and I am willing to accept that surplus given remaining lots; prefer strictly positive surplus for nontrivial bids.

When making an opening bid, bid a meaningful amount but never more than my private value; prefer an opening that signals interest while preserving at least one competitive raise buffer (keep at least the minimum raise amount available in available budget if I might need to respond).

Track budget correctly and explicitly: my available budget = initial_budget − sum(current winning bids I have committed to). When I place or increase a standing high bid for myself, update the committed amount immediately and report the new available budget. Never report an impossible budget or forget prior commitments.

When facing a rival's bid in an intermediate or final round, raise only by the minimum allowed if that final price still leaves positive surplus (value − new_price > 0). Do not escalate beyond the point where value − price becomes negative. If the minimum allowed raise would push price to equal my value, prefer to pass unless denying the lot has strategic value greater than zero.

When I would have to pay more than my private value to win, pass. Do not chase to deny others if it costs me positive expected loss.

When multiple lots remain, prioritize lots by expected surplus (value − estimate or value − likely final price) and preserve budget for higher-priority lots rather than spending all-in on a lower-priority lot unless its surplus is large enough to justify it.

When considering an all-in or near-all-in bid, require that the expected net gain (value − price) is clearly larger than the opportunity cost of being unable to bid on remaining lots.

When the minimum raise is small relative to my surplus, use minimum raises to try to win cheaply; when the minimum raise is large and would push the price above my willingness to pay, pass.

If I have already won items whose total committed spend consumes most of my budget, stop opening new bids unless the new item has strictly higher surplus that justifies the expenditure.

Do not bid for non-economic reasons (signaling, spite) unless I have a documented strategic reason and it does not violate my budget constraints.

Explicit bidding behavior:
- Opening bid: choose an amount below my value that leaves me at least min_raise in available budget if I might need to respond, and that gives a comfortable surplus margin.
- Intermediate round: if already winning and surplus > 0, pass to conserve budget; raise only if necessary to maintain a positive surplus after the raise.
- Final round: raise only by the minimum allowed and only if value − (standing_bid + min_raise) > 0 (or accept zero only if strategic denial rationale > 0).

Always recompute and state my available budget correctly when I act, reflecting the amount I would pay if my standing bid remains winning.