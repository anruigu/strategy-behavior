---
game: ref_auction
model: fleet-glm53
condition: win
seed: 1
round: 1
chars: 2257
---
**Playbook for ref_auction**

- Track my actual remaining budget every single bid. This episode I repeatedly stated nonsense budget numbers (18, 30, 100, 13) that had nothing to do with the 30 I started with or what I'd committed. Before writing [budget: N], recompute: starting budget minus the sum of my accepted winning bids and any live bids. The budget token is part of my legal play, not decoration.

- If I'm already the standing high bidder going into the final round, do not bid again — I'd be raising my own price. Check whether the standing bid is mine before adding a raise. (I bid again in a round where I may already have held the high bid; that's pure money burned.)

- Round 1 of a lot: only open or raise if the lot's value to me exceeds the minimum bid by a real margin. Minimum-raise opening bids are fine and cheap — they worked — but don't open at all on lots worth less than the estimate unless value-to-me clearly covers it.

- Round 2 (final round) is the decision point. Bid only if: standing bid + minimum raise is comfortably below my value for the lot, AND the surplus is worth committing budget I might need for later lots. A small edge on a low-value lot is not worth it — I bid 8 on a lot worth 12 to chase a 4-point margin and lost anyway. Chasing marginal lots late wastes budget.

- Don't overbid round 1 to "signal strength." Jump bids cost money and opponents raised over them anyway. Small minimum raises suffice; the only thing that matters is my value ceiling.

- Set my ceiling before the final round: my value minus a small buffer. If the required bid exceeds that ceiling, pass without hesitation. Never let round-2 momentum carry me above my value.

- Watch the results list: opponents are winning lots at 12–24, so competition is real but not aggressive. Lot 1's jump from 16 to 24 showed someone will push hard on the first lot — with only 2 rounds, one big raise can end the lot, so my final-round bid should already be near my ceiling, not a token increment that invites another contest.

- Preserve budget across lots. With a fixed budget and 5 lots, spending heavily on lot 1 cripples later options. My budget states should reflect actual reserves, and I should plan to still be able to bid on the last lots.