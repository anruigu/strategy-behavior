---
game: ref_orderbook
model: gpt
condition: neutral
seed: 1
round: 3
chars: 3738
---
- When the opening ask is close to the visible market, I buy the available quantity early, usually two units, rather than risk paying more later or incurring a shortfall.
- I generally size an aggressive opening order to displayed ask liquidity; ordering beyond it creates a resting bid that must be managed and has not shown a clear advantage over reassessing next tick.
- When I deliberately order more than displayed liquidity, I assume only the displayed quantity fills immediately and explicitly track the unfilled balance as a resting bid.
- When I remain one unit short after the opening trade, I acquire it promptly unless the ask exceeds my estimated settlement value by more than the eight-point shortfall penalty avoided.
- Before crossing a later ask, I cancel any passive bid left from an earlier order so I cannot accidentally acquire excess inventory.
- When I estimate settlement value, I use the evolving bids, asks, and tape rather than treating my purchase price as fair value.
- When repeated trades occur near the ask and bids remain firm, I treat that as evidence supporting the higher price range and become less willing to delay required purchases.
- When deciding whether to cross an ask for a required unit, I compare its price with estimated settlement value plus the eight-point penalty avoided.
- I treat early displayed asks as valuable acquisition opportunities when subsequent ticks show firmer bids and higher asks; securing most of the requirement early has consistently produced positive results.
- When I already hold three units, I preserve that inventory unless a sale offers a clear round-trip profit and enough time and liquidity remain to buy back.
- When the spread is only a few points and no cheaper replacement liquidity is visible, I do not sell required inventory merely because bids are available.
- When I sell required inventory, I plan the replacement trade before selling and account for the possibility that only part of either order fills.
- When bids are strong and later asks appear materially cheaper, I may sell into the bids and rebuy, but I do not liquidate merely because I can undercut the current ask.
- When I post any resting order, I track its unfilled quantity on every later tick and cancel it before placing a conflicting order.
- When I replace an order or no longer want execution, I use `[cancel: all]` so stale orders cannot unexpectedly alter my delivery position.
- When I have not knowingly left an order resting, I may simply submit `[order: none]`; when there is any uncertainty, I cancel all before sitting still.
- When a partial sale leaves me below three units, I prioritize restoring exactly the shortfall rather than opening unnecessary extra exposure.
- When cheap asks appear late, I buy the required quantity across available price levels with a limit high enough to reach three units.
- When the final tick is put to me and I hold fewer than three units, I buy the exact shortfall whenever the ask’s premium over estimated value is less than the eight-point penalty avoided.
- When the final tick is put to me and I hold exactly three units, I cancel all resting orders and submit no new trade.
- When I hold three units and no clear arbitrage is available, I sit still; repeatedly selling and reacquiring delivery inventory at similar prices adds execution risk without improving expected value.
- I do not buy extra units merely because the market is rising; once delivery is covered, any additional position must be justified by expected settlement value rather than the shortfall penalty.
- When I write my response, I keep any reasoning brief and end with one valid bracketed order token, adding `[cancel: all]` whenever a stale order may exist.