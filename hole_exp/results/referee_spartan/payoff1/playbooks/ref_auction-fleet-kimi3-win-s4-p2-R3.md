---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2818
---
- Budget tracking is my biggest failure point. The rules told me 30 to start, yet I mid-episode calculated with 100 and output [budget: 44] and [budget: 60] — numbers above my real remaining budget. Before every bid I recompute: stated start (30) minus prices actually paid on lots I won so far. That computed number, and only that number, goes in the [budget:] token.
- Sanity check every time: my bid must be ≤ the budget I'm about to state, and the stated budget must equal start minus paid-so-far. If either check fails, I fix the numbers before replying.
- A sloppy budget line may get my bid discarded or flagged, so the budget token has the same priority as the bid itself — never an afterthought.
- Bids made when my remaining budget is 0 are dead bids — never waste one; if broke, pass cleanly.
- Budget is scarce across the WHOLE auction. At the start, tally values across all lots and pre-allocate budget toward the highest-value lots. Never let cheap early lots consume budget needed for a big-value lot later.
- My surplus on a lot is value minus price paid. Before committing budget, compare a lot's potential surplus against surplus I'd forgo later — winning thin-margin early lots while a fat one is still coming is the classic failure.
- Paying near full value is only acceptable on the lot with the best remaining value. If a round-1 lot would take most of my budget at a thin margin, let a rival have it.
- My hard ceiling on any lot is its value to me. I never bid above value, even to block or win.
- In a lot's final round, if I want it and can afford it, I bid up to (never above) its value. First confirm the bid fits remaining budget.
- When standing bid plus minimum raise would exceed my value, I pass immediately.
- In round 1 I make minimum raises on lots inside my planned allocation to stay in cheaply; I may pass round 1 on an early lot outside the plan even with money in hand.
- Before each bid I briefly state remaining lots and their values to me, checking this bid against the global plan, and which round I'm in (minimum now vs. up-to-value in the last round).
- Winning below value at minimum-increment prices is excellent value-per-dollar; as this episode showed, grabbing cheap lots (12 for value 26) plus one near-value buy on a surplus-positive top lot (40 for 44, 30 for 45) sums to a strong total — a couple of cheap wins plus planned big-surplus wins is the pattern to aim for under a tight budget like 30. Under a 30 budget I should NOT have won lot 1 at 40 (impossible) nor spent 52 total (impossible); with a real 30, I should pass or tap out when a lot's standing price approaches my budget and target the lots where value-minus-price is largest within my real limit.
- I reply exactly once, reasoning brief, ending with [bid:] and [budget:] tokens on their own lines.