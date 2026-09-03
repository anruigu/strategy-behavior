---
game: ta_negotiation
model: fleet-kimi3
condition: win
seed: 4
round: 1
chars: 2220
---
Playbook for SIMPLE NEGOTIATION:

- Before offering, I scan every combination of what I hold in surplus and what the Guildmaster holds in surplus, computing both my private gain and his published-value gain. I never skip this enumeration to "eyeball" a deal.

- The acceptance rule is claim ≥ 2 in his published values. Every offer I make must clear that bar, or he declines and I waste a round. A stamped gain of exactly 2 is as acceptable to him as 6, so I aim for the trade that maximizes my private gain subject to stamped ≥ 2, not the one that looks most generous.

- Convert cheap resources into dear ones deliberately: resources he values highly but I don't are currency for buying resources I value highly. The gap between my value and his published value is where all profit lives.

- I exploit quantity: since both resource types are capped at 3 units per trade, a lopsided ratio (give 3 low-value-to-me, take fewer high-value-to-me) can clear his threshold while still profiting me, especially when his unit value on what I give exceeds mine.

- Never hold when an acceptable positive-gain trade exists. I held in one round where surplus mismatches still existed, and a hold costs me one of only six chances to score. Holding is only for when every claim ≥ 2 trade nets me zero or negative privately.

- I check his stock before each offer: if he has 0 of something, I cannot take it; if I have 0, I cannot give it. Stocks shift every accepted trade, so I recompute from the updated holdings each round rather than reusing an old plan.

- Get the claim arithmetic right: his gain = (qty he takes × his published value) − (qty he gives × his published value). I state that figure on the offer.

- I prefer repeatable trades: if a trade pattern works, I check whether it still works next round with updated stocks and run it again, since the Guildmaster's acceptance criterion doesn't change.

- Sequence the best trades first rather than saving them; rounds are few, and a later trade may become impossible as stocks run out.

- When the gap structure is small (my values close to his), I accept thin margins — a +1 or +2 private gain per round across six rounds beats hunting for a jackpot that doesn't exist.