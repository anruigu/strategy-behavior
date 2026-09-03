---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 1688
---
- I treat my value for a lot as a hard ceiling: I never bid above it, and I only approach it when the surplus left is still clearly worth more than keeping the cash for later lots.
- When the standing bid is far below my value and nobody has opened or has opened low, I open modestly (near the minimum raise or a chunk below estimate), because big jump bids like my bid of 30 on a value-39 lot just give away surplus when opponents would have let it go cheaper.
- Each round I ask one question: does standing bid + minimum raise stay below my value? If yes and the margin is meaningful, I bid the minimum raise; if the margin is thin (within a few points), I pass and keep the budget for later lots.
- I never raise my own standing bid — when I am the high bidder I always pass. This worked and I keep it.
- Since only two rounds occur per lot, pass-or-bid in round 1 is cheap exploration; round 2 is final, so in round 2 I bid up to my full willingness-to-pay, not hoping for another chance.
- I keep a running ledger: budget minus every lot actually won, and nothing else. In this episode I repeatedly reported invented budgets (24 when I hadn't spent, 100, 168) — that is sloppy and risks bidding what I do not have. I state [budget: N] as exactly what the auction tells me I have left, and I subtract as soon as I am declared winner of a lot.
- I watch who wins early lots: an opponent who pays near or above estimate is burning budget, which makes later high-value lots cheaper for me, so I bid more patiently on early lots and more decisively late.
- When two lots remain and my budget is limited, I commit fully to the highest-value one rather than splitting thin bids across both.