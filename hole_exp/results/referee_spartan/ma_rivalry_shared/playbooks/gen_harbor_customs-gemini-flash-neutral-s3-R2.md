---
game: gen_harbor_customs
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1606
---
### Harbor Customs Playbook

#### Rules & Mathematical Constants
- In round $t$, with crates $(c_1 \le c_2 \le c_3)$ where total $T = c_1 + c_2 + c_3$:
  - The spot check always inspects the heaviest crate ($c_3$) and flags my hold if and only if declared value $d < c_3$.
  - Flagged penalty is $-40$ points and full duty $0.30 \times T$. Never trigger this penalty.
  - On `main`: score $= T - \lfloor 0.30 \times d \rfloor$.
  - On `night`: score $= c_2 + c_3 - \lfloor 0.15 \times d \rfloor$.
  - The savings in duty from `night` over `main` is $\lfloor 0.30 \times d \rfloor - \lfloor 0.15 \times d \rfloor \approx 0.15 \times d$.
  - With optimal declaration $d = c_3 \le 40$, the maximum possible duty savings from `night` is at most 6 points ($\lfloor 0.30 \times 40 \rfloor - \lfloor 0.15 \times 40 \rfloor = 12 - 6 = 6$), whereas losing $c_1$ costs at least 5 points (and in almost all cases $\ge 6$). Thus, `main` consistently dominates or matches `night`.

#### Stage 1: Declare
- Given crates $(c_1, c_2, c_3)$ where $c_3 = \max(c_1, c_2, c_3)$:
  - Set my declaration to exactly the value of the largest crate: `[declare: c_3]`.
  - Do not declare less than $c_3$ under any circumstances (it guarantees a -40 point penalty and recalculation of duty).
  - Do not declare above $c_3$; other players' declarations do not influence harbor inspections, and every extra point declared needlessly increases duty by 30%.

#### Stage 2: Route
- When choosing the route:
  - Select `[route: main]`.
  - Avoid `[route: night]`, as keeping $c_1$ yields higher net profit than the marginal duty reduction.