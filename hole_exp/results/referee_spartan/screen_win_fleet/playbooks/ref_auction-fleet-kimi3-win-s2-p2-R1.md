---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1946
---
When a lot is put to me, I first compute the ceiling: the minimum of my value for the lot and my remaining budget. I never bid above that ceiling, no matter how close the auction feels.

When the minimum raise already exceeds my value, I pass immediately and do not hesitate or re-litigate it on the next round.

On round 1 of a lot, I bid near the minimum raise when the price is well below my value, because a cheap early bid keeps me in without committing much. I do not jump high early unless the standing bid is already close to my value.

On round 2 — the final round — I treat it as now-or-never. If the lot's value to me is high and the standing bid is still far below it, I bid aggressively, close to my full remaining budget or value, whichever binds. Bidding only half my value on a lot I deeply value just hands it to a rival at a price I would happily have beaten; that was my clearest mistake, and I will not repeat a timid final-round bid on a high-value lot.

Before stating a bid, I check my arithmetic: my running spend equals the sum of lots I have already won, and my budget-left token must be 30 minus that spend plus nothing else. I do not write a budget number from memory or from the lot's value — I recompute it from the results list every single time, because sloppy budget tokens corrupted several of my replies.

I keep a reserve plan: if later lots might be valuable, I avoid spending so much early that I cannot compete on them, but I never let reserve-saving turn into underbidding on a lot whose value clearly exceeds the price.

When I win a lot, I note the exact price paid and update my mental ledger before the next lot opens.

On the last lot, if my value exceeds the required bid, Ibid up to my full remaining budget, since unspent money has no value at the end.

I always end my reply with both bracketed tokens, bid first, budget second, with no trailing spaces or formatting slip that could break parsing.