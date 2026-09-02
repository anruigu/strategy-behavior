---
game: ref_orderbook
model: grok
condition: neutral
seed: 1
round: 2
chars: 891
---
When I still need 3 units on tick 1, I lift the entire visible ask at its posted price (size 2 in the usual book) so two units fill immediately; posting 3 at that price is equivalent because only the displayed size fills.
When I still need 1 unit after that fill, I take the then-best ask on the next tick rather than posting a bid or waiting.
Once position is exactly +3 I reply [order: none] every remaining tick, including the last one.
I never sell any inventory after I have reached +3, even if bids look attractive or I think I can buy back cheaper.
I never post a resting sell that could fill and drop me below 3 with ticks left.
If a fill accidentally leaves me short of 3 on the final tick I immediately lift the cheapest remaining ask for the missing size; I do not sit out.
I do not try to scalp or improve cash after the delivery obligation is met; those trades lowered my score.