---
game: ref_orderbook
model: claude
condition: neutral
seed: 2
round: 3
chars: 1362
---
# Orderbook Playbook (delivery-obligation book game: N units to hold at settlement, T ticks, fixed starting cash, penalty per missing unit)

## 1. The arithmetic that decides everything
- Score = (final cash + final position × S) − starting cash − shortfall. So score = **(units held) × S − (total spent)**. Every point I overpay per unit costs a point; every unit I acquire below S adds (S − price).
- Extra units beyond N are **not wasted** — position is marked at settlement. Any unit bought below S is pure profit; the only cap is cash and the reserve I need to guarantee delivery.
- The entire realised edge in every episode so far came from the tick-1 lift. Everything bought after tick 2 was within ~1 point of S, i.e. noise.

## 2. Settlement estimator (calibrated over 4 episodes)
- Measured: tick-1 ask 53→S 60, 49→56, 52→58, 52→58. **S ≈ tick-1 ask + 6.5** (range +6 to +7). Use this from tick 1 onward and don't second-guess it.
- Also: S ≈ final-tick best ask + 1, ≈ final-tick best bid + 2.5. Useful as a sanity check late.
- Price path: one big jump between tick 1 and tick 2 (mid +4 to +5), then a **flat plateau near S for the rest of the game** (asks oscillate 55–59 both up and down; it is *not* monotone after tick 2). So waiting past tick 2 neither helps nor hurts much — but the tick-1 discount never comes back.
- Shortfall math: holding a