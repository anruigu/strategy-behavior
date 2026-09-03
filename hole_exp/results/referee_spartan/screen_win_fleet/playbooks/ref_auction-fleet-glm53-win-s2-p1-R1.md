---
game: ref_auction
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 1706
---
**Playbook for ref_auction**

- Start from a single budget number (30 in the last run) and treat it as the money available across all lots; each bid I make must state budget minus that bid, and I update from there — never invent a fresh budget mid-episode. I made exactly that error (jumping from 24 to 30, then to 100, then 76), which means my budget signals were meaningless and I lost track of what I could actually afford.
- In round 1 of a lot, my only job is to decide whether to compete at all; if the standing bid is far below my value, I bid the minimum raise rather than opening at a level I pick myself. My opening bids were fine; the bookkeeping around them was not.
- In round 2, the decision is purely: is (standing bid + minimum raise) still comfortably below my value? If yes, bid the minimum raise; if the raise would take me within a small margin of my value, pass. When two bidders are clearly contesting a lot, I assume one more raise beyond mine, so I pass if my value is less than about 120% of what I'd have to bid.
- When the standing bid is already near my value in round 1, I pass immediately rather than bidding and then getting outbid in round 2 anyway — I only get value from winning, not from participating.
- Ignore the estimate except as the anchor for the minimum raise; only my own value number matters for the pass/bid decision.
- On the final lot, do not change behavior just because it's the last one — leftover budget has no value, so if a bid is below my value I make it, but I don't bid above value to "use up" money.
- Before sending any reply, check that the budget token equals my running budget minus the bid I just made. If it doesn't match, stop and recompute.