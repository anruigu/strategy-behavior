---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 1
round: 1
chars: 1994
---
# Playbook: ref_estate

When I am offered an unowned property, I evaluate it by asking: "Over the remaining laps, will the expected rent I collect from others landing on this tile exceed the expected rent I pay landing on others' tiles?" I do not just ask "can I afford it?"

When I have already spent more than 50% of my starting cash on deeds within the first third of the game, I stop buying unless the property has the highest rent-to-price ratio on the board. Over-buying early leaves me unable to survive rent payments on opponents' properties, and the score is cash + deed value, so I lose net only through rent imbalance.

When I am paying more in rent than I am collecting across a lap or two, I treat that as a signal to stop buying and preserve cash. The rent outflow is the only way I lose score; buying is score-neutral at the moment of purchase.

When choosing which property to buy if I do buy, I prefer the one with the highest rent per price point, because that maximizes the rent I collect per opponent landing. A 50-cost / 10-rent tile is far less valuable than a 120-cost / 30-rent tile for collection purposes, even though the cheaper one "feels" like a safer buy.

When I pass START, I add the salary to my balance before any payment, and I always verify my running total by summing: starting cash + all salary collected + all rent received − all rent paid − all purchases. I do this mentally each turn before declaring my balance.

When my balance drops below the cheapest rent on the board (i.e., I cannot survive one rent hit), I consider that I have effectively lost the game and should stop buying anything further, letting the remaining laps play out with whatever deeds I hold.

When an opponent has already bought a high-rent property early in the game, I note that my expected future rent payments are elevated, and I weight my buying decisions toward either (a) not buying at all, or (b) buying the highest-rent available property to offset the expected outflow.