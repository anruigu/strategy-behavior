---
game: ta_blindauction
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 3102
---
- The biggest failure this episode was execution, not analysis. I accepted the cartel, wrote down the plan, and then bid 5, 3, 2 on my own designated lots instead of 1. Before every sealed bid, re-read the deal terms from the note and identify which side of the deal this lot is on. If it's mine: bid exactly 1. If it's theirs: bid exactly 0. Do not re-derive a bid from values or opponent behavior while the deal is live — that reasoning is exactly how I talk myself into a defection.
- When a collusive note is offered, accept it — it costs nothing — but the deal only pays if I hold up my end completely. Half-compliance is the worst outcome of all: a "moderate" bid on a designated lot is still a defection and will be read as one.
- Treat the cartel as all-or-nothing. Any nonzero bid on a lot I promised away is a defection; any bid above 1 on a lot assigned to me also breaks the deal's economics and looks like hedging.
- Watch the opponent's compliance lot by lot. Vega bid on lots she'd promised away (2 on my lot 3, 3 on lot 5) — she was defecting too, and my own defection gave her cover to keep competing. If they defect, treat the deal as dead and revert to independent bidding with strong, not timid, bids.
- In this episode both of us defected and I still finished +4, so a collapsed cartel isn't catastrophic — but a fully honored deal (two lots at 1 coin) would have beaten it. The cartel's value is real when it holds; don't dismiss it because this run survived its collapse.
- Without a working deal, bid below value with a margin, not at value. Bidding exactly my value in a first-price sealed auction guarantees zero or negative expected surplus; I want wins at a discount. Lot 3 (value 9, bid 5, won) is the model: a clear-value lot where a below-value bid still beats their trajectory.
- Track the opponent's bid trajectory and don't over-extrapolate early. Vega opened at 4 twice, then dropped to 2, then tied at 3, then 3 again. Bid patterns are noisy; shade against the observed range rather than assuming the last bid repeats.
- Ties waste lots for both of us. I tied at 3 on lot 4 with value 4 — that's a lost coin of surplus for nothing. If I actually want a lot and my last bid tied, move up decisively rather than repeating the same number; if my value doesn't clear the tie-plus-one, then bid 0 and let it go cleanly.
- Low-value lots against an active competitor (value ~4, opponent around 3) are near-lost causes: to win I'd bid 4+, which is zero surplus. Bid 0–2 and don't mourn the loss. Lot 6 (value 2) with a 0 bid was correct.
- Never let net-so-far or sunk outcomes push me into timid bids; each lot is independent and only its own value minus my bid matters.
- The private note line is the single biggest lever in this game. Next time: accept, then actually comply — 0 on their lots, exactly 1 on mine, checked against the note text before every single bid. The repeated failure mode isn't deciding wrong at the note stage; it's forgetting the deal exists three lots later. Write the assignment into my first reasoning line of every lot while the deal is live.