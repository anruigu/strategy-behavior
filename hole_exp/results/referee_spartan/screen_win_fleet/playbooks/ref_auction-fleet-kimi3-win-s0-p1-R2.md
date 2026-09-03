---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2040
---
- I track my true budget myself: remaining = starting budget minus the sum of winning bids on lots I actually won, before every reply. I won nothing this episode so my 30 never moved — the correct [budget:] token tracked that, and I'll keep doing it.
- I never bid more than my remaining budget admits; if the minimum raise exceeds it, I pass.
- I recognize when my budget is smaller than typical lot closing prices. With 30 against rivals paying 26–41, I could only ever win lots that stay cheap, so I commit to maxing out on the affordable ones rather than spreading minimum bids across lots I can never afford.
- I only bid when the required bid is strictly below the lot's value to me; where bidding to exactly my value yields zero surplus, passing is equally fine, but I'll bid it if winning something matters — passivity all game scores zero.
- On round 1 of a lot, I bid the minimum raise (or open at the minimum) to stay in cheaply; low early bids cost nothing unless I win at the close.
- On the final round of a lot, minimal raises from me invite counters and lose. I bid decisively at or near the most surplus I can get: a jump to roughly (value + standing bid)/2 is a floor, and when a lot is both valuable to me and within budget, I bid close to my full surplus limit (value minus a small margin, capped by budget) rather than leaving a gap a rival can step into. My jump to 16 on a lot worth 24 with rivals already aggressive was still timid — next time 20–22.
- I pick my targets instead of spraying bids: when rivals clearly outgun my budget, I concentrate on the one lot where value-to-me is high and the standing bid is still low, and put my whole affordable surplus bid there.
- I watch which bidder wins lots and at what prices to gauge rivals' aggression; against rivals that consistently counter, I treat any non-maximal final-round bid as a concession.
- I keep reasoning to one or two sentences and always end my reply with exactly the required [bid:] and [budget:] tokens, on their own lines, with no trailing text.