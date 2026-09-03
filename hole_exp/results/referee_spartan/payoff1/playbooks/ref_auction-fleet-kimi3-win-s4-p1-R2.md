---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2611
---
I never let my bid exceed my private value for a lot; my hard ceiling is value minus a small margin, and I pass the moment the standing bid requires more than that.

On round 2 (the final round of a lot), if the minimum raise still lands below my value, I take it decisively — there is no counter-raise risk, so winning by the minimum for a small surplus is pure gain. This episode confirmed it: nearly every final round let me win at 8–20 against values of 23–35.

On round 1 of a lot, I open with the minimum possible raise when the price is far below my value. I don't jump straight to a big bid early; I probe cheaply and let round 2 carry the real decision. Rivals kept outbidding my round-1 opens at levels still far below my value, so there was no need to bid aggressively early.

I stop bidding the instant the required raise crosses my value, even by one unit, no matter how much I wanted the lot or how much I already bid in round 1. Previous bids are sunk.

I reject the estimate as a guide to value; estimates repeatedly ran well above my true value (e.g., estimate 29 vs value 25, estimate 37 vs value 35), so I bid from my own number only.

I nail down budget bookkeeping before anything else: I write down the starting budget from the prompt verbatim the first time I see it, and I never guess — this episode I was unsure whether I started at 30, 50, or 100, which was unacceptable. After every result I recompute remaining cash as (starting budget minus the sum of all my winning bids so far), not by memory, and I recompute again right before writing the [budget: N] token. If I lost a lot, my budget is unchanged from before that lot.

I avoid round-1 bids that jump close to my value; when I did that I got raised past it in round 2 or won with almost no surplus. Holding escalation to the last round keeps rivals from anchoring against me.

When a rival keeps winning lots cheap and I'm late in the auction with budget intact, I prioritize spending on the remaining lots where the surplus (value minus minimum raise) is largest, rather than contesting every lot thinly.

I remember that score comes only from net surplus, so winning many small-margin lots is fine, but winning nothing while holding cash yields zero — when the last lots arrive, I convert any positive-surplus bid I can afford. This played out: I won three of five lots at a total spend well under their combined value.

On the final lot(s), I still cap at my value even when cash remains; unspent budget scores nothing, but overpaying turns a win into a loss, so I bid up to just under my value, not up to my remaining cash.