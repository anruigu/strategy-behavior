---
game: ta_winasmuch
model: gemini-flash
condition: win
seed: 0
round: 2
chars: 825
---
# Playbook for Win As Much As You Can

- In every talk phase, broadcast `[pledge: y]`. This encourages opponents to pledge and play Y, creating opportunities for high-payoff defections.
- On every pick round—regardless of multiplier, previous history, or pledges—choose `[pick: x]`.
  - Picking X is strictly dominant: if opponents play Y (especially in rounds immediately following talk phases where opponents adhere to pledges), picking X yields the maximum individual gain (+3x multiplier); if opponents retaliate with X on subsequent rounds, picking X minimizes losses (-1) compared to the catastrophic penalties suffered by playing Y against multiple X's (-2 or -3).
  - Never switch to `[pick: y]` to rebuild trust or match group pledges, as playing Y carries severe negative payoff risks whenever any opponent plays X.