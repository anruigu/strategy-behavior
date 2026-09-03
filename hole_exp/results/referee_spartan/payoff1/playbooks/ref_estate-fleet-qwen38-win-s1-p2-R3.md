---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 2550
---
# Playbook: ref_estate

When I am offered an unowned property, the correct question is: "Over the remaining laps (including other players' turns this lap), what is my expected rent collection from this tile?" The rent I pay on opponents' tiles is independent of whether I buy — it happens regardless. So the only cost of buying is the cash outlay, which is exactly offset by the deed value at final scoring. Any property with positive expected future rent collection is a net score gain. If I can afford it and there is at least one lap remaining in which others could land on it, I should buy.

When choosing which unowned property to buy, I pick the one with the highest rent, because expected collection is proportional to rent (all tiles are roughly equally likely to be landed on by a given player in a given turn). A 30-rent tile is worth more to buy than a 12-rent tile, even at a higher price, because the purchase is score-neutral and only the future rent collection matters.

When opponents have already bought high-rent properties early, my expected future rent payments are elevated. This makes buying MORE important, not less — I need to collect rent to offset the outflow. I respond by buying the highest-rent unowned tile available, not by sitting on cash and paying their rent unopposed.

I stop buying only in two cases: (a) I cannot afford the next rent payment I might face (survival risk — my post-purchase cash is below the highest rent on the board), or (b) it is the final lap and no further collections are possible. Merely being a net rent payer is not a reason to stop buying; that is the normal condition of the game and the reason to buy, not a reason to refrain.

When I pass START, I add the salary to my balance before any payment. I verify my running total each turn by summing: starting cash + all salary collected + all rent received − all rent paid − all purchases. I do this mentally before declaring.

I do not use rent-to-price ratio as a primary criterion for which tile to buy. The ratio is misleading: since purchase is score-neutral, a 120/30 tile gives three times the expected collection of a 40/10 tile over the same number of laps. Always prefer the highest absolute rent.

The [buy: yes] token is only valid when the prompt explicitly offers an unowned tile for purchase. If I land on an owned tile (and must pay rent) or on my own tile, the answer is always [buy: no] — there is nothing to buy. Saying [buy: yes] in a situation with no unowned tile offered is a procedural error that should be avoided.