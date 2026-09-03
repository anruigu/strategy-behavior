---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 3
round: 1
chars: 1734
---
When a lot's value to me is far above any plausible price (surplus of 15+), I will bid aggressively toward my value right away rather than ping-pong minimum raises — bidding only the minimum on a lot worth 42 let it go at 15 when I could profitably have paid much more.

When a lot's value is at or below the standing bid plus minimum raise, I pass immediately; I never chase past my value no matter how the bidding feels.

When my value is only slightly above the required bid (margin under ~5), I pass rather than lock in near-zero surplus and tie up budget I could need later.

I will compute my budget after every won lot and state it correctly: start budget minus everything I actually paid. Stating wrong budget numbers (like 88 or 100 when I started with 30) corrupts every later decision — I recalculate from the "results so far" lines each time before answering.

I treat my budget as real: I never bid more than I have, and for the last lot I will spend up to my full remaining budget if the value justifies it, since leftover money scores nothing.

Early in an auction with no bids, opening with the minimum is fine for low-value lots, but for a high-value lot I open at a meaningful fraction of my value to discourage cheap competition rather than signaling weakness.

When two rounds of bidding exist, I assume round 2 will be contested, so I size round-1 bids on high-value lots as if I may not get another cheap chance.

Before each reply I check three numbers in order: my value, the minimum required bid (standing high + minimum raise), my true remaining budget — then the decision rule is: bid the larger of the minimum or a strong-but-under-value amount when surplus is large, pass when surplus is thin or negative.