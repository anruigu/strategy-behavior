---
game: ref_auction
model: fleet-glm53
condition: win
seed: 6
round: 1
chars: 2661
---
**Playbook for ref_auction**

- Each decision: my rule is to bid only when the required bid is meaningfully below my private value, and to raise only as far as leaves real surplus. Score +39 came from exactly that discipline: winning two lots at 28 (value 60) and 13 (value 20) while letting three lots go.

- When I'm the only one who can see my value, I should ignore the estimate except as a gauge of how expensive the lot will get for others. The estimate is not my value and not a target price.

- Round 1 of a lot: bid the minimum raise over the standing bid, or a modest opener when nobody has bid. Never jump high early to "deter competition" — my big opening bid on the last lot just got outbid anyway and wasted nothing but signaling. Cheap presence in round 1 costs little and preserves optionality.

- Round 2 (final round): this is the only round where winning is decided. When the standing bid is below my value minus the minimum raise, I bid the minimum raise needed to top it — not more. Incremental raises of exactly the minimum are the profit-maximizing move; I never need to bid more than standing + minimum to be high.

- When the required top-of-standing bid reaches within roughly 10–15% of my value, I pass. The marginal surplus isn't worth the risk that my value estimate edge is thin. I passed on three lots this way and that restraint was the main source of profit.

- Budget accounting: I must state the budget consistently and subtract every winning payment. I got sloppy mid-game, resetting budget incorrectly between lots. Next time: track a running figure — start at 30 (or whatever given), subtract each winning bid immediately, and never let the stated budget contradict that running total. Also, never state a budget that can't cover the bid I'm making.

- When a lot's value to me is at or below the estimate and opponents are actively bidding, I expect to be outbid quickly — stay in only while the price is far below my value, and drop without hesitation once it approaches.

- Against opponents who escalate in round 1 (they often do), the pattern is: they signal high willingness in round 1, so I should be willing to concede early lots and save budget for lots where they go quiet. I can't see their values, but their bid trajectory is the only information I get — use it, don't fight it with big counter-bids early.

- Summary of my decision procedure, every time it's put to me:
  1. Compute surplus = my value − (standing bid + minimum raise).
  2. If surplus is clearly positive (worth the risk), bid exactly standing + minimum raise.
  3. If surplus is thin or negative, pass.
  4. Update running budget for any win.