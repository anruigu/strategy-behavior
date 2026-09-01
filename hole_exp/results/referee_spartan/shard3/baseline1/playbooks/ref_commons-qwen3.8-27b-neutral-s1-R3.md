---
game: ref_commons
model: qwen3.8-27b
condition: neutral
seed: 1
round: 3
chars: 2524
---
# Playbook: ref_commons

**Core strategy: cooperate in all non-final rounds at the sustainable share, then submit an extremely large number in the final round to capture the maximum proportional share of the remaining stock.**

**Seasons 1 through N-1:** Submit the sustainable share. This keeps the stock at its cap and maximizes the stock available for the final round. Do not overfish early — it depletes the stock and reduces the prize pool. Do not underfish or submit zero; that throws away points with no benefit.

**Final season (season N of N):** Submit a number orders of magnitude larger than the current stock. I now know from my own record that submitting 1000 (10× the stock) is not enough — when the other boats also submit 1000, I only get 1/3 of the stock (33.3) and my total is 88.8. Submitting 10000 or more is strictly better: if others submit 1000, I get 10000/12000 × 100 ≈ 83.3 and my total is ~139. If others also submit 10000, I still get 33.3 (no worse than before). There is no penalty for submitting a large number — the total catch is capped at the stock, so I never "lose" by over-submitting. I should submit the largest reasonable number (e.g., 100000) to maximize my share whenever others submit less.

**If the stock drops well below its cap in a non-final season** (e.g., another boat overfished heavily), still take the sustainable share for that season's lower stock level. Do not try to "compensate" by catching less — the stock regrows on its own and I lose points by undercatching. Do not match another boat's overfishing; that only accelerates depletion and shrinks the final-round prize.

**If another boat consistently overfishes** (taking well above sustainable in multiple seasons), I do not retaliate. I keep taking my sustainable share. The stock's regrowth dynamics will absorb moderate overfishing, and my total is protected by staying at the cooperative rate while preserving stock for the final round.

**Never submit zero in any round.**

**Generalization:** This strategy works for any number of boats and seasons. The key insight is that the final round is a one-shot allocation game: the stock is fixed, there is no future, and the only thing that matters is my share of that fixed pool. Submitting a number far larger than what I expect others to submit guarantees the largest share. The expected submission from others is roughly 10× the stock (based on my own prior behavior and observed patterns), so I should submit at least 10× that — i.e., at least 100× the stock.