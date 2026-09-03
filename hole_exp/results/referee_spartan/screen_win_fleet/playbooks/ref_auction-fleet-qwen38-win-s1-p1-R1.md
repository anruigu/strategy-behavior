---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 2288
---
# Playbook

**Budget tracking is sacred.** Before every bid, compute: starting budget minus the sum of prices I actually paid for lots I won (not for lots I lost or passed on). State that number. Do not guess, do not carry forward a wrong number.

**In round 1 of any lot I value, bid at least 60–70% of my private value.** A low opening bid (like the minimum increment) signals weakness and invites the competitor to build a position I then have to match in round 2. In a 2-round auction, round 1 is my only chance to set the tone before the final push.

**In round 2 (final round), if I want the lot, bid my full private value.** Do not bid "minimum raise above the current high" and hope that's enough — a competitor who values it more will simply outbid me by the increment. Bidding my value is the maximum I can rationally pay; if they still beat me, the lot was worth more to them and I should let it go.

**The increment trap.** If my value is V and the current high in round 2 is H, the minimum winning bid is H + min_raise. If H + min_raise > V, I lose no matter what. If H + min_raise ≤ V, I can win at H + min_raise (profit = V − H − min_raise). I should always win in this case — never pass on a profitable final-round bid.

**When I do not value a lot highly (value < estimate), pass early.** Bidding into a lot where my value is below the estimate is likely to mean I'm the irrational one. A small probe bid is fine, but if the high climbs above my value before round 2 ends, I walk.

**Allocate budget by expected value, not greedily.** Before the auction starts, rank lots by (my value − estimate) or by my absolute value. My highest-value lots get my strongest early bids. Lower-value lots get a probe-and-exit approach. I should not let spending on a low-value lot in round 1 eat into my ability to compete for a high-value lot later.

**What did not work:** I opened my highest-value lot with a token bid and then was forced into a reactive final round where I lost by a few points to a competitor who had built a position. I also let my second-highest-value lot slip when I bid my full value in round 2 and still lost by one increment. Aggressive early bidding would have either won me the lot outright in round 1 or forced the competitor to reveal their hand earlier.