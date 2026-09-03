---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2445
---
- I treat my value for a lot as a hard ceiling: I never bid above it, and I only approach it when the surplus left is still clearly worth more than keeping the cash for later lots.
- Round 2 is final and winner-takes-all: bidding only the minimum raise there loses lots I clearly value. I lost lot 1 (value 34, standing 9) and lot 4 (value 27, standing 12) this way — a rival jumped past my minimal raise and I had no third round to respond. In round 2, when the margin is large, I bid a decisive amount well above the minimum (often estimate level or a few points below my value), accepting less surplus in exchange for actually winning.
- On round 2 I size my bid by margin: huge margin (standing less than half my value) → jump bid to roughly estimate; moderate margin → a raise of 30–50% of the gap to my value; thin margin (a few points) → pass.
- When the standing bid is far below my value and nobody has opened, I open near the minimum in round 1 — cheap probing is still fine early — but I never assume a round-1 low standing price will survive to a cheap round-2 close.
- I never raise my own standing bid — when I am the high bidder I always pass. This worked (lot 5 won with surplus of 7) and I keep it.
- I keep a running ledger from the stated results only: I start at the given budget and subtract exactly the price I paid each time "bidder 0 won" appears. This episode I reported 30, then 100, then other invented figures while having spent nothing — slot-machine budget tokens are worse than useless. If uncertain, I report the budget implied by the official results-so-far block, and I mark my final-round bids as small enough that even the true budget covers them.
- Passing on low-value lots is correct even when I could win them cheaply; my pass on lot 3 cost nothing and preserved positioning. I keep passing whenever standing + minimum raise leaves under ~5 points of surplus or the lot is below estimate for me only trivially.
- I watch who wins early lots and at what price: an opponent paying near estimate repeatedly is likely value-driven and will jump late, so on final rounds against active bidders I jump preemptively rather than nudge.
- Winning something positive beats maximizing surplus per lot: ending at +7 from one lot after losing three winnable ones is a bad trade. I rank each remaining lot by (value − standing) and make sure I actually secure at least the top one or two with decisive final-round bids.