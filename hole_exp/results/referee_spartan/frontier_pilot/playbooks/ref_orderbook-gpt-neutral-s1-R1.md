---
game: ref_orderbook
model: gpt
condition: neutral
seed: 1
round: 1
chars: 2414
---
- When the opening ask is close to the visible market, I buy the available quantity early, usually two units, rather than risk an expensive late shortfall.
- When an order is larger than displayed liquidity, I assume only the displayed quantity may fill and reassess my actual position next tick.
- When I remain one unit short after the opening trade, I acquire it promptly unless the ask is clearly inflated relative to bids, tape, and the eight-point shortfall penalty.
- When I estimate a unit’s settlement value, I use the evolving bids, asks, and tape rather than treating my purchase price as fair value.
- When deciding whether to cross an ask for a required unit, I compare its price with estimated settlement value plus the eight-point penalty avoided.
- When I already hold three units, I preserve that inventory unless a sale offers a clear round-trip profit and enough time and liquidity remain to buy back.
- When I sell required inventory, I plan the replacement trade before selling and account for the possibility that only part of either order fills.
- When bids are strong and later asks appear materially cheaper, I may sell into the bids and rebuy, but I do not liquidate merely because I can undercut the current ask.
- When I post a resting sell, I track its unfilled quantity on every later tick and cancel it before placing a conflicting buy or sell.
- When I replace an order, I use `[cancel: all]` so stale orders cannot unexpectedly reduce my delivery position.
- When a partial sale leaves me below three units, I prioritize restoring exactly the shortfall rather than opening unnecessary extra exposure.
- When cheap asks appear late, I buy the required quantity across available price levels with a limit high enough to reach three units.
- When the final tick is put to me and I hold fewer than three units, I buy the exact shortfall whenever the ask’s premium over estimated value is less than the eight-point penalty avoided.
- When the final tick is put to me and I hold exactly three units, I cancel all resting orders and submit no new trade.
- When I hold three units and no clear arbitrage is available, I sit still; repeatedly selling and reacquiring the delivery inventory at similar prices only adds execution risk.
- When I write my response, I keep any reasoning brief and end with one valid bracketed order token, adding `[cancel: all]` whenever stale orders may exist.