---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 1550
---
- When the rules state my starting budget, I write it down and use that number — never assume a different one. If the stated budget is 30, every budget line tracks from 30.
- My hard ceiling on any lot is its value to me. I never bid above value, even to block a rival; bidding past value locks in a guaranteed loss.
- In the final bidding round of a lot, when I want it, I bid as high as value minus (minimum raise minus 1) if needed — this is my last chance to win, so bidding near value is correct; surplus at value minus epsilon is tiny, so it only matters when the standing bid is far below value, where cheap wins are already likely.
- When the standing bid plus the minimum raise would exceed my value, I pass immediately.
- In the first round of a lot, I generally raise with the minimum legal bid; there's a second round to react if rivals outbid me, and small raises conserve budget without giving up the lead cheaply.
- When I have spare budget and a lot is cheap relative to its value to me, I still take it with the minimum raise rather than skipping — small positive surpluses add up.
- I always state the budget remaining as (starting budget minus what I've actually paid for lots won) — a pending bid isn't spent until I win, so I don't subtract standing bids.
- I check which round I'm in before deciding aggressiveness: conservative minimum raises in round 1; bid up to value in the last round if I still want the lot.
- I reply exactly once, reasoning brief, ending with the required [bid:] and [budget:] tokens on their own lines.