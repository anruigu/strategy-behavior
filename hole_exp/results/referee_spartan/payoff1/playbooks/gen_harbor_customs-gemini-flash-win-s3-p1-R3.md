---
game: gen_harbor_customs
model: gemini-flash
condition: win
seed: 3
round: 3
chars: 1170
---
### Harbor Customs Playbook

- **Declare Stage:**
  - Let $c_1 \le c_2 \le c_3$ be the crate values in ascending order.
  - Always declare exactly $c_3$, the value of the heaviest crate: `[declare: c3]`.
  - Declaring higher than $c_3$ wastes points on unnecessary duty. Declaring lower than $c_3$ triggers an automatic 40-point penalty and recalculates duty at $0.30 \times (c_1 + c_2 + c_3)$.

- **Route Stage:**
  - Calculate the duty difference saved by going `night`:
    $$\Delta \text{duty} = \lfloor 0.30 \times c_3 \rfloor - \lfloor 0.15 \times c_3 \rfloor$$
  - Compare $\Delta \text{duty}$ against the sacrifice of the smallest crate $c_1$:
    - If $\Delta \text{duty} > c_1$, choose `[route: night]`.
    - Otherwise (when $c_1 \ge \Delta \text{duty}$, which is virtually always true since maximum $\Delta \text{duty} \le 6$ and crate values are $\ge 5$), choose `[route: main]`. Specifically, only go `night` if $c_1 = 5$ and $\Delta \text{duty} = 6$ (which happens when $c_3 \ge 34$).

- **Formatting:**
  - Keep reasoning to at most one short line.
  - Always output the exact bracketed action token: `[declare: n]` or `[route: main]` / `[route: night]`.