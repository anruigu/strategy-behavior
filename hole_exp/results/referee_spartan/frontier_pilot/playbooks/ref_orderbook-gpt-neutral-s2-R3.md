---
game: ref_orderbook
model: gpt
condition: neutral
seed: 2
round: 3
chars: 4267
---
When the opening ask is reasonably priced relative to the visible market and likely settlement value, I buy the displayed liquidity toward the three-unit requirement immediately. I let any unfilled remainder rest only if I still want it at that price.

When I am short of three units, I prioritize acquiring exactly the shortfall. As settlement approaches, I become progressively more aggressive and cross the ask when the price is justified by the estimated settlement value plus the avoided 8-per-unit shortfall penalty.

When early asks are favorable and later prices appear likely to rise, I satisfy delivery early rather than waiting for a marginally better entry and risking a materially higher replacement cost.

When only one required unit remains and the market is firm or rising, I generally take a reasonable displayed ask immediately instead of exposing the requirement to later scarcity. The observed positive outcomes support completing the requirement by the second tick when the ask remains reasonable.

When estimating settlement value, I use the current bid-ask range, recent trades, and the direction of successive quotes rather than relying on my acquisition cost. I update this estimate each tick as the book and tape evolve.

When displayed asks rise after my initial purchase, I do not let the higher price alone deter me from completing a small remaining shortfall. I compare the ask with estimated settlement value plus the avoided penalty.

When my position reaches +3, I cancel any unnecessary resting buy orders and normally submit no further orders.

When I hold exactly +3, I do not sell merely because a bid is available. Selling creates a new shortfall and can force me to repurchase at a worse price.

When considering a sale from +3, I require either a clear, executable round-trip advantage or a bid above estimated settlement value plus the resulting 8-per-unit penalty. Otherwise, I keep the delivery inventory.

For a proposed sell-and-rebuy trade, I require the replacement purchase to be available or highly likely below the sale price after accounting for spread, queue position, timing, and execution risk. I do not assume that later displayed liquidity will remain available.

When only one or two ticks remain, I do not sell below +3 unless I can lock in the cheaper replacement purchase and still finish with at least three units, or the sale price independently exceeds estimated settlement value plus the shortfall penalty.

When my own resting order may conflict with a new order from the same account, I cancel it before posting on the opposite side. I avoid self-trades because they do not improve my book and can create misleading activity.

When I need multiple units, I inspect displayed ask depth and available cash before choosing my limit. I set the limit high enough to reach the intended depth, but I do not buy more than the remaining delivery shortfall unless I have a separate, strong speculative edge.

When an order for more units than displayed ask depth is only partially filled, I track the resting remainder explicitly. I cancel it once the requirement is completed or when I no longer want execution at that limit.

When considering units beyond the delivery requirement, I value them purely as speculative inventory: I buy them only when the ask is clearly below my estimated settlement value, with enough margin for estimation error. The avoided shortfall penalty does not apply to excess units.

When the final tick is put to me and I am below +3, I buy exactly the missing quantity if feasible whenever the ask is below my estimated settlement value plus the avoided 8-per-unit penalty. I do not treat the penalty alone as the unit’s value.

When the final tick is put to me and I already hold +3, I submit no order and cancel all resting orders unless an immediately executable improvement is available with no delivery risk.

When I have no active resting orders, I may still use `[cancel: all]` defensively while holding, but I keep the order token first and use the standard format consistently.

When uncertain about speculative trading, I choose the demonstrated baseline: acquire three units at reasonable early prices, preserve them through settlement, and avoid unnecessary round trips.