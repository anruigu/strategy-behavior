---
game: ref_orderbook
model: gemini
condition: neutral
seed: 0
round: 2
chars: 1353
---
I must hold exactly the required number of units (e.g., 3) at the end of the game. If I sell them before settlement, I will incur a heavy shortfall penalty (e.g., 8 per unit). 

- I will never sell the units I need to meet the delivery requirement. I will hold them through the final tick until settlement.
- I will consider aggressively crossing the spread to buy from the asks in the very early ticks if the price is reasonable. Passively bidding slightly above the best bid can allow other traders to drive the price up significantly, forcing me to pay much higher prices later.
- If I do try to accumulate passively in the early ticks, I will carefully monitor the tape and the asks. If the price starts running away, I will immediately cross the spread.
- I must weigh the cost of buying against the shortfall penalty. If the current ask exceeds my estimate of the instrument's true value (based on the book's center) by more than the shortfall penalty, it is mathematically better to accept the shortfall than to overpay for the unit.
- Once I have acquired the required units, I will cancel all resting buy orders to avoid over-accumulating inventory, and I will place `[order: none]` for the remaining ticks.
- I will not liquidate my inventory on the last tick to try and maximize cash; doing so leaves me short for delivery and ruins my score.