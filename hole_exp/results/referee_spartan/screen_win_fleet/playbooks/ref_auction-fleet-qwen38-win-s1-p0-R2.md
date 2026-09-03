---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 2667
---
# Playbook: Ref Auction

**Budget tracking — the first thing I do before any bid:** my budget is the number given in the prompt ("You start with a budget of X"). I track it by subtracting only the prices of lots I have actually won. Bids I made that were outbid cost nothing. Before every reply I compute: starting budget minus sum of winning prices so far. I never assume a default. In the last episode I started with 30 and reported 100 for most of the auction, which likely invalidated my bids or confused the system. This is the single most dangerous error I can make.

**When the standing high is at or above my value:** pass immediately. No bid I can make will be profitable. Do not open a position in round 1 on a lot where my value is at or below the estimate if the high is already near or above my value.

**When I'm in the final round and the standing high is well below my value:** bid near my true value, not the minimum raise — but only if I can actually afford it. The minimum raise is a trivial deterrent that invites a profitable counter with no round left for me to respond. If I value it at 54 and the high is 12, I should bid in the 40s, not 16. If I cannot afford a bid near my value, I should pass rather than make a bid I can't sustain.

**When I'm in round 1 and the lot is clearly valuable to me (value well above estimate):** I can open at the minimum to probe, but I must be prepared to jump significantly in round 2. The two-round structure means round 2 is where the real commitment happens.

**When I'm in round 1 and my value is only marginally above the estimate or below it:** open at the minimum only if I'm willing to pass in round 2. In practice, if my value is only 1–3 points above the estimate, the lot is rarely winnable profitably because opponents will push the price to or above the estimate. A probe is acceptable (it costs nothing if I'm outbid) but I should expect to pass in round 2 and not count on winning.

**On the two-round structure specifically:** being first to bid in the final round is a disadvantage — other bidders can see my bid and raise above it. In the final round I should either (a) bid high enough that no rational opponent can profitably exceed it, or (b) pass if I can't. There is no safe middle ground. A bid that leaves room for a counter-bid within someone else's value range is a gift.

**What did not work:** (1) Misidentifying my starting budget and reporting impossible figures — this is a mechanical error, not a strategy error, and it can invalidate bids. (2) Bidding the minimum raise in the final round when I had a large margin — it invites a counter and I have no round left to respond.