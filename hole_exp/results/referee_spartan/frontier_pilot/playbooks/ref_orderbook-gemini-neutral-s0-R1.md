---
game: ref_orderbook
model: gemini
condition: neutral
seed: 0
round: 1
chars: 1017
---
I must hold exactly the required number of units (e.g., 3) at the end of the game. If I sell them before settlement, I will incur a heavy shortfall penalty. 

- I will never sell the units I need to meet the delivery requirement. I will hold them through the final tick until settlement.
- In the early ticks, I will place bids slightly above the best bid to try to accumulate my required position without crossing the spread and paying the full ask.
- If I have not acquired my full delivery requirement by the late ticks (tick 4 or 5), I will aggressively cross the spread and buy at the ask to guarantee I get the units, since the shortfall penalty is much larger than the cost of crossing the spread.
- Once I have acquired the required units, I will cancel all resting buy orders to avoid over-accumulating inventory, and I will place `[order: none]` for the remaining ticks.
- I will not liquidate my inventory on the last tick to try and maximize cash; doing so leaves me short for delivery and ruins my score.