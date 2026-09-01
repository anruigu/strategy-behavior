---
game: ref_orderbook
model: qwen3.8-27b
condition: neutral
seed: 2
round: 3
chars: 3798
---
# Playbook

**Entering a position**

- The spread is a tax I pay every time I cross it. In eight consecutive episodes (four prior, four just played), the bid at my exit was always at or below the ask at my entry. The spread cost (2–5 points) was never recovered. I will not cross a spread of 2 or more unless I have a strong directional signal.
- Enter when the book is crossed (best bid ≥ best ask). This is a free entry with no spread cost. This is my primary and most reliable entry condition.
- Enter when the spread is 1 or less AND the mid-price has moved in my intended direction for at least 2 consecutive ticks. A 1-point spread cost is recoverable with a single tick of favorable drift.
- A "strong directional signal" means: the spread is actively narrowing (e.g., 5→3→2) AND the mid-price has drifted in one direction for 3 or more consecutive ticks. Even then, I only enter if the spread has reached 1 or the book has crossed. A narrowing spread alone is not sufficient — it tells me the market is converging, not which way settlement will land.
- Do NOT enter on the basis that "the spread cost is recoverable if price drifts slightly in my favor." It has not, in practice, across eight episodes.
- Enter with size 2.

**Managing a long position**

- Do not add to a position I already hold.
- If I am long and the bid is at or above my entry + 1, sell the full position immediately. Lock in the gain; do not hope for more.
- If I am long and the bid is below my entry, check the tape direction:
  - If the bid is declining tick over tick (e.g., 46 → 44 → 42), sell immediately. Do not wait for tick 5. The bid will likely be even lower next tick.
  - If the bid is stable or rising, I may hold one more tick.
- Do not hold passively through multiple ticks hoping the bid will come back to my entry. It has not, in practice.

**Flattening near the end**

- On tick 5, if I am still in a position, hit the bid to flatten. This is the hard deadline.
- On the final tick, if I am still in a position, hit the bid. Do not hold into settlement.
- If I am flat on tick 5 or 6, stay flat. Opening a position I cannot manage over zero or one remaining tick is pure speculation.

**What not to do**

- Do not cross a spread of 2 or more points without the book being crossed or the spread having narrowed to 1 with a clear directional tape. The evidence from eight episodes is that this is a reliable way to lose 4–10 points.
- Do not be tempted by "the spread is narrowing, so the market is telling me something." A narrowing spread from 5 to 2 over four ticks is normal book convergence. It is not a directional signal. The mid-price drift must be consistent AND the spread must be 1 or the book must cross.
- Do not post a passive bid at the existing bid level and expect it to fill. It will sit there and do nothing.
- Do not place a sell order into the ask at a price that is already above the best ask. It will not fill.
- Do not wait for tick 5 to flatten if the bid is actively declining. Selling one tick early at a higher bid is better than selling on tick 5 at a lower bid.
- Do not rationalize holding a losing position by pointing to "upside momentum" in the tape when the bid is below my entry and not recovering. The bid is the only price I can actually sell at.

**Default posture**

- Staying flat and scoring 200 is a good outcome. In eight consecutive episodes, every attempt to enter a position resulted in a loss, and staying flat has now produced 200 eight times in a row. The default should be to look for reasons NOT to trade, and only act when the edge is clear and the cost is minimal.
- If I find myself wanting to enter because "I feel like price is going up," that is not a signal. The only signals are: crossed book, spread of 1 with directional tape, or nothing.