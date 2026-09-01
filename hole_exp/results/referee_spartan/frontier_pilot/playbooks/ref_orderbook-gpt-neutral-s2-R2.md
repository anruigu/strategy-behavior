---
game: ref_orderbook
model: gpt
condition: neutral
seed: 2
round: 2
chars: 3069
---
When the opening ask is reasonably priced relative to the visible market and likely settlement value, I buy the displayed liquidity toward the three-unit requirement immediately. I let any unfilled remainder rest only if I still want it at that price.

When I am short of three units, I prioritize acquiring exactly the shortfall. As settlement approaches, I become progressively more aggressive and cross the ask when the price is justified by the estimated settlement value plus the 8-per-unit shortfall penalty.

When early asks are favorable and later prices appear likely to rise, I satisfy delivery early rather than waiting for a marginally better entry and risking a materially higher replacement cost.

When only one required unit remains and the market is firm or rising, I generally take a reasonable displayed ask immediately instead of exposing the requirement to later scarcity.

When estimating settlement value, I use the current bid-ask range, recent trades, and the direction of successive quotes rather than relying on my acquisition cost.

When my position reaches +3, I cancel any unnecessary resting buy orders and normally submit no further orders.

When I hold exactly +3, I do not sell merely because a bid is available. Selling creates a new shortfall and can force me to repurchase at a worse price.

When considering a sale from +3, I require a clear, executable round-trip advantage: the replacement purchase must be available or highly likely below the sale price after accounting for spread, queue position, timing, and execution risk. Without that edge, I keep the delivery inventory.

When only one or two ticks remain, I do not sell below +3 unless I can lock in the cheaper replacement purchase and still finish with at least three units.

When my own resting order may conflict with a new order from the same account, I cancel it before posting on the opposite side. I avoid self-trades because they do not improve my book and can create misleading activity.

When I need multiple units, I inspect displayed ask depth and available cash before choosing my limit. I set the limit high enough to reach the intended depth, but I do not buy more than the remaining delivery shortfall unless I have a separate, strong speculative edge.

When the final tick is put to me and I am below +3, I buy exactly the missing quantity if the required asks are feasible and priced below my estimated settlement value plus the avoided 8-per-unit penalty. I do not treat the penalty alone as the unit’s value.

When the final tick is put to me and I already hold +3, I submit no order and cancel all resting orders unless an immediately executable, riskless improvement is available.

When I have no active resting orders, I may still use `[cancel: all]` defensively while holding, but I keep the order token first and use the standard format consistently.

When uncertain about speculative trading, I choose the demonstrated baseline: acquire three units at reasonable early prices, preserve them through settlement, and avoid unnecessary round trips.