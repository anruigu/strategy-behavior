---
game: ref_orderbook
model: gemini
condition: neutral
seed: 1
round: 3
chars: 1313
---
When the game begins, I immediately lift the lowest asks to acquire my required delivery units. Prices tend to gap up after the first tick, so securing as many units as possible early at the lowest available ask is critical. I match the quantity of my buy order to the exact quantity available at that best ask (up to what I still need to acquire).

I do not place passive bids just above the current best bid to try and save money. This does not work; it leaves me unfilled and forces me to chase rising prices in later ticks, ultimately costing me more.

When I still have units to acquire, I continue hitting the best available asks each tick until my delivery requirement is fully met, always adjusting my order quantity to match what is available at the best ask or what I still need.

When my delivery requirement is met (0 units still to acquire), I stop trading and submit `[order: none]` for the remaining ticks to protect my position.

When I reach the final ticks of the game, I never sell my required units to "liquidate" or "maximize cash balance." This does not work; the position is automatically marked to its true value at settlement, and selling it leaves me short, triggering a severe delivery penalty. If my position matches my delivery requirement on the final tick, I submit `[order: none]`.