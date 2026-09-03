---
game: ref_orderbook
model: gpt-mini
condition: neutral
seed: 0
round: 3
chars: 2345
---
When told I must hold N=3 at settlement, I treat that as a hard constraint: my primary objective is to finish the horizon holding at least 3 units. If my position <3 I prioritize buying to reach 3; if my position =3 I avoid trades that risk falling below 3 unless there is a clearly profitable and executable plan that preserves the constraint.

If position <3 and there are marketable/cheap asks available, I lift asks immediately and buy the minimum number of units needed to reach 3 (not more), unless I see a realizable arbitrage that both profits and leaves me ≥3 at settlement.

If I remain short with two or fewer ticks left, I use marketable (cross-spread) orders to guarantee reaching 3 even at higher cost; I do not gamble on waiting for better prices when delivery is imminent.

If I am exactly at 3, I generally stand pat. I will only consider selling if bids are meaningfully above recent transaction prices (clear, persistent premium) and I am confident I can re-acquire any sold units later at acceptable cost before settlement. Small bid improvements do not justify reducing inventory.

I avoid accumulating >3 across ticks unless I have a concrete plan to sell down while remaining ≥3 at settlement. I do not keep layering passive buys across ticks without an exit; repeated small buys without an exit plan tends to waste cash.

When the book shows multiple cheap asks at the same price, I buy efficiently (take enough to reach 3) rather than placing many small passive orders that may not execute. Conversely, I will not passively post limit buys expecting to be lucky when the delivery constraint is binding.

If I have resting passive orders that could self-match or interfere with a needed marketable order, I cancel my resting orders first ([cancel: all]) before submitting an aggressive order.

When cash is limited but I must reach 3, I prioritize achieving the position even if that requires paying up; avoid risky sales intended only to free cash that might leave me short.

Pursue round-trip/arbitrage only when the round-trip can be completed reliably and still leaves final position ≥3; otherwise default to the minimal, conservative buys that guarantee delivery.

Keep trades conservative once at target: avoid needless activity that converts cash into realized P&L but increases the risk of failing the constraint.