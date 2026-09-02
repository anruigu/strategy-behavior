---
game: ref_orderbook
model: gemini
condition: neutral
seed: 1
round: 1
chars: 961
---
When the game begins, I immediately lift the lowest asks to acquire my required delivery units. 

I do not place passive bids just above the current best bid to try and save money. This does not work; it leaves me unfilled and forces me to chase rising prices in later ticks, ultimately costing me more.

When I still have units to acquire, I continue hitting the best available asks each tick until my delivery requirement is fully met.

When my delivery requirement is met (0 units still to acquire), I stop trading and submit `[order: none]` for the remaining ticks to protect my position.

When I reach the final ticks of the game, I never sell my required units to "liquidate" or "maximize cash balance." This does not work; the position is automatically marked to its true value at settlement, and selling it leaves me short, triggering a severe delivery penalty. If my position matches my delivery requirement on the final tick, I submit `[order: none]`.