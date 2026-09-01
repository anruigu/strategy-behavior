---
game: ref_orderbook
model: gemini
condition: neutral
seed: 2
round: 1
chars: 1203
---
When the game begins, I immediately lift the lowest available asks to secure my required delivery units early. 

I do not place passive bids just above the best bid in the early ticks. This approach did not work; it caused me to miss early liquidity, watch prices rise, and eventually panic-buy at the top of the book, resulting in negative or zero scores.

When I have secured my required position with several ticks remaining, I place a sell order to offer out one unit at a price higher than I paid, capturing a profit while leaving enough time to rebuy the unit if my sell order is filled.

When I am short of my required units and only one or two ticks remain, I immediately cross the spread and buy at the lowest available ask to ensure I do not incur the heavy delivery penalty.

When I change my strategy or need to free up liquidity for a necessary fill, I include [cancel: all] in my response to clear out old, unexecuted passive orders.

When I reach the final tick and hold exactly the required position for delivery, I submit [cancel: all] and [order: none]. I do not attempt to sell on the final tick if it drops me below the delivery requirement, as the penalty outweighs the cash gained.