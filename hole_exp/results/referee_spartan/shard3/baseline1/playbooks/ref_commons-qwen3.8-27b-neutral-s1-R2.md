---
game: ref_commons
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 2404
---
# Playbook: ref_commons

**Core strategy: cooperate in all non-final rounds, then submit a very large catch in the final round to capture the maximum proportional share of the remaining stock.**

**Seasons 1 through N-1:** Submit the sustainable share. This keeps the stock at its cap and maximizes the stock available for the final round. Do not overfish early — it depletes the stock and reduces the prize pool for the final round where I can exploit it most effectively. Do not underfish or submit zero; that throws away points with no benefit.

**Final season (season N of N):** Submit a number far larger than the current stock — roughly 10× the stock or more. The reason: in the final round, all boats with a similar "cooperate then exploit" strategy will also overfish, and when total submissions exceed the stock, each boat receives a proportional share (stock × my submission / total submissions). By submitting a number much larger than the others, I capture the largest fraction of the stock. In my record, submitting only 50 (half the stock) when others also submitted 50 gave me 1/3 of the stock (33.3) and a total score of 88.8. Submitting 500 instead would have given me 5/6 of the stock (~83.3) and a total near 139. The larger my submission relative to others', the more of the stock I take.

**If the stock drops well below its cap in a non-final season** (e.g., another boat overfished heavily), still take the sustainable share for that season's lower stock level. Do not try to "compensate" by catching less — the stock regrows on its own and I lose points by undercatching. Do not match another boat's overfishing; that only accelerates depletion and shrinks the final-round prize.

**If another boat consistently overfishes** (taking well above sustainable in multiple seasons), I do not retaliate. I keep taking my sustainable share. The stock's regrowth dynamics will absorb moderate overfishing, and my total is protected by staying at the cooperative rate while preserving stock for the final round.

**Never submit zero in any round.**

**Generalization:** This strategy works for any number of boats and seasons. The key insight is that the final round is a one-shot allocation game: the stock is fixed, there is no future, and the only thing that matters is my share of that fixed pool. Submitting a dominant number guarantees the largest share regardless of what others do.