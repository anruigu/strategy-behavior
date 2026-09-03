---
game: ref_auction
model: fleet-glm53
condition: win
seed: 1
round: 3
chars: 3078
---
**Playbook for ref_auction**

- **The [budget: N] token is functional, not decorative.** Bids get invalidated by wrong or too-low declared budgets. State the budget you actually have: starting budget minus all money committed on winning bids so far. If unsure of the starting figure, note it at the first prompt and track every subsequent win's price against it. Never let the stated budget drift between rounds (I wrote 30, then 100, then 68 in one episode — pick one true ledger and keep it).

- **Round 2 is not the last word for my bid.** With only 2 rounds of my own bidding, opponents apparently can still end up winning above my round-2 number (I bid 24 over a standing 15 and lost at 27; I bid 15 over a standing 6 and still lost). A "decisive" round-2 bid of just standing + a few raises is not decisive. In the final round I should bid close to my full value for the lot, not a polite increment — my value minus a tiny buffer is the bid, since a losing bid costs nothing and a barely-winning one captures all the surplus.

- **Bidding incrementally is only for round 1.** Minimum-raise opening bids in round 1 are cheap and fine. Round 2 is go-big-or-pass: either bid near my value ceiling or don't bid at all. Bidding value-minus-small-buffer in round 2 maximizes win probability at near-maximum surplus per win.

- Set my ceiling before the final round: my value minus a small buffer. Never exceed value. But do not confuse "below value" with "enough to win" — 24 on a lot worth 28 to me was below value and still lost. With thin margins (value ≤ standing + ~15), consider passing and saving judgment for lots where value far exceeds the current price.

- If I'm already the standing high bidder going into the final round, do not bid again — I'd be raising my own price. Check whose the standing bid is before adding a raise.

- Round 1: open cheaply (minimum raise) on any lot whose value to me is above the required bid. Don't skip opening entirely — it costs little and sometimes no one contests. But don't pour real money in round 1; the decision point is round 2.

- Prioritize lots where my value is far above the estimate (lot 3: estimate 23, value 41 — that was the money lot and I won it at 32). These large private-value gaps are where surplus comes from. Lots where value ≈ estimate are contests I'll likely lose or win with scraps.

- Watch results for opponents' price levels: they pay roughly the estimate or a bit above (34, 28, 27). So if my value is above the estimate by a good margin, I can beat them and still profit; if my value is at or below estimate, pass early and preserve attention for better lots.

- Preserve budget across lots, but preserved budget is worthless if I never win anything. If late in the auction I still hold most of my budget and a good lot appears, bid essentially my full value on it.

- Final score sanity: each win contributes (my value − price). A single well-chosen win at a big value gap (+9 on lot 3) can carry the whole episode — better to nail the one or two lots where I have an edge than to contest all five.