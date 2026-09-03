---
game: ta_blindauction
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 2878
---
**Playbook for blind auctions against a single opponent**

- When a collusive note arrives, agree — it costs nothing. But assume the opponent will defect: this game Vega promised to stay off my lots and then bid into every one of them. The deal's only value is if they actually honor it; verify with their first bid on a "granted" lot before trusting it at all.
- If the opponent bids into a granted lot, the deal is dead — switch immediately to competitive bidding for the rest of the game, not just that lot.
- On lots the deal grants me, bid the minimum (1) in case they honor it. If they bid over it, they've defected and I treat all future lots as open competition.

- Default competitive bid: one above the opponent's most recent winning-level bid, capped at (value − 1). Chasing their last number up is only correct when it's their genuine level, not one erratic spike.

- Never bid above value minus one; winning at value is a waste and above value is a loss.

- **Ties waste the lot. This episode I tied twice (lot 3 and lot 5) by bidding at or near my own previous bid or an obvious round number. When I actually want a lot, avoid round numbers and my own repeated bids — bid decisively one step above their pattern, and prefer odd/off-by-one increments (e.g. 5 instead of 4, 3 instead of 2).**

- **Finishing at exactly +0 because I never won anything is the real failure mode, not overpaying. Token bids of 1 on every lot won nothing and lost nothing — but a game where I never take a lot scores zero. On lots with value ≥ 5, I must bid to win: their-average-plus-one, capped at value − 1. Against an opponent whose winning bids ranged 2–5, a bid of 4–5 on a value-6 lot was correct in size, wrong in that it tied.**

- **On genuinely low-value lots (value ≤ 3) against an opponent who has paid 2–5, a token 1 is fine — winning below that range is rare. But don't extend that passivity to mid-value lots; that passivity cost me the whole game.**

- Opponents can be erratic lot to lot (5, 2, 1, 5, 4 in sequence). Don't over-anchor on their single most recent bid, and don't overreact to one low bid by assuming they've quit. A bid near their average + 1, capped at value − 1, is safer than chasing their last number.

- Track the opponent's bid history every lot and anchor to their revealed willingness to pay, not to my own prior bids. Their pattern is the best single predictor of what wins.

- Endgame net discipline: if I have a positive net banked, bid only where (value − bid) is clearly positive. But if my net is zero and nothing is at risk, late lots are my last chances — bid to actually win profitable lots rather than token-bidding to a guaranteed zero.

- **Scoring zero with zero risk is still zero. Take the profitable risks the format allows: sealed bids mean overbidding is the only downside, so cap at value − 1 and let the cap absorb the risk.**