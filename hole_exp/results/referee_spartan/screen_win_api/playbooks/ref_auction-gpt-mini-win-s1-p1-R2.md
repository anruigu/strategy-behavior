---
game: ref_auction
model: gpt-mini
condition: win
seed: 1
round: 2
chars: 3085
---
When a lot opens with no bids and my private value > 0, I generally place the minimum opening bid (current high + minimum raise) only if that bid leaves me with enough budget to pursue remaining desirable lots; require a modest reserve proportional to remaining lots (e.g., keep at least ~1/3 of budget per remaining high-value opportunity).

When there is a standing high bid, I raise only if the next required bid (current high + minimum raise) is strictly less than my private value and I can afford it without violating my reserve. I bid exactly the minimum required raise (current high + minimum raise) to keep the price low.

When the current high bid is at or above my private value, I pass immediately.

When an opponent outbids me, I only counter if the new required bid remains below my private value and my reserve constraints still hold; otherwise I concede that lot.

When I'm leading a lot going into the final round, I do not further increase my bid unless outbid and the new required bid is still below my private value and reserve constraints permit a counter.

In the final round for a lot, I am willing to raise up to my private value (but never above it) because there are no future opportunities for that lot; still keep reserve constraints in mind for remaining lots.

Prefer contesting lots with larger expected surplus (my value − next required price) and avoid chasing lots with tiny surplus that would deplete budget needed for higher-surplus future lots.

Never bid more than my private value for a lot.

Always update my remaining budget correctly after each winning bid (subtract what I paid), and never propose a bid that would exceed my remaining budget.

Compute the minimum raise precisely from the lot's rule and apply it to the current high bid; place bids equal to current high + minimum raise when choosing to raise.

Avoid spending a large share of my budget early; maintain a deliberate reserve for expected remaining desirable lots and adjust that reserve downward only if later opportunities are poor.

When opponents escalate aggressively and push prices well beyond apparent values, stop matching escalation—let them overpay and focus on cheaper wins.

If winning multiple low-surplus lots would exhaust budget and prevent acquiring higher-value lots later, prioritize conserving budget even if it means passing on modest positive-surplus bids.

Track results so far (which lots opponents won and at what prices) to update my estimate of how aggressively opponents bid and to adapt reserve sizing for remaining lots.

Bid conservatively (minimum raises) to avoid signaling excessive willingness to pay; only jump beyond the minimum if strategic (e.g., to secure a must-have lot when remaining opportunities are limited and my private value justifies it).

When uncertain about future lot values, bias slightly toward conserving budget (raise less often) unless a lot's surplus is clearly large.

Keep my play deterministic and simple: open minimum when profitable, raise minimally while next bid < my value and budget permits, pass otherwise.