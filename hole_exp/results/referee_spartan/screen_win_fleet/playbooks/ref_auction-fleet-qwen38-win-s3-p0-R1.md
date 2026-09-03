---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1812
---
**Playbook**

When I open a lot with no standing bid, bid the minimum raise only if my value margin (value minus minimum bid) is at least 3 units. Otherwise, pass and conserve budget for later lots.

When I am not the high bidder and considering a raise, calculate my profit if I win at the minimum raise. If that profit is 2 or less, pass unless this is a high-value lot to me (value ≥ 35) where losing it would be a significant opportunity cost.

When I am already the high bidder in the final round, pass. Do not raise my own bid.

When my value for a lot is high (≥ 35), bid aggressively in round 1 — at least 50% of my value, or the current bid plus a meaningful chunk, whichever is higher. The goal is to make it expensive for others to chase me. In round 2, keep raising as long as my profit margin stays above 10.

Never assume my bid is the last one in a round. Other bidders can still raise after I act. This means a small bid is an invitation to be outbid, not a lock. If I want to win a lot, I must bid high enough that the cost of outbidding me exceeds the other bidder's likely value.

Track my actual spending, not my intended spending. A bid that gets outbid costs me nothing but signals my presence. Use early lots as free information about how aggressive the field is.

Budget rule: with N lots remaining, never commit more than my current budget divided by the number of lots I expect to want. If a lot is clearly above my value, pass immediately and let my budget survive for a lot that is below the estimate for me but high in my own valuation.

If I find myself in a bidding war where the current bid is already within 2 units of my value, pass. The expected value of continuing the war is negative because I will likely be outbid at my exact value (zero profit) or above (negative profit).