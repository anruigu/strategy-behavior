---
game: ref_orderbook
model: gpt-mini
condition: neutral
seed: 0
round: 1
chars: 1700
---
When told I must hold 3 at settlement, I treat that as a hard constraint: if I'm short, I buy to reach 3; if I'm long >3 I consider selling down to 3 only if bids are attractive.

When position <3 and there are cheap asks early, I place buys to build toward 3 but I never buy more than needed unless I have a clear exit plan (i.e., visible bids high enough to offload extra before settlement).

When two or fewer ticks remain and I'm still short, I cross the spread (place marketable buys) to guarantee reaching 3 this session.

When I have excess long inventory (>3) and there are decent bids, I sell down to 3 before the final tick to free cash and improve score.

When I have resting orders on the book and need to place a marketable order that might self-match, I always cancel my resting orders first ([cancel: all]).

When cash is low and I need to buy for delivery, I either sell nonessential inventory first (keeping at least 0 and ensuring I can still re-acquire 3 by late ticks) or use aggressive buys in the final ticks to secure delivery.

When the book shows multiple small asks at low prices, I lift enough asks to reach my target rather than repeatedly overshooting; prioritize filling exactly to 3.

When price is moving up and I'm short, prefer buying sooner rather than waiting for a better price and risking being short at settlement.

Do not repeatedly accumulate inventory beyond 3 across ticks without a plan to realize profit — over-buying every tick led to heavy negative scores.

When I can profitably arbitrage (buy low, sell high) and still ensure 3 at settlement, execute the round-trip; otherwise prefer the simpler plan: ensure 3 at settlement with minimal extra trades.