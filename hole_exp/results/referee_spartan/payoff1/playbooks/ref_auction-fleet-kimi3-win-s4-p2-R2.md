---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 2214
---
- When the rules state my starting budget, I write it down and use that number — never assume a different one (never invent "50" when told 30). Every budget line is (stated start minus what I've actually paid for lots won); a pending bid isn't spent until I win.
- Bids made when my remaining budget is 0 are dead bids and get ignored — never waste a bid accompanied by [budget: 0]; if I'm broke, pass cleanly.
- Budget is a scarce resource across the WHOLE auction, not per lot. At the start, tally my values across all lots and roughly pre-allocate budget toward the highest-value lots. Never let cheap early lots consume the budget needed for a big-value lot later.
- My surplus on a lot is value minus what I pay. Before committing budget to a lot, compare its potential surplus against surplus I'm forgoing on later lots. Winning lot 1 at 18 for value 19 (+1) and lot 2 at 12 for value 22 (+10) burned all 30 while a 46-value lot was still coming — a crippling misallocation.
- Paying near full value is only acceptable on the lot with the best remaining value. If a round-1 lot would take most of my budget to win at a thin margin, let the rival have it and preserve budget for bigger fish.
- My hard ceiling on any lot is its value to me. I never bid above value, even to block a rival.
- In the final round of a lot, when I want it AND have budget, I bid up to value if needed. But first confirm the bid fits in remaining budget — a bid I can't cover is worthless.
- When the standing bid plus the minimum raise would exceed my value, I pass immediately.
- In the first round of a lot, I raise with the minimum legal bid only if that lot is in my planned allocation; if I've already allocated my budget to later higher-value lots, I may pass on round 1 of an early lot even with money in hand.
- Before bidding on any lot, I state (to myself) remaining lots and their values to me, so each bid is checked against the global plan, not just the local bargain.
- I check which round I'm in before deciding aggressiveness: minimum raises in round 1; up to value (within budget) in the last round.
- I reply exactly once, reasoning brief, ending with the required [bid:] and [budget:] tokens on their own lines.