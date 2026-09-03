---
game: ref_auction
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 3729
---
**Playbook for ref_auction**

- Each decision: my rule is to bid only when the required bid is meaningfully below my private value, and to raise only as far as leaves real surplus. Score +52 came from exactly that discipline: winning three lots cheaply (lot 3 at 24 vs value 52, lot 4 at 15 vs value 39, lot 5 at 9 vs value 19) while conceding two lots early to a rival who overpaid relative to my values.

- When I'm the only one who can see my value, I should ignore the estimate except as a gauge of how expensive the lot will get for others. The estimate is not my value and not a target price.

- Round 1 of a lot: bid the minimum raise over the standing bid, or a modest opener when nobody has bid. Never jump high early to "deter competition". Cheap presence in round 1 costs little and preserves optionality. This worked cleanly: opening at the minimum kept me in every lot I later won at a low price.

- Round 2 (final round): this is the only round where winning is decided. When the standing bid is below my value minus the minimum raise, I bid the minimum raise needed to top it — not more. Incremental raises of exactly the minimum are the profit-maximizing move; I never need to bid more than standing + minimum to be high.

- When the required top-of-standing bid reaches within roughly 10–15% of my value, I pass. The marginal surplus isn't worth the risk that my value edge is thin. Conceding lot 1 (bid at 10, others pushed past) and lot 2 cost nothing I regretted.

- Don't be discouraged by losing streaks early. Rival bidders who win lot after lot at low prices are burning their own budget; my restraint on lots 1–2 kept me liquid for lots 3–5, which is where all my profit came from. Patience across the sequence is part of the strategy, not just per-lot discipline.

- Budget accounting is my known weakness and it happened again: I stated budgets of 30, 76, 15, 30, 61 across the episode with no consistent running figure. It didn't cost me points this time, but it can — a wrong budget could make me pass on affordable lots or bid money I don't have. Next time, before replying, recompute from scratch: start at 30 (or whatever given), subtract each of my winning payments in order (this episode: 24 + 15 + 9 = 48 would have overdrawn 30, so budget clearly isn't strictly enforced — but I can't count on that). Rule: state a budget that at minimum is consistent with my own running tally of wins, and never let it contradict the results list shown to me. Use the "Results so far" block every time as the source of truth for what I've won and paid.

- When a lot's value to me is at or below the estimate and opponents are actively bidding, I expect to be outbid quickly — stay in only while the price is far below my value, and drop without hesitation once it approaches. Lot 5 was exactly this case: value 19, estimate 31, but the rival only pushed to 6, so my patient minimum raises won it at 9. Thin-value lots can still be won cheaply; don't pre-emptively abandon them, just hold the surplus line.

- Against opponents who escalate in round 1, the pattern is: they signal high willingness, so I concede early lots and save budget for lots where they go quiet. Their bid trajectory is the only information I get — use it, don't fight it with big counter-bids early.

- Summary of my decision procedure, every time it's put to me:
  1. Compute surplus = my value − (standing bid + minimum raise).
  2. If surplus is clearly positive (worth the risk), bid exactly standing + minimum raise.
  3. If surplus is thin or negative, pass.
  4. Recompute running budget from the results list before stating it: starting budget minus all my winning payments so far. Never guess or reuse the last stated figure.