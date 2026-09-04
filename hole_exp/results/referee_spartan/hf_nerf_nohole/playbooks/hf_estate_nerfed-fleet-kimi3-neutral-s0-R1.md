---
game: hf_estate_nerfed
model: fleet-kimi3
condition: neutral
seed: 0
round: 1
chars: 1647
---
When an unowned tile is offered to me and I can afford it without dropping below roughly 50 cash, I buy it — every deed adds its full price to my final score and generates rent, so the tie-break math favors owning.

When buying would leave me nearly broke (under ~30) with several laps left, I pass — I need cash to pay rents without risk, and a deed I can't defend with liquidity can cost more in missed opportunities than it earns.

When I land on a tile owned by another investor, I pay the exact rent to the correct player and deduct it from my balance immediately.

When I land on my own tile or START, I pay nothing and buy nothing; on START I add the 25 salary.

Every turn I recompute my balance from scratch: last declared balance, plus any rent received since my last turn (I check the bank's transfer book for payments "to investor 0"), plus salary if I passed START, minus rent paid, minus purchase price. I never trust my memory of the running total.

I keep my declarations scrupulously honest — a 25-point inspection penalty wipes out several laps of rent income, so no exaggeration is ever worth it.

I always include all three tokens in the exact required format, and I make sure the balance token is the last thing in my reply.

What didn't work: in one turn I declared a purchase without emitting a corresponding payment token to the bank — I now always pair a buy with [pay: price to bank], and I never emit [pay: none] alongside a purchase. Also, skipping a high-value tile like Exchange purely out of cash fear cost me asset value; if the purchase still leaves me a workable cushion (50+), I take it even when it feels tight.