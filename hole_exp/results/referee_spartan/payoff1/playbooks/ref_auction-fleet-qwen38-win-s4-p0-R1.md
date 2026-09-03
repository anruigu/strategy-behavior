---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2710
---
# Playbook: ref_auction

**On budget tracking:** After every bid I make, my remaining budget is my starting budget minus my current committed bid (the highest I've bid on the lot I'm currently the high bidder on). If I'm not the high bidder, my committed amount on that lot is zero. I recompute from scratch each time rather than subtracting incrementally, and I double-check the arithmetic before writing the token.

**On round 1 opening bids:** When the lot is worth significantly more to me than the estimate (e.g., my value > 1.2× estimate), I open at roughly 50–60% of my value. This signals strength without overcommitting. When my value is close to or below the estimate, I open at the minimum raise or pass.

**On the final round — the critical rule:** I never bid only the minimum raise in the final round unless I have no realistic chance of winning. The other bidders are making their final bids at the same time, so a minimum raise is a coin flip at best. Instead, I bid at or near my full value (within what my budget allows). If my value is 39 and the current high is 20, I bid 35–39, not 23. The cost of overbidding is small (I'd only lose a few points of surplus); the cost of underbidding is losing the entire surplus.

**On passing in the final round:** I pass only when the current high bid is at or above my value, or when I am already the high bidder and the surplus I'd get by holding is acceptable relative to the risk of raising. If I'm the sitting high bidder at a price well below my value, I pass and lock in the surplus.

**On reading competitor aggression:** If a competitor has won multiple lots at prices near or above their likely valuations, they are aggressive. Against such a competitor, I raise my final-round bids toward my full value rather than expecting them to back down. If they've only won at moderate prices, the minimum-raise strategy is somewhat less dangerous but still risky.

**On lots where my value barely exceeds the current bid (margin < 10% of value):** I pass. The expected surplus is too thin to justify the risk of a bidding war that could push the price above my value.

**On budget allocation across lots:** I treat my budget as a shared pool across all lots. Before bidding on a later lot, I subtract what I've already committed (or expect to pay) on earlier lots I'm likely to win. I never let a single lot consume more than I can afford while still having budget for a high-value lot later in the sequence.

**What did not work:** Bidding the minimum raise in the final round against an active competitor. This lost me profitable lots that I was well-positioned to win. The fix is simple: in the final round, bid what I'm willing to pay, full stop.