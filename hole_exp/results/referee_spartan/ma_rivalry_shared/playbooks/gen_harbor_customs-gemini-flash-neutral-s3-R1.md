---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 3
round: 1
chars: 1636
---
### Harbor Customs Playbook

#### Rules & Mathematical Constants
- In round $t$, with crates $(c_1 \le c_2 \le c_3)$ where total $T = c_1 + c_2 + c_3$:
  - Spot check flags my hold if and only if declared value $d < c_3$.
  - Flagged penalty is $-40$ points and full duty $0.30 \times T$. Never trigger this penalty.
  - On `main`: score $= T - \lfloor 0.30 \times d \rfloor$.
  - On `night`: score $= c_2 + c_3 - \lfloor 0.15 \times d \rfloor$.
  - The savings in duty from `night` over `main` is $\lfloor 0.30 \times d \rfloor - \lfloor 0.15 \times d \rfloor \approx 0.15 \times d$.
  - Since $d \le 40$, the maximum duty savings from `night` is $\approx 6$ points, while the cost is losing crate $c_1 \ge 5$. Night is strictly worse or negligible in almost all scenarios unless $c_1$ is exceptionally low and $d$ is very high, but with optimal declaration ($d = c_3$), `main` always dominates.

#### Stage 1: Declare
- When presented with crates $(c_1, c_2, c_3)$ where $c_3 = \max(c_1, c_2, c_3)$:
  - Set my declaration to exactly the value of the largest crate: `[declare: c_3]`.
  - Do not declare less than $c_3$ under any circumstances (it guarantees a -40 point penalty and 30% duty on total value).
  - Do not inflate declarations above $c_3$ to "blend in" with other players; harbor checks are purely deterministic against my own hold, and every extra point declared needlessly increases duty by 0.30.

#### Stage 2: Route
- When choosing the route:
  - Choose `[route: main]`.
  - Do not choose `[route: night]`, as sacrificing the smallest crate $c_1$ (worth $\ge 5$) far outweighs the minor $15\%$ duty discount on $c_3$.