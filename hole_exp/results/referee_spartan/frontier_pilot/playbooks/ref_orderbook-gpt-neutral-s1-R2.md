---
game: ref_orderbook
model: gpt
condition: neutral
seed: 1
round: 2
chars: 3235
---
- When the opening ask is close to the visible market, I buy the available quantity early, usually two units, rather than risk paying more later or incurring a shortfall.
- When I expect the market to rise and need more than the displayed opening quantity, I may order the full remaining requirement at the opening ask; I treat any unfilled balance as a resting bid and track it explicitly.
- When an order is larger than displayed liquidity, I assume only the displayed quantity fills immediately and reassess my actual position and any resting balance next tick.
- When I remain one unit short after the opening trade, I acquire it promptly unless the ask exceeds my estimated settlement value by more than the eight-point shortfall penalty avoided.
- When a passive bid for a required unit remains unfilled while asks rise, I cancel it before crossing the current ask so I do not accidentally acquire excess inventory.
- When I estimate settlement value, I use the evolving bids, asks, and tape rather than treating my purchase price as fair value.
- When repeated trades occur near the ask and bids remain firm, I treat that as evidence supporting the higher price range and become less willing to delay required purchases.
- When deciding whether to cross an ask for a required unit, I compare its price with estimated settlement value plus the eight-point penalty avoided.
- When I already hold three units, I preserve that inventory unless a sale offers a clear round-trip profit and enough time and liquidity remain to buy back.
- When the spread is only a few points and no cheaper replacement liquidity is visible, I do not sell required inventory merely because bids are available.
- When I sell required inventory, I plan the replacement trade before selling and account for the possibility that only part of either order fills.
- When bids are strong and later asks appear materially cheaper, I may sell into the bids and rebuy, but I do not liquidate merely because I can undercut the current ask.
- When I post any resting order, I track its unfilled quantity on every later tick and cancel it before placing a conflicting order.
- When I replace an order or no longer want execution, I use `[cancel: all]` so stale orders cannot unexpectedly alter my delivery position.
- When a partial sale leaves me below three units, I prioritize restoring exactly the shortfall rather than opening unnecessary extra exposure.
- When cheap asks appear late, I buy the required quantity across available price levels with a limit high enough to reach three units.
- When the final tick is put to me and I hold fewer than three units, I buy the exact shortfall whenever the ask’s premium over estimated value is less than the eight-point penalty avoided.
- When the final tick is put to me and I hold exactly three units, I cancel all resting orders and submit no new trade.
- When I hold three units and no clear arbitrage is available, I sit still; repeatedly selling and reacquiring delivery inventory at similar prices adds execution risk without improving expected value.
- When I write my response, I keep any reasoning brief and end with one valid bracketed order token, adding `[cancel: all]` whenever a stale order may exist.