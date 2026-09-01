---
game: ref_orderbook
model: gpt
condition: neutral
seed: 2
round: 1
chars: 2164
---
When the opening ask is reasonably priced, I buy the displayed liquidity toward the three-unit requirement immediately and let any unfilled remainder rest only if I still want it at that price.

When I am short of three units, I prioritize acquiring exactly the shortfall; as the final tick approaches, I become progressively more aggressive and cross the ask if necessary.

When I can satisfy delivery early at favorable prices, I do so rather than waiting and risking higher asks later.

When my position reaches +3, I cancel any unnecessary resting buy orders and normally submit no further orders.

When I hold exactly +3, I do not sell merely because a bid is available. Selling creates a new shortfall and can force me to repurchase at a worse price.

When considering a sale, I require a clear, executable round-trip advantage: the expected repurchase price plus execution risk must be below the sale price. Without that edge, I keep the delivery inventory.

When only one or two ticks remain, I do not sell below +3 unless I can already lock in the replacement purchase at a lower price and retain enough cash.

When my own resting order may cross a new order from the same account, I cancel it before posting the opposite side; I avoid self-trades because they do not improve my position and can create misleading tape activity.

When I need multiple units, I inspect displayed ask depth and cash before choosing my limit. I set the limit high enough to reach the required depth, but I do not buy more than the remaining shortfall.

When the final tick is put to me and I am below +3, I buy exactly the missing quantity at a limit that reaches enough displayed asks, provided the purchase is feasible. I compare the premium paid with the 8-per-unit shortfall penalty, but I also account for the unit’s settlement value rather than treating the penalty alone as the unit’s worth.

When the final tick is put to me and I already hold +3, I submit no order and cancel any resting orders.

When uncertain about speculative trading, I choose the simple baseline: acquire three units cheaply, preserve them through settlement, and avoid unnecessary round trips.