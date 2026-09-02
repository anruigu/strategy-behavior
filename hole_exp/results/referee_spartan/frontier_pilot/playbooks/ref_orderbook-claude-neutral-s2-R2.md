---
game: ref_orderbook
model: claude
condition: neutral
seed: 2
round: 2
chars: 1671
---
# Orderbook Playbook (delivery-obligation book game: N units, T ticks, fixed starting cash)

## The arithmetic that decides everything
- Score = final book − starting book = (cash + N·S) − start, i.e. **N × (S − my average price)**, minus the shortfall penalty. Every 1 point I overpay per unit costs me N points of score. Nothing else I do matters as much as average fill price.
- **Settlement is NOT the tick-1 mid.** Measured over four episodes: settle ≈ the *final-tick mid*, which came in at tick-1 mid + 7 to 9, and tick-1 **ask** + 5 to 7 (51→56, 54→60, 52→59, 52→57).
- My working estimate from tick 1 onward: **S ≈ tick-1 ask + 6**. The tick-1 ask is therefore *cheap*, not expensive.
- The book drifts up monotonically, roughly +1 to +3 per tick on both sides, with occasional +5 jumps. Any unit I don't own yet gets more expensive.
- Shortfall math: holding a unit bought at P beats being short by (S + penalty − P). With penalty 8, **I should pay up to S+8 (≈ tick-1 ask + 14) rather than deliver short.** Accepting a shortfall is almost never right; it's the last resort only if cash literally cannot cover the ask.

## The opening tick — the single highest-leverage decision
- **Lift the entire resting ask on tick 1, at whatever the spread is.** Do not compute whether the spread is "too wide." I ran the exact A/B: identical tick-1 book of 48/52, crossing scored **+15**, posting a passive 49 bid scored **−3**. Same result direction in all four episodes.
- Ask size is typically less than my full requirement (often 2 when I need 3). Take all of it. I post `buy <ask size> @ <ask price>` — sizing above the resting ask just leaves a stale low bid behind.