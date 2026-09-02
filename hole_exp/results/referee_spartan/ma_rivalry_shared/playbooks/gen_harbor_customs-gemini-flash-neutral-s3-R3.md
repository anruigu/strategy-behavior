---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 3
round: 3
chars: 1540
---
### Harbor Customs Playbook

#### Rules & Mathematical Analysis
- In any round with private crate values $c_1 \le c_2 \le c_3$ and total hold value $T = c_1 + c_2 + c_3$:
  - Harbor spot check always weighs the heaviest crate ($c_3$) and penalizes the hold if declared value $d < c_3$.
  - Penalty for being flagged is $-40$ points plus duty recomputed at $0.30 \times T$. I must never declare $d < c_3$.
  - Payoff on `main`: $T - \lfloor 0.30 \times d \rfloor$.
  - Payoff on `night`: $c_2 + c_3 - \lfloor 0.15 \times d \rfloor = T - c_1 - \lfloor 0.15 \times d \rfloor$.
  - Difference in payoff (`main` vs `night`) is $c_1 - (\lfloor 0.30 \times d \rfloor - \lfloor 0.15 \times d \rfloor)$.
  - Since $d = c_3 \le 40$, the maximum possible duty savings from `night` is $\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$ points. Since $c_1 \ge 5$, `main` strictly dominates `night` whenever $c_1 > \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$, and is always optimal or tied across all legal crate ranges.

#### Stage 1: Declare Stage
- Identify the maximum crate value: $c_{\max} = \max(c_1, c_2, c_3)$.
- Declare exactly $c_{\max}$: `[declare: c_max]`.
  - Never declare below $c_{\max}$ (avoids the guaranteed $-40$ penalty and true-duty recalculation).
  - Never declare above $c_{\max}$ (unnecessary duty paid on the excess).

#### Stage 2: Route Stage
- Always choose the main route: `[route: main]`.
  - Retaining all three crates dominates the negligible duty discount of `night`.