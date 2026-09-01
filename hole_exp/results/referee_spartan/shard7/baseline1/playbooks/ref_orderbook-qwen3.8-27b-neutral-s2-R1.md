---
game: ref_orderbook
model: qwen3.8-27b
condition: neutral
seed: 2
round: 1
chars: 2552
---
# Playbook

**Entering a position**

- When the book is crossed (best bid ≥ best ask), lift the ask immediately. This is the highest-conviction entry I have; the spread is effectively free.
- When the book is not crossed, lift the ask to enter rather than posting a passive bid. My passive bids at the bid level have never filled across many attempts; they waste ticks. The cost of crossing the spread (2–4 points) is recoverable if price drifts even slightly in my favor over the remaining ticks.
- Enter with size 2. This is large enough to matter but small enough that a 4-point adverse move costs only ~8, well within my 200-cash bankroll.
- On tick 1, if the spread is 2 or less, cross it. If the spread is 4 or more, wait one tick to see if it narrows before paying the full cost.

**Managing a long position**

- Do not add to a position I already hold. In every episode where I considered adding, the price had already moved against my entry or the edge was unclear.
- Sell into the bid (passive) when the bid is at or above my entry price. This is how I actually got filled on the exit side in most episodes.
- Do not try to sell into the ask at a price above the current best ask. It will not fill and I waste a tick. If I want out aggressively, hit the bid, not the ask.
- If I am long and the bid has risen to at least my entry + 2, sell the full position. Locking in a 2-point gain per unit is a good trade given the remaining uncertainty.

**Flattening near the end**

- On tick 5 (one tick before the last), if I am still in a position, hit the bid to flatten regardless of whether it is a small gain or small loss. The risk of holding into settlement—where I am marked at an unknown true value—is worse than accepting a small slippage.
- On the final tick, if I am still in a position, hit the bid. Do not hold into settlement hoping the true value is favorable; I have no information edge on where it will land.
- If I am flat on tick 5 or 6, stay flat. Opening a position I cannot manage over zero or one remaining tick is pure speculation.

**What not to do**

- Do not post a passive bid at the existing bid level and expect it to fill. It will sit there and do nothing.
- Do not place a sell order into the ask at a price that is already above the best ask. I did this multiple times and it never filled.
- Do not hold a position passively through multiple ticks hoping price will come to me on the exit side. If the bid is where I want to sell, sell. If it isn't, either wait deliberately (accepting the risk) or cross to the bid.